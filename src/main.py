from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QLabel
import sys
from extract import pdf_table_to_excel, save_to_db
from datetime import datetime


class PdfTable2Excel(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Esktrak Tabel di PDF ke Excel")
        self.setGeometry(200,200,300,200)

        # self.btn = QPushButton("Pilih File PDF", self)
        # self.btn.clicked.connect(self.buka_file)

        self.label = QLabel("Pilih File PDF", self)

        # Button convert to Excel
        self.btn2Excel = QPushButton("Konversi Tabel PDF ke Excel", self)
        self.btn2Excel.clicked.connect(self.table2Excel)

        self.btn2Db = QPushButton("Simpan ke Database", self)
        self.btn2Db.clicked.connect(self.save2Db)

        layout = QVBoxLayout()
        layout.addWidget(self.btn2Excel)
        layout.addWidget(self.btn2Db)
        self.setLayout(layout)

    def table2Excel(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Pilih File PDF:", "", "PDF Files (*.pdf)")
        if file_path:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            output_path = file_path.replace(".pdf", "")
            output_filename = f"{output_path}-{timestamp}.xlsx"
            if pdf_table_to_excel(file_path, output_filename):
                print(f"Tabel berhasil disimpan sebagai: {output_filename}")
            else:
                print(f"Ekstrak tabel gagal.")

    def save2Db(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Pilih File PDF:", "", "PDF Files (*.pdf)")
        if file_path:
            if save_to_db(file_path):
               print(f"Data berhasil disimpan ke database")
            else:
                print("Penyimpanan Data Gagal")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PdfTable2Excel()
    window.show()
    sys.exit(app.exec_())