from enum import Enum, unique

@unique
class SqliteQueriesEnum(Enum):
    """A simple enumerator that describes the versions of the queries for versioned reports
    """
    original = 0,
    filemode = 1

@unique
class ReportEnum(Enum):
    """A simple enumerator that describes the different types of reports that can be generated
    """
    user = 0,
    crawl = 1