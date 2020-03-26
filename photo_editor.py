# import necessary modules
import os, sys, cv2
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QAction,
    QToolButton, QToolBar, QDockWidget, QMessageBox, QFileDialog, QGridLayout, 
    QScrollArea, QSizePolicy)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap, QImage, QTransform, QPalette

icon_path = "icons"

class imageLabel(QLabel):
    """Subclass of QLabel for displaying image"""
    def __init__(self, parent, image=None):
        super().__init__(parent)
        self.parent = parent
        self.image = image
        #self.image = "images/parrot.png"

        # Load image
        pixmap = QPixmap(self.image)
        self.setAlignment(Qt.AlignCenter)
        self.setPixmap(pixmap)

class PhotoEditorGUI(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.initializeUI()

        #self.image = QImage()

    def initializeUI(self):
        self.setMinimumSize(300, 200)
        self.setWindowTitle("Photo Editor")
        self.showMaximized()

        self.zoom_factor = 1

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

        # Actions for Tools menu
        self.rotate90_cw_act = QAction(QIcon(os.path.join(icon_path, "rotate90_cw.png")),'Rotate 90º CW', self)
        self.rotate90_cw_act.triggered.connect(lambda: self.rotateImage90("cw"))

        self.rotate90_ccw_act = QAction(QIcon(os.path.join(icon_path, "rotate90_ccw.png")),'Rotate 90º CCW', self)
        self.rotate90_ccw_act.triggered.connect(lambda: self.rotateImage90("ccw"))

        self.flip_horizontal = QAction(QIcon(os.path.join(icon_path, "flip_horizontal.png")), 'Flip Horizontal', self)
        self.flip_horizontal.triggered.connect(lambda: self.flipImage("horizontal"))

        self.flip_vertical = QAction(QIcon(os.path.join(icon_path, "flip_vertical.png")), 'Flip Vertical', self)
        self.flip_vertical.triggered.connect(lambda: self.flipImage('vertical'))
        
        self.zoom_in = QAction(QIcon(os.path.join(icon_path, "zoom_in.png")), 'Zoom In', self)
        self.zoom_in.setShortcut('Ctrl++')
        self.zoom_in.triggered.connect(lambda: self.zoomOnImage(1.25))

        self.zoom_out = QAction(QIcon(os.path.join(icon_path, "zoom_out.png")), 'Zoom Out', self)
        self.zoom_out.setShortcut('Ctrl+-')
        self.zoom_out.triggered.connect(lambda: self.zoomOnImage(0.75))

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

        tool_menu = menu_bar.addMenu('Tools')
        tool_menu.addAction(self.rotate90_cw_act)
        tool_menu.addAction(self.rotate90_ccw_act)
        tool_menu.addAction(self.flip_horizontal)
        tool_menu.addAction(self.flip_vertical)
        tool_menu.addSeparator()
        tool_menu.addAction(self.zoom_in)
        tool_menu.addAction(self.zoom_out)

        views_menu = menu_bar.addMenu('Views')
        views_menu.addAction(self.tools_menu_act)

    def createToolBar(self):
        """Set up the toolbar."""
        tool_bar = QToolBar("Main Toolbar")
        tool_bar.setIconSize(QSize(26, 26))
        self.addToolBar(tool_bar)

        # Add actions to the toolbar
        tool_bar.addAction(self.open_act)
        tool_bar.addAction(self.exit_act)
        tool_bar.addSeparator()
        tool_bar.addAction(self.rotate90_ccw_act)
        tool_bar.addAction(self.rotate90_cw_act)
        tool_bar.addAction(self.flip_horizontal)
        tool_bar.addAction(self.flip_vertical)
        tool_bar.addSeparator()
        tool_bar.addAction(self.zoom_in)
        tool_bar.addAction(self.zoom_out)
    
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
        self.scroll_area = QScrollArea()
        self.scroll_area.setBackgroundRole(QPalette.Dark)
        self.scroll_area.setAlignment(Qt.AlignCenter)
        #scroll_area.setMinimumSize(800, 800)
        
        self.image_label = imageLabel(self)
        #TODO: Display image without distortion
        #self.image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        #self.image_label.setScaledContents(True)
        self.image_label.resize(self.image_label.pixmap().size())

        self.scroll_area.setWidget(self.image_label)
        #self.scroll_area.setVisible(False)

        self.setCentralWidget(self.scroll_area)

        #self.resize(QApplication.primaryScreen().availableSize() * 3 / 5)

    def openImage(self):
        """ """
        image_file, _ = QFileDialog.getOpenFileName(self, "Open Image", 
                "", "PNG Files (*.png);;JPG Files (*.jpeg *.jpg );;Bitmap Files (*.bmp);;\
                GIF Files (*.gif)")
        
        if image_file:
            self.image = QImage(image_file)

            #pixmap = QPixmap(image_file)
            self.image_label.setPixmap(QPixmap().fromImage(self.image))
            #image_size = self.image_label.sizeHint()
            self.image_label.resize(self.image_label.pixmap().size())

            #self.scroll_area.setMinimumSize(image_size)

            #self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), 
            #    Qt.KeepAspectRatio, Qt.SmoothTransformation))
        elif image_file == "":
            # User selected Cancel
            pass
        else:
            QMessageBox.information(self, "Error", 
                "Unable to open image.", QMessageBox.Ok)

    def rotateImage90(self, direction):
        """Rotate image 90º clockwise or counterclockwise."""
        if self.image.isNull() == False:
            if direction == "cw":
                transform90 = QTransform().rotate(90)
            elif direction == "ccw":
                transform90 = QTransform().rotate(-90)

            pixmap = QPixmap(self.image)

            rotated = pixmap.transformed(transform90, mode=Qt.SmoothTransformation)

            self.image_label.setPixmap(rotated)
            #self.image_label.setPixmap(rotated.scaled(self.image_label.size(), 
            #    Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.image = QImage(rotated) 
            #self.image = QPixmap(rotated)
            self.image_label.repaint() # repaint the child widget

            """
            self.image = QImage(image_file)

            #pixmap = QPixmap(image_file)
            self.image_label.setPixmap(QPixmap().fromImage(self.image))
            """
        else:
            # No image to rotate
            pass

    def flipImage(self, axis):
        """
        Mirror the image across the horizontal axis.
        """
        if self.image.isNull() == False:
            if axis == "horizontal":
                flip_h = QTransform().scale(-1, 1)
                pixmap = QPixmap(self.image)
                flipped = pixmap.transformed(flip_h)
            elif axis == "vertical":
                flip_v = QTransform().scale(1, -1)
                pixmap = QPixmap(self.image)
                flipped = pixmap.transformed(flip_v)

            self.image_label.setPixmap(flipped)
            #self.image_label.setPixmap(flipped.scaled(self.image_label.size(), 
            #    Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.image = QImage(flipped)
            #self.image = QPixmap(flipped)
            self.image_label.repaint()
        else:
            # No image to flip
            pass

    def zoomOnImage(self, zoom_value):
        """ """
        self.zoom_factor *= zoom_value
        self.image_label.resize(self.zoom_factor * self.image_label.pixmap().size())

        #self.scroll_area.horizontalScrollBar()

    def adjustScrollBar(self, scroll_bar, value):
        """Adjust the scrollbar when zooming in or out."""
        #self.scroll_area.setValue()
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
