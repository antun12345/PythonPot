import sqlite3


def create_connection(db_file):
    db_connection = None

    try:
        db_connection = sqlite3.connect(db_file)
        return db_connection
    except sqlite3.Error as db_error:
        print(db_error)

    return db_connection


def create_table(db_connection, create_table_sql):
    try:
        cursor = db_connection.cursor()
        cursor.execute(create_table_sql)
    except sqlite3.Error as db_error:
        print(db_error)


def insert_data(db_connection, data, query):
    cursor = db_connection.cursor()
    cursor.execute(query, data)
    db_connection.commit()
    return cursor.lastrowid


def update_base(db_connection, table, column_name, id, new_value):
    query = f"UPDATE {table} SET {column_name} = ? WHERE id = ?"
    cursor = db_connection.cursor()
    cursor.execute(query, (new_value, id))
    db_connection.commit()


def update_plant_base(db_connection, plant_info, query):
    cursor = db_connection.cursor()
    cursor.execute(query, plant_info)
    db_connection.commit()


def delete_data(db_connection, table, locator, data):
    sql = f'DELETE FROM {table} WHERE {locator}=?'
    cursor = db_connection.cursor()
    cursor.execute(sql, (data,))
    db_connection.commit()


def delete_all_data(db_connection, table):
    sql = f'DELETE FROM {table}'
    cursor = db_connection.cursor()
    cursor.execute(sql)
    db_connection.commit()


def select_all_data(db_connection, table):
    cursor = db_connection.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    return cursor.fetchall()


def select_employees_by_id(db_connection, emp_id):
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM Employees WHERE priority=?", (emp_id,))
    rows = cursor.fetchall()

    for row in rows:
        print(row)
