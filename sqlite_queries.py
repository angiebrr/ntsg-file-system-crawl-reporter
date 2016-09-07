from abc import ABCMeta, abstractmethod

class SqliteQueries(metaclass=ABCMeta):
    """Base class for sqlite queries used for the different versions of the crawls and reports.

    Although the children classes will make queries that have the same names, it allows a consistent
    interface for creating reports on crawls that had different versions. These different versions
    might have different columns, types of files, etc., but this class allows these different
    queries to be accessed from the same place without too much redundancy.
    """

    # ==============================================================================================
    # HELPER STRINGS
    # ==============================================================================================
    def UNION_KEYWORD(self):
        return \
        """
            UNION
        """

    def ORDER_BY_TOTAL_SIZE(self):
        return \
        """
            ORDER BY total_size_in_gb DESC
        """

    # ==============================================================================================
    # ALL USERS QUERY
    # ==============================================================================================
    @abstractmethod
    def ALL_USERS_QUERY(self): pass

    @abstractmethod
    def ALL_USERS_QUERY_COLUMNS(self): pass

    # ==============================================================================================
    # ALL FILES BY USER QUERY
    # ==============================================================================================
    @abstractmethod
    def ALL_FILES_BY_USER_QUERY(self): pass

    @abstractmethod
    def ALL_FILES_BY_USER_QUERY_COLUMNS(self): pass

    # ==============================================================================================
    # ALL FILES QUERY
    # ==============================================================================================
    @abstractmethod
    def ALL_FILES_QUERY(self): pass

    @abstractmethod
    def ALL_FILES_QUERY_COLUMNS(self): pass

    # ==============================================================================================
    # TOTAL SIZE BY USER BY EXT QUERY
    # ==============================================================================================
    @abstractmethod
    def TOTAL_SIZE_BY_USER_BY_EXT_QUERY(self): pass

    @abstractmethod
    def TOTAL_SIZE_BY_USER_BY_EXT_QUERY_COLUMNS(self): pass

    # ==============================================================================================
    # TOTAL SIZE BY EXT QUERY
    # ==============================================================================================
    @abstractmethod
    def TOTAL_SIZE_BY_EXT_QUERY(self): pass

    @abstractmethod
    def TOTAL_SIZE_BY_EXT_QUERY_COLUMNS(self): pass

    # ==============================================================================================
    # TOTAL SIZE BY USER QUERY
    # ==============================================================================================
    @abstractmethod
    def TOTAL_SIZE_BY_USER_QUERY(self): pass

    @abstractmethod
    def TOTAL_SIZE_BY_USER_QUERY_COLUMNS(self): pass

    # ==============================================================================================
    # TOTAL SIZE QUERY
    # ==============================================================================================
    @abstractmethod
    def TOTAL_SIZE_QUERY(self): pass

    @abstractmethod
    def TOTAL_SIZE_QUERY_COLUMNS(self): pass