# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'week11.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets
import csv

class Ui_FilmManager(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("FilmManager")
        self.resize(900, 600)

        self.centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralWidget)

    
        self.formScrollArea = QtWidgets.QScrollArea()
        self.formScrollArea.setWidgetResizable(True)
        self.formWidget = QtWidgets.QWidget()
        self.formLayout = QtWidgets.QHBoxLayout(self.formWidget)

        self.titleInput = QtWidgets.QLineEdit()
        self.titleInput.setPlaceholderText("Judul Film")
        self.formLayout.addWidget(self.titleInput)

        self.pasteBtn = QtWidgets.QPushButton("📋")
        self.pasteBtn.clicked.connect(self.paste_from_clipboard)
        self.formLayout.addWidget(self.pasteBtn)

        self.genreInput = QtWidgets.QLineEdit()
        self.genreInput.setPlaceholderText("Genre")
        self.formLayout.addWidget(self.genreInput)

        self.yearInput = QtWidgets.QLineEdit()
        self.yearInput.setPlaceholderText("Tahun")
        self.formLayout.addWidget(self.yearInput)

        self.saveBtn = QtWidgets.QPushButton("💾 Simpan")
        self.saveBtn.setStyleSheet("background-color: pink; font-weight: bold;")
        self.formLayout.addWidget(self.saveBtn)

        self.formWidget.setLayout(self.formLayout)
        self.formScrollArea.setWidget(self.formWidget)
        self.mainLayout.addWidget(self.formScrollArea)

        self.dock = QtWidgets.QDockWidget("Panel Pencarian", self)
        self.dock.setFeatures(QtWidgets.QDockWidget.DockWidgetMovable | QtWidgets.QDockWidget.DockWidgetFloatable)
        self.searchInput = QtWidgets.QLineEdit()
        self.searchInput.setPlaceholderText("🔍 Cari judul film...")
        self.dock.setWidget(self.searchInput)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dock)


        self.tableWidgetScrollArea = QtWidgets.QScrollArea()
        self.tableWidgetScrollArea.setWidgetResizable(True)
        self.tableWidgetContainer = QtWidgets.QWidget()
        self.tableLayout = QtWidgets.QVBoxLayout(self.tableWidgetContainer)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Judul", "Genre", "Tahun"])
        self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableLayout.addWidget(self.table)

        self.tableWidgetContainer.setLayout(self.tableLayout)
        self.tableWidgetScrollArea.setWidget(self.tableWidgetContainer)
        self.mainLayout.addWidget(self.tableWidgetScrollArea)

    
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.deleteBtn = QtWidgets.QPushButton("🗑️ Hapus")
        self.deleteBtn.setStyleSheet("background-color: #ffb6c1;")
        self.exportBtn = QtWidgets.QPushButton("📁 Export CSV")
        self.exportBtn.setStyleSheet("background-color: #ffc0cb;")
        self.buttonLayout.addWidget(self.deleteBtn)
        self.buttonLayout.addWidget(self.exportBtn)
        self.mainLayout.addLayout(self.buttonLayout)

    
        self.statusBar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ameylia Intan Zurtika Ayu | NIM: F1D022110")

    
        self.saveBtn.clicked.connect(self.simpan_data)
        self.deleteBtn.clicked.connect(self.hapus_baris)
        self.exportBtn.clicked.connect(self.ekspor_csv)
        self.searchInput.textChanged.connect(self.cari_data)

        self.next_id = 1

    def paste_from_clipboard(self):
        clipboard = QtWidgets.QApplication.clipboard()
        self.titleInput.setText(clipboard.text())

    def simpan_data(self):
        judul = self.titleInput.text()
        genre = self.genreInput.text()
        tahun = self.yearInput.text()

        if not judul or not genre or not tahun:
            QtWidgets.QMessageBox.warning(self, "Peringatan", "Semua data harus diisi!")
            return

        row_pos = self.table.rowCount()
        self.table.insertRow(row_pos)
        self.table.setItem(row_pos, 0, QtWidgets.QTableWidgetItem(str(self.next_id)))
        self.table.setItem(row_pos, 1, QtWidgets.QTableWidgetItem(judul))
        self.table.setItem(row_pos, 2, QtWidgets.QTableWidgetItem(genre))
        self.table.setItem(row_pos, 3, QtWidgets.QTableWidgetItem(tahun))

        self.next_id += 1

        self.titleInput.clear()
        self.genreInput.clear()
        self.yearInput.clear()

    def hapus_baris(self):
        selected = self.table.currentRow()
        if selected >= 0:
            self.table.removeRow(selected)

    def ekspor_csv(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Simpan CSV", "", "CSV Files (*.csv)")
        if path:
            with open(path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Judul", "Genre", "Tahun"])
                for row in range(self.table.rowCount()):
                    rowdata = []
                    for col in range(self.table.columnCount()):
                        item = self.table.item(row, col)
                        rowdata.append(item.text() if item else '')
                    writer.writerow(rowdata)

    def cari_data(self):
        keyword = self.searchInput.text().lower()
        for row in range(self.table.rowCount()):
            match = False
            item = self.table.item(row, 1)
            if item and keyword in item.text().lower():
                match = True
            self.table.setRowHidden(row, not match)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_FilmManager()
    window.setWindowTitle("Aplikasi Manajemen Film")
    window.show()
    sys.exit(app.exec_())

