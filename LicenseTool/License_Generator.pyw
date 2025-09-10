import sys
from PySide6 import QtWidgets
from license_keys import make_license

class Gen(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VisitorSuite – Lizenzgenerator")
        self.resize(640, 360)
        w = QtWidgets.QWidget(); self.setCentralWidget(w)
        f = QtWidgets.QFormLayout(w)
        self.product = QtWidgets.QComboBox(); self.product.addItems(["VS_USER"])
        self.customer = QtWidgets.QLineEdit("Kunde GmbH")
        self.days = QtWidgets.QSpinBox(); self.days.setRange(0, 3650); self.days.setValue(3)
        self.out = QtWidgets.QPlainTextEdit(); self.out.setReadOnly(True)
        btn = QtWidgets.QPushButton("Lizenz erzeugen"); btn.clicked.connect(self.make)
        f.addRow("Produkt:", self.product); f.addRow("Kunde:", self.customer)
        f.addRow("Gültigkeit (Tage, 0=perpetual):", self.days); f.addRow(btn); f.addRow("Lizenzschlüssel:", self.out)

    def make(self):
        days = int(self.days.value())
        d = None if days == 0 else days
        key = make_license(self.product.currentText(), self.customer.text().strip() or "Kunde", d)
        self.out.setPlainText(key)

def main():
    app = QtWidgets.QApplication(sys.argv)
    w = Gen(); w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
