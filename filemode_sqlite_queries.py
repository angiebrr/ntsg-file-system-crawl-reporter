from sqlite_queries import SqliteQueries

@SqliteQueries.register
class FilemodeSqliteQueries(SqliteQueries):
    """Contains sqlite queries for versions of databases that have crawls that support file modes.
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
                file_mode,
                IFNULL(full_file_parent_path, '') || '/' || IFNULL(file_name, '') || IFNULL(file_ext, '') AS full_path,
                file_ext,
                file_real_path,
                CAST(file_size_in_bytes AS FLOAT) / 1073741824.0 AS total_size_in_gb,
                file_owner_username,
                file_uid,
                file_gid,
                file_ctime,
                file_accessed_time,
                file_modified_time,
                '{crawlname}' AS crawl_name
            FROM {crawlname}
            WHERE file_owner_username = '{username}'
            AND (file_mode = 'FILE' OR file_mode = 'LINK')
        """

    def ALL_FILES_BY_USER_QUERY_COLUMNS(self):
        return \
        [
            'file_mode',
            'full_path',
            'file_ext',
            'file_real_path',
            'total_size_in_gb',
            'file_owner_username',
            'file_uid',
            'file_gid',
            'file_ctime',
            'file_accessed_time',
            'file_modified_time',
            'crawl_name'
        ]

    # ==============================================================================================
    # ALL FILES QUERY
    # ==============================================================================================
    def ALL_FILES_QUERY(self): 
        return \
        """
            SELECT
                file_mode,
                IFNULL(full_file_parent_path, '') || '/' || IFNULL(file_name, '') || IFNULL(file_ext, '') AS full_path,
                file_ext,
                file_real_path,
                CAST(file_size_in_bytes AS FLOAT) / 1073741824.0 AS total_size_in_gb,
                file_owner_username,
                file_uid,
                file_gid,
                file_ctime,
                file_accessed_time,
                file_modified_time,
                '{crawlname}' AS crawl_name
            FROM {crawlname}
            WHERE (file_mode = 'FILE' OR file_mode = 'LINK')
        """

    def ALL_FILES_QUERY_COLUMNS(self): 
        return \
        [
            'file_mode',
            'full_path',
            'file_ext',
            'file_real_path',
            'total_size_in_gb',
            'file_owner_username',
            'file_uid',
            'file_gid',
            'file_ctime',
            'file_accessed_time',
            'file_modified_time',
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
                CAST(SUM(file_size_in_bytes) AS FLOAT) / 1073741824.0 as total_size_in_gb,
                '{crawlname}' AS crawl_name
            FROM {crawlname}
            WHERE file_owner_username = '{username}'
            AND (file_mode = 'FILE' OR file_mode = 'LINK')
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
                CAST(SUM(file_size_in_bytes) AS FLOAT) / 1073741824.0 as total_size_in_gb,
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
                CAST(SUM(file_size_in_bytes) AS FLOAT) / 1073741824.0 as total_size_in_gb,
                '{crawlname}' AS crawl_name
            FROM {crawlname}
            WHERE file_owner_username = '{username}'
            AND (file_mode = 'FILE' OR file_mode = 'LINK')
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
                CAST(SUM(file_size_in_bytes) AS FLOAT) / 1073741824.0 as total_size_in_gb,
                '{crawlname}' AS crawl_name
            FROM {crawlname}
            WHERE (file_mode = 'FILE' OR file_mode = 'LINK')
        """

    def TOTAL_SIZE_QUERY_COLUMNS(self): 
        return \
        [
            'total_size_in_gb',
            'crawl_name'
        ]

