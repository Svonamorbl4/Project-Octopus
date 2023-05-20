import asyncio
import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore
import subprocess
from PyQt5.QtWidgets import QTableWidgetItem
import interface
from modules.mTest import mTest
from modules.mInstallation import mInstallation
from modules.mDeinstallation import mDeinstallation
from interface import Ui_MainWindow
# from modules.mPing import mPing
import paramiko

# Класс приложения
class ExampleApp(QtWidgets.QMainWindow, interface.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.goodHosts = []

        modules = ['Test',
                   'Installation',
                   'Deinstallation',
                   ]
        self.comboBtn.addItems(modules)

        self.inventoryBtn.clicked.connect(self.inventory)
        self.accessibilityBtn.clicked.connect(self.accessibility)

        # self.actionBtn.clicked.connect(self.action)
        self.actionBtn.clicked.connect(self.useAction)
        self.clearBtn.clicked.connect(self.clear)

    # Метод создания таблицы с хостами
    def createTable(self):
        self.inventoryBrowser.setColumnCount(3)
        inventoryHeaders = ['Username', 'Hostname', 'Password']
        hostsLen = len(self.hosts)
        self.inventoryBrowser.setHorizontalHeaderLabels(inventoryHeaders)
        self.inventoryBrowser.setRowCount(hostsLen)
        self.inventoryBrowser.setColumnCount(3)
        header = self.inventoryBrowser.horizontalHeader()
        self.inventoryBrowser.verticalHeader().hide()
        header.setStretchLastSection(True)
        # print(self.hosts)
        for row in range(hostsLen):
            for column in range(3):
                self.inventoryBrowser.setItem(row, column, QTableWidgetItem(self.hosts[row][column]))
                self.inventoryBrowser.setItem(row, column, QTableWidgetItem(self.hosts[row][column]))
                self.inventoryBrowser.setItem(row, column, QTableWidgetItem(self.hosts[row][column]))

    # Метод для кнопки с инвенторным файлом
    def inventory(self):
        if (self.inventoryBrowser.rowCount() > 0):
            while (self.inventoryBrowser.rowCount() > 0):
                self.inventoryBrowser.removeRow(0)
        self.hosts = []
        inventory = QtWidgets.QFileDialog.getOpenFileName(self, "Инвенторный файл")
        with open(inventory[0]) as file:
            for line in file:
                line = line.replace('\n', '')
                line = line.split('@')
                self.hosts.append(line)
                # print(line)
            self.inventory = inventory[0]
        print(self.hosts
              )
        self.createTable()

    # Метод проверки доступности хостов
    def accessibility(self):
        self.statusBrowser.clear()
        self.statusBrowser.addItem("Hostname\t\tStatus\n")

        for host in self.hosts:
            accessibilityCommand = ['ping', '-c', '1', '-s', '1', host[1]]
            response = subprocess.call(accessibilityCommand)
            if (response == 0):
                self.goodHosts.append(host)
                if (len(host[1]) > 11):
                    self.statusBrowser.addItem(host[1] + "\tOK")
                else:
                    self.statusBrowser.addItem(host[1] + "\t\tOK")
            else:
                if (len(host[1]) > 11):
                    self.statusBrowser.addItem(host[1] + "\tFAILED")
                else:
                    self.statusBrowser.addItem(host[1] + "\t\tFAILED")
        # print(self.goodHosts)

    def clear(self):
        self.statusBrowser.clear()


    def useAction(self):
        asyncio.run(self.action())


    # Метод для вызова модуля
    async def action(self):
        self.statusBrowser.clear()
        self.statusBrowser.addItem("Hostname\t\tStatus\n")
        # Вызов модуля Test
        if self.comboBtn.currentText() == 'Test':
            for host in self.goodHosts:
                result = mTest(host[0], host[1], host[2])
                if result:
                    self.statusBrowser.addItem(host[1] + ' - FAILED')
                    print(result)
                else:
                    self.statusBrowser.addItem(host[1] + ' - OK')
                    continue
                    print(result)
        elif self.comboBtn.currentText() == 'Installation':
            pkgName = self.commandLine.text()
            if pkgName:
                for host in self.goodHosts:
                    # result = mInstallation(host[0], host[1], host[2], pkgName)
                    task = asyncio.create_task(mInstallation(host[0], host[1], host[2], pkgName))
                    result = await task
                    if result:
                        self.statusBrowser.addItem(host[1] + ' - FAILED')
                        print(result)
                    else:
                        self.statusBrowser.addItem(host[1] + ' - OK')
                        print(result)
            else:
                self.statusBrowser.clear()
                self.statusBrowser.addItem('You have not given any parameters to the module!')
        elif self.comboBtn.currentText() == 'Deinstallation':
            pkgName = self.commandLine.text()
            if pkgName:
                for host in self.goodHosts:
                    # result = mInstallation(host[0], host[1], host[2], pkgName)
                    task = asyncio.create_task(mDeinstallation(host[0], host[1], host[2], pkgName))
                    result = await task
                    if result:
                        self.statusBrowser.addItem(host[1] + ' - FAILED')
                        print(result)
                    else:
                        self.statusBrowser.addItem(host[1] + ' - OK')
                        print(result)
            else:
                self.statusBrowser.clear()
                self.statusBrowser.addItem('You have not given any parameters to the module!')

# Функция для отрисовки GUI
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()

# Вызов функции отрисовки GUI
if __name__ == '__main__':
    main()