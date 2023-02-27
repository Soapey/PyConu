# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'conu/ui/ui_files/MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.page_handler = QtWidgets.QStackedWidget(self.centralwidget)
        self.page_handler.setStyleSheet("")
        self.page_handler.setObjectName("page_handler")
        self.page_login = QtWidgets.QWidget()
        self.page_login.setStyleSheet("")
        self.page_login.setObjectName("page_login")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.page_login)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.login_txtPassword = QtWidgets.QLineEdit(self.page_login)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.login_txtPassword.setFont(font)
        self.login_txtPassword.setStyleSheet("QLineEdit {\n"
"    background-color: white;\n"
"    border-style: inset;\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    border-color: black;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-width: 2px;\n"
"    border-color: #028090;\n"
"}")
        self.login_txtPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login_txtPassword.setObjectName("login_txtPassword")
        self.gridLayout_2.addWidget(self.login_txtPassword, 3, 2, 1, 1)
        self.login_txtUsername = QtWidgets.QLineEdit(self.page_login)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.login_txtUsername.setFont(font)
        self.login_txtUsername.setStyleSheet("QLineEdit {\n"
"    background-color: white;\n"
"    border-style: inset;\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    border-color: black;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-width: 2px;\n"
"    border-color: #028090;\n"
"}")
        self.login_txtUsername.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.login_txtUsername.setObjectName("login_txtUsername")
        self.gridLayout_2.addWidget(self.login_txtUsername, 2, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.page_login)
        font = QtGui.QFont()
        font.setFamily("Impact")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet("QLabel {\n"
"    color: #6c757d;\n"
"}")
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.page_login)
        font = QtGui.QFont()
        font.setFamily("Impact")
        font.setPointSize(36)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("QLabel {\n"
"    background-color: #02c39a;\n"
"    border-style: outset;\n"
"    border-radius: 10px;\n"
"    padding: 10px;\n"
"}")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 1, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.page_login)
        font = QtGui.QFont()
        font.setFamily("Impact")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("QLabel {\n"
"    color: #6c757d;\n"
"}")
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 3, 1, 1, 1)
        self.login_btnLogin = QtWidgets.QPushButton(self.page_login)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.login_btnLogin.setFont(font)
        self.login_btnLogin.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.login_btnLogin.setFocusPolicy(QtCore.Qt.NoFocus)
        self.login_btnLogin.setStyleSheet("QPushButton\n"
"{\n"
"    background-color: #05668d;\n"
"    color: white;\n"
"    border-style: outset;\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover\n"
"{\n"
"    background-color: #028090;\n"
"}\n"
"")
        self.login_btnLogin.setObjectName("login_btnLogin")
        self.gridLayout_2.addWidget(self.login_btnLogin, 4, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 0, 6, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 3, 6, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem2, 5, 1, 1, 2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem3, 0, 1, 1, 2)
        self.page_handler.addWidget(self.page_login)
        self.page_assignee_listingview = QtWidgets.QWidget()
        self.page_assignee_listingview.setObjectName("page_assignee_listingview")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.page_assignee_listingview)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.assignee_listingview_tblAssignee = QtWidgets.QTableWidget(self.page_assignee_listingview)
        self.assignee_listingview_tblAssignee.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.assignee_listingview_tblAssignee.setStyleSheet("QTableWidget {\n"
"    background-color: white;\n"
"    border-style: inset;\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    border-color: black;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QTableWidget:focus {\n"
"    border-width: 2px;\n"
"    border-color: #028090;\n"
"}")
        self.assignee_listingview_tblAssignee.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.assignee_listingview_tblAssignee.setTabKeyNavigation(False)
        self.assignee_listingview_tblAssignee.setAlternatingRowColors(False)
        self.assignee_listingview_tblAssignee.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.assignee_listingview_tblAssignee.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.assignee_listingview_tblAssignee.setCornerButtonEnabled(False)
        self.assignee_listingview_tblAssignee.setObjectName("assignee_listingview_tblAssignee")
        self.assignee_listingview_tblAssignee.setColumnCount(0)
        self.assignee_listingview_tblAssignee.setRowCount(0)
        self.assignee_listingview_tblAssignee.horizontalHeader().setStretchLastSection(True)
        self.assignee_listingview_tblAssignee.verticalHeader().setVisible(False)
        self.gridLayout_3.addWidget(self.assignee_listingview_tblAssignee, 3, 0, 1, 3)
        self.label_4 = QtWidgets.QLabel(self.page_assignee_listingview)
        font = QtGui.QFont()
        font.setFamily("Impact")
        font.setPointSize(20)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("QLabel {\n"
"    color: white;\n"
"    background-color: #05668d;\n"
"    border-style: outset;\n"
"    border-radius: 10px;\n"
"    padding: 10px;\n"
"    margin: 0px 0px 20px 0px;\n"
"}")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 0, 0, 1, 3)
        self.assignee_listingview_btnNew = QtWidgets.QPushButton(self.page_assignee_listingview)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.assignee_listingview_btnNew.setFont(font)
        self.assignee_listingview_btnNew.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.assignee_listingview_btnNew.setFocusPolicy(QtCore.Qt.NoFocus)
        self.assignee_listingview_btnNew.setStyleSheet("QPushButton {\n"
"    color: white;\n"
"    background-color: #0db39e;\n"
"    border-style: outset;\n"
"    border-radius: 10px;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"        background-color: #16db93;\n"
"}")
        self.assignee_listingview_btnNew.setObjectName("assignee_listingview_btnNew")
        self.gridLayout_3.addWidget(self.assignee_listingview_btnNew, 1, 0, 1, 1)
        self.assignee_listingview_btnDelete = QtWidgets.QPushButton(self.page_assignee_listingview)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.assignee_listingview_btnDelete.setFont(font)
        self.assignee_listingview_btnDelete.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.assignee_listingview_btnDelete.setFocusPolicy(QtCore.Qt.NoFocus)
        self.assignee_listingview_btnDelete.setStyleSheet("QPushButton {\n"
"    color: white;\n"
"    background-color: #f94144;\n"
"    border-style: outset;\n"
"    border-radius: 10px;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"        background-color: #ff595e;\n"
"}")
        self.assignee_listingview_btnDelete.setObjectName("assignee_listingview_btnDelete")
        self.gridLayout_3.addWidget(self.assignee_listingview_btnDelete, 1, 2, 1, 1)
        self.assignee_listingview_txtSearch = QtWidgets.QLineEdit(self.page_assignee_listingview)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.assignee_listingview_txtSearch.setFont(font)
        self.assignee_listingview_txtSearch.setStyleSheet("QLineEdit {\n"
"    background-color: white;\n"
"    border-style: inset;\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    border-color: black;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-width: 2px;\n"
"    border-color: #028090;\n"
"}")
        self.assignee_listingview_txtSearch.setClearButtonEnabled(True)
        self.assignee_listingview_txtSearch.setObjectName("assignee_listingview_txtSearch")
        self.gridLayout_3.addWidget(self.assignee_listingview_txtSearch, 2, 0, 1, 3)
        self.assignee_listingview_btnEdit = QtWidgets.QPushButton(self.page_assignee_listingview)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.assignee_listingview_btnEdit.setFont(font)
        self.assignee_listingview_btnEdit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.assignee_listingview_btnEdit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.assignee_listingview_btnEdit.setStyleSheet("QPushButton {\n"
"    color: white;\n"
"    background-color: #f8961e;\n"
"    border-style: outset;\n"
"    border-radius: 10px;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"        background-color: #f9c74f;\n"
"}")
        self.assignee_listingview_btnEdit.setObjectName("assignee_listingview_btnEdit")
        self.gridLayout_3.addWidget(self.assignee_listingview_btnEdit, 1, 1, 1, 1)
        self.page_handler.addWidget(self.page_assignee_listingview)
        self.page_assignee_entryform = QtWidgets.QWidget()
        self.page_assignee_entryform.setObjectName("page_assignee_entryform")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.page_assignee_entryform)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.assignee_entryform_btnSave = QtWidgets.QPushButton(self.page_assignee_entryform)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.assignee_entryform_btnSave.setFont(font)
        self.assignee_entryform_btnSave.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.assignee_entryform_btnSave.setFocusPolicy(QtCore.Qt.NoFocus)
        self.assignee_entryform_btnSave.setStyleSheet("QPushButton {\n"
"    width: 60px;\n"
"    color: white;\n"
"    background-color: #006494;\n"
"    border-style: outset;\n"
"    border-radius: 10px;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"        background-color: #0582ca;\n"
"}")
        self.assignee_entryform_btnSave.setObjectName("assignee_entryform_btnSave")
        self.gridLayout_4.addWidget(self.assignee_entryform_btnSave, 4, 2, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem4, 4, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.page_assignee_entryform)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.label_7.setObjectName("label_7")
        self.gridLayout_4.addWidget(self.label_7, 3, 0, 1, 1)
        self.assignee_entryform_txtDescription = QtWidgets.QTextEdit(self.page_assignee_entryform)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.assignee_entryform_txtDescription.setFont(font)
        self.assignee_entryform_txtDescription.setStyleSheet("QTextEdit {\n"
"    background-color: white;\n"
"    border-style: inset;\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    border-color: black;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QTextEdit:focus {\n"
"    border-width: 2px;\n"
"    border-color: #028090;\n"
"}\n"
"")
        self.assignee_entryform_txtDescription.setDocumentTitle("")
        self.assignee_entryform_txtDescription.setObjectName("assignee_entryform_txtDescription")
        self.gridLayout_4.addWidget(self.assignee_entryform_txtDescription, 3, 1, 1, 2)
        self.assignee_entryform_txtName = QtWidgets.QLineEdit(self.page_assignee_entryform)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.assignee_entryform_txtName.setFont(font)
        self.assignee_entryform_txtName.setStyleSheet("QLineEdit {\n"
"    background-color: white;\n"
"    border-style: inset;\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    border-color: black;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-width: 2px;\n"
"    border-color: #028090;\n"
"}\n"
"")
        self.assignee_entryform_txtName.setClearButtonEnabled(True)
        self.assignee_entryform_txtName.setObjectName("assignee_entryform_txtName")
        self.gridLayout_4.addWidget(self.assignee_entryform_txtName, 2, 1, 1, 2)
        self.assignee_entryform_btnBack = QtWidgets.QPushButton(self.page_assignee_entryform)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.assignee_entryform_btnBack.setFont(font)
        self.assignee_entryform_btnBack.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.assignee_entryform_btnBack.setFocusPolicy(QtCore.Qt.NoFocus)
        self.assignee_entryform_btnBack.setStyleSheet("QPushButton {\n"
"    color: white;\n"
"    background-color: #6c757d;\n"
"    border-style: outset;\n"
"    border-radius: 10px;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"        background-color: #adb5bd;\n"
"}")
        self.assignee_entryform_btnBack.setObjectName("assignee_entryform_btnBack")
        self.gridLayout_4.addWidget(self.assignee_entryform_btnBack, 4, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.page_assignee_entryform)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_4.addWidget(self.label_6, 2, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.page_assignee_entryform)
        font = QtGui.QFont()
        font.setFamily("Impact")
        font.setPointSize(20)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("QLabel {\n"
"    color: white;\n"
"    background-color: #05668d;\n"
"    border-style: outset;\n"
"    border-radius: 10px;\n"
"    padding: 10px;\n"
"    margin: 0px 0px 20px 0px;\n"
"}")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 0, 0, 1, 3)
        self.label_8 = QtWidgets.QLabel(self.page_assignee_entryform)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("QLabel {\n"
"    color: grey;\n"
"}")
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_4.addWidget(self.label_8, 1, 0, 1, 1)
        self.assignee_entryform_lblId = QtWidgets.QLabel(self.page_assignee_entryform)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.assignee_entryform_lblId.setFont(font)
        self.assignee_entryform_lblId.setStyleSheet("QLabel {\n"
"    background-color: lightgrey;\n"
"    border-style: inset;\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    border-color: black;\n"
"    padding: 4px;\n"
"}")
        self.assignee_entryform_lblId.setText("")
        self.assignee_entryform_lblId.setObjectName("assignee_entryform_lblId")
        self.gridLayout_4.addWidget(self.assignee_entryform_lblId, 1, 1, 1, 2)
        self.page_handler.addWidget(self.page_assignee_entryform)
        self.gridLayout.addWidget(self.page_handler, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.page_handler.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.login_txtUsername, self.login_txtPassword)
        MainWindow.setTabOrder(self.login_txtPassword, self.login_btnLogin)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CONU"))
        self.label.setText(_translate("MainWindow", "USERNAME"))
        self.label_3.setText(_translate("MainWindow", "CONU"))
        self.label_2.setText(_translate("MainWindow", "PASSWORD"))
        self.login_btnLogin.setText(_translate("MainWindow", "Log In"))
        self.assignee_listingview_tblAssignee.setSortingEnabled(True)
        self.label_4.setText(_translate("MainWindow", "ASSIGNEES"))
        self.assignee_listingview_btnNew.setText(_translate("MainWindow", "New"))
        self.assignee_listingview_btnDelete.setText(_translate("MainWindow", "Delete"))
        self.assignee_listingview_txtSearch.setPlaceholderText(_translate("MainWindow", "Search"))
        self.assignee_listingview_btnEdit.setText(_translate("MainWindow", "Edit"))
        self.assignee_entryform_btnSave.setText(_translate("MainWindow", "Save"))
        self.label_7.setText(_translate("MainWindow", "Description"))
        self.assignee_entryform_txtDescription.setPlaceholderText(_translate("MainWindow", "OPTIONAL"))
        self.assignee_entryform_txtName.setPlaceholderText(_translate("MainWindow", "REQUIRED"))
        self.assignee_entryform_btnBack.setText(_translate("MainWindow", "Back to listing view"))
        self.label_6.setText(_translate("MainWindow", "Name"))
        self.label_5.setText(_translate("MainWindow", "ASSIGNEE ENTRY FORM"))
        self.label_8.setText(_translate("MainWindow", "ID"))
