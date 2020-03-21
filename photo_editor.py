# import necessary modules
import os, sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QAction,
    QToolBar, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap

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
        self.createMainLabel()

        self.show()

    def createMenu(self):
        """Set up the menubar."""
        icon_path = "icons"

        self.open_act = QAction(QIcon(os.path.join(icon_path, "open.png")),'Open...', self)
        self.open_act.setShortcut('Ctrl+O')
        self.open_act.triggered.connect(self.openImage)

        self.exit_act = QAction(QIcon(os.path.join(icon_path, "exit.png")), 'Exit', self)
        self.exit_act.setShortcut('Ctrl+Q')
        self.exit_act.triggered.connect(self.close)

        # Create menubar
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        # Create file menu and add actions
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(self.open_act)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_act)

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
        pass

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
