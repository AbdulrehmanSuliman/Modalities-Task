from PyQt5.QtWidgets import QWidget
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont
import numpy as np

TEXT_COLOR = "color: #BCBCBC;"

PUSH_BUTTON_STYLE = """QPushButton {
    color: #BCBCBC;
    background: #0F62FE;
    border-width: 0px;
    border-color: yellow;
    border-style: solid;
    border-radius: 10px;
    min-width: 3em;
    min-height: 30px;
    padding: 6px;}
    
    QPushButton:hover {
background-color: #c2c2c2;
color: black;
}
    QPushButton:pressed {
background-color: #FFFFFF;
color: black;
}
"""

PRESSED_PUSH_BUTTON_STYLE = """QPushButton {
    color: #BCBCBC;
    background: #07255e;
    border-width: 0px;
    border-color: yellow;
    border-style: solid;
    border-radius: 10px;
    min-width: 3em;
    min-height: 30px;
    padding: 6px;}
    
    QPushButton:hover {
background-color: #c2c2c2;
color: black;
}
    QPushButton:pressed {
background-color: #FFFFFF;
color: black;
}
"""


class BrowseWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.layout_browse = QtWidgets.QHBoxLayout()
        self.layout_browse.setContentsMargins(10, 10, 10, 10)
        self.browse_button = QtWidgets.QPushButton('Browse')
        self.browse_button.setStyleSheet(PUSH_BUTTON_STYLE)

        self.crosshair_button = QtWidgets.QPushButton('Crosshair')
        self.crosshair_button.setStyleSheet(PUSH_BUTTON_STYLE)

        self.measurmentsLine_button = QtWidgets.QPushButton('Line')
        self.measurmentsLine_button.setStyleSheet(PUSH_BUTTON_STYLE)

        self.measurmentsPolygon_button = QtWidgets.QPushButton('Polygon')
        self.measurmentsPolygon_button.setStyleSheet(PUSH_BUTTON_STYLE)

        self.measurmentsAngle_button = QtWidgets.QPushButton('Angle')
        self.measurmentsAngle_button.setStyleSheet(PUSH_BUTTON_STYLE)

        self.measurmentsEllipse_button = QtWidgets.QPushButton('Elipse')
        self.measurmentsEllipse_button.setStyleSheet(PUSH_BUTTON_STYLE)

        self.layout_browse.addWidget(self.browse_button)
        self.layout_browse.addWidget(self.crosshair_button)
        self.layout_browse.addWidget(self.measurmentsLine_button)
        self.layout_browse.addWidget(self.measurmentsAngle_button)
        self.layout_browse.addWidget(self.measurmentsPolygon_button)
        self.layout_browse.addWidget(self.measurmentsEllipse_button)

        self.setLayout(self.layout_browse)

    def setButtonStyle(self, button, isPressed):
        if button == 0:
            if isPressed:
                self.measurmentsLine_button.setStyleSheet(
                    PRESSED_PUSH_BUTTON_STYLE)
            else:
                self.measurmentsLine_button.setStyleSheet(PUSH_BUTTON_STYLE)
        elif button == 1:
            if isPressed:
                self.measurmentsAngle_button.setStyleSheet(
                    PRESSED_PUSH_BUTTON_STYLE)
            else:
                self.measurmentsAngle_button.setStyleSheet(PUSH_BUTTON_STYLE)
        elif button == 2:
            if isPressed:
                self.measurmentsPolygon_button.setStyleSheet(
                    PRESSED_PUSH_BUTTON_STYLE)
            else:
                self.measurmentsPolygon_button.setStyleSheet(PUSH_BUTTON_STYLE)
        elif button == 3:
            if isPressed:
                self.measurmentsEllipse_button.setStyleSheet(
                    PRESSED_PUSH_BUTTON_STYLE)
            else:
                self.measurmentsEllipse_button.setStyleSheet(PUSH_BUTTON_STYLE)
        elif button == 4:
            if isPressed:
                self.crosshair_button.setStyleSheet(PRESSED_PUSH_BUTTON_STYLE)
            else:
                self.crosshair_button.setStyleSheet(PUSH_BUTTON_STYLE)
