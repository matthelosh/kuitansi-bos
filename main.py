from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout
import sys
from extract import pdf_table_to_excel

class PdfTable2Excel(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Esktrak Tabel di PDF ke Excel")
        self.setGeometry(100,100,300,200)

        self.btn = QPushButton("Pilih File PDF", self)
        self.btn.clicked.connect(self.buka_file)

        layout = QVBoxLayout()
        layout.addWidget(self.btn)
        self.setLayout(layout)

    def buka_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Pilih File PDF:", "", "PDF Files (*.pdf)")
        if file_path:
            output_path = file_path.replace(".pdf", ".xlsx")
            if pdf_table_to_excel(file_path, output_path):
                print(f"Tabel berhasil disimpan sebagai: {output_path}")
            else:
                print(f"Ekstrak tabel gagal.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PdfTable2Excel()
    window.show()
    sys.exit(app.exec_())