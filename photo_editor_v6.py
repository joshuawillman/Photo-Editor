# QT Image viewer
# https://doc.qt.io/qt-5/qtwidgets-widgets-imageviewer-example.html
# Classes to consider: QImageReader

# Import necessary modules
import os, sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
    QSlider, QToolButton, QToolBar, QDockWidget, QMessageBox, QFileDialog, QGridLayout, 
    QScrollArea, QSizePolicy, QRubberBand)
from PyQt6.QtCore import Qt, QSize, QRect
from PyQt6.QtGui import QIcon, QPixmap, QImage, QTransform, QPalette, qRgb, QColor, QAction
from Stylesheet import style_sheet

icon_path = "icons"

#TODO: Handle png images with no background

# TODO: redo mouse events, paint event

class imageLabel(QLabel):
    """Subclass of QLabel for displaying image"""
    def __init__(self, parent, image=None):
        super().__init__(parent)
        self.parent = parent 
        self.image = QImage()
        #self.image = "images/parrot.png"

        #self.original_image = self.image.copy
        self.original_image = self.image

        self.rubber_band = QRubberBand(QRubberBand.Shape.Rectangle, self)

        # setBackgroundRole() will create a bg for the image
        #self.setBackgroundRole(QPalette.Base)
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.setScaledContents(True)

        # Load image
        self.setPixmap(QPixmap().fromImage(self.image))
        self.setAlignment(Qt.Alignment.AlignCenter)

    def openImage(self):
        """Load a new image into the """
        image_file, _ = QFileDialog.getOpenFileName(self, "Open Image", 
                "", "PNG Files (*.png);;JPG Files (*.jpeg *.jpg );;Bitmap Files (*.bmp);;\
                GIF Files (*.gif)")
        
        if image_file:
            # Reset values when opening an image
            self.parent.zoom_factor = 1
            #self.parent.scroll_area.setVisible(True)
            self.parent.print_act.setEnabled(True)
            self.parent.updateActions()

            # Reset all sliders
            self.parent.brightness_slider.setValue(0)

            # Get image format
            image_format = self.image.format()
            self.image = QImage(image_file)
            self.original_image = self.image.copy()

            #pixmap = QPixmap(image_file)
            self.setPixmap(QPixmap().fromImage(self.image))
            #image_size = self.image_label.sizeHint()
            self.resize(self.pixmap().size())

            #self.scroll_area.setMinimumSize(image_size)

            #self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), 
            #    Qt.KeepAspectRatio, Qt.SmoothTransformation))
        elif image_file == "":
            # User selected Cancel
            pass
        else:
            QMessageBox.information(self, "Error", 
                "Unable to open image.", QMessageBox.Ok)
    
    def saveImage(self):
        """Save the image displayed in the label."""
        #TODO: Add different functionality for the way in which the user can save their image.
        if self.image.isNull() == False:
            image_file, _ = QFileDialog.getSaveFileName(self, "Save Image", 
                "", "PNG Files (*.png);;JPG Files (*.jpeg *.jpg );;Bitmap Files (*.bmp);;\
                    GIF Files (*.gif)")

            if image_file and self.image.isNull() == False:
                self.image.save(image_file)
            else:
                QMessageBox.information(self, "Error", 
                    "Unable to save image.", QMessageBox.Ok)
        else:
            QMessageBox.information(self, "Empty Image", 
                    "There is no image to save.", QMessageBox.Ok)

    def clearImage(self):
        """ """
        #TODO: If image is not null ask to save image first.
        pass

    def revertToOriginal(self):
        """Revert the image back to original image."""
        #TODO: Display message dialohg to confirm actions
        self.image = self.original_image
        self.setPixmap(QPixmap().fromImage(self.image))
        self.repaint()

        #self.parent.zoom_factor = 1

    def resizeImage(self):
        """Resize image."""
        #TODO: Resize image by specified size
        if self.image.isNull() == False:
            resize = QTransform().scale(0.5, 0.5)

            pixmap = QPixmap(self.image)

            resized_image = pixmap.transformed(resize, mode=Qt.SmoothTransformation)
            #rotated = pixmap.trueMatrix(transform90, pixmap.width, pixmap.height)

            #self.image_label.setPixmap(rotated)
            
            #self.image_label.setPixmap(rotated.scaled(self.image_label.size(), 
            #    Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.image = QImage(resized_image) 
            self.setPixmap(resized_image)
            #self.image = QPixmap(rotated)
            self.setScaledContents(True)
            self.repaint() # repaint the child widget
        else:
            # No image to rotate
            pass

    def cropImage(self):
        """Crop selected portions in the image."""
        if self.image.isNull() == False:
            rect = QRect(10, 20, 400, 200)
            original_image = self.image
            cropped = original_image.copy(rect)

            self.image = QImage(cropped)
            self.setPixmap(QPixmap().fromImage(cropped))

    def rotateImage90(self, direction):
        """Rotate image 90º clockwise or counterclockwise."""
        if self.image.isNull() == False:
            if direction == "cw":
                transform90 = QTransform().rotate(90)
            elif direction == "ccw":
                transform90 = QTransform().rotate(-90)

            pixmap = QPixmap(self.image)

            #TODO: Try flipping the height/width when flipping the image

            rotated = pixmap.transformed(transform90, mode=Qt.SmoothTransformation)
            self.resize(self.image.height(), self.image.width())
            #rotated = pixmap.trueMatrix(transform90, pixmap.width, pixmap.height)
            
            #self.image_label.setPixmap(rotated.scaled(self.image_label.size(), 
            #    Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.image = QImage(rotated) 
            #self.setPixmap(rotated)
            self.setPixmap(rotated.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
            self.repaint() # repaint the child widget
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

            #self.image_label.setPixmap(flipped)
            #self.image_label.setPixmap(flipped.scaled(self.image_label.size(), 
            #    Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.image = QImage(flipped)
            self.setPixmap(flipped)
            #self.image = QPixmap(flipped)
            self.repaint()
        else:
            # No image to flip
            pass

    def convertToGray(self):
        """Convert image to grayscale."""
        if self.image.isNull() == False:
            converted_img = self.image.convertToFormat(QImage.Format_Grayscale16)
            #self.image = converted_img
            self.image = QImage(converted_img)
            self.setPixmap(QPixmap().fromImage(converted_img))
            self.repaint()

    def convertToRGB(self):
        """Convert image to RGB format."""
        if self.image.isNull() == False:
            converted_img = self.image.convertToFormat(QImage.Format_RGB32)
            #self.image = converted_img
            self.image = QImage(converted_img)
            self.setPixmap(QPixmap().fromImage(converted_img))
            self.repaint()

    def convertToSepia(self):
        """Convert image to sepia filter."""
        #TODO: Sepia #704214 rgb(112, 66, 20)
        #TODO: optimize speed that the image converts, or add to thread
        if self.image.isNull() == False:
            for row_pixel in range(self.image.width()):
                for col_pixel in range(self.image.height()):
                    current_val = QColor(self.image.pixel(row_pixel, col_pixel))
            
                    # Calculate r, g, b values for current pixel
                    red = current_val.red()
                    green = current_val.green()
                    blue = current_val.blue()

                    new_red = int(0.393 * red + 0.769 * green + 0.189 * blue)
                    new_green = int(0.349 * red + 0.686 * green + 0.168 * blue)
                    new_blue = int(0.272 * red + 0.534 * green + 0.131 * blue)

                    # Set the new RGB values for the current pixel
                    if new_red > 255:
                        red = 255
                    else:
                        red = new_red

                    if new_green > 255:
                        green = 255
                    else:
                        green = new_green

                    if new_blue > 255:
                        blue = 255
                    else:
                        blue = new_blue

                    new_value = qRgb(red, green, blue)
                    self.image.setPixel(row_pixel, col_pixel, new_value)

        self.setPixmap(QPixmap().fromImage(self.image))
        self.repaint()
    
    def changeBrighteness(self, value):
        #TODO: Reset the value of brightness, remember the original values 
        # as going back to 0, i.e. keep track of original image's values
        #TODO: modify values based on original image
        if (value < -255 | value > 255):
            return self.image

        for row_pixel in range(self.image.width()):
            for col_pixel in range(self.image.height()):
                current_val = QColor(self.image.pixel(row_pixel, col_pixel))
                red = current_val.red()
                green = current_val.green()
                blue = current_val.blue()

                new_red = red + value
                new_green = green + value
                new_blue = blue + value

                # Set the new RGB values for the current pixel
                if new_red > 255:
                    red = 255
                elif new_red < 0:
                    red = 0
                else:
                    red = new_red

                if new_green > 255:
                    green = 255
                elif new_green < 0:
                    green = 0
                else:
                    green = new_green

                if new_blue > 255:
                    blue = 255
                elif new_blue < 0:
                    blue = 0
                else:
                    blue = new_blue

                new_value = qRgb(red, green, blue)
                self.image.setPixel(row_pixel, col_pixel, new_value)

        self.setPixmap(QPixmap().fromImage(self.image))

    def changeContrast(self, contrast):
        """Change the contrast of the pixels in the image.
           Contrast is the difference between max and min pixel intensity."""
        for row_pixel in range(self.image.width()):
            for col_pixel in range(self.image.height()):
                # Calculate a contrast correction factor
                factor = float(259 * (contrast + 255) / (255 * (259 - contrast)))
                
                current_val = QColor(self.image.pixel(row_pixel, col_pixel))
                red = current_val.red()
                green = current_val.green()
                blue = current_val.blue()

                new_red = factor * (red - 128) + 128
                new_green = factor * (green - 128) + 128
                new_blue = factor * (blue - 128) + 128

                new_value = qRgb(new_red, new_green, new_blue)
                self.image.setPixel(row_pixel, col_pixel, new_value)

        self.setPixmap(QPixmap().fromImage(self.image))

    def changeHue(self):
        for row_pixel in range(self.image.width()):
            for col_pixel in range(self.image.height()):
                current_val = QColor(self.image.pixel(row_pixel, col_pixel))

                hue = current_val.hue()

                current_val.setHsv(hue, current_val.saturation(), 
                        current_val.value(), current_val.alpha())
                self.image.setPixelColor(row_pixel, col_pixel, current_val)

        self.setPixmap(QPixmap().fromImage(self.image))

    def mousePressEvent(self, event):
        """Handle mouse press event."""
        self.origin = event.pos()
        if not(self.rubber_band):
            self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)
        self.rubber_band.setGeometry(QRect(self.origin, QSize()))
        self.rubber_band.show()

        #print(self.rubber_band.height())
        print(self.rubber_band.x())

    def mouseMoveEvent(self, event):
        """Handle mouse move event."""
        self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        """Handle when the mouse is released."""
        self.rubber_band.hide()

