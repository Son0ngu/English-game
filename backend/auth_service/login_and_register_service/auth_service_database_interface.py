import sqlite3


class auth_service_database_interface:
    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='auth_service'")
        table_exists = self.cursor.fetchone() is not None
        if not table_exists:
            with open('auth_service/login_and_register_service/auth_service.sql', 'r') as file:
                sql_script = file.read()
                self.cursor.executescript(sql_script)
                self.connection.commit()
        self.cursor.close()
        self.connection.close()
        print("Database initialized (db.auth_service_database_interface)")
        pass

    def get_user(self, username):
        if self.check_if_user_exist(username):
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM auth_service WHERE username = ?", (username,))
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            return result
        else:
            print("User not found (db.get_user)")
            return None

    def add_user(self, user_id , username, password,role):
        if not self.check_if_user_exist(username):
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            cursor.execute("INSERT INTO auth_service (user_id,username, password,role) VALUES (?, ?,?,?)", (user_id, username, password,role))
            cursor.close()
            connection.commit()
            connection.close()
            return True
        else :
            print("User already exists (db.add_user)")
            return False
    def update_user(self, username, password,role):
        if self.login(username, password):
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            cursor.execute("UPDATE auth_service SET password = ? AND role = ? WHERE username = ?", (password,role, username))
            cursor.close()
            connection.commit()
            connection.close()
            return True
        else :
            print("User not found (db.update_user)")

    def delete_user(self, username):
        if self.check_if_user_exist(username):
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            cursor.execute("DELETE FROM auth_service WHERE username = ?", (username,))
            cursor.close()
            connection.commit()
            connection.close()
            return True
        else:
            print("User not found (db.delete_user)")
            return False

    def check_if_user_exist(self, username):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("SELECT user_id FROM auth_service WHERE username = ?", (username,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result is not None

    def login(self, username, password):
        if self.check_if_user_exist(username):
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM auth_service WHERE username = ? AND password = ?", (username, password))
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            if result:
                return True
            else:
                print("Wrong password (db.login)")
                return False
        else:
            print("User not found (db.login)")
            return False

    def get_id_from_username(self, username):
        if self.check_if_user_exist(username):
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            cursor.execute("SELECT user_id FROM auth_service WHERE username = ?", (username,))
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            return result[0]
        else:
            print("User not found (db.get_id_from_username)")
            return None

    def get_role_from_id(self, user_id):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("SELECT role FROM auth_service WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result:
            return result[0]
        else:
            print("User not found (db.get_role_from_id)")
            return None
