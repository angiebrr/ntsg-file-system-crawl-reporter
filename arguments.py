from argparse import ArgumentParser
from enums import ReportEnum, SqliteQueriesEnum
from original_sqlite_queries import OriginalSqliteQueries
from filemode_sqlite_queries import FilemodeSqliteQueries

class Arguments(object):
    """Uses ArgumentParser to gather and parse arguments given by the user in the command line.

    Attributes:
        argParser (ArgumentParser): An ArgumentParser instance used to gather and parse the given arguments
        inputFile (str): A parsed argument; The path to the sqlite database file
        outputPath (str): A parsed argument; The path to generate the reports
        reportType (ReportEnum): Derived from a parsed argument; The type of reports that are generated
        queriesData (SqliteQueries): Derived from a parsed argument; The version of the queries to use for the reports
    """
    def __init__(self):
        # Setup arguments to parse
        self.argParser = ArgumentParser(description='Dumps the results of the filecrawler (that has been imported into a sqlite database) into csv user reports that are in folders '
                                                    'separated by username')

        # Required Named arguments
        requiredNamed = self.argParser.add_argument_group('required named arguments')
        requiredNamed.add_argument('-i','--input', type=str, required=True, help='The input sqlite file')
        requiredNamed.add_argument('-o','--output', type=str, required=True, help='The path to generate the reports that are sorted into directories of usernames with reports')
        queriesVersionsList = [enum.name for enum in SqliteQueriesEnum]
        requiredNamed.add_argument('-q','--queries', choices=queriesVersionsList, required=True, help='The version of the queries to use for the reports')
        reportNameList = [enum.name for enum in ReportEnum]
        requiredNamed.add_argument('-rt','--report', choices=reportNameList, required=True, help='The type of reports that are generated')

        # Parse all arguments
        args = vars(self.argParser.parse_args())
        self.inputFile = args['input']
        self.outputPath = args['output']
        self.reportType = ReportEnum[args['report']]
        self.queriesData = self.getQueryData(SqliteQueriesEnum[args['queries']])

    def getQueryData(self, queriesVersion):
        """Based on the given query version, it will return a SqliteQueries object of that version

        Params:
            queriesVersion (SqliteQueriesEnum): The version of the queries to use for the reprots
        """
        if queriesVersion is SqliteQueriesEnum.original:
            return OriginalSqliteQueries()
        elif queriesVersion is SqliteQueriesEnum.filemode:
            return FilemodeSqliteQueries()
        else:
            raise ValueError("Query Version can only be %s" % [enum.name for enum in SqliteQueriesEnum])