class PhotoEditorGUI(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.initializeUI()

        self.image = QImage()

    def initializeUI(self):
        self.setMinimumSize(300, 200)
        self.setWindowTitle("Photo Editor")
        self.showMaximized()

        self.zoom_factor = 1

        self.createMainLabel()
        self.createEditingBar()
        self.createMenu()
        self.createToolBar()

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
        self.new_act = QAction(QIcon(os.path.join(icon_path, "new.png")), 'New...')

        self.open_act = QAction(QIcon(os.path.join(icon_path, "open.png")),'Open...', self)
        self.open_act.setShortcut('Ctrl+O')
        self.open_act.triggered.connect(self.image_label.openImage)

        self.print_act = QAction(QIcon(os.path.join(icon_path, "print.png")), "Print...", self)
        self.print_act.setShortcut('Ctrl+P')
        #self.print_act.triggered.connect(self.printImage)
        self.print_act.setEnabled(False)

        self.save_act = QAction(QIcon(os.path.join(icon_path, "save.png")), "Save...", self)
        self.save_act.setShortcut('Ctrl+S')
        self.save_act.triggered.connect(self.image_label.saveImage)
        self.save_act.setEnabled(False)

        # Actions for Edit menu
        self.revert_act = QAction("Revert to Original", self)
        self.revert_act.triggered.connect(self.image_label.revertToOriginal)
        self.revert_act.setEnabled(False)

        # Actions for Tools menu
        self.crop_act = QAction(QIcon(os.path.join(icon_path, "crop.png")), "Crop", self)
        self.crop_act.setShortcut('Shift+X')
        self.crop_act.triggered.connect(self.image_label.cropImage)

        self.resize_act = QAction(QIcon(os.path.join(icon_path, "resize.png")), "Resize", self)
        self.resize_act.setShortcut('Shift+Z')
        self.resize_act.triggered.connect(self.image_label.resizeImage)

        self.rotate90_cw_act = QAction(QIcon(os.path.join(icon_path, "rotate90_cw.png")),'Rotate 90º CW', self)
        self.rotate90_cw_act.triggered.connect(lambda: self.image_label.rotateImage90("cw"))

        self.rotate90_ccw_act = QAction(QIcon(os.path.join(icon_path, "rotate90_ccw.png")),'Rotate 90º CCW', self)
        self.rotate90_ccw_act.triggered.connect(lambda: self.image_label.rotateImage90("ccw"))

        self.flip_horizontal = QAction(QIcon(os.path.join(icon_path, "flip_horizontal.png")), 'Flip Horizontal', self)
        self.flip_horizontal.triggered.connect(lambda: self.image_label.flipImage("horizontal"))

        self.flip_vertical = QAction(QIcon(os.path.join(icon_path, "flip_vertical.png")), 'Flip Vertical', self)
        self.flip_vertical.triggered.connect(lambda: self.image_label.flipImage('vertical'))
        
        self.zoom_in_act = QAction(QIcon(os.path.join(icon_path, "zoom_in.png")), 'Zoom In', self)
        self.zoom_in_act.setShortcut('Ctrl++')
        self.zoom_in_act.triggered.connect(lambda: self.zoomOnImage(1.25))
        self.zoom_in_act.setEnabled(False)

        self.zoom_out_act = QAction(QIcon(os.path.join(icon_path, "zoom_out.png")), 'Zoom Out', self)
        self.zoom_out_act.setShortcut('Ctrl+-')
        self.zoom_out_act.triggered.connect(lambda: self.zoomOnImage(0.8))
        self.zoom_out_act.setEnabled(False)

        self.normal_size_Act = QAction("Normal Size", self)
        self.normal_size_Act.setShortcut('Ctrl+=')
        self.normal_size_Act.triggered.connect(self.normalSize)
        self.normal_size_Act.setEnabled(False)

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
        file_menu.addAction(self.save_act)
        file_menu.addSeparator()
        file_menu.addAction(self.print_act)

        edit_menu = menu_bar.addMenu('Edit')
        edit_menu.addAction(self.revert_act)

        tool_menu = menu_bar.addMenu('Tools')
        tool_menu.addAction(self.crop_act)
        tool_menu.addAction(self.resize_act)
        tool_menu.addSeparator()
        tool_menu.addAction(self.rotate90_cw_act)
        tool_menu.addAction(self.rotate90_ccw_act)
        tool_menu.addAction(self.flip_horizontal)
        tool_menu.addAction(self.flip_vertical)
        tool_menu.addSeparator()
        tool_menu.addAction(self.zoom_in_act)
        tool_menu.addAction(self.zoom_out_act)
        tool_menu.addAction(self.normal_size_Act)

        views_menu = menu_bar.addMenu('Views')
        views_menu.addAction(self.tools_menu_act)

    def createToolBar(self):
        """Set up the toolbar."""
        tool_bar = QToolBar("Main Toolbar")
        tool_bar.setIconSize(QSize(26, 26))
        self.addToolBar(tool_bar)

        # Add actions to the toolbar
        tool_bar.addAction(self.open_act)
        tool_bar.addAction(self.save_act)
        tool_bar.addAction(self.print_act)
        tool_bar.addAction(self.exit_act)
        tool_bar.addSeparator()
        tool_bar.addAction(self.crop_act)
        tool_bar.addAction(self.resize_act)
        tool_bar.addSeparator()
        tool_bar.addAction(self.rotate90_ccw_act)
        tool_bar.addAction(self.rotate90_cw_act)
        tool_bar.addAction(self.flip_horizontal)
        tool_bar.addAction(self.flip_vertical)
        tool_bar.addSeparator()
        tool_bar.addAction(self.zoom_in_act)
        tool_bar.addAction(self.zoom_out_act)
    
    def createEditingBar(self):
        """Create dock widget for editing tools."""
        #TODO: Add a tab widget for the different editing tools
        self.editing_bar = QDockWidget("Tools")
        self.editing_bar.setAllowedAreas(Qt.DockWidgetAreas.LeftDockWidgetArea | Qt.DockWidgetAreas.RightDockWidgetArea)
        self.editing_bar.setMinimumWidth(90)

        # Create editing tool buttons
        filters_label = QLabel("Filters")

        convert_to_grayscale = QToolButton()
        convert_to_grayscale.setIcon(QIcon(os.path.join(icon_path, "grayscale.png")))
        convert_to_grayscale.clicked.connect(self.image_label.convertToGray)

        convert_to_RGB = QToolButton()
        convert_to_RGB.setIcon(QIcon(os.path.join(icon_path, "rgb.png")))
        convert_to_RGB.clicked.connect(self.image_label.convertToRGB)

        convert_to_sepia = QToolButton()
        convert_to_sepia.setIcon(QIcon(os.path.join(icon_path, "sepia.png")))
        convert_to_sepia.clicked.connect(self.image_label.convertToSepia)

        change_hue = QToolButton()
        change_hue.setIcon(QIcon(os.path.join(icon_path, "")))
        change_hue.clicked.connect(self.image_label.changeHue)

        brightness_label = QLabel("Brightness")
        self.brightness_slider = QSlider(Qt.Orientations.Horizontal)
        self.brightness_slider.setRange(-255, 255)
        self.brightness_slider.setTickInterval(35)
        self.brightness_slider.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.brightness_slider.valueChanged.connect(self.image_label.changeBrighteness)

        contrast_label = QLabel("Contrast")
        self.contrast_slider = QSlider(Qt.Orientations.Horizontal)
        self.contrast_slider.setRange(-255, 255)
        self.contrast_slider.setTickInterval(35)
        self.contrast_slider.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.contrast_slider.valueChanged.connect(self.image_label.changeContrast)

        # Set layout for dock widget
        editing_grid = QGridLayout()
        #editing_grid.addWidget(filters_label, 0, 0, 0, 2, Qt.AlignTop)
        editing_grid.addWidget(convert_to_grayscale, 1, 0)
        editing_grid.addWidget(convert_to_RGB, 1, 1)
        editing_grid.addWidget(convert_to_sepia, 2, 0)
        editing_grid.addWidget(change_hue, 2, 1)
        editing_grid.addWidget(brightness_label, 3, 0)
        editing_grid.addWidget(self.brightness_slider, 4, 0, 1, 0)
        editing_grid.addWidget(contrast_label, 5, 0)
        editing_grid.addWidget(self.contrast_slider, 6, 0, 1, 0)
        editing_grid.setRowStretch(7, 10)

        container = QWidget()
        container.setLayout(editing_grid)

        self.editing_bar.setWidget(container)

        self.addDockWidget(Qt.DockWidgetAreas.LeftDockWidgetArea, self.editing_bar)

        self.tools_menu_act = self.editing_bar.toggleViewAction()

    def createMainLabel(self):
        """Create an instance of the imageLabel class and set it 
           as the main window's central widget."""
        self.image_label = imageLabel(self)
        self.image_label.resize(self.image_label.pixmap().size())

        self.scroll_area = QScrollArea()
        self.scroll_area.setBackgroundRole(QPalette.ColorRole.Dark)
        self.scroll_area.setAlignment(Qt.Alignment.AlignCenter)
        #self.scroll_area.setWidgetResizable(False)
        #scroll_area.setMinimumSize(800, 800)
        
        self.scroll_area.setWidget(self.image_label)
        #self.scroll_area.setVisible(False)

        self.setCentralWidget(self.scroll_area)

        #self.resize(QApplication.primaryScreen().availableSize() * 3 / 5)

    def updateActions(self):
        """Update the values of menu and toolbar items when an image 
        is loaded."""
        self.save_act.setEnabled(True)
        self.revert_act.setEnabled(True)
        self.zoom_in_act.setEnabled(True)
        self.zoom_out_act.setEnabled(True)
        self.normal_size_Act.setEnabled(True)
    
    def zoomOnImage(self, zoom_value):
        """Zoom in and zoom out."""
        self.zoom_factor *= zoom_value
        self.image_label.resize(self.zoom_factor * self.image_label.pixmap().size())

        self.adjustScrollBar(self.scroll_area.horizontalScrollBar(), zoom_value)
        self.adjustScrollBar(self.scroll_area.verticalScrollBar(), zoom_value)

        self.zoom_in_act.setEnabled(self.zoom_factor < 4.0)
        self.zoom_out_act.setEnabled(self.zoom_factor > 0.333)

    def normalSize(self):
        """View image with its normal dimensions."""
        self.image_label.adjustSize()
        self.zoom_factor = 1.0

    def adjustScrollBar(self, scroll_bar, value):
        """Adjust the scrollbar when zooming in or out."""
        scroll_bar.setValue(int(value * scroll_bar.value()) + ((value - 1) * scroll_bar.pageStep()/2))

    def aboutDialog(self):
        QMessageBox.about(self, "About Photo Editor", 
            "Photo Editor\nVersion 0.2\n\nCreated by Joshua Willman")

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
    #app.setAttribute(Qt.AA_DontShowIconsInMenus, True) # No enum for not showing icons
    #app.setStyleSheet(style_sheet)
    window = PhotoEditorGUI()
    sys.exit(app.exec())