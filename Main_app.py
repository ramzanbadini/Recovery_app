import sys
import os
import shutil
from Database import DatabaseManager
from Multimedia import VideoPlayerWidget
from Multimedia import CustomVideoWidget
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize
from PyQt6 import QtWidgets, QtCore, QtGui, QtMultimedia, QtMultimediaWidgets
from PyQt6.QtCore import Qt

master_key = "ramzee"
master_password = "1234"

class LoginDialog(QtWidgets.QDialog):
    def __init__(self, radar_type, db_manager, parent=None):
        super().__init__(parent)
        self.radar_type = radar_type
        self.db_manager = db_manager
        self.setWindowTitle("Only Admin Authorized")
        self.setFixedSize(400, 200)

        self.init_ui()
        
    def init_ui(self):
        layout = QtWidgets.QFormLayout(self)

        self.username_input = QtWidgets.QLineEdit()
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        layout.addRow("Username:", self.username_input)
        layout.addRow("Password:", self.password_input)

        self.login_button = QtWidgets.QPushButton("Login")
        self.login_button = self.but_styl(self.login_button,"#578959")
        self.login_button.clicked.connect(self.check_credentials)
        
        layout.addWidget(self.login_button)
        
        self.change_password_button = QtWidgets.QPushButton("Change Password")
        self.change_password_button = self.but_styl(self.change_password_button, "#ea9999")
        self.change_password_button.clicked.connect(self.open_change_password_dialog)

        spacer = QtWidgets.QSpacerItem(
            20, 10,
            QtWidgets.QSizePolicy.Policy.Expanding, 
            QtWidgets.QSizePolicy.Policy.Minimum
        )

        layout.addItem(spacer)
        
        layout.addWidget(self.change_password_button)


        self.setLayout(layout)
        self.access_granted = False


    def but_styl(self, button, color: str):
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                font-size: 14px;
                font-weight: bold;
                border: none;
                padding: 6px 6px;           /* reduced from 16px to 12px */
                border-radius: 6px;
                min-width: 60px;             /* adjust this */
                max-width: 140px;            /* optional cap */
            }}
            QPushButton:hover {{
                background-color: #257526;
            }}
            QPushButton:pressed {{
                background-color: #2471a3;
            }}
        """)
        return button

    def check_credentials(self):

        
##        username = "admin" #self.username_input.text()
##        password = "1234" #self.password_input.text()

        username = self.username_input.text()
        password = self.password_input.text()

        result = self.db_manager.authenticate(username)
        print ("this is the pass: ", result)
        
        if result and password == result[0]:
            self.access_granted = True
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, "Access Denied", "Invalid username or password")

    def open_change_password_dialog(self):
        dialog = ChangePasswordDialog(self.radar_type, self.db_manager, self)
        dialog.exec()



####
class ChangePasswordDialog(QtWidgets.QDialog):
    def __init__(self, radar_type, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setFixedSize(400, 200)
        self.setWindowTitle("Change Password")


        layout = QtWidgets.QFormLayout(self)
 ## the old user name and passoerd
        self.old_user_input = QtWidgets.QLineEdit()
        
        self.old_password_input = QtWidgets.QLineEdit()
       #self.old_password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)     #to hide te password in dots

## new user and password
        self.new_user_input = QtWidgets.QLineEdit()
        
        self.new_password_input = QtWidgets.QLineEdit()
        #self.new_password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        layout.addRow("Old User:", self.old_user_input)
        layout.addRow("Old Password:", self.old_password_input)

        layout.addRow("New User:", self.new_user_input)
        layout.addRow("New Password:", self.new_password_input)
        
        self.submit_button = QtWidgets.QPushButton("Submit")
        self.submit_button.clicked.connect(self.change_password)
        layout.addWidget(self.submit_button)

    def change_password(self):
        old_user = self.old_user_input.text()
        old_pw = self.old_password_input.text()
        
        new_user = self.new_user_input.text()
        new_pw = self.new_password_input.text()

   
        results = self.db_manager.get_user_password(old_user)
        print ("the old password is: ", results)


        if results and results[0] == old_user:
            if results[1] == old_pw:

                update_user = self.db_manager.update_user(new_user, new_pw, results[0], results[1])

                QtWidgets.QMessageBox.information(self, "Success", "Password changed successfully.")
                self.accept()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Old password is incorrect.")
                
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Old user or Password incorrect.")



## uploading data diaglloge
class UploadDialog(QtWidgets.QDialog):
    def __init__(self, radar_type, db_manager, parent=None):
        super().__init__(parent)
        self.radar_type = radar_type
        self.db_manager = db_manager
        self.setWindowTitle("Upload New System")
        self.resize(600, 500)

        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

##        layout.addWidget(QtWidgets.QLabel("Upload Systems and Sub-Systems"))
##        layout.addWidget(self.upload_date_edit)

        label = QtWidgets.QLabel("Upload Systems or Sub-Systems")
        label.setStyleSheet("""
            QLabel {
                font-size: 16pt;
                font-weight: bold;
                color: #2C3E50;
                font-family: 'Segoe UI', sans-serif;
            }
        """)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the label
        layout.addWidget(label)

        
## system laoyt
        new_sys_layout = QtWidgets.QHBoxLayout()
        new_sys_layout.addWidget(QtWidgets.QLabel("New Equipment"))
        # System name
        self.system_name_edit = QtWidgets.QLineEdit(self)
        self.system_name_edit.setFixedWidth(400)  # Fix width

        self.system_name_edit.setPlaceholderText("System Name")
        new_sys_layout.addWidget(self.system_name_edit)

##parent laout
        # Parent system selection

        exi_layout = QtWidgets.QHBoxLayout()
        exi_layout.addWidget(QtWidgets.QLabel("Add to existing System"))
        
        self.parent_combo = QtWidgets.QComboBox(self)
        self.parent_combo.setFixedWidth(400)  # Fix width
        self.parent_combo.addItem("New", userData=None)
        
        # Populate with top-level systems of this radar type
        for sys_id, name in self.db_manager.get_top_level_systems(self.radar_type):
            self.parent_combo.addItem(name, userData=sys_id)
        #exi_layout.addWidget(QtWidgets.QLabel("Parent System (optional):"))
        exi_layout.addWidget(self.parent_combo)

        layout.addLayout(new_sys_layout)
        layout.addLayout(exi_layout)



        # Description
        self.description_edit = QtWidgets.QTextEdit(self)
        self.description_edit.setPlaceholderText("Description/Rectification Steps")
##        self.description_edit.toHtml()
        layout.addWidget(self.description_edit)

#### the datelaoyt
        date_layout = QtWidgets.QHBoxLayout()

        # Upload date
        self.upload_date_edit = QtWidgets.QDateEdit(self)
        self.upload_date_edit.setFixedWidth(400)  # Fix width
        self.upload_date_edit.setCalendarPopup(True)
        self.upload_date_edit.setDate(QtCore.QDate.currentDate())
        date_layout.addWidget(QtWidgets.QLabel("Upload Date:"))
        date_layout.addWidget(self.upload_date_edit)

        layout.addLayout(date_layout)

###### uploadername layout
        uploader_layout = QtWidgets.QHBoxLayout()
        
        # Uploader name
        uploader_layout.addWidget(QtWidgets.QLabel("Uploaded by :"))

        self.uploader_name_edit = QtWidgets.QLineEdit(self)
        self.uploader_name_edit.setFixedWidth(400)  # Fix width
        self.uploader_name_edit.setPlaceholderText("Uploader Name")
        uploader_layout.addWidget(self.uploader_name_edit)

        layout.addLayout(uploader_layout)

###### video path layout
        # Video file selection
        file_layout = QtWidgets.QHBoxLayout()

        file_layout.addWidget(QtWidgets.QLabel("Upload Video: "))

        self.video_path_edit = QtWidgets.QLineEdit(self)
        self.video_path_edit.setFixedWidth(300)  # Fix width
        self.video_path_edit.setPlaceholderText("Select MP4 Video")
        file_layout.addWidget(self.video_path_edit)
        browse_btn = QtWidgets.QPushButton("Browse", self)
        browse_btn = self.button_style(browse_btn, "#346e1b")
        

        
        browse_btn.clicked.connect(self.browse_video)
        file_layout.addWidget(browse_btn)
        layout.addLayout(file_layout)

###### separator line

        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        layout.addWidget(line)

        # Dialog buttons: Submit and Cancel
        btn_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok |
                                             QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        btn_box = self.button_style(btn_box, "#2778b4")        
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)


    def button_style(self, button, color: str):
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                font-size: 14px;
                font-weight: bold;
                border: none;
                padding: 6px 6px;           /* reduced from 16px to 12px */
                border-radius: 6px;
                min-width: 60px;             /* adjust this */
                max-width: 90px;            /* optional cap */
            }}
            QPushButton:hover {{
                background-color: #257526;
            }}
            QPushButton:pressed {{
                background-color: #2471a3;
            }}
        """)
        return button

    def browse_video(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setNameFilter("MP4 files (*.mp4)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                source_path = os.path.abspath(selected_files[0])  # Absolute path of selected file
                file_name = os.path.basename(source_path)

                # Define Videos folder relative to Main_app.py location
                base_dir = os.path.dirname(os.path.abspath(__file__))  # Folder where Main_app.py is located
                videos_dir = os.path.join(base_dir, "Videos")

                # Create Videos folder if it doesn't exist
                os.makedirs(videos_dir, exist_ok=True)

                # Destination path
                destination_path = os.path.join(videos_dir, file_name)

                #until the video is copying
                self.video_path_edit.setText("Copying, please wait...")
                QtWidgets.QApplication.processEvents()  # Force UI to update immediately

                # Copy only if it's not already in the Videos folder
                if source_path != destination_path:
                    shutil.copy2(source_path, destination_path)

                # Set the new path in the QLineEdit
                self.video_path_edit.setText(destination_path)
                print(destination_path)
                

    def get_upload_data(self):
        parent_id = self.parent_combo.currentData()  # Eacg sub_sys will have a parent ID and for top level that would be none
        return {
            "parent_id": parent_id,
            "system_name": self.system_name_edit.text(),
            "description": self.description_edit.toHtml(),  #toPlainText(),
            "upload_date": self.upload_date_edit.date().toString(QtCore.Qt.DateFormat.ISODate),
            "uploader_name": self.uploader_name_edit.text(),
            "video_path": self.video_path_edit.text(),
            "radar_type": self.radar_type
        }

class RemoveDialog(QtWidgets.QDialog):
    def __init__(self, radar_type, db_manager, parent=None):
        super().__init__(parent)
        self.radar_type = radar_type
        self.db_manager = db_manager
        self.setWindowTitle("Delete System")
        self.resize(500, 400)

        self.init_ui()

    def init_ui(self):

        parent_layout = QtWidgets.QVBoxLayout(self)

##  delete title
        self.del_title = QtWidgets.QLabel("Delete Systems")

        self.del_title.setStyleSheet("""
        QLabel {
            font-weight: bold;
            font-size: 18px;
            color: #2c3e50;
            }
        """)

        sys_layout  = QtWidgets.QHBoxLayout(self)        
        # system labele and combo
        self.sys_label = self.del_labels("Select System")
        sys_layout.addWidget(self.sys_label)

        self.mainCombo = QtWidgets.QComboBox()
        self.mainCombo.setStyleSheet("""
            QComboBox {
                border: 2px solid #555;
                border-radius: 5px;
                padding: 5px;
                background-color: #f0f0f0;
                font-size: 14px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left: 1px solid #555;
            }
            
            QComboBox QAbstractItemView {
                background-color: #fff;
                selection-background-color: #6fa8dc;
                border: 1px solid #aaa;
            }
        """)
    
        sys_layout.addWidget(self.mainCombo)

### sub system lable and combo
        subsys_layout  = QtWidgets.QHBoxLayout(self)

        self.subsys_label = self.del_labels("Select Sub-System")
        subsys_layout.addWidget(self.subsys_label)
                    
        self.subCombo = QtWidgets.QComboBox()

        self.subCombo.setStyleSheet("""
            QComboBox {
                border: 2px solid #555;
                border-radius: 5px;
                padding: 5px;
                background-color: #f0f0f0;
                font-size: 14px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left: 1px solid #555;
            }
            QComboBox QAbstractItemView {
                background-color: #fff;
                selection-background-color: #6fa8dc;
                border: 1px solid #aaa;
            }
        """)
        
        subsys_layout.addWidget(self.subCombo)
######
        self.load_main_items()
        self.mainCombo.currentIndexChanged.connect(self.load_sub_items)
##        self.okButton.clicked.connect(self.delete_item)

######        
        delete_button = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok |
                                             QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        ok_button = delete_button.button(QtWidgets.QDialogButtonBox.StandardButton.Ok)
        ok_button.setText("Delete")
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border: none;
                padding: 6px 16px;
                border-radius: 6px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #2471a3;
            }
        """)
        delete_button.accepted.connect(self.accept)
        delete_button.rejected.connect(self.reject)
        #layout.addWidget(btn_box)

        
################

        parent_layout.addLayout(sys_layout)
        parent_layout.addLayout(subsys_layout)

        parent_layout.addWidget(delete_button)



    def del_labels(self,text):
        label = QtWidgets.QLabel(text)

        label.setStyleSheet("""
        QLabel {
            font-weight: bold;
            font-size: 15px;
            color: #2c3e50;
            padding: 4px;
            }
        """)
        return label

##### New code
    def load_main_items(self):
        self.mainCombo.clear()
        self.main_items = {}

        sys_name = self.db_manager.combo_data(self.radar_type)
##            for entry in sys_name:
##                self.syscombo.addItem(entry[1], entry[0])
##            
##            cur = self.conn.cursor()
##            cur.execute("SELECT id, system_name FROM systems WHERE parent_id IS NULL")
        for item_id, name in sys_name:
            self.main_items[name] = item_id
            self.mainCombo.addItem(name)

        if self.mainCombo.count() > 0:
            self.load_sub_items()    


    def load_sub_items(self):
        self.subCombo.clear()
        self.subCombo.addItem("All")  # For deleting whole system
        selected_main = self.mainCombo.currentText()
        main_id = self.main_items.get(selected_main)
        if not main_id:
            return

        sub_sys_name = self.db_manager.sub_combo_data(self.radar_type, main_id)

##            cur = self.conn.cursor()
##            cur.execute("SELECT id, system_name FROM systems WHERE parent_id = ?", (main_id,))
        self.sub_items = {}
        for sub_id, name in sub_sys_name:
            self.sub_items[name] = sub_id
            self.subCombo.addItem(name)

    def delete_item(self):
        selected_main = self.mainCombo.currentText()
        main_id = self.main_items.get(selected_main)
        selected_sub = self.subCombo.currentText()

##        cur = self.conn.cursor()

        if selected_sub == "All":
            reply = QtWidgets.QMessageBox.question(
                self, "Confirm Deletion",
                f"Delete main system '{selected_main}' and all its sub-systems?",
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
            )
            if reply == QtWidgets.QMessageBox.StandardButton.Yes:

                del_sys = self.db_manager.delete_systems(self.radar_type, main_id)
                
##                cur.execute("DELETE FROM systems WHERE parent_id = ?", (main_id,))
##                cur.execute("DELETE FROM systems WHERE id = ?", (main_id,))
##                self.conn.commit()
                QtWidgets.QMessageBox.information(self, "Deleted", f"'{selected_main}' and all its sub-systems deleted.")
                self.load_main_items()
        else:
            sub_id = self.sub_items.get(selected_sub)
            if sub_id:
                reply = QtWidgets.QMessageBox.question(
                    self, "Confirm Deletion",
                    f"Delete sub-system '{selected_sub}'?",
                    QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
                )
                if reply == QtWidgets.QMessageBox.StandardButton.Yes:

                    del_sub_sys = self.db_manager.delete_sub_systems(self.radar_type, sub_id)

##                    cur.execute("DELETE FROM systems WHERE id = ?", (sub_id,))
##                    self.conn.commit()
                    QtWidgets.QMessageBox.information(self, "Deleted", f"'{selected_sub}' deleted.")
                    self.load_sub_items()



### Window for uploading radar type
class RadarAppMainWindow(QtWidgets.QMainWindow):
    def __init__(self, radar_type, db_manager, parent=None):
        super().__init__(parent)
        self.radar_type = radar_type
        self.db_manager = db_manager
        self.setWindowTitle(f"Radar Recovery Application - {radar_type}")
        self.showMaximized()
       # self.setMinimumSize(1000, 700)
        self.init_ui()
        self.setStyleSheet("background-color: #e2f1f6;")  # Light blue background


    def init_ui(self):
        # Create main widget and a horizontal splitter for left (tree) and right (content)
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        main1_layout = QtWidgets.QVBoxLayout(central_widget)

        main2_layout = QtWidgets.QHBoxLayout()


        #### title buttons Home and Exit
        title_layout = QtWidgets.QHBoxLayout()
##        title_layout.setSpacing(30)

##        title_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Align to left

        home_button = self.but_style("Home", "#8d9d8c")
        home_button.clicked.connect(self.go_home)
        title_layout.addWidget(home_button)

        title_layout.addStretch() ## push the button to the left and right most corners

        exit_button = self.but_style("Exit", "#8d9d8c")
        exit_button.clicked.connect(QtWidgets.QApplication.quit)
        title_layout.addWidget(exit_button)

        main1_layout.addLayout(title_layout)
        
        self.main_splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)
        self.main_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: lightgray;
                width: 1px;
            }
        """)
        main2_layout.addWidget(self.main_splitter)


        main1_layout.addLayout(main2_layout)


        # Left panel: Search bar and tree iew in a vertical layout
        left_panel = QtWidgets.QWidget(self)
        left_layout = QtWidgets.QVBoxLayout(left_panel)
        left_layout.setContentsMargins(5, 0, 5, 0)

        self.search_bar = QtWidgets.QLineEdit(self)
        self.search_bar.setFixedHeight(30)  # Adjust height as needed
        self.search_bar.setPlaceholderText("Search systems...")
        left_layout.addWidget(self.search_bar)

        self.tree = QtWidgets.QTreeWidget(self)
        self.tree.setHeaderHidden(True)
        self.tree.setIndentation(15)  # Default is usually 20
        left_layout.addWidget(self.tree)
        self.main_splitter.addWidget(left_panel)
        self.main_splitter.setStretchFactor(0, 2)  # Approximately 1/3     #### (index, factor size)                self.main_splitter.setSizes([20, 40])  # Left: 200px, Right: 400px


        # Right panel: Vertical splitter for description (top) and video (bottom)
        right_panel = QtWidgets.QWidget(self)
        right_layout = QtWidgets.QVBoxLayout(right_panel)
        right_layout.setContentsMargins(5, 0, 0, 0)
        

        self.content_splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Vertical)
        right_layout.addWidget(self.content_splitter)

        # Right upper panel: Text description (read-only)
        self.text_description = QtWidgets.QTextEdit(self)
        self.text_description.setReadOnly(True)
        
        groupBox = QtWidgets.QGroupBox("Notes / Comments")  # ✅ This is your title
        groupLayout = QtWidgets.QVBoxLayout()
        groupLayout.addWidget(self.text_description)
        groupBox.setLayout(groupLayout)

        self.content_splitter.addWidget(groupBox)


        add_rem_layout = QtWidgets.QHBoxLayout()

        # Upload Button
        self.Upload_button = self.but_style("Upload", "#4a8349")
        self.Upload_button.clicked.connect(lambda: self.request_login("upload"))

        
