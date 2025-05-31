### this is the edited and loaded code

import sqlite3

class DatabaseManager:
    def __init__(self, db_name="radar_systems.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS systems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parent_id INTEGER,
            system_name TEXT NOT NULL,
            description TEXT,
            upload_date TEXT,
            uploader_name TEXT,
            video_path TEXT,
            docs_path TEXT,
            radar_type TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Authentication (
            username TEXT PRIMARY KEY DEFAULT 'admin',
            password TEXT DEFAULT 'admin'
        )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS About_compiler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                extra_label TEXT DEFAULT 'Extra Info',
                header_label TEXT DEFAULT 'Header',
                conceived_label TEXT DEFAULT 'Conceived By',
                author_label TEXT DEFAULT 'compiler Name'
            )
        """)




        
                
        self.conn.commit()

    def insert_system(self, parent_id, system_name, description, upload_date, uploader_name, video_path, docs_path, radar_type):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO systems (parent_id, system_name, description, upload_date, uploader_name, video_path,docs_path, radar_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (parent_id, system_name, description, upload_date, uploader_name, video_path, docs_path, radar_type))
        self.conn.commit()
        return cursor.lastrowid

    def get_top_level_systems(self, radar_type):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, system_name FROM systems WHERE radar_type = ? AND parent_id IS NULL", (radar_type,))
        return cursor.fetchall()

    def get_subsystems(self, parent_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, system_name FROM systems WHERE parent_id = ?", (parent_id,))
        return cursor.fetchall()

    def get_system_details(self, system_id):
        cursor = self.conn.cursor()
##        cursor.execute("SELECT * FROM systems ORDER BY id DESC LIMIT 1")
        cursor.execute("SELECT * FROM systems WHERE id = ?", (system_id,))
        return cursor.fetchone()
    

    def delete_systems(self,radar_type, main_id):
        cursor = self.conn.cursor()
##        cursor.execute("DELETE FROM systems WHERE id=?", (system_id,))
        cursor.execute("DELETE FROM systems WHERE radar_type = ? AND parent_id = ?", (radar_type, main_id))
        cursor.execute("DELETE FROM systems WHERE radar_type = ? AND id = ?", (radar_type, main_id))
        self.conn.commit()

    def delete_sub_systems(self,radar_type, sub_id):
        cursor = self.conn.cursor()
##        cursor.execute("DELETE FROM systems WHERE id=?", (system_id,))
        cursor.execute("DELETE FROM systems WHERE radar_type = ? AND id = ?", (radar_type, sub_id))
        self.conn.commit()


###### combo data manipulation

    def combo_data(self,radar_type):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, system_name FROM systems WHERE radar_type = ? AND parent_id IS NULL", (radar_type,))
        return cursor.fetchall()


    def sub_combo_data(self,radar_type, main_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, system_name FROM systems WHERE radar_type = ? AND parent_id = ?", (radar_type, main_id))
        return cursor.fetchall()


############## for table authentication
    
    def insert_user(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO Authentication (username, password)
            VALUES (?, ?)
        """, (username, password))
        self.conn.commit()
        return cursor.lastrowid

    def authenticate(self, username):
        cursor = self.conn.cursor()
        
        # Check if the table is empty
        cursor.execute("SELECT COUNT(*) FROM Authentication")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO Authentication (username, password)
                VALUES (?, ?)
            """, ("admin", "admin"))
            self.conn.commit()

        
        ##        cursor.execute("SELECT * FROM systems ORDER BY id DESC LIMIT 1")
        cursor.execute("SELECT password FROM Authentication WHERE username = ?", (username,))
        return cursor.fetchone()

    def get_user_password(self, old_username):
        cursor = self.conn.cursor()
        cursor.execute("SELECT username, password FROM Authentication WHERE username = ?", (old_username,))
        return cursor.fetchone()  # returns a single tuple: (username, password) or None


    def update_user(self, new_username, new_password, old_username, old_password):
        cursor = self.conn.cursor()
        ##        cursor.execute("DELETE FROM systems WHERE id=?", (system_id,))

        cursor.execute("""
            UPDATE Authentication
            SET username = ?, password = ?
            WHERE username = ? AND password = ?
        """, (new_username, new_password, old_username, old_password))
        
        self.conn.commit()

####### fetching for editings
    def fetch_for_edit(self, system_name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM systems WHERE system_name = ?", (system_name,))
        return cursor.fetchone()
        
    def edit_system(self, sys_id, parent_id, system_name, description, upload_date, uploader_name, video_path, docs_path, radar_type):
        cursor = self.conn.cursor()
        ##        cursor.execute("DELETE FROM systems WHERE id=?", (system_id,))

        cursor.execute("""
            UPDATE systems
            SET parent_id = ?, system_name = ?, description = ?, upload_date = ?, uploader_name = ?, video_path = ?, docs_path = ?, radar_type = ?
            WHERE id = ?
        """, (parent_id, system_name, description, upload_date, uploader_name, video_path, docs_path, radar_type, sys_id))
        
        self.conn.commit()

###### adding labels
        
    def update_labels(self, values):       
        cursor = self.conn.cursor()
        # Check if the table is empty
        cursor.execute("SELECT COUNT(*) FROM About_compiler")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO About_compiler (extra_label, header_label, conceived_label, author_label)
                VALUES (?, ?, ?, ?)
            """, ("Extra Info", "Header", "Conceived By", "Author Name"))
            self.conn.commit()
        
        cursor.execute("""
            UPDATE About_compiler
            SET extra_label = ?, header_label = ?, conceived_label = ?, author_label = ?
            WHERE id = ?
        """, (values[0], values[1], values[2], values[3], 1))

        self.conn.commit()
            
##        """, (values[0], values[1], values[2], values[3]))
##        self.conn.commit()
##        return cursor.lastrowid

    def get_compiler_labels(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT extra_label, header_label, conceived_label, author_label FROM About_compiler LIMIT 1")
        row = cursor.fetchone()
        return row if row else ("", "", "", "")


### the practice area
##  
##db = DatabaseManager("radar_systems.db")
##lis = [8,11,12,13,17,18,19,20,24,29,32,33]
##for i in lis:
##    result = db.delete_systems("Radar 1", i)        #self,radar_type, main_id
########_, parent_id, system_name, description, upload_date, uploader_name, video_path, radar_type = result
##print ()

##db = DatabaseManager("radar_systems.db")
##print(db.update_user("balochi", "kings", "ramzee", "1234"))


##print(" ")
##
##for entry in db.combo_data("Radar 1"):
##    print (entry[1])
##    print(" ")
