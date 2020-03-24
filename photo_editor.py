# import necessary modules
import os, sys, cv2
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QAction,
    QToolButton, QToolBar, QDockWidget, QMessageBox, QFileDialog, QGridLayout)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap, QImage, QTransform

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

        self.image = QImage()

    def initializeUI(self):
        self.setMinimumSize(500, 400)
        self.setWindowTitle("Photo Editor")
        self.showMaximized()

        self.createEditingBar()
        self.createMenu()
        self.createToolBar()
        self.createMainLabel()

        self.show()

    def createMenu(self):
        """Set up the menubar."""
        # Actions for Photo Editor menu
        about_act = QAction('About', self)
        about_act.triggered.connect(self.aboutDialog)

        self.exit_act = QAction(QIcon(os.path.join(icon_path, "exit.png")), 'Quit Photo Editor', self)
        self.exit_act.setShortcut('Ctrl+Q')
        self.exit_act.triggered.connect(self.close)

        # Actions for File menu
        self.open_act = QAction(QIcon(os.path.join(icon_path, "open.png")),'Open...', self)
        self.open_act.setShortcut('Ctrl+O')
        self.open_act.triggered.connect(self.openImage)

        # Actions for Edit menu
        self.rotate_90_act = QAction(QIcon(os.path.join(icon_path, "rotate90.png")),'Rotate 90º', self)
        self.rotate_90_act.triggered.connect(self.rotateImage90)

        # Actions for Views menu
        #self.tools_menu_act = QAction(QIcon(os.path.join(icon_path, "edit.png")),'Tools View...', self, checkable=True)

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
        edit_menu.addAction(self.rotate_90_act)

        views_menu = menu_bar.addMenu('Views')
        views_menu.addAction(self.tools_menu_act)

    def createToolBar(self):
        """Set up the toolbar."""
        tool_bar = QToolBar("Main Toolbar")
        tool_bar.setIconSize(QSize(30, 30))
        self.addToolBar(tool_bar)

        # Add actions to the toolbar
        tool_bar.addAction(self.open_act)
        tool_bar.addAction(self.exit_act)
        tool_bar.addSeparator()
        tool_bar.addAction(self.rotate_90_act)

    def createEditingBar(self):
        """Create dock widget for editing tools."""
        self.editing_bar = QDockWidget("Tools")
        self.editing_bar.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.editing_bar.setMinimumWidth(90)

        # Create editing tool buttons
        convert_to_grayscale = QToolButton()
        convert_to_grayscale.setIcon(QIcon(os.path.join(icon_path, "grayscale.png")))
        convert_to_grayscale.clicked.connect(self.convertToGray)

        convert_to_RGB = QToolButton()
        convert_to_RGB.setIcon(QIcon(os.path.join(icon_path, "rgb.png")))
        convert_to_RGB.clicked.connect(self.convertToRGB)

        # Set layout for dock widget
        editing_grid = QGridLayout()
        editing_grid.addWidget(convert_to_grayscale, 0, 0, Qt.AlignTop)
        editing_grid.addWidget(convert_to_RGB, 0, 1, Qt.AlignTop)

        container = QWidget()
        container.setLayout(editing_grid)

        self.editing_bar.setWidget(container)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.editing_bar)

        self.tools_menu_act = self.editing_bar.toggleViewAction()

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
            self.image = QImage(image_file)

            #pixmap = QPixmap(image_file)
            self.image_label.setPixmap(QPixmap().fromImage(self.image))

            #self.image_label.setPixmap(image.scaled(self.image_label.size(), 
            #    Qt.KeepAspectRatio, Qt.SmoothTransformation))
        elif image_file == "":
            # User selected Cancel
            pass
        else:
            QMessageBox.information(self, "Error", 
                "Unable to open image.", QMessageBox.Ok)

    def rotateImage90(self):
        """Rotate image 90º clockwise."""
        if self.image.isNull() == False:
            transform90 = QTransform().rotate(90)
            pixmap = QPixmap(self.image)

            rotated = pixmap.transformed(transform90, mode=Qt.SmoothTransformation)

            self.image_label.setPixmap(rotated)
            #self.image_label.setPixmap(rotated.scaled(self.image_label.size(), 
            #    Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.image = QPixmap(rotated) 
            self.image_label.repaint() # repaint the child widget
        else:
            # No image to rotate
            pass


    def convertToGray(self):
        """Convert image to grayscale."""
        converted_img = self.image.convertToFormat(QImage.Format_Grayscale8)
        self.image_label.setPixmap(QPixmap().fromImage(converted_img))
        self.image_label.repaint()

    def convertToRGB(self):
        """Convert image to RGB format."""
        converted_img = self.image.convertToFormat(QImage.Format_RGB32)
        self.image_label.setPixmap(QPixmap().fromImage(converted_img))
        self.image_label.repaint()

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
