"""
Replace old long filenames that are longer than some number, with 
links that point to smaller-name having same file contents.

Use Linux soft links.

Also store log what changes were made.

Example
----------------------------------------------

Structure of folder before:

. file_1.py                                                        # file with short name
. loooooooooooooooooooooooooooooooooooooooooooooong_file.py        # file with long name (allowed max length is controlled below)

Structure of folder after:

. file_1.py                                                        # not changed
. loooooooooooooooooooooooooooooooooooooooooooooong_file.py        # old file name still exists, but now it is a soft link to smaller name-having file below this line 
. looooooooooooooooooooooooooooooooo.py                            # file that upper file links to. Only filenames became shorter, extension remains as it may be useful for apps using it

Next time we run it again, it will try to do similar renaming only for files that are not links.

"""

import glob
import logging
import os
import sys

# configure logging
root = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter(
        "%(asctime)s | %(name)s | %(funcName)s | %(levelname)s | %(message)s"
    )
)


root.addHandler(handler)

logger = logging.getLogger("FILENAMES_SHORTENER")
logger.setLevel(logging.DEBUG)


def _get_shorter_name_filepath(long_name_filepath, max_allowed_filename_length):
    parent_dir = os.path.dirname(long_name_filepath)

    long_name_filename = long_name_filepath.split("/")[-1]

    if "." in long_name_filename:
        # file with extension case
        name, extension = long_name_filename.rsplit(".", maxsplit=1)

        max_allowed_filename_length = max_allowed_filename_length - len(extension) - 1

        shorter_filename = f"{name[:max_allowed_filename_length]}.{extension}"

        max_allowed_filename_length += len(extension) + 1
    else:
        shorter_filename = name[:max_allowed_filename_length]

    assert len(shorter_filename) == max_allowed_filename_length

    return os.path.join(parent_dir, shorter_filename)


def _process_long_name_having_file(
    long_name_filepath,
    max_allowed_filename_length,
):
    shorter_name_filepath = _get_shorter_name_filepath(
        long_name_filepath, max_allowed_filename_length
    )

    # rename long name-having file to short name-file
    os.rename(long_name_filepath, shorter_name_filepath)

    logger.info(f"Renamed {long_name_filepath} to {shorter_name_filepath}")

    # create link with long filename that links to new shorter filename
    # "Create a symbolic link pointing to src named dst.""
    os.symlink(dst=long_name_filepath, src=shorter_name_filepath)

    logger.info(
        f"Created soft/symbolic link from {long_name_filepath} to {shorter_name_filepath}"
    )


def _get_files_to_process(folder_path):
    files_to_process = []

    for i in glob.glob(f"{folder_path}/**/*", recursive=True):

        if os.path.isfile(i):
            if os.path.islink(i):
                continue

            if len(i.split("/")[-1]) > max_allowed_filename_length:

                files_to_process.append(i)

    return files_to_process


def replace_longer_filenames_with_links_to_same_files_with_shorter_names(
    folder_path,
    max_allowed_filename_length,
    ask_confirmation=True,
):
    # useful checks
    assert (
        folder_path.endswith("/")
        and os.path.isdir(folder_path)
        and sys.platform.lower() == "linux"
    )

    # get list of files to process
    files_to_process = _get_files_to_process(folder_path)

    # wait to see if numbers seem correct
    print(f"Going to process {len(files_to_process)} files in {folder_path} ")

    if ask_confirmation:
        # allow interrupt before starting
        if not input("Press y to continue\n").lower() == "y":
            print("Stopping as you have not pressed y to confirm")
            return

    # replace with logging
    logger.info(f"Started processing {len(files_to_process)} files")

    # do work
    for i in files_to_process:
        _process_long_name_having_file(i, max_allowed_filename_length)

    # Done
    logger.info(f"Processing completed")


# GO
if __name__ == "__main__":
    # all long files will be processed in any subdirectory of this folder.
    folder_path = sys.argv[1]

    # minimum length of filename to process will be this number + 1
    # do not change this number when running on same folder more than 1 times to avoid data loss
    max_allowed_filename_length = 143

    # set to False if not running by hand (ex: if using cronjob)
    # also, to redirect log output to some file, you can run this file like:
    # your_python_binary_location this_filename.py &>> log_filename_location
    ask_confirmation = 1

    replace_longer_filenames_with_links_to_same_files_with_shorter_names(
        folder_path=folder_path,
        max_allowed_filename_length=max_allowed_filename_length,
        ask_confirmation=ask_confirmation,
    )
