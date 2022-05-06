# Upwork client project repository

### Short description:
run_me.py allows for files that are not links and have very long names, rename their name to new - shorter names and create old long named files, but this time they are soft/symbolic links to new short-name-having files. 

#### Name shortening happens for file name only, extensions remain unchanged:

```
Example:  

structure of folder before:

. file_1.py                                                        # file with short name
. loooooooooooooooooooooooooooooooooooooooooooooong_file.py        # file with long name

Structure of folder after:

. file_1.py                                                        # not changed
. loooooooooooooooooooooooooooooooooooooooooooooong_file.py        # old file name still exists, but now it is a soft link to smaller name-having file below this line 
. looooooooooooooooooooooooooooooooo.py                            # file that upper file links to

```

#### Make sure to not change max_allowed_filename_length argument in run_me.py after running in some folder once

#### You should run run_me.py with &>> or other redirection operators to save logs to a file for future debugging purposes

#### Here you also see _demo_folder_with_files testing folder that can be used to see how everything works for really long-name-having files

## When running run_me.py file, pass full folder path that you want to process, for example:
```bash
/usr/bin/python3 run_me.py /home/your_name/some_folder_on_our_pc earlier_than_now_minus_hours_number  &>> your_log_file_location.log
```

