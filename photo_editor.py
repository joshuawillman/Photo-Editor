# import necessary modules
import os, sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QAction,
    QToolButton, QToolBar, QDockWidget, QMessageBox, QFileDialog, QGridLayout)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap

icon_path = "icons"

class imageLabel(QLabel):
    """Subclass of QLabel for displaying image"""
    def __init__(self, parent, image=None):
        super().__init__(parent)
        self.parent = parent
        self.image = image

        # Load image
        pixmap = QPixmap(self.image)
        self.setAlignment(Qt.AlignCenter)
        self.setPixmap(pixmap)

class PhotoEditorGUI(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.initializeUI()

    def initializeUI(self):
        self.setMinimumSize(500, 400)
        self.setWindowTitle("Photo Editor")
        self.showMaximized()

        self.createMenu()
        self.createToolBar()
        self.createEditingBar()
        self.createMainLabel()

        self.show()

    def createMenu(self):
        """Set up the menubar."""
        about_act = QAction('About', self)
        about_act.triggered.connect(self.aboutDialog)

        self.open_act = QAction(QIcon(os.path.join(icon_path, "open.png")),'Open...', self)
        self.open_act.setShortcut('Ctrl+O')
        self.open_act.triggered.connect(self.openImage)

        self.exit_act = QAction(QIcon(os.path.join(icon_path, "exit.png")), 'Quit Photo Editor', self)
        self.exit_act.setShortcut('Ctrl+Q')
        self.exit_act.triggered.connect(self.close)

        # Create menubar
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        # Create Photo Editor menu and add actions
        main_menu = menu_bar.addMenu('Photo Editor')
        main_menu.addAction(about_act)
        main_menu.addSeparator()
        main_menu.addAction(self.exit_act)

        # Create file menu and add actions
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(self.open_act)

        edit_menu = menu_bar.addMenu('Edit')
        #edit_menu.addAction()

    def createToolBar(self):
        """Set up the toolbar."""
        tool_bar = QToolBar("Main Toolbar")
        tool_bar.setIconSize(QSize(30, 30))
        self.addToolBar(tool_bar)

        # Add actions to the toolbar
        tool_bar.addAction(self.open_act)
        tool_bar.addAction(self.exit_act)

    def createEditingBar(self):
        """Create toolbar for editing tools."""
        editing_bar = QDockWidget("Tools")
        editing_bar.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        convert_to_grayscale = QToolButton()
        convert_to_grayscale.setIcon(QIcon(os.path.join(icon_path, "grayscale.png")))

        editing_grid = QGridLayout()
        editing_grid.addWidget(convert_to_grayscale, 0, 0, Qt.AlignTop)

        container = QWidget()
        container.setLayout(editing_grid)

        editing_bar.setWidget(container)

        self.addDockWidget(Qt.LeftDockWidgetArea, editing_bar)

    def createMainLabel(self):
        """Create an instance of the imageLabel class and set it 
           as the main window's central widget."""
        self.image_label = imageLabel(self)

        self.setCentralWidget(self.image_label)

    def openImage(self):
        """ """
        image_file, _ = QFileDialog.getOpenFileName(self, "Open Image", 
                "", "PNG Files (*.png);;JPG Files (*.jpeg *.jpg );;Bitmap Files (*.bmp);;\
                GIF Files (*.gif)")
        
        if image_file:
            image = QPixmap(image_file)
            self.image_label.setPixmap(image)

            #self.image_label.setPixmap(image.scaled(self.image_label.size(), 
            #    Qt.KeepAspectRatio, Qt.SmoothTransformation))
        elif image_file == "":
            # User selected Cancel
            pass
        else:
            QMessageBox.information(self, "Error", 
                "Unable to open image.", QMessageBox.Ok)

    def aboutDialog(self):
        QMessageBox.about(self, "About Photo Editor", 
            "Photo Editor\nversion0.1\n\nCreated by Joshua Willman")

    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key_Escape:
            self.close()
        if event.key() == Qt.Key_F1: # fn + F1 on Mac
            if self.isMaximized():
                self.showNormal()
            else:
                self.showMaximized()

    def closeEvent(self, event):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontShowIconsInMenus, True)
    window = PhotoEditorGUI()
    sys.exit(app.exec_())
