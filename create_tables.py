import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def create_database():
    """
    Main function to create the database.

    Args:
        None

    Returns:
        None
    """

    # connect to default database
    conn = psycopg2.connect("host=127.0.0.1 dbname=studentdb user=student password=student")
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    # create sparkify database with UTF8 encoding
    cur.execute(database_drop)
    cur.execute(database_create)

    # close connection to default database
    conn.close()

    # connect to sparkify database
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    return cur, conn


def drop_tables(cur, conn):
    """
    This function drops tables from psql database.

    Args:
        cur (psql cursor): connection cursor for postgres db.
        conn (psql connection): connection for postgres db using psycopg2.

    Returns:
        None
    """

    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    This function creates tables using sql_queries.py in the psql database.

    Args:
        cur (psql cursor): connection cursor for postgres db.
        conn (psql connection): connection for postgres db using psycopg2.

    Returns:
        None
    """

    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Main function to create the tables in the database and that database itself.

    Args:
        None

    Returns:
        None
    """

    cur, conn = create_database()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
