import psycopg2
from psycopg2.extensions import connection

class GroupService():

    #----------------------------------------------------------------------------------------------------
    # region SQL's
    CREATE_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS public."groups" (
        id int NOT NULL GENERATED ALWAYS AS IDENTITY,
        name text NOT NULL,
        uuid text NOT NULL,
        CONSTRAINT groups_pk PRIMARY KEY (id)
    );
    """

    CREATE_INDEX_SQL = """
    CREATE UNIQUE INDEX IF NOT EXISTS groups_name_idx ON public."groups" ("name");
    """

    DROP_TABLE_SQL = """
    DROP TABLE IF EXISTS public."groups";
    """

    DROP_INDEX_SQL = """
    DROP INDEX IF EXISTS groups_name_idx;
    """

    INSERT_GROUP_SQL = """
    INSERT INTO public."groups" (name, uuid) VALUES (%s, %s) ON CONFLICT (name) DO UPDATE SET uuid = EXCLUDED.uuid;
    """

    UPDATE_GROUP_SQL = """
    UPDATE public."groups" SET uuid = %s WHERE name = %s;
    """

    DELETE_GROUP_SQL = """
    DELETE public."groups" WHERE name = %s;
    """

    SELECT_GROUP_SQL = """
    SELECT uuid FROM public."groups" WHERE name = %s;
    """

    SELECT_ALL_GROUPS_SQL = """
    SELECT name FROM public."groups";
    """
    # endregion
    #----------------------------------------------------------------------------------------------------

    __conn: connection

    def __init__(self, **kwargs) -> None:
        self.__conn = psycopg2.connect(**kwargs)
        self.__init_database()

    #----------------------------------------------------------------------------------------------------
    # region Database
    def __init_database(self):
        curs = self.__conn.cursor()
        curs.execute(self.CREATE_TABLE_SQL)
        curs.execute(self.CREATE_INDEX_SQL)
        self.__conn.commit()

    def __drop_database(self):
        curs = self.__conn.cursor()
        curs.execute(self.DROP_INDEX_SQL)
        curs.execute(self.DROP_TABLE_SQL)
        self.__conn.commit()
    # endregion
    #----------------------------------------------------------------------------------------------------

    def add_group(self, name: str, uuid: str):
        curs = self.__conn.cursor()
        curs.execute(self.INSERT_GROUP_SQL, (name, uuid))
        self.__conn.commit()

    def add_groups(self, groups: list):
        curs = self.__conn.cursor()
        curs.executemany(self.INSERT_GROUP_SQL, groups)
        self.__conn.commit()

    def update_group(self, name: str, uuid: str):
        self.add_group(name, uuid)

    def delete_group(self, name):
        curs = self.__conn.cursor()
        curs.execute(self.DELETE_GROUP_SQL, (name,))
        self.__conn.commit()

    def get_group_uuid(self, name: str) -> str:
        curs = self.__conn.cursor()
        curs.execute(self.SELECT_GROUP_SQL, (name,))
        result = curs.fetchone()
        if result:
            return result[0]
        else:
            return None

    def get_all_groups(self) -> list:
        curs = self.__conn.cursor()
        curs.execute(self.SELECT_ALL_GROUPS_SQL)
        result = curs.fetchall()
        return [r[0] for r in result]
