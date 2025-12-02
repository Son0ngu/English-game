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

    def list_permissions(self, role=None, service=None):
        """List permissions với filters"""
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        try:
            if role and service:
                # Filter by both role and service
                if role == 'student':
                    cursor.execute("SELECT service, path, method FROM permission WHERE service = ? AND student = 1", (service,))
                elif role == 'teacher':
                    cursor.execute("SELECT service, path, method FROM permission WHERE service = ? AND teacher = 1", (service,))
                elif role == 'admin':
                    cursor.execute("SELECT service, path, method FROM permission WHERE service = ? AND admin = 1", (service,))
                else:
                    return {"success": False, "error": "Invalid role"}
            elif role:
                # Filter by role only
                if role == 'student':
                    cursor.execute("SELECT service, path, method FROM permission WHERE student = 1")
                elif role == 'teacher':
                    cursor.execute("SELECT service, path, method FROM permission WHERE teacher = 1")
                elif role == 'admin':
                    cursor.execute("SELECT service, path, method FROM permission WHERE admin = 1")
                else:
                    return {"success": False, "error": "Invalid role"}
            elif service:
                # Filter by service only
                cursor.execute("SELECT service, path, method, student, teacher, admin FROM permission WHERE service = ?", (service,))
            else:
                # Get all permissions
                cursor.execute("SELECT service, path, method, student, teacher, admin FROM permission")
            
            rows = cursor.fetchall()
            permissions = []
            
            if role and not service:
                # Format for role-specific queries
                for row in rows:
                    permissions.append({
                        "service": row[0],
                        "path": row[1],
                        "method": row[2]
                    })
            elif service and not role:
                # Format for service-specific queries with role info
                for row in rows:
                    roles = []
                    if row[3]: roles.append("student")
                    if row[4]: roles.append("teacher") 
                    if row[5]: roles.append("admin")
                    permissions.append({
                        "service": row[0],
                        "path": row[1],
                        "method": row[2],
                        "roles": roles
                    })
            else:
                # Format for all permissions or role+service
                for row in rows:
                    if len(row) == 3:  # role+service query
                        permissions.append({
                            "service": row[0],
                            "path": row[1],
                            "method": row[2]
                        })
                    else:  # all permissions query
                        roles = []
                        if row[3]: roles.append("student")
                        if row[4]: roles.append("teacher")
                        if row[5]: roles.append("admin")
                        permissions.append({
                            "service": row[0],
                            "path": row[1],
                            "method": row[2],
                            "roles": roles
                        })
            
            return {"success": True, "permissions": permissions}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            cursor.close()
            connection.close()

    def delete_permission(self, role, path, service, method):
        """Xóa permission cho một role cụ thể"""
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        try:
            # Lấy permission hiện tại
            cursor.execute("SELECT student, teacher, admin FROM permission WHERE service = ? AND path = ? AND method = ?",
                          (service, path, method))
            existing = cursor.fetchone()
            
            if not existing:
                return {"success": False, "error": "Permission not found"}
            
            current_student, current_teacher, current_admin = existing
            
            # Cập nhật permission - chỉ remove role được chỉ định
            if role == 'student':
                new_student = 0
                new_teacher = current_teacher
                new_admin = current_admin
            elif role == 'teacher':
                new_student = current_student
                new_teacher = 0
                new_admin = current_admin
            elif role == 'admin':
                new_student = current_student
                new_teacher = current_teacher
                new_admin = 0
            else:
                return {"success": False, "error": "Invalid role"}
            
            # Nếu không còn role nào, xóa record
            if not any([new_student, new_teacher, new_admin]):
                cursor.execute("DELETE FROM permission WHERE service = ? AND path = ? AND method = ?",
                              (service, path, method))
            else:
                cursor.execute(
                    "UPDATE permission SET student = ?, teacher = ?, admin = ? WHERE service = ? AND path = ? AND method = ?",
                    (new_student, new_teacher, new_admin, service, path, method))
            
            connection.commit()
            return {"success": True, "message": f"Permission removed for {role}"}
            
        except Exception as e:
            connection.rollback()
            return {"success": False, "error": str(e)}
        finally:
            cursor.close()
            connection.close()

    def get_role_permissions(self, role):
        """Get all permissions cho một role"""
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        try:
            if role == 'student':
                cursor.execute("SELECT service, path, method FROM permission WHERE student = 1")
            elif role == 'teacher':
                cursor.execute("SELECT service, path, method FROM permission WHERE teacher = 1")
            elif role == 'admin':
                cursor.execute("SELECT service, path, method FROM permission WHERE admin = 1")
            else:
                return {"success": False, "error": "Invalid role"}
            
            rows = cursor.fetchall()
            permissions = []
            for row in rows:
                permissions.append({
                    "service": row[0],
                    "path": row[1],
                    "method": row[2]
                })
            
            return {"success": True, "permissions": permissions}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            cursor.close()
            connection.close()