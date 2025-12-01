import sqlite3
class permission_service:
    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='permission'")
        table_exists = self.cursor.fetchone() is not None
        if not table_exists:
            with open('auth_service/role_permission_service/permission_service.sql', 'r') as file:
                sql_script = file.read()
                self.cursor.executescript(sql_script)
                self.connection.commit()
        self.cursor.close()
        self.connection.close()
        print("Database initialized (db.permission_service)")
        pass

    def check_permission(self, role, path,service, method):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("SELECT student, teacher,admin FROM permission WHERE  service = ? AND path = ? AND method = ?", (service,path,method))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result:
            role_index = {'student': 0, 'teacher': 1, 'admin': 2}
            index = role_index.get(role.lower())
            if index is not None and result[index]:
                return True
            else:
                print("Permission denied (db.check_permission)")
                return False
        else:
            print("Permission not found (db.check_permission)")
            return False

    def add_permission(self, role, path, service, method):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        if role == 'student':
            cursor.execute("INSERT INTO permission (service,path,method,student,teacher,admin) VALUES (?, ?, ?, ?,?,?)",
                           (service,path,method, 1,0,0))
        elif role == 'teacher':
            cursor.execute("INSERT INTO permission (service,path,method,student,teacher,admin) VALUES (?, ?, ?, ?,?,?)",
                           (service, path, method, 0, 1, 0))
        elif role == 'admin':
            cursor.execute("INSERT INTO permission (service,path,method,student,teacher,admin) VALUES (?, ?, ?, ?,?,?)",
                           (service, path, method, 0, 0, 1))
        cursor.close()
        connection.commit()
        connection.close()
        print("Permission added (db.add_permission)")