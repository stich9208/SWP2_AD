from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QAbstractItemView
from PyQt5.QtWidgets import QGridLayout, QListWidget, QListWidgetItem, QLabel
from PyQt5.QtWidgets import QLineEdit, QToolButton, QMessageBox

from dataController import DataController

class RecycleApp(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.dataController = DataController()

        # load data
        try:
            self.dataController.loadData()
        except (EOFError):
            self.dataController.parsingData()
            self.dataController.saveData(self.dataController.recycles)
        finally:
            self.recycleData = self.dataController.loadData()

        # listWindow
        self.listWindow = QListWidget(self)
        self.listWindow.setMinimumSize(700, 200)
        for data in self.recycleData:
            item = QListWidgetItem()
            item.setText(data["name"])
            self.listWindow.addItem(item)
        self.listWindow.sortItems()

        # list layout
        listLayout = QGridLayout()

        listLayout.addWidget(self.listWindow, 0, 0)

        # status layout
        statusLayout = QGridLayout()

        # dump label
        self.dumpTitle = QLabel("How to dump")
        self.dumpTitle.setAlignment(Qt.AlignLeft)
        font = self.dumpTitle.font()
        font.setPointSize(font.pointSize() + 8)
        font.setWeight(75)
        self.dumpTitle.setFont(font)
        statusLayout.addWidget(self.dumpTitle, 0, 0, 1, 3)
        # dump result
        self.dumpResult = QLineEdit()
        self.dumpResult.setReadOnly(True)
        statusLayout.addWidget(self.dumpResult, 1, 0, 1, 2)
        # dump check button
        self.checkButton = QToolButton()
        self.checkButton.setText("check")
        self.checkButton.setMinimumWidth(60)
        self.checkButton.clicked.connect(self.checkBtnClicked)
        statusLayout.addWidget(self.checkButton, 1, 2)

        # add name label
        self.addNameLabel = QLabel("Name: ")
        statusLayout.addWidget(self.addNameLabel, 2, 0)
        # add name
        self.addName = QLineEdit()
        statusLayout.addWidget(self.addName, 2, 1)
        # add dump label
        self.addDumpLabel = QLabel("Dump: ")
        statusLayout.addWidget(self.addDumpLabel, 3, 0)
        # add dump
        self.addDump = QLineEdit()
        statusLayout.addWidget(self.addDump, 3, 1)
        # add button
        self.addButton = QToolButton()
        self.addButton.setText("Add")
        self.addButton.setMinimumHeight(50)
        self.addButton.setMinimumWidth(60)
        self.addButton.clicked.connect(self.addBtnClicked)
        statusLayout.addWidget(self.addButton, 2, 2, 2, 1)

        # search
        self.searchName = QLineEdit()
        self.searchName.setPlaceholderText("search for name")
        statusLayout.addWidget(self.searchName, 4, 0, 1, 2)
        # search button
        self.searchButton = QToolButton()
        self.searchButton.setText("search")
        self.searchButton.setMinimumWidth(60)
        self.searchButton.clicked.connect(self.searchBtnClicked)
        statusLayout.addWidget(self.searchButton, 4, 2)

        # delete
        self.deleteName = QLineEdit()
        self.deleteName.setPlaceholderText("delete for name")
        statusLayout.addWidget(self.deleteName, 5, 0, 1, 2)
        #delete button
        self.deleteButton = QToolButton()
        self.deleteButton.setText("delete")
        self.deleteButton.setMinimumWidth(60)
        self.deleteButton.clicked.connect(self.delBtnClicked)
        statusLayout.addWidget(self.deleteButton, 5, 2)

        # mainlayout
        mainLayout = QGridLayout()
        mainLayout.addLayout(listLayout, 0, 0)
        mainLayout.addLayout(statusLayout, 1, 0)

        # alert
        self.alert = QMessageBox()

        self.setWindowTitle('분리배출')
        self.setLayout(mainLayout)

    def checkBtnClicked(self):
        for item in self.recycleData:
            if item["name"] == self.listWindow.currentItem().text():
                self.dumpResult.setText(item["dump"])

    def addBtnClicked(self):
        if self.addName.text() == "" or self.addDump.text() == "":
            self.alert.information(self, "alert", "can`t add blank")
        else:
            same = self.listWindow.findItems(self.addName.text(), Qt.MatchExactly)
            if len(same) > 0:
                self.alert.information(self, "alert", "already exist")
            else:
                item = {}
                item["name"] = self.addName.text()
                item["dump"] = self.addDump.text()
                self.recycleData.append(item)
                # save data to recycle.dat
                self.dataController.saveData(self.recycleData)

                self.listWindow.addItem(self.addName.text())
                self.listWindow.repaint()
                self.listWindow.sortItems()
                self.addName.clear()
                self.addDump.clear()

    def searchBtnClicked(self):
        sameList = self.listWindow.findItems(self.searchName.text(), Qt.MatchExactly)
        if len(sameList) > 0:
            sameList[0].setSelected(True)
            self.listWindow.scrollToItem(sameList[0], QAbstractItemView.PositionAtTop)
            self.searchName.clear()
        else:
            self.alert.information(self, "alert", "no such item")

    def delBtnClicked(self):
        deleteList = self.listWindow.findItems(self.deleteName.text(), Qt.MatchExactly)
        if len(deleteList) > 0:
            for item in self.recycleData:
                if item["name"] == self.deleteName.text():
                    self.recycleData.remove(item)
            # save data to recycle.dat
            self.dataController.saveData(self.recycleData)

            self.listWindow.takeItem(self.listWindow.row(deleteList[0]))
            self.deleteName.clear()
        else:
            self.alert.information(self, "alert", "no such item")






if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    recycleApp = RecycleApp()
    recycleApp.show()
    sys.exit(app.exec_())

