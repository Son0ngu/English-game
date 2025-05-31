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

    def permission_exists(self, role, service, path, method):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        if role == 'student':
            cursor.execute(
                "SELECT COUNT(*) FROM permission WHERE service = ? AND path = ? AND method = ? AND student = 1",
                (service, path, method))
        elif role == 'teacher':
            cursor.execute(
                "SELECT COUNT(*) FROM permission WHERE service = ? AND path = ? AND method = ? AND teacher = 1",
                (service, path, method))
        elif role == 'admin':
            cursor.execute(
                "SELECT COUNT(*) FROM permission WHERE service = ? AND path = ? AND method = ? AND admin = 1",
                (service, path, method))
        else:
            cursor.close()
            connection.close()
            return False

        result = cursor.fetchone()[0] > 0
        cursor.close()
        connection.close()
        if result:
            return True
        else: return False

    def add_permission(self, roles, path, service, method):
        if not isinstance(roles, list):
            roles = [roles]

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM permission WHERE service = ? AND path = ? AND method = ?",
                       (service, path, method))
        exists = cursor.fetchone()[0] > 0

        student_val = 1 if 'student' in roles else 0
        teacher_val = 1 if 'teacher' in roles else 0
        admin_val = 1 if 'admin' in roles else 0

        if exists:
            cursor.execute(
                "UPDATE permission SET student = ?, teacher = ?, admin = ? WHERE service = ? AND path = ? AND method = ?",
                (student_val, teacher_val, admin_val, service, path, method))
        else:
            cursor.execute(
                "INSERT INTO permission (service,path,method,student,teacher,admin) VALUES (?, ?, ?, ?,?,?)",
                (service, path, method, student_val, teacher_val, admin_val))

        cursor.close()
        connection.commit()
        connection.close()
        print(f"Permission added for roles {roles} (db.add_permission)")
        return True

    def change_permission_to_existing_path(self, roles, path, service, method):

        if not isinstance(roles, list):
            roles = [roles]

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        cursor.execute("SELECT student, teacher, admin FROM permission WHERE service = ? AND path = ? AND method = ?",
                       (service, path, method))
        existing = cursor.fetchone()

        if not existing:
            cursor.close()
            connection.close()
            print(f"Path {service}/{path} with method {method} does not exist")
            return False

        current_student, current_teacher, current_admin = existing

        student_val = 1 if 'student' in roles or current_student == 1 else 0
        teacher_val = 1 if 'teacher' in roles or current_teacher == 1 else 0
        admin_val = 1 if 'admin' in roles or current_admin == 1 else 0

        cursor.execute(
            "UPDATE permission SET student = ?, teacher = ?, admin = ? WHERE service = ? AND path = ? AND method = ?",
            (student_val, teacher_val, admin_val, service, path, method))

        cursor.close()
        connection.commit()
        connection.close()
        print(f"Permission added for roles {roles} to existing path {service}/{path} (method: {method})")
        return True