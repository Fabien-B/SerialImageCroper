from PyQt5 import QtCore, QtWidgets, QtGui
from ui.sie_ui import Ui_MainWindow
import traceback

class Sie(Ui_MainWindow):
  
  def __init__(self, parent=None):
    Ui_MainWindow.__init__(self)
  
  def built(self):
    self.openButton.clicked.connect(self.open_directory)
    pass
  
  def closing(self):
    pass
  
  def open_directory(self):
    _dir = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select a folder:', './', QtWidgets.QFileDialog.ShowDirsOnly)
    print(_dir)
