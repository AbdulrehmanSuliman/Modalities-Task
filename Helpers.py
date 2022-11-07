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


class BrowseWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.layout_browse = QtWidgets.QHBoxLayout()
        self.layout_browse.setContentsMargins(10, 10, 10, 10)
        self.browse_label = QtWidgets.QLabel()
        self.browse_label = QtWidgets.QLabel("Open: ")
        self.browse_label.setFont(QFont('impact', 15))
        self.browse_label.setStyleSheet(TEXT_COLOR)

        self.browse_text = QtWidgets.QLineEdit()
        self.browse_text.setStyleSheet(TEXT_COLOR)
        self.browse_button = QtWidgets.QPushButton('Browse')
        self.browse_button.setStyleSheet(PUSH_BUTTON_STYLE)

        self.layout_browse.addWidget(self.browse_label)
        self.layout_browse.addWidget(self.browse_text)
        self.layout_browse.addWidget(self.browse_button)

        self.setLayout(self.layout_browse)
