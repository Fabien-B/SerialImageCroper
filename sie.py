from PyQt5 import QtCore, QtWidgets, QtGui
from ui.sie_ui import Ui_MainWindow
import os


class Sie(Ui_MainWindow):

    def __init__(self, parent=None):
        Ui_MainWindow.__init__(self)
        self.scene = QtWidgets.QGraphicsScene()
        self.files = []
        self.openShortcut = None
        self.saveEnterShortcut = None
        self.saveShortcut = None
        self.skipShortcut = None
        self.last_rect = None
        self.last_rotation = 0

    def built(self):
        self.openShortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+O"), self.centralwidget)
        self.saveShortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+S"), self.centralwidget)
        self.saveEnterShortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Space), self.centralwidget)
        self.skipShortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Tab), self.centralwidget)

        self.graphicsView.setScene(self.scene)
        self.scene.setBackgroundBrush(QtCore.Qt.white)
        self.openButton.clicked.connect(self.select_files)
        self.rotateCwButton.clicked.connect(lambda: self.graphicsView.rotate_pixmap(45))
        self.rotateCcwButton.clicked.connect(lambda: self.graphicsView.rotate_pixmap(-45))
        self.saveButton.clicked.connect(self.save_image)
        self.skipButton.clicked.connect(self.skip_image)
        self.openShortcut.activated.connect(self.select_files)
        self.saveShortcut.activated.connect(self.save_image)
        self.skipShortcut.activated.connect(self.skip_image)
        self.saveEnterShortcut.activated.connect(self.save_image)
        self.graphicsView.dropHandler = self.drop_handler
        self.graphicsView.setFocus()

    def closing(self):
        pass

    def select_files(self):
        files = QtWidgets.QFileDialog.getOpenFileNames(None, "Select files", "/home/fabien/Images/",
                                                       "Images (*.png *.xpm *.jpg);;Python_files (*.py)")
        self.files = files[0]
        if len(self.files) > 0:
            self.load_image(self.files[0])

    def load_image(self, image_path):
        self.scene.clear()
        pixmap = QtGui.QPixmap(image_path)
        pixmap_item = self.scene.addPixmap(pixmap)         # type: QtWidgets.QGraphicsPixmapItem
        self.graphicsView.current_pixmap_item = pixmap_item
        self.graphicsView.rotate_pixmap(self.last_rotation)
        if self.last_rect is not None:
            self.graphicsView.rect_item = self.scene.addRect(self.last_rect)
        rect = pixmap.rect()  # type: QtCore.QRect
        rect.setWidth(rect.width() * 2)
        rect.setHeight(rect.height() * 2)
        rect.setLeft(rect.x() - rect.width() / 2)
        rect.setTop(rect.y() - rect.height() / 2)
        self.scene.setSceneRect(QtCore.QRectF(rect))
        self.graphicsView.fitInView(pixmap_item.boundingRect(), QtCore.Qt.KeepAspectRatio)

    def load_next_image(self):
        self.graphicsView.current_pixmap_item = None
        self.graphicsView.rect_item = None
        if len(self.files) > 0:
            self.load_image(self.files[0])
        else:
            self.scene.clear()
            text_item = self.scene.addText("No images left !")
            self.graphicsView.fitInView(text_item.boundingRect(), QtCore.Qt.KeepAspectRatio)

    def save_image(self):
        if self.graphicsView.rect_item is not None and len(self.files) > 0:
            rect = self.graphicsView.rect_item.boundingRect()   # type
            self.graphicsView.removeRect()
            self.last_rect = rect
            self.last_rotation = self.graphicsView.current_pixmap_item.rotation()
            outImg = QtGui.QPixmap(rect.width(), rect.height())
            painter = QtGui.QPainter(outImg)
            self.scene.setSceneRect(rect)
            self.scene.render(painter)
            out_dir = os.path.dirname(self.files[0]) + "/cropped/"      # TODO improve output
            name = os.path.basename(self.files[0])
            name, _ = os.path.splitext(name)
            os.makedirs(out_dir, exist_ok=True)
            path = out_dir + name + ".png"
            outImg.save(path, "PNG")
            painter.end()
            del self.files[0]
            self.load_next_image()

    def drop_handler(self, e: QtGui.QDropEvent):
        urls = e.mimeData().urls()
        self.files = [url.path() for url in urls]
        self.load_next_image()

    def skip_image(self):
        if len(self.files) > 0:
            del self.files[0]
            self.load_next_image()

