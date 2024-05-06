import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox
import sqlite3

class Film:
    def __init__(self, adi, yonetmen, tur):
        self.adi = adi
        self.yonetmen = yonetmen
        self.tur = tur

class FilmDiziServisi:
    def __init__(self):
        self.conn = sqlite3.connect("filmler.db")  # Veritabanına bağlan
        self.cursor = self.conn.cursor()
        self.create_table()  # Tabloyu oluştur

    def create_table(self):
        # Filmler tablosunu oluştur
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS filmler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                adi TEXT NOT NULL,
                yonetmen TEXT NOT NULL,
                tur TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def film_ekle(self, adi, yonetmen, tur):
        self.cursor.execute("INSERT INTO filmler (adi, yonetmen, tur) VALUES (?, ?, ?)", (adi, yonetmen, tur))
        self.conn.commit()

    def filmleri_listele(self):
        self.cursor.execute("SELECT adi FROM filmler")
        return [film[0] for film in self.cursor.fetchall()]

    def film_bilgisi_al(self, adi):
        self.cursor.execute("SELECT * FROM filmler WHERE adi=?", (adi,))
        film = self.cursor.fetchone()
        if film:
            return Film(film[1], film[2], film[3])
        else:
            return None

class FilmDiziUygulamasi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Film ve Dizi İzleme Servisi")
        self.servis = FilmDiziServisi()
        self.init_ui()

    def init_ui(self):
        self.label_adi = QLabel("Film Adı:")
        self.input_adi = QLineEdit()
        self.label_yonetmen = QLabel("Yönetmen:")
        self.input_yonetmen = QLineEdit()
        self.label_tur = QLabel("Tür:")
        self.input_tur = QLineEdit()
        self.button_film_ekle = QPushButton("Film Ekle")
        self.liste_filmler = QListWidget()
        self.button_izle = QPushButton("İzle")

        layout = QVBoxLayout()
        form_layout = QHBoxLayout()
        form_layout.addWidget(self.label_adi)
        form_layout.addWidget(self.input_adi)
        form_layout.addWidget(self.label_yonetmen)
        form_layout.addWidget(self.input_yonetmen)
        form_layout.addWidget(self.label_tur)
        form_layout.addWidget(self.input_tur)
        form_layout.addWidget(self.button_film_ekle)
        layout.addLayout(form_layout)
        layout.addWidget(self.liste_filmler)
        layout.addWidget(self.button_izle)

        self.setLayout(layout)

        self.button_film_ekle.clicked.connect(self.film_ekle)
        self.button_izle.clicked.connect(self.film_izle)

        self.liste_filmler.addItems(self.servis.filmleri_listele())

    def film_ekle(self):
        adi = self.input_adi.text()
        yonetmen = self.input_yonetmen.text()
        tur = self.input_tur.text()
        self.servis.film_ekle(adi, yonetmen, tur)
        self.liste_filmler.addItem(adi)

    def film_izle(self):
        secili_item = self.liste_filmler.currentItem()
        if secili_item:
            secili_film_adi = secili_item.text()
            secili_film = self.servis.film_bilgisi_al(secili_film_adi)
            if secili_film:
                self.izleme_penceresini_goster(secili_film)
            else:
                QMessageBox.warning(self, "Hata", "Seçilen film bulunamadı.")
        else:
            QMessageBox.warning(self, "Hata", "İzlemek için bir film seçiniz.")

    def izleme_penceresini_goster(self, film):
        izleme_mesaji = f"Film Adı: {film.adi}\nYönetmen: {film.yonetmen}\nTür: {film.tur}\n\n{film.adi} izleniyor..."
        QMessageBox.information(self, "İzle", izleme_mesaji)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    uygulama = FilmDiziUygulamasi()
    uygulama.show()
    sys.exit(app.exec_())
