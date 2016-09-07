from sqlite_queries import SqliteQueries

@SqliteQueries.register
class OriginalSqliteQueries(SqliteQueries):
    """Contains sqlite queries for versions of databases that have crawls that do not support filemodes (i.e. did not process symbolic links and shortcuts).
    """

    # ==============================================================================================
    # ALL USERS QUERY
    # ==============================================================================================
    def ALL_USERS_QUERY(self):
        return \
        """
            SELECT DISTINCT file_owner_username
            FROM {crawlname}
        """

    def ALL_USERS_QUERY_COLUMNS(self):
        return \
        [
            'file_owner_username'
        ]

    # ==============================================================================================
    # ALL FILES BY USER QUERY
    # ==============================================================================================
    def ALL_FILES_BY_USER_QUERY(self):
        return \
        """
             SELECT
                full_file_parent_path,
                file_name,
                file_ext,
                file_owner_username,
                file_uid,
                file_gid,
                file_ctime,
                file_accessed_time,
                file_modified_time,
                CAST(file_size AS FLOAT) / 1073741824.0 as total_size_in_gb,
                '{crawlname}' AS crawl_name
            FROM {crawlname}
            WHERE file_owner_username = '{username}'
        """

    def ALL_FILES_BY_USER_QUERY_COLUMNS(self):
        return \
        [
            'full_file_parent_path',
            'file_name',
            'file_ext',
            'file_owner_username',
            'file_uid',
            'file_gid',
            'file_ctime',
            'file_accessed_time',
            'file_modified_time',
            'total_size_in_gb',
            'crawl_name'
        ]

    # ==============================================================================================
    # ALL FILES QUERY
    # ==============================================================================================

    def ALL_FILES_QUERY(self):
        return \
        """
            SELECT
                full_file_parent_path,
                file_name,
                file_ext,
                file_owner_username,
                file_uid,
                file_gid,
                file_ctime,
                file_accessed_time,
                file_modified_time,
                CAST(file_size AS FLOAT) / 1073741824.0 as total_size_in_gb,
                '{crawlname}' AS crawl_name
            FROM {crawlname}
        """

    def ALL_FILES_QUERY_COLUMNS(self):
        return \
        [
            'full_file_parent_path',
            'file_name',
            'file_ext',
            'file_owner_username',
            'file_uid',
            'file_gid',
            'file_ctime',
            'file_accessed_time',
            'file_modified_time',
            'total_size_in_gb',
            'crawl_name'
        ]

    # ==============================================================================================
    # TOTAL SIZE BY USER BY EXT QUERY
    # ==============================================================================================
    def TOTAL_SIZE_BY_USER_BY_EXT_QUERY(self):
        return \
        """
            SELECT
                file_ext,
                CAST(SUM(file_size) AS FLOAT) / 1073741824.0 as total_size_in_gb,
                '{crawlname}' AS crawl_name
            FROM {crawlname}
            WHERE file_owner_username = '{username}'
            GROUP BY file_ext
        """

    def TOTAL_SIZE_BY_USER_BY_EXT_QUERY_COLUMNS(self):
        return \
        [
            'file_ext',
            'total_size_in_gb',
            'crawl_name'
        ]

    # ==============================================================================================
    # TOTAL SIZE BY EXT QUERY
    # ==============================================================================================
    def TOTAL_SIZE_BY_EXT_QUERY(self):
        return \
        """
            SELECT
                file_ext,
                CAST(SUM(file_size) AS FLOAT) / 1073741824.0 as total_size_in_gb,
                '{crawlname}' AS crawl_name
            FROM {crawlname}
            GROUP BY file_ext
        """

    def TOTAL_SIZE_BY_EXT_QUERY_COLUMNS(self):
        return \
        [
            'file_ext',
            'total_size_in_gb',
            'crawl_name'
        ]

    # ==============================================================================================
    # TOTAL SIZE BY USER QUERY
    # ==============================================================================================
    def TOTAL_SIZE_BY_USER_QUERY(self):
        return \
        """
            SELECT
                CAST(SUM(file_size) AS FLOAT) / 1073741824.0 as total_size_in_gb,
                '{crawlname}' AS crawl_name
            FROM {crawlname}
            WHERE file_owner_username = '{username}'
        """

    def TOTAL_SIZE_BY_USER_QUERY_COLUMNS(self):
        return \
        [
            'total_size_in_gb',
            'crawl_name'
        ]

    # ==============================================================================================
    # TOTAL SIZE QUERY
    # ==============================================================================================
    def TOTAL_SIZE_QUERY(self):
        return \
            """
                SELECT
                    CAST(SUM(file_size) AS FLOAT) / 1073741824.0 as total_size_in_gb,
                    '{crawlname}' AS crawl_name
                FROM {crawlname}
            """

    def TOTAL_SIZE_QUERY_COLUMNS(self):
        return \
            [
                'total_size_in_gb',
                'crawl_name'
            ]

