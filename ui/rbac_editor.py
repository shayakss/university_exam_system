"""
RBAC Editor UI
Handles role and permission management
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from controllers.rbac_controller import rbac_controller
from controllers.user_controller import user_controller

class RBACEditorPage(QWidget):
    """Page for managing roles and permissions"""
    
    def __init__(self, parent=None, user_data=None):
        super().__init__(parent)
        self.user_data = user_data
        self.user_id = user_data.get('user_id')
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("🔐 RBAC Editor")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_roles_tab(), "Role Management")
        self.tabs.addTab(self.create_user_roles_tab(), "User Role Assignment")
        layout.addWidget(self.tabs)
        
    def create_roles_tab(self):
        """Create the role management tab"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        # Left: Roles List
        left_panel = QFrame()
        left_panel.setFixedWidth(300)
        left_panel.setStyleSheet("background-color: white; border-radius: 10px; padding: 15px;")
        left_layout = QVBoxLayout(left_panel)
        
        left_layout.addWidget(QLabel("<b>Roles</b>"))
        self.roles_list = QListWidget()
        self.roles_list.currentItemChanged.connect(self.load_role_permissions)
        left_layout.addWidget(self.roles_list)
        
        add_role_btn = QPushButton("➕ Create New Role")
        add_role_btn.setStyleSheet("background-color: #3498db; color: white;")
        add_role_btn.clicked.connect(self.show_create_role_dialog)
        left_layout.addWidget(add_role_btn)
        
        layout.addWidget(left_panel)
        
        # Right: Permissions Matrix
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: white; border-radius: 10px; padding: 15px;")
        right_layout = QVBoxLayout(right_panel)
        
        right_layout.addWidget(QLabel("<b>Permissions</b>"))
        
        # Tree widget for categorized permissions
        self.perm_tree = QTreeWidget()
        self.perm_tree.setHeaderLabels(["Permission", "Description"])
        self.perm_tree.setColumnWidth(0, 300)
        self.perm_tree.itemChanged.connect(self.handle_permission_change)
        right_layout.addWidget(self.perm_tree)
        
        layout.addWidget(right_panel)
        
        self.load_roles()
        self.load_all_permissions()
        
        return widget
        
    def create_user_roles_tab(self):
        """Create the user role assignment tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Filter
        filter_layout = QHBoxLayout()
        self.user_search = QLineEdit()
        self.user_search.setPlaceholderText("Search User...")
        self.user_search.textChanged.connect(self.load_users)
        filter_layout.addWidget(self.user_search)
        layout.addLayout(filter_layout)
        
        # Users Table
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(4)
        self.users_table.setHorizontalHeaderLabels(["Username", "Full Name", "Current Roles", "Action"])
        self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.users_table)
        
        self.load_users()
        
        return widget

    def load_roles(self):
        """Load all roles"""
        self.roles_list.clear()
        roles = rbac_controller.get_all_roles()
        for role in roles:
            item = QListWidgetItem(role['role_name'])
            item.setData(Qt.UserRole, role['role_id'])
            self.roles_list.addItem(item)

    def load_all_permissions(self):
        """Load all permissions into tree"""
        self.perm_tree.clear()
        permissions = rbac_controller.get_all_permissions()
        
        categories = {}
        for p in permissions:
            cat = p['category']
            if cat not in categories:
                categories[cat] = QTreeWidgetItem(self.perm_tree, [cat, ""])
                categories[cat].setExpanded(True)
            
            item = QTreeWidgetItem(categories[cat], [p['permission_name'], p['description']])
            item.setData(0, Qt.UserRole, p['permission_id'])
            item.setCheckState(0, Qt.Unchecked)

    def load_role_permissions(self, current, previous):
        """Load permissions for selected role"""
        if not current:
            return
            
        role_id = current.data(Qt.UserRole)
        role_perms = rbac_controller.get_role_permissions(role_id)
        role_perm_ids = [p['permission_id'] for p in role_perms]
        
        # Block signals to prevent triggering itemChanged
        self.perm_tree.blockSignals(True)
        
        iterator = QTreeWidgetItemIterator(self.perm_tree)
        while iterator.value():
            item = iterator.value()
            perm_id = item.data(0, Qt.UserRole)
            if perm_id: # Leaf node
                if perm_id in role_perm_ids:
                    item.setCheckState(0, Qt.Checked)
                else:
                    item.setCheckState(0, Qt.Unchecked)
            iterator += 1
            
        self.perm_tree.blockSignals(False)

    def handle_permission_change(self, item, column):
        """Handle permission checkbox toggle"""
        role_item = self.roles_list.currentItem()
        if not role_item:
            return
            
        role_id = role_item.data(Qt.UserRole)
        perm_id = item.data(0, Qt.UserRole)
        
        if not perm_id: # Category node
            return
            
        if item.checkState(0) == Qt.Checked:
            rbac_controller.assign_permission_to_role(role_id, perm_id)
        else:
            rbac_controller.remove_permission_from_role(role_id, perm_id)

    def show_create_role_dialog(self):
        """Show dialog to create new role"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Create Role")
        dialog.setMinimumWidth(300)
        
        layout = QVBoxLayout(dialog)
        
        layout.addWidget(QLabel("Role Name:"))
        name_edit = QLineEdit()
        layout.addWidget(name_edit)
        
        layout.addWidget(QLabel("Description:"))
        desc_edit = QLineEdit()
        layout.addWidget(desc_edit)
        
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Create")
        save_btn.clicked.connect(dialog.accept)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)
        
        if dialog.exec_() == QDialog.Accepted:
            if not name_edit.text():
                return
                
            success, msg = rbac_controller.create_role(name_edit.text(), desc_edit.text())
            if success:
                self.load_roles()
            else:
                QMessageBox.warning(self, "Error", msg)

    def load_users(self):
        """Load users for role assignment"""
        search = self.user_search.text().lower()
        users = user_controller.get_all_users()
        
        filtered_users = [u for u in users if search in u['username'].lower() or search in u['full_name'].lower()]
        self.users_table.setRowCount(len(filtered_users))
        
        for row, user in enumerate(filtered_users):
            self.users_table.setItem(row, 0, QTableWidgetItem(user['username']))
            self.users_table.setItem(row, 1, QTableWidgetItem(user['full_name']))
            
            # Get user roles
            user_roles = rbac_controller.get_user_roles(user['user_id'])
            role_names = [r['role_name'] for r in user_roles]
            self.users_table.setItem(row, 2, QTableWidgetItem(", ".join(role_names)))
            
            btn = QPushButton("Manage Roles")
            btn.clicked.connect(lambda checked, u=user: self.show_user_roles_dialog(u))
            self.users_table.setCellWidget(row, 3, btn)

    def show_user_roles_dialog(self, user):
        """Show dialog to manage user roles"""
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Manage Roles - {user['username']}")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        
        # List current roles
        current_roles = rbac_controller.get_user_roles(user['user_id'])
        current_role_ids = [r['role_id'] for r in current_roles]
        
        roles_list = QListWidget()
        all_roles = rbac_controller.get_all_roles()
        
        for role in all_roles:
            item = QListWidgetItem(role['role_name'])
            item.setData(Qt.UserRole, role['role_id'])
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            
            if role['role_id'] in current_role_ids:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
                
            roles_list.addItem(item)
            
        layout.addWidget(roles_list)
        
        btn = QPushButton("Save Changes")
        btn.clicked.connect(lambda: self.save_user_roles(user['user_id'], roles_list, dialog))
        layout.addWidget(btn)
        
        dialog.exec_()

    def save_user_roles(self, user_id, list_widget, dialog):
        """Save changes to user roles"""
        try:
            for i in range(list_widget.count()):
                item = list_widget.item(i)
                role_id = item.data(Qt.UserRole)
                
                if item.checkState() == Qt.Checked:
                    rbac_controller.assign_role_to_user(user_id, role_id, self.user_id)
                else:
                    rbac_controller.remove_role_from_user(user_id, role_id)
            
            QMessageBox.information(dialog, "Success", "User roles updated successfully")
            dialog.accept()
            self.load_users()
            
        except Exception as e:
            QMessageBox.warning(dialog, "Error", f"Failed to update roles: {str(e)}")