##        self.Upload_button.clicked.connect(self.request_login, "upload")
        add_rem_layout.addWidget(self.Upload_button)

        # Remove Button
        self.remove_button = self.but_style("Remove", "#4a8349")
        self.remove_button.clicked.connect(lambda: self.request_login("remove"))
        
        #self.remove_button.clicked.connect(self.request_login, "remove")
        add_rem_layout.addWidget(self.remove_button)

        # Log 
        self.remove_button = self.but_style("Log", "#4a8349")
        self.remove_button.clicked.connect(lambda: self.request_login("log"))

        #self.remove_button.clicked.connect(self.request_login, "log")
        add_rem_layout.addWidget(self.remove_button)


        left_layout.addLayout(add_rem_layout)


        # Right lower panel: Video player widget
        self.video_player = VideoPlayerWidget(self)
        self.content_splitter.addWidget(self.video_player)

        # Ensure both description and video share equal space initially
        self.content_splitter.setStretchFactor(0, 1)    ## the (description par, 1 factor)
        self.content_splitter.setStretchFactor(1, 4)    ## the (vid, 1 factor ) both equial
        self.main_splitter.addWidget(right_panel)
        self.main_splitter.setStretchFactor(1, 3)       ## index 1 ie right panel will get more size

        # Status Bar
        self.status = self.statusBar()
        self.update_status("No system selected", "", "")

        # Menu Bar: Upload and Home actions
