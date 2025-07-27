import sqlite3
from modules.data_handlers.executable_file_redirector import *

class ManageData:
    def __init__(self) -> None:
        self.database_path = convert().get_resource_path('amadeus_database.db')
        if not os.path.exists(self.database_path):
            print(f"Database file not found: {self.database_path}")
        try:
            # Establish a connection to the database
            self.conn = sqlite3.connect(self.database_path)
            self.cursor = self.conn.cursor()
        except sqlite3.OperationalError as e:
            print(f"Error connecting to the database: {e}")


''' Fetch any kind of data in any table in the app's file-base DB '''
class FetchData(ManageData):
    def __init__(self) -> None:
        super().__init__()

    def check_user(self, user_id: str, password:str) -> tuple[bool, str] | None:
        try:
            self.cursor.execute(f"SELECT user_name, password FROM users WHERE  user_name = ? and password = ?", (user_id, password,))
            result = self.cursor.fetchall()
            if len(result) != 0:
                return True, user_id
            else:
                return False, user_id
        except sqlite3.OperationalError as e:
            print('error in check_user:')
            print(e)
    
    def check_chatroom(self, user_id:str) -> str | None:
        try:
            self.cursor.execute(f"SELECT chat_id FROM chatrooms WHERE  user = ? ", (user_id,))
            result = self.cursor.fetchall()
            if result:
                return result[0][0]
            else:
                return None
        except sqlite3.OperationalError as e:
            print('error in check_chatroom:')
            print(e)


''' Add, Delete or Update existing data in the app's file-base DB '''
class EditData(ManageData):
    def __init__(self)-> None:
        super().__init__()
    
    def add_chatroom(self, user_id:str, chat_id:str)-> bool:
        try:
            sql = "INSERT INTO chatrooms (user, chat_id) VALUES (?, ?);"
            self.cursor.execute(sql, (user_id, chat_id))
            self.conn.commit()
            return True
        except sqlite3.OperationalError as e:
            print('error in add_chatroom:')
            print(f"Error inserting chat room: {e}")
            return False
        finally:
            if self.conn:
                self.conn.close()
    
    def delete_chatroom(self, user_id:str)-> bool:
        try:
            self.cursor.execute(f"DELETE FROM chatrooms WHERE  user = ? ", (user_id,))
            self.conn.commit()
            print('chatroom deleted')
            return True
        except sqlite3.OperationalError as e:
            print(e)
            return False
