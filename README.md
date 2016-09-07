# Dependencies

- Python 3.5
- tqdm 4.8

# Overview

This uses a sqlite database based on the data that the [File System Crawler](https://bitbucket.org/ntsg_annex/file-system-crawler) generates.

# Query versions

The tables that the crawler is expecting will have the following columns. You can specify what version ("original" or "filemode") your tables will be in with the `queries` argument. *(See Script Arguments)*

## v1.0 (Up to August 18th 2016; Queries version "original")

| Column Name              | Description                                                   |
| ------------------------ | ------------------------------------------------------------- |
| `full_file_parent_path`  | The file parent directory's absolute path                     |
| `file_name`              | The file's name (stem) without its "suffix" (extension)       |
| `file_ext`               | The file's extension                                          |
| `file_size`              | The file's size (in bytes)                                    |
| `file_uid`               | The file's UID                                                |
| `file_gid`               | The file's GID                                                |
| `file_ctime`             | The file's "ctime"                                            |
| `file_accessed_time`     | The file's last accessed time                                 |
| `file_modified_time`     | The file's last modified time                                 |
| `current_os`             | The current operating system                                  |

## v2.0 (Current; Queries version "filemode")

| Column Name              | Description                                                   |
| ------------------------ | ------------------------------------------------------------- |
| `full_file_parent_path`  | The file parent directory's absolute path                     |
| `file_mode`              | The file's "mode" {DIR, FILE, LINK}                           |
| `file_name`              | The file's name (stem) without its "suffix" (extension)       |
| `file_ext`               | The file's extension                                          |
| `file_size_in_bytes`     | The file's size (in bytes)                                    |
| `file_uid`               | The file's UID                                                |
| `file_gid`               | The file's GID                                                |
| `file_ctime`             | The file's "ctime"                                            |
| `file_accessed_time`     | The file's last accessed time                                 |
| `file_modified_time`     | The file's last modified time                                 |
| `file_real_path`         | If it's a LINK file, the file's "real path" or target path    |
| `current_os`             | The current operating system                                  |

If you decide to update the table structure (i.e. create another version), be sure to:

1. Create a class that inherits from the `SqliteQueries` class and implements all the different queries needed.
2. In the `enums` module, add your new version to the `ReportEnum`.
3. In the `arguments` module, add another `elif` that will create your new queries type.

# Report Types

## User

Generates reports for each user and saves these sets of user reports into a separate directory.

The reports generated for each user include:

- Total size of all files owned by the user in each crawl
- Total size of all files by extension owned by the user for all crawls
- Basic report of all files owned by the user for all crawls

## Crawl

Generates reports that have information about all crawls.

These reports include:

- Total size of all files in each crawl
- Total size of all files by extension for all crawls
- Basic report of all files for all crawls

# Script Arguments

| Argument Flags                        | Description                                                                                               | Required? |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------- | --------- |
| `-h`, `--help`                        | Show help message and exit                                                                                | No        |
| `-i INPUT`, `--input INPUT`           | The path to the sqlite database file                                                                      | Yes       |
| `-o OUTPUT`, `--output OUTPUT`        | The directory to the store the reports. If it does not exist, it will be created for you                  | Yes       |
| `-q QUERIES`, `--queries QUERIES`     | The version of the queries to use for the reports. Choices are {original, filemode}                       | Yes       |
| `-rt REPORT`, `--report REPORT`       | The type of the reports that are generated. Choices are {user, crawl}                                     | Yes       |

In order to get an up-to-date version of the arguments that are passed in to the module, all you have to do is type:
```
#!bash

python fscreporter --help
```
And you should get a listing of the different arguments that can be passed in.

# Example Invocations

A very simple invocation that will use the `crawls.db` file to generate reports for all crawls in `/crawler_reporter_output`:
```
#!bash

python fscreporter -i '/crawler_output/crawls.db' -o '/crawler_reporter_output' -q filemode -rt crawl
```

This is a similar invocationto the one above, but this one generates user reports in `/crawler_reporter_output/user_reports` instead of reports for all crawls:
```
#!bash

python fscreporter -i '/crawler_output/crawls.db' -o '/crawler_reporter_output/user_reports' -q filemode -rt user
```

# Logging

A file is created with the same name (but ".log" extension) as the output file and is placed in the output directory.

The following things are logged:

* When the crawler begins (it includes the input and output variables)
* When an error occurs when processing a report
* When the crawl ends and the data store is finalized

It includes a message and a timestamp that may look something like this:


```
#!bash
# /reporter_output/user_reports/report_script.log

INFO:root:[2016-09-07 13:30:53.237696]: Generating reports from sqlite file /sqlite/files.db, and output directory /reporter_output/user_reports 
INFO:root:[2016-09-07 14:06:53.720100]: Report generation is finished
```

-------------------------------------------------------------------------------

** Script Author:** Angela Gross