##        menu = self.menuBar()
##        file_menu = menu.addMenu("File")
##        upload_action = QtGui.QAction("Upload", self)
##        upload_action.triggered.connect(self.open_upload_dialog)
##        file_menu.addAction(upload_action)
##
##        remove_action = QtGui.QAction("Remove", self)
##        remove_action.triggered.connect(self.open_remove_dialog)
##        file_menu.addAction(remove_action)
##
##        home_action = QtGui.QAction("Home", self)
##        home_action.triggered.connect(self.go_home)
##        file_menu.addAction(home_action)

        # Connect tree view selection and search bar
        self.tree.itemClicked.connect(self.tree_item_clicked)
        self.search_bar.textChanged.connect(self.filter_tree)

        # Populate tree from database
        self.populate_tree()


    def but_style(self, text, color: str):
        self.button = QtWidgets.QPushButton(text)

        self.button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                font-size: 14px;
                font-weight: bold;
                border: none;
                padding: 6px 6px;           /* reduced from 16px to 12px */
                border-radius: 6px;
                min-width: 60px;             /* adjust this */
                max-width: 90px;            /* optional cap */
            }}
            QPushButton:hover {{
                background-color: #257526;
            }}
            QPushButton:pressed {{
                background-color: #2471a3;
            }}
        """)
        return self.button




    def populate_tree(self):
        self.tree.clear()
        # Get top-level systems for this radar type
        top_systems = self.db_manager.get_top_level_systems(self.radar_type)
##        print(top_systems)
        for sys_id, name in top_systems:
            parent_item = QtWidgets.QTreeWidgetItem([name])
            parent_item.setData(0, QtCore.Qt.ItemDataRole.UserRole, sys_id)
        # Always add a dummy child to force the drop-down arrow
            dummy_child = QtWidgets.QTreeWidgetItem([""])
            parent_item.addChild(dummy_child)

            # Add real subsystems (if any), and remove dummy if real ones are found
            if self.add_subsystems(parent_item, sys_id):
                parent_item.removeChild(dummy_child)
            
            #self.add_subsystems(parent_item, sys_id)
            self.tree.addTopLevelItem(parent_item)
        self.tree.expandAll()

    def add_subsystems(self, parent_item, parent_id):
        subsystems = self.db_manager.get_subsystems(parent_id)
        if not subsystems:
            return False  # No subsystems added

        for sub_id, name in subsystems:
            child_item = QtWidgets.QTreeWidgetItem([f"- {name}"])
            child_item.setData(0, QtCore.Qt.ItemDataRole.UserRole, sub_id)
            parent_item.addChild(child_item)
            # Recursively add deeper levels if any
            self.add_subsystems(child_item, sub_id)
        return True

    def tree_item_clicked(self, item, column):
        system_id = item.data(0, QtCore.Qt.ItemDataRole.UserRole)
        details = self.db_manager.get_system_details(system_id)
        if details:
            # Unpack details (columns: id, parent_id, system_name, description, upload_date, uploader_name, video_path, radar_type)
            _, _, system_name, description, upload_date, uploader_name, video_path, _ = details
            self.text_description.setHtml(description)
            self.update_status(system_name, upload_date, uploader_name)
            self.video_player.load_video(video_path)

##    def filter_tree(self, text):
##        # Simple filtering: iterate over top-level items and hide those that don't match.
##        root = self.tree.invisibleRootItem()
##        child_count = root.childCount()
##        for i in range(child_count):
##            item = root.child(i)
##            match = text.lower() in item.text(0).lower()
##            item.setHidden(not match)
##            # Could be enhanced to search recursively over all children.

    def filter_tree(self, text):
        def search_item(item, text):
            match = text.lower() in item.text(0).lower()
            child_match = False

            # Recursively search children
            for i in range(item.childCount()):
                child = item.child(i)
                child_visible = search_item(child, text)
                child.setHidden(not child_visible)
                if child_visible:
                    child_match = True

            # Show item if it matches or any of its children match
            item.setHidden(not (match or child_match))
            return match or child_match

        root = self.tree.invisibleRootItem()
        for i in range(root.childCount()):
            top_item = root.child(i)
            search_item(top_item, text)


    def update_status(self, system_name, upload_date, uploader):
        status_message = f"System: {system_name} | Date Added: {upload_date} | Added by: {uploader}"
        self.status.showMessage(status_message)

    ###  authentication for deletion
    def request_login(self, action: str):
        login_dialog = LoginDialog(self.radar_type, self.db_manager, self)
        if login_dialog.exec():
            if login_dialog.access_granted:
                print("done")
                if action == "upload":
                    try:
                        self.open_upload_dialog()
                    except NameError as e:
                        print(f"An error occurred: {e}")
                    
                if action == "remove":
                    try:
                        self.open_remove_dialog()
                    except NameError as e:
                        print(f"An error occurred: {e}")

                if action == "log":
                    try:
                        self.open_log_dialog()
                    except AttributeError:
                        print("Method 'open_log_dialog' does not exist.")
                        QtWidgets.QMessageBox.warning(self, "Access Denied", "Feature not A/A yet")

                        

    def open_upload_dialog(self):
        dialog = UploadDialog(self.radar_type, self.db_manager, self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            data = dialog.get_upload_data()
            # Insert new system record into the database
            self.db_manager.insert_system(data["parent_id"], data["system_name"],
                                          data["description"], data["upload_date"],
                                          data["uploader_name"], data["video_path"],
                                          data["radar_type"])
            QtWidgets.QMessageBox.information(self, "Upload", "New system uploaded successfully!")
            # Refresh tree view to reflect new data
            self.populate_tree()

    def open_remove_dialog(self):
        
        dialog = RemoveDialog(self.radar_type, self.db_manager, self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            dialog = dialog.delete_item()
            print("item Deleted")            
            self.populate_tree()


    def go_home(self):
        self.close()
        self.parent().show_main_menu()


class MainMenuWindow(QtWidgets.QMainWindow):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setWindowTitle("Radar Recovery Software - Main Menu")
        self.setStyleSheet("background-color: #B4f96D;")  # Light blue background

        #self.setMinimumSize(700, 500)
        self.init_ui()
        self.showMaximized()

    def init_ui(self):
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)

      
        layout = QtWidgets.QVBoxLayout(central_widget)
        layout.setContentsMargins(10, 10, 10, 10)  # adjust as needed
      #  layout.setSpacing(20)                      # space between left and right


        Upper_layout =QtWidgets.QHBoxLayout()
        Upper_layout.setSpacing(250)       # space between buttons

        ### Wessec Monogram
##        monogram_label_1 = QtWidgets.QLabel()
##        pixmap1 = QPixmap(r"C:\Users\PMYLS\Documents\radar_recovery\487_mono.png")        
##        monogram_label_1.setPixmap(pixmap1)                 
##        monogram_label_1.setScaledContents(True)           # scale 
##        monogram_label_1.setFixedSize(200-50, 250-50)            # display dimensions
##        monogram_label_1.setAlignment(Qt.AlignmentFlag.AlignLeft)  # 
##        Upper_layout.insertWidget(0, monogram_label_1) 

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        #Upper_layout.addWidget(Upper_lable)
        ### 487 Monogram
        mono_487 = os.path.join(BASE_DIR, "Photos", "487_mono.png")
        monogram_label_2 = QtWidgets.QLabel()
        pixmap2 = QPixmap(mono_487)        
        monogram_label_2.setPixmap(pixmap2)                 
        monogram_label_2.setScaledContents(True)           # scale pixmap to label’s size 
        monogram_label_2.setFixedSize(200-50, 250-50)            # display dimensions
        monogram_label_2.setAlignment(Qt.AlignmentFlag.AlignRight)  
        Upper_layout.insertWidget(0, monogram_label_2) 

        
        ### title
        title_path = os.path.join(BASE_DIR, "Photos", "Title.png")
        title_label = QtWidgets.QLabel()
        pixmap3 = QPixmap(title_path)        
        title_label.setPixmap(pixmap3)                 
        title_label.setScaledContents(True)           # scale pixmap to label’s size 
        title_label.setFixedSize(400, 150)            # display dimensions
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  
        Upper_layout.insertWidget(0, title_label) 




        rad_gify_path = os.path.join(BASE_DIR, "Photos", "rad_gify.gif")
        gif_label = QtWidgets.QLabel()
        gif_label.setScaledContents(True)           # scale 
        gif_label.setFixedSize(200-50, 200-50)            # display dimensions
        gif_label.setAlignment(Qt.AlignmentFlag.AlignRight)  # 
        movie = QtGui.QMovie(rad_gify_path)  
        gif_label.setMovie(movie)
        movie.start()  # Start the animation
        Upper_layout.insertWidget(0,gif_label) 



##middle layout
        middle_layout_1 = QtWidgets.QHBoxLayout()

        ### 487 label
        label_487 = os.path.join(BASE_DIR, "Photos", "lable_487_2.png")
        monogram_label_3 = QtWidgets.QLabel()
        pixmap3 = QPixmap(label_487)        
        monogram_label_3.setPixmap(pixmap3)                 
        monogram_label_3.setScaledContents(True)           # scale pixmap to label’s size 
        monogram_label_3.setFixedSize(300, 70)            # display dimensions
##        monogram_label_3.setAlignment(Qt.AlignmentFlag.AlignRight)
        monogram_label_3.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        middle_layout_1.addWidget(monogram_label_3)

        middle_layout_2 = QtWidgets.QVBoxLayout()

##        middle_layout.insertWidget(1, monogram_label_3) 


        # Header information with larger fonts
        header_label = QtWidgets.QLabel("Idea Conceived by: XXX")
        author_label = QtWidgets.QLabel("Developed by:  Flt Lt M. Ramzan Badini")
        conceived_label = QtWidgets.QLabel("Aproved by:  xxxx")
        for label in (header_label, author_label, conceived_label):
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("font-size: 18px; font-weight: bold;")
            middle_layout_2.addWidget(label)


        # container widget for buttons
        button_container = QtWidgets.QWidget()
        button_container.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,     # Do not expand horizontally
            QtWidgets.QSizePolicy.Policy.Preferred   # Allow vertical adjustment
        )
        button_container.setMaximumWidth(450)  # Optional cap on width
 
        button_layout = QtWidgets.QHBoxLayout(button_container)  
        button_layout_L = QtWidgets.QHBoxLayout(button_container)  

        button_layout.setSpacing(40)       # space between buttons
        button_layout_L.setSpacing(400)       # space between buttons

        button_layout_L.setContentsMargins(0, 0, 0, 15)   # gap from lower 15 pixs 
        button_layout.setContentsMargins(0, 0, 0, 10)   # gap from lower 15 pixs


        # Radar system font making
        self.radar1_btn = QtWidgets.QPushButton("Radar Systems", self)
        self.radar1_btn = self.main_but_style(self.radar1_btn, "#007ACC")
        self.radar1_btn.setMinimumSize(200, 80)
        self.radar1_btn.clicked.connect(lambda: self.open_radar_app("RADAR"))

        # comm system buttoning
        self.radar2_btn = QtWidgets.QPushButton("Comm Systems", self)
        self.radar2_btn = self.main_but_style(self.radar2_btn, "#5aa539")
        self.radar2_btn.setMinimumSize(200, 80)
        self.radar2_btn.clicked.connect(lambda: self.open_radar_app("COMM"))

        # Electric system buttoning
        self.radar3_btn = QtWidgets.QPushButton("---", self)
        self.radar3_btn = self.main_but_style(self.radar3_btn, "#6a6a6a")
        self.radar3_btn.setMinimumSize(200, 80)
        self.radar3_btn.clicked.connect(lambda: self.open_other_sys("ELECT"))

        # MTF system buttoning
        self.radar4_btn = QtWidgets.QPushButton("---", self)
        self.radar4_btn = self.main_but_style(self.radar4_btn, "#6a6a6a")
        self.radar4_btn.setMinimumSize(200, 80)
        self.radar4_btn.clicked.connect(lambda: self.open_other_sys("DnM"))

        button_layout.addWidget(self.radar1_btn)
        button_layout.addWidget(self.radar2_btn)

        button_layout_L.addWidget(self.radar3_btn)
        button_layout_L.addWidget(self.radar4_btn)

        

        button_layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # keeps them at the top of their column
        button_layout_L.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # keeps them at the top of their column

        layout.addLayout(Upper_layout)

        layout.addLayout(middle_layout_1)
        layout.addLayout(middle_layout_2)
        
        layout.addStretch()           # pushes the button column all the way right

        layout.addWidget(button_container)
        layout.setAlignment(button_container, Qt.AlignmentFlag.AlignHCenter)   

        layout.addLayout(button_layout)
        layout.addLayout(button_layout_L)
        


    def main_but_style(self, button, color: str):
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: black;
                font-size: 22px;
                font-weight: bold;
                border: none;
                border-radius: 16px;
                padding: 6px 12px;
                max-width: 120;
            }}
            QPushButton:hover {{
                background-color: #157a2c;
            }}
            QPushButton:pressed {{
                background-color: #0f6523;
            }}
            """)
        return button


    def open_other_sys(self, radar_type):

        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msg_box.setWindowTitle("Access Denied")
        msg_box.setText("This system is not A/A yet")

        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #2b2b2b;
                border: 1px solid #000000;
            }
            QLabel {
                color: white;
                font: 12pt "Segoe UI";
                background-color: transparent;
                selection-background-color: transparent;
                selection-color: white;
            }
            QPushButton {
                background-color: #a1a1a1;
                color: black;
                padding: 6px 12px;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
        """)

        msg_box.exec()



##        QtWidgets.QMessageBox.warning(self, "Access Denied", "System yet to be added")


    def open_radar_app(self, radar_type):
        self.radar_window = RadarAppMainWindow(radar_type, self.db_manager, parent=self)
        self.radar_window.show()
        self.hide()

    def show_main_menu(self):
        self.show()


# ---------------------------
# Main Application Execution
# ---------------------------
def main():    
    app = QtWidgets.QApplication(sys.argv)
    # Set a global stylesheet for a larger, cleaner font
    app.setStyleSheet("QWidget { font-size: 13px; }")

    db_manager = DatabaseManager()
    main_menu = MainMenuWindow(db_manager)
    main_menu.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
