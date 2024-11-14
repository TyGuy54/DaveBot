import sqlite3
from util.apis.database.db_connection import connect_to_db

class DB_Ops(sqlite3.Cursor):
    """
        Generic databse operations
    """
    def __init__(self, database: str):
        db = connect_to_db(database)

        self.conn = db[0]
        self.curr = db[1]

        super().__init__(self.conn)

    def instert_data(self, table_name: str, data_dict: dict):
        get_len = len(data_dict)
        get_keys = tuple(data_dict.keys())

        _tuple = ()
        _list = list(_tuple)

        for x in range(get_len):
            _list.insert(x, '?')

        new_tuple = tuple(_list)
        insert_statment = f"INSERT INTO {table_name} {*get_keys,} VALUES {*new_tuple,}".replace("'", "")
        
        self.curr.execute(insert_statment, list(data_dict.values()))

        self.conn.commit()

    def get_all_data(self, table_name: str):
        db_data = []

        sql_query = f"SELECT * FROM {table_name};"
        data = self.curr.execute(sql_query)

        col_names = [col[0] for col in data.description]
        
        try:
            self.conn.row_factory = sqlite3.Row

            self.curr.execute(f"SELECT * FROM {table_name}")
            rows = self.curr.fetchall()

            for i in range(len(rows)):
                data = {}

                for j, col_name in enumerate(col_names):
                    data[col_name] = rows[i][j]

            db_data.append(data)

            self.conn.commit()
        except sqlite3.Error as e:
            data = []
            self.conn.rollback()
            return data.append(e)
        finally:
            self.curr.close()
            self.conn.close()

        return db_data

    def get_data_by_id(self, table_name: str, _id: int):
        db_data = {}

        sql_query = f"SELECT * FROM {table_name} WHERE id = ?;"
        
        try:
            self.conn.row_factory = sqlite3.Row

            data = self.curr.execute(sql_query, (_id,))
            row = self.curr.fetchone()

            if row:
                col_names = [col[0] for col in data.description]

                for j, col_name in enumerate(col_names):
                    db_data[col_name] = row[j]

            self.conn.commit()
        except sqlite3.Error as e:
            self.conn.rollback()
            return {"error": str(e)}
        finally:
            self.curr.close()
            self.conn.close()

        return db_data
                
    def delete_data_by_id(self, table_name: str, _id: str):
        message = {}
        try:
            self.cur.execute(f'DELETE FROM {table_name} WHERE id = ?', (_id,))

            self.conn.commit()
            message["status"] = "Data deleted successfully"
        except Exception as e:
            self.conn.rollback()
            message["status"] = "Cannot delete data"
            return e
        finally:
            self.conn.close()

    def close(self):
        """Close the database connection."""
        self.conn.close()
                                