import sqlite3


def extract_data_from_db(table, cols, DB_PATH):
    """
    :param table: table of db to extract data
    :param cols: columns of table to extract data
    :param DB_PATH: path to database
    :return: result as list or cortex
    """
    # get regions features
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(f"""SELECT {','.join(cols)} from {table}""")
    result_data = cursor.fetchall()
    connection.close()

    return result_data