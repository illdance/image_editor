from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QFileDialog
import os
from PIL import Image, ImageOps, ImageFilter
from PyQt5.QtGui import QPixmap

workdir = ''

class IamgeProcess():
    def __init__(self):
        self.filename = None
        self.image = None
        self.dir = None
        self.saveDir = 'Modified/'
    def loadImage(self, filename):
        self.filename = filename
        self.dir = workdir
        file_path = os.path.join(workdir, filename)
        self.image = Image.open(file_path)
    def showImage(self, path):
        pixmapimage = QPixmap(path)
        label_width, label_height = img_kartinka.width(), img_kartinka.height()
        scaled_pixmap = pixmapimage.scaled(label_width, label_height, Qt.KeepAspectRatio)
        img_kartinka.setPixmap(scaled_pixmap)
        img_kartinka.setVisible(True)
    def saveImage(self):
        path = os.path.join(workdir, self.saveDir)
        if not (
            os.path.exists(path)
            or os.path.isdir(path)
        ):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
    def do_cb(self):
        self.image = ImageOps.grayscale(self.image)
        self.saveImage()
        image_path = os.path.join(
            workdir, self.saveDir, self.filename
        )
        self.showImage(image_path)
    def do_levo(self):
        self.image =  self.image.rotate(-90)
        self.saveImage()
        image_path = os.path.join(
            workdir, self.saveDir, self.filename
        )
        self.showImage(image_path)
    def do_pravo(self):
        self.image = self.image.rotate(90)
        self.saveImage()
        image_path = os.path.join(
            workdir, self.saveDir, self.filename
        )
        self.showImage(image_path)
    def do_rezko(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(
            workdir, self.saveDir, self.filename
        )
        self.showImage(image_path)
    def do_zerk(self):
        self.image = ImageOps.mirror(self.image)
        self.saveImage()
        image_path = os.path.join(
            workdir, self.saveDir, self.filename
        )
        self.showImage(image_path)

workImage = IamgeProcess()

def showChosenImage():
    if img_kartinki.currentRow() >= 0:
        filename = img_kartinki.currentItem().text()
        workImage.loadImage(filename)
        image_path = os.path.join(workdir, filename)
        workImage.showImage(image_path)


def showFilenamesList():
    chooseWordir()
    extensions = ['.png', '.jpg', '.jpeg', '.gif', '.jfif']
    files = os.listdir(workdir)
    files = filter(files, extensions)
    img_kartinki.clear()
    img_kartinki.addItems(files)

def chooseWordir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
                break
    return result

prilojuha = QApplication([])
okno = QWidget()
okno.resize(700,500)

img_kartinka = QLabel('Картинка')
img_kartinki = QListWidget()
btn_papka =  QPushButton('Папка')
btn_levo = QPushButton('Лево')
btn_pravo = QPushButton('Право')
btn_zerkalo = QPushButton('Зеркально')
btn_rezko = QPushButton('Резко')
btn_chb = QPushButton('Ч/Б')
glav_lin = QHBoxLayout()
gor_lin = QHBoxLayout()
vert_lin = QVBoxLayout()
vert_lin0 = QVBoxLayout()

okno.setLayout(glav_lin)
glav_lin.addLayout(vert_lin)
glav_lin.addLayout(vert_lin0)
glav_lin.addWidget(img_kartinka)
glav_lin.addWidget(img_kartinki)
gor_lin.addWidget(btn_levo)
gor_lin.addWidget(btn_pravo)
gor_lin.addWidget(btn_zerkalo)
gor_lin.addWidget(btn_rezko)
gor_lin.addWidget(btn_chb)
vert_lin.addWidget(btn_papka)
vert_lin.addWidget(img_kartinki)
vert_lin0.addWidget(img_kartinka)
vert_lin0.addLayout(gor_lin)

img_kartinki.currentRowChanged.connect(showChosenImage)
btn_chb.clicked.connect(workImage.do_cb)
btn_levo.clicked.connect(workImage.do_levo)
btn_pravo.clicked.connect(workImage.do_pravo)
btn_rezko.clicked.connect(workImage.do_rezko)
btn_zerkalo.clicked.connect(workImage.do_zerk)

btn_papka.clicked.connect(showFilenamesList)
img_kartinki.currentRowChanged.connect(showChosenImage)

okno.show()
prilojuha.exec()