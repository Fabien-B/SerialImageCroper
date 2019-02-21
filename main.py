#!/usr/bin/python3
import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from sie import Sie
import argparse

def main():
  app = QtWidgets.QApplication(sys.argv)
  MainWindow = QtWidgets.QMainWindow()
  sie = Sie()
  app.aboutToQuit.connect(sie.closing)
  sie.setupUi(MainWindow)
  sie.built()
  MainWindow.show()
  sys.exit(app.exec_())


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Serial Image Editor")
  #parser.add_argument('config_file', help="JSON configuration file")
  #args = parser.parse_args()
  #main(args.config_file)
  main()
