# File System Crawl Reporter

> [!WARNING]
> Archived and no longer maintained; kept for reference. Written in 2016 for Python 3.5, which is end-of-life, and the crawl table names are hardcoded (see [Using it](#using-it)).

- [File System Crawl Reporter](#file-system-crawl-reporter)
  - [Overview](#overview)
    - [What it reports](#what-it-reports)
  - [Using it](#using-it)
    - [Dependencies](#dependencies)
    - [Query versions](#query-versions)
      - [v1.0 (up to August 18th 2016; queries version "original")](#v10-up-to-august-18th-2016-queries-version-original)
      - [v2.0 (current; queries version "filemode")](#v20-current-queries-version-filemode)
    - [Report types](#report-types)
      - [User](#user)
      - [Crawl](#crawl)
    - [Script arguments](#script-arguments)
    - [Example invocations](#example-invocations)
    - [Logging](#logging)

## Overview

A Python script that turns the output of my [ntsg-file-system-crawler](https://github.com/angiebrr/ntsg-file-system-crawler) into CSV reports on who is using how much disk space, and on what kinds of files.

I wrote this in 2016 as the Linux sysadmin for NTSG, a research group at the University of Montana. It runs a set of queries over the crawler's CSVs once they're imported into a SQLite database, one table per crawl.

**Tech:** Python 3.5, SQLite, tqdm, CSV

### What it reports

- Total size per crawl
- Total size by file extension
- A full file listing, either for everything or split into a folder per user
- Works with both crawler output formats (v1.0 and v2.0, which added file modes, link targets, and directory rows); pick the one matching your tables with `--queries`

## Using it

The reporter expects three tables named `home_crawl`, `projects_crawl`, and `measures_crawl`, one per crawl. Those names are hardcoded in `sqlite_reporter.py`, so change them there to match your own database.

### Dependencies

- Python 3.5
- tqdm 4.8

### Query versions

The tables that the reporter is expecting will have the following columns. You can specify what version ("original" or "filemode") your tables will be in with the `queries` argument. *(See [Script arguments](#script-arguments))*

#### v1.0 (up to August 18th 2016; queries version "original")

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

#### v2.0 (current; queries version "filemode")

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
2. In the `enums` module, add your new version to the `SqliteQueriesEnum`.
3. In the `arguments` module, add another `elif` that will create your new queries type.

### Report types

#### User

Generates reports for each user and saves these sets of user reports into a separate directory.

The reports generated for each user include:

- Total size of all files owned by the user in each crawl
- Total size of all files by extension owned by the user for all crawls
- Basic report of all files owned by the user for all crawls

#### Crawl

Generates reports that have information about all crawls.

These reports include:

- Total size of all files in each crawl
- Total size of all files by extension for all crawls
- Basic report of all files for all crawls

### Script arguments

| Argument Flags                        | Description                                                                                               | Required? |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------- | --------- |
| `-h`, `--help`                        | Show help message and exit                                                                                | No        |
| `-i INPUT`, `--input INPUT`           | The path to the sqlite database file                                                                      | Yes       |
| `-o OUTPUT`, `--output OUTPUT`        | The directory to store the reports. It needs to exist already                                             | Yes       |
| `-q QUERIES`, `--queries QUERIES`     | The version of the queries to use for the reports. Choices are {original, filemode}                       | Yes       |
| `-rt REPORT`, `--report REPORT`       | The type of the reports that are generated. Choices are {user, crawl}                                     | Yes       |

In order to get an up-to-date version of the arguments that are passed in to the module, all you have to do is type:

```bash
python file-system-crawl-reporter --help
```

And you should get a listing of the different arguments that can be passed in.

### Example invocations

A very simple invocation that will use the `crawls.db` file to generate reports for all crawls in `/crawler_reporter_output`:

```bash
python file-system-crawl-reporter -i '/crawler_output/crawls.db' -o '/crawler_reporter_output' -q filemode -rt crawl
```

This is a similar invocation to the one above, but this one generates user reports in `/crawler_reporter_output/user_reports` instead of reports for all crawls:

```bash
python file-system-crawl-reporter -i '/crawler_output/crawls.db' -o '/crawler_reporter_output/user_reports' -q filemode -rt user
```

### Logging

A log file, `report_script.log`, is created in the output directory.

The following things are logged:

* When the reporter begins (it includes the input and output variables)
* When an error occurs when processing a report
* When report generation is finished

It includes a message and a timestamp that may look something like this:

```
# /reporter_output/user_reports/report_script.log

INFO:root:[2016-09-07 13:30:53.237696]: Generating reports from sqlite file /sqlite/files.db, and output directory /reporter_output/user_reports 
INFO:root:[2016-09-07 14:06:53.720100]: Report generation is finished
```
