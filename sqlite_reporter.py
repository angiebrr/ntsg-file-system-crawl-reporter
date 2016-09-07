import os, errno, sqlite3, csv, logging
from datetime import datetime
from tqdm import tqdm
from enums import ReportEnum

class SqliteReporter(object):
    """A class that helps execute sqlite queries and store the results as CSV files.

    Attributes:
        outputDir (str): The path to generate the reports
        inputSqlFile (str): The path to the sqlite database file
        conn (sqlite3.connect): The connection to the sqlite database
        reportType (ReportEnum): The type of report that will be generated
        queriesData (SqliteQueries): The version of the queries to use for the reports
    """

    def __init__(self, inputSqlFile, outputDir, reportType, queriesData):
        self.outputDir = outputDir
        self.inputSqlFile = inputSqlFile
        self.conn = None
        self.reportType = reportType
        self.queriesData =  queriesData

    def open_conn(self):
        """Opens a connection to the sqlite database.
        """
        self.conn = sqlite3.connect(self.inputSqlFile)

    def close_conn(self):
        """Closes the connection to the sqlite database and sets self.conn to None.
        """
        self.conn.close()
        self.conn = None

    def is_connected(self):
        """Returns whether or not the sqlite database is currently connected.
        """
        return self.conn != None

    def generate_reports(self):
        """Generate the CSV file reports.
        """
        self.open_conn()

        if self.reportType is ReportEnum.user:
            self.generate_user_reports()
        elif self.reportType is ReportEnum.crawl:
            self.generate_crawl_reports()

        self.close_conn()

    def generate_crawl_reports(self):
        """Generates reports that have information about all crawls.

        These reports include:
        - Total size of all files in each crawl
        - Total size of all files by extension for all crawls
        - Basic report of all files for all crawls
        """
        try:
            with tqdm(desc="Generating the total size report for all crawls...", unit="report", total=3) as pbar:

                self.generate_report\
                (
                    'total-size',
                    self.queriesData.TOTAL_SIZE_QUERY(),
                    self.queriesData.TOTAL_SIZE_QUERY_COLUMNS()
                )

                pbar.set_description("Generating the total size by extension report for all crawls...")
                pbar.update(1)
                self.generate_report \
                (
                    'total-size-by-extension',
                    self.queriesData.TOTAL_SIZE_BY_EXT_QUERY(),
                    self.queriesData.TOTAL_SIZE_BY_EXT_QUERY_COLUMNS()
                )

                pbar.set_description("Generating a basic report with all files for all crawls...")
                pbar.update(1)
                self.generate_report \
                (
                    'all-files',
                    self.queriesData.ALL_FILES_QUERY(),
                    self.queriesData.ALL_FILES_QUERY_COLUMNS()
                )

                pbar.set_description("Finished generating all three reports.")
                pbar.update(1)


        except Exception as ex:
            logging.error("[%s]: Problem generating report for crawls \r\n %s" % (str(datetime.now()), ex))

    def generate_user_reports(self):
        """Generates reports for each user and saves these sets of user reports into a separate directory.

        The reports generated for each user include:
        - Total size of all files owned by the user in each crawl
        - Total size of all files by extension owned by the user for all crawls
        - Basic report of all files owned by the user for all crawls
        """

        # retrieve all users
        users = self.get_users()

        # iterate over all of the users and generate a report for each
        pbarDesc = "Processing user %s"
        pbarUsers = tqdm(users, desc=pbarDesc % 'N/A', unit="user")
        for row in pbarUsers:
            username = row[0]
            pbarUsers.set_description(pbarDesc % username)
            try:
                self.create_user_directory(username)
                # generate a report with all files found for a user
                self.generate_report \
                (
                        'all-files',
                        self.queriesData.ALL_FILES_BY_USER_QUERY(),
                        self.queriesData.ALL_FILES_BY_USER_QUERY_COLUMNS(),
                        username=username
                    )
                # generate a report with the aggregate size of all files by crawl by user
                self.generate_report \
                (
                    'total-size-by-crawl',
                    self.queriesData.TOTAL_SIZE_BY_USER_QUERY(),
                    self.queriesData.TOTAL_SIZE_BY_USER_QUERY_COLUMNS(),
                    username=username
                )
                # generate a report with the aggregate size of all files by crawl by user by file extension
                self.generate_report \
                (
                    'total-size-by-extension-by-crawl',
                    self.queriesData.TOTAL_SIZE_BY_USER_BY_EXT_QUERY(),
                    self.queriesData.TOTAL_SIZE_BY_USER_BY_EXT_QUERY_COLUMNS(),
                    username=username
                )

            except Exception as ex:
                logging.error("[%s]: Problem generating report for user %s \r\n %s" % (str(datetime.now()), username, ex))
        pbarUsers.close()

    def generate_report(self, reportName, query, columns, username=None):
        """Runs the given query against the database and saves the results as a CSV file

        Params:
            reportName (str): Name that will on the CSV report file.
            query (str): Sqlite query that will used to generated the report. Ensure that you have {crawlname} and, if it's a user query, {username}, in the query string.
            columns (list of str): A list of the columns returned in the given query.
            username (str): Default is None. If this is a user report, then include the user's username.
        """

        if username == None:
            # get report based on crawl name
            reportData = self.conn.execute \
            (
                query.format(crawlname="home_crawl") + self.queriesData.UNION_KEYWORD() +
                query.format(crawlname="projects_crawl") + self.queriesData.UNION_KEYWORD() +
                query.format(crawlname="measures_crawl") + self.queriesData.ORDER_BY_TOTAL_SIZE()
            )
            # get the csv path based on report name
            csvPath = self.outputDir + '/{reportname}_report.csv'.format(reportname=reportName)
        else:
            # get report based on username (e.g. get files owned by user)
            reportData = self.conn.execute \
            (
                query.format(crawlname="home_crawl", username=username) + self.queriesData.UNION_KEYWORD() +
                query.format(crawlname="projects_crawl", username=username) + self.queriesData.UNION_KEYWORD() +
                query.format(crawlname="measures_crawl", username=username) + self.queriesData.ORDER_BY_TOTAL_SIZE()
            )
            # get the csv path based on username
            csvPath = self.get_user_directory(username) + '/{username}_{reportname}_report.csv'.format(username=username, reportname=reportName)

        # write the report data into either the user's directory or the output directory
        with open(csvPath, 'w', newline='', encoding='utf-8') as csvFile:
            csvWriter = csv.writer(csvFile)
            csvWriter.writerow(columns)
            csvWriter.writerows(reportData)

    def get_users(self):
        """Retrieves all unique users across all crawls.

        Return:
            sqlite3.Cursor: Sqlite object that allows you to iterate over the rows of returned users
        """

        return self.conn.execute \
        (
            self.queriesData.ALL_USERS_QUERY().format(crawlname="home_crawl") + self.queriesData.UNION_KEYWORD() +
            self.queriesData.ALL_USERS_QUERY().format(crawlname="projects_crawl") + self.queriesData.UNION_KEYWORD() +
            self.queriesData.ALL_USERS_QUERY().format(crawlname="measures_crawl")
        )

    def create_user_directory(self, username):
        """Creates a directory with the given name (username).

        If the directory already exists, then nothing is done.

        Params:
            username (str): The name of the user. It will be used as the directory name.
        """

        try:
            os.makedirs( self.get_user_directory(username) )
        except OSError as ex:
            if ex.errno != errno.EEXIST:
                logging.error("[%s]: Problem creating directory for user %s \r\n %s" % (str(datetime.now()), username, ex))

    def get_user_directory(self, username):
        """Returns the full path of the directory including the output dir.

        Returns:
            str: The full path of the directory
        """

        return self.outputDir + '/' + username
