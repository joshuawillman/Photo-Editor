# import necessary modules
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QAction,
    QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class imageLabel(QLabel):
    """Subclass of QLabel for displaying image"""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Load image
        pixmap = QPixmap("images/parrot.png")
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

        self.image_label = None

        self.createMenu()
        self.createMainLabel()

        self.show()

    def createMenu(self):
        """Set up the menubar."""
        open_act = QAction('Open...', self)
        open_act.setShortcut('Ctrl+O')
        open_act.triggered.connect(self.openImage)

        exit_act = QAction('Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.triggered.connect(self.close)

        # Create menubar
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        # Create file menu and add actions
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(open_act)
        file_menu.addSeparator()
        file_menu.addAction(exit_act)

        edit_menu = menu_bar.addMenu('Edit')
        #edit_menu.addAction()

    def createMainLabel(self):
        """Create an instance of the imageLabel class and set it 
           as the main window's central widget."""
        self.image_label = imageLabel(self)

        self.setCentralWidget(self.image_label)

    def openImage(self):
        """ """
        image_file, _ = QFileDialog.getOpenFileName(self, "Open Image", 
                "", "JPG Files (*.jpeg *.jpg );;PNG Files (*.png);;Bitmap Files (*.bmp);;\
                GIF Files (*.gif)")
        """
        if image_file:
            self.image = QPixmap(image_file)
        """

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
    window = PhotoEditorGUI()
    sys.exit(app.exec_())
