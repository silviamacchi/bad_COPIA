from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Message(object):
    def setupUi(self, Message):
        Message.setObjectName("Message")
        Message.resize(450, 150)
        Message.setWindowTitle("Operation Status")
        Message.setWindowFlags(Message.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        Message.setStyleSheet("""
            QDialog {
                background-color: #f0f9f0;
                border: 2px solid #4CAF50;
                border-radius: 10px;
            }
            QLabel#label {
                color: #2e7d32;
                font-weight: bold;
            }
            QLabel#label_2 {
                color: #4CAF50;
            }
        """)

        self.gridLayout_2 = QtWidgets.QGridLayout(Message)
        self.gridLayout_2.setContentsMargins(20, 20, 20, 20)
        self.gridLayout_2.setSpacing(15)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(15)

        self.iconLabel = QtWidgets.QLabel(Message)
        pixmap = QtGui.QPixmap("E:/BAD/bad/Success.PNG")
        if pixmap.isNull():
            pixmap = QtGui.QPixmap(64, 64)
            pixmap.fill(QtCore.Qt.transparent)
            painter = QtGui.QPainter(pixmap)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            pen = QtGui.QPen(QtGui.QColor("#4CAF50"), 6)
            painter.setPen(pen)
            painter.drawLine(16, 32, 28, 44)
            painter.drawLine(28, 44, 48, 16)
            painter.end()

        self.iconLabel.setPixmap(pixmap.scaled(64, 64, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.iconLabel.setFixedSize(64, 64)
        self.horizontalLayout.addWidget(self.iconLabel)

        self.verticalTextLayout = QtWidgets.QVBoxLayout()
        self.verticalTextLayout.setSpacing(5)

        self.label = QtWidgets.QLabel(Message)
        self.label.setObjectName("label")
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.verticalTextLayout.addWidget(self.label)

        self.label_2 = QtWidgets.QLabel(Message)
        self.label_2.setObjectName("label_2")
        font2 = QtGui.QFont()
        font2.setPointSize(12)
        self.label_2.setFont(font2)
        self.label_2.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.verticalTextLayout.addWidget(self.label_2)

        self.horizontalLayout.addLayout(self.verticalTextLayout)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0)

        # Optional: Spacer to keep content aligned vertically
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 1, 0)

        self.retranslateUi(Message)
        QtCore.QMetaObject.connectSlotsByName(Message)

    def retranslateUi(self, Message):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("Message", "SUCCESSFULLY DONE!"))
        self.label_2.setText(_translate("Message", "You can go on."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Message = QtWidgets.QDialog()
    ui = Ui_Message()
    ui.setupUi(Message)
    Message.show()
    sys.exit(app.exec_())
