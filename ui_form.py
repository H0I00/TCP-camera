# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QRadioButton, QSizePolicy,
    QTextBrowser, QVBoxLayout, QWidget)

class Ui_tcpui(object):
    def setupUi(self, tcpui):
        if not tcpui.objectName():
            tcpui.setObjectName(u"tcpui")
        tcpui.resize(620, 420)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(tcpui.sizePolicy().hasHeightForWidth())
        tcpui.setSizePolicy(sizePolicy)
        tcpui.setMinimumSize(QSize(620, 420))
        tcpui.setMaximumSize(QSize(620, 420))
        tcpui.setSizeIncrement(QSize(620, 420))
        tcpui.setBaseSize(QSize(620, 420))
        self.image_label = QLabel(tcpui)
        self.image_label.setObjectName(u"image_label")
        self.image_label.setGeometry(QRect(10, 120, 320, 240))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(160)
        sizePolicy1.setVerticalStretch(120)
        sizePolicy1.setHeightForWidth(self.image_label.sizePolicy().hasHeightForWidth())
        self.image_label.setSizePolicy(sizePolicy1)
        self.image_label.setMinimumSize(QSize(320, 240))
        self.image_label.setMaximumSize(QSize(320, 240))
        self.image_label.setStyleSheet(u"background-color:rgb(220, 220, 220)")
        self.textBrowser = QTextBrowser(tcpui)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(350, 120, 251, 241))
        self.sendEdit = QLineEdit(tcpui)
        self.sendEdit.setObjectName(u"sendEdit")
        self.sendEdit.setGeometry(QRect(350, 370, 171, 31))
        self.layoutWidget = QWidget(tcpui)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 20, 191, 31))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.client_ip = QLabel(self.layoutWidget)
        self.client_ip.setObjectName(u"client_ip")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.client_ip.sizePolicy().hasHeightForWidth())
        self.client_ip.setSizePolicy(sizePolicy2)
        self.client_ip.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout.addWidget(self.client_ip)

        self.server_ip_edit = QLineEdit(self.layoutWidget)
        self.server_ip_edit.setObjectName(u"server_ip_edit")
        sizePolicy2.setHeightForWidth(self.server_ip_edit.sizePolicy().hasHeightForWidth())
        self.server_ip_edit.setSizePolicy(sizePolicy2)
        self.server_ip_edit.setMaximumSize(QSize(120, 16777215))

        self.horizontalLayout.addWidget(self.server_ip_edit)

        self.layoutWidget1 = QWidget(tcpui)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(230, 20, 101, 31))
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.server_port = QLabel(self.layoutWidget1)
        self.server_port.setObjectName(u"server_port")
        sizePolicy2.setHeightForWidth(self.server_port.sizePolicy().hasHeightForWidth())
        self.server_port.setSizePolicy(sizePolicy2)
        self.server_port.setMaximumSize(QSize(40, 50))

        self.horizontalLayout_2.addWidget(self.server_port)

        self.server_port_edit = QLineEdit(self.layoutWidget1)
        self.server_port_edit.setObjectName(u"server_port_edit")
        sizePolicy2.setHeightForWidth(self.server_port_edit.sizePolicy().hasHeightForWidth())
        self.server_port_edit.setSizePolicy(sizePolicy2)
        self.server_port_edit.setMinimumSize(QSize(0, 0))
        self.server_port_edit.setMaximumSize(QSize(50, 50))
        self.server_port_edit.setLayoutDirection(Qt.LeftToRight)
        self.server_port_edit.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.server_port_edit)

        self.layoutWidget2 = QWidget(tcpui)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(10, 70, 191, 31))
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.server_ip = QLabel(self.layoutWidget2)
        self.server_ip.setObjectName(u"server_ip")
        sizePolicy2.setHeightForWidth(self.server_ip.sizePolicy().hasHeightForWidth())
        self.server_ip.setSizePolicy(sizePolicy2)
        self.server_ip.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout_3.addWidget(self.server_ip)

        self.client_ip_edit = QLineEdit(self.layoutWidget2)
        self.client_ip_edit.setObjectName(u"client_ip_edit")
        sizePolicy2.setHeightForWidth(self.client_ip_edit.sizePolicy().hasHeightForWidth())
        self.client_ip_edit.setSizePolicy(sizePolicy2)
        self.client_ip_edit.setMaximumSize(QSize(120, 16777215))

        self.horizontalLayout_3.addWidget(self.client_ip_edit)

        self.layoutWidget3 = QWidget(tcpui)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(230, 70, 101, 31))
        self.horizontalLayout_4 = QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.client_port = QLabel(self.layoutWidget3)
        self.client_port.setObjectName(u"client_port")
        sizePolicy2.setHeightForWidth(self.client_port.sizePolicy().hasHeightForWidth())
        self.client_port.setSizePolicy(sizePolicy2)
        self.client_port.setMaximumSize(QSize(40, 50))

        self.horizontalLayout_4.addWidget(self.client_port)

        self.client_port_edit = QLineEdit(self.layoutWidget3)
        self.client_port_edit.setObjectName(u"client_port_edit")
        sizePolicy2.setHeightForWidth(self.client_port_edit.sizePolicy().hasHeightForWidth())
        self.client_port_edit.setSizePolicy(sizePolicy2)
        self.client_port_edit.setMinimumSize(QSize(0, 0))
        self.client_port_edit.setMaximumSize(QSize(50, 50))

        self.horizontalLayout_4.addWidget(self.client_port_edit)

        self.layoutWidget4 = QWidget(tcpui)
        self.layoutWidget4.setObjectName(u"layoutWidget4")
        self.layoutWidget4.setGeometry(QRect(340, 20, 111, 81))
        self.verticalLayout = QVBoxLayout(self.layoutWidget4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.server_mode_check = QRadioButton(self.layoutWidget4)
        self.server_mode_check.setObjectName(u"server_mode_check")
        self.server_mode_check.setChecked(True)

        self.verticalLayout.addWidget(self.server_mode_check)

        self.client_mode_check = QRadioButton(self.layoutWidget4)
        self.client_mode_check.setObjectName(u"client_mode_check")

        self.verticalLayout.addWidget(self.client_mode_check)

        self.layoutWidget5 = QWidget(tcpui)
        self.layoutWidget5.setObjectName(u"layoutWidget5")
        self.layoutWidget5.setGeometry(QRect(470, 20, 131, 81))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.start_button = QPushButton(self.layoutWidget5)
        self.start_button.setObjectName(u"start_button")

        self.verticalLayout_2.addWidget(self.start_button)

        self.stop_button = QPushButton(self.layoutWidget5)
        self.stop_button.setObjectName(u"stop_button")

        self.verticalLayout_2.addWidget(self.stop_button)

        self.sendButton = QPushButton(tcpui)
        self.sendButton.setObjectName(u"sendButton")
        self.sendButton.setGeometry(QRect(530, 370, 71, 31))
        self.widget = QWidget(tcpui)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(10, 374, 321, 31))
        self.horizontalLayout_5 = QHBoxLayout(self.widget)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.fps_label = QLabel(self.widget)
        self.fps_label.setObjectName(u"fps_label")
        self.fps_label.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout_5.addWidget(self.fps_label)

        self.image_size_label = QLabel(self.widget)
        self.image_size_label.setObjectName(u"image_size_label")

        self.horizontalLayout_5.addWidget(self.image_size_label)

        self.save_check = QCheckBox(self.widget)
        self.save_check.setObjectName(u"save_check")
        self.save_check.setMaximumSize(QSize(90, 16777215))

        self.horizontalLayout_5.addWidget(self.save_check)


        self.retranslateUi(tcpui)

        QMetaObject.connectSlotsByName(tcpui)
    # setupUi

    def retranslateUi(self, tcpui):
        tcpui.setWindowTitle(QCoreApplication.translate("tcpui", u"tcpui", None))
        self.image_label.setText(QCoreApplication.translate("tcpui", u"\u56fe\u7247\u9884\u89c8", None))
        self.client_ip.setText(QCoreApplication.translate("tcpui", u"\u5ba2\u6237\u7aef IP", None))
        self.server_ip_edit.setText(QCoreApplication.translate("tcpui", u"192.168.x.60", None))
        self.server_port.setText(QCoreApplication.translate("tcpui", u"\u7aef\u53e3", None))
        self.server_port_edit.setText(QCoreApplication.translate("tcpui", u"8089", None))
        self.server_ip.setText(QCoreApplication.translate("tcpui", u"\u670d\u52a1\u5668 IP", None))
        self.client_ip_edit.setText(QCoreApplication.translate("tcpui", u"192.168.x.179", None))
        self.client_port.setText(QCoreApplication.translate("tcpui", u"\u7aef\u53e3", None))
        self.client_port_edit.setText(QCoreApplication.translate("tcpui", u"8089", None))
        self.server_mode_check.setText(QCoreApplication.translate("tcpui", u"\u670d\u52a1\u5668\u6a21\u5f0f", None))
        self.client_mode_check.setText(QCoreApplication.translate("tcpui", u"\u5ba2\u6237\u7aef\u6a21\u5f0f", None))
        self.start_button.setText(QCoreApplication.translate("tcpui", u"\u5f00\u59cb", None))
        self.stop_button.setText(QCoreApplication.translate("tcpui", u"\u505c\u6b62", None))
        self.sendButton.setText(QCoreApplication.translate("tcpui", u"\u53d1\u9001", None))
        self.fps_label.setText(QCoreApplication.translate("tcpui", u"FPS:", None))
        self.image_size_label.setText(QCoreApplication.translate("tcpui", u"\u5206\u8fa8\u7387:", None))
        self.save_check.setText(QCoreApplication.translate("tcpui", u"\u4fdd\u5b58\u56fe\u7247", None))
    # retranslateUi

