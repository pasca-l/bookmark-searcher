import os
from contextlib import contextmanager
from enum import Enum, auto
from typing import Any, Generator, Optional, Union

import psycopg
from psycopg.rows import dict_row


class FetchType(Enum):
    NONE = auto()
    ONE = auto()
    ALL = auto()
    ROWCOUNT = auto()


class Database:
    def __init__(
        self,
        connection_string: Optional[str] = None,
    ):
        if connection_string:
            self.connection_string = connection_string
        else:
            host = os.getenv("DB_HOST", "localhost")
            port = os.getenv("DB_PORT", "5432")
            db_name = os.getenv("DB_NAME", "bookmark_searcher_db")
            user = os.getenv("DB_USER", "bookmark_searcher_user")
            password = os.getenv("DB_PASSWORD", "bookmark_searcher_password")

            self.connection_string = (
                f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
            )

    @contextmanager
    def get_connection(
        self,
    ) -> Generator[psycopg.Connection[dict[str, Any]], None, None]:
        conn = psycopg.connect(self.connection_string, row_factory=dict_row)
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @contextmanager
    def get_cursor(
        self, connection: Optional[psycopg.Connection[dict[str, Any]]] = None
    ) -> Generator[psycopg.Cursor[dict[str, Any]], None, None]:
        if connection:
            with connection.cursor() as cursor:
                yield cursor
        else:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    yield cursor

    def execute_query(
        self,
        query: str,
        params: tuple = (),
        fetch: FetchType = FetchType.NONE,
        conn: Optional[psycopg.Connection[dict[str, Any]]] = None,
    ) -> Union[dict[str, Any], list[dict[str, Any]], int, None]:
        with self.get_cursor(conn) as cursor:
            cursor.execute(query, params)

            result: Union[dict[str, Any], list[dict[str, Any]], int, None]
            match fetch:
                case FetchType.ONE:
                    result = cursor.fetchone()
                case FetchType.ALL:
                    result = cursor.fetchall()
                case FetchType.ROWCOUNT:
                    result = cursor.rowcount
                case _:
                    result = None
            return result

    def execute_many(
        self,
        query: str,
        params_list: list[tuple],
        conn: Optional[psycopg.Connection[dict[str, Any]]] = None,
    ) -> int:
        if not params_list:
            return 0

        with self.get_cursor(conn) as cursor:
            cursor.executemany(query, params_list)
            return cursor.rowcount


def new_database(connection_string: Optional[str] = None) -> Database:
    return Database(connection_string=connection_string)
