from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QScrollArea, QSizePolicy, QComboBox, QMenu, \
    QAction, QStyle, QApplication, QFileDialog, QGridLayout, QPushButton, QListView, QMessageBox
from PyQt5.QtGui import QPixmap, QPalette, QColor, QMouseEvent, QImage, QPainter, QTransform, QIcon, QFont
from PyQt5.QtCore import Qt, pyqtSignal, QPoint
from .Network import Fetcher, Anime
import os


class AnimeScrollView(QScrollArea):

    clicked = pyqtSignal(Anime)

    def __init__(self, theme, json):
        super(AnimeScrollView, self).__init__()

        self.setObjectName("AnimeScrollView")
        self.fontColor = ""
        self.mainBackgroundColor = ""
        self.altBackgroundColor = ""

        self.widget = QWidget()
        self.animeLabels = []
        self.layout = QGridLayout(self.widget)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.widget)
        self.setWidgetResizable(True)
        self.setGeometry(0, 0, 400, 138)
        self.setFixedHeight(138)
        self.verticalScrollBar().setSingleStep(138)
        self.hide()

        self.errorLabel = QLabel(self.widget)
        self.errorLabel.setAlignment(Qt.AlignCenter)
        self.errorLabel.hide()
        self.error = None

        self.theme = theme
        self.json = json
        self.setTheme(theme)

    def setTheme(self, theme):
        self.theme = theme
        self.setStyleSheet(f"QWidget#AnimeScrollView{{background-color:{theme.mainBackgroundColor};}}")
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(theme.mainBackgroundColor))
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        self.errorLabel.setStyleSheet(
            f"QLabel{{color: {self.theme.fontColor}; background-color: {self.theme.altBackgroundColor}; font: 13pt \"Rubik\";}}")
        for animeLabel in self.animeLabels:
            animeLabel.setTheme(theme)

    def setText(self, json):
        self.json = json
        if self.error:
            self.errorLabel.setText(json.get(self.error.name))

    def fill(self, animes):
        for i in reversed(range(self.layout.count())):
            widget_to_remove = self.layout.itemAt(i).widget()
            self.layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)
        self.animeLabels.clear()
        for index, anime in enumerate(animes):
            column_span = 1
            if index == len(animes) - 1 and len(animes) % 2 != 0:
                column_span = 2
            self.animeLabels.append(AnimeLabel(anime, self.theme))
            self.animeLabels[-1].labelClicked.connect(self.onClick)
            self.layout.addWidget(self.animeLabels[-1], index // 2, index % 2, 1, column_span)
        self.show()

    def onError(self, error):
        self.fill(list())
        self.error = error
        self.errorLabel.setParent(self.widget)
        self.errorLabel.setText(self.json.get(self.error.name, "Unknown error"))
        self.errorLabel.show()
        self.layout.addWidget(self.errorLabel)
        self.show()

    def onClick(self, anime):
        self.clicked.emit(anime)


class AnimeLabel(QWidget):
    labelClicked = pyqtSignal(Anime)

    def __init__(self, anime: Anime, theme):
        super(AnimeLabel, self).__init__()

        self.setAutoFillBackground(True)

        self.anime = anime
        self.theme = theme

        self.layout = QHBoxLayout()

        self.image = QPixmap()
        self.image.loadFromData(self.anime.largeDataImage)
        self.image = self.image.scaledToHeight(50, Qt.SmoothTransformation)
        self.imLabel = QLabel()
        self.imLabel.setPixmap(self.image)
        self.imLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)

        self.titleLabel = QLabel(self)
        self.titleLabel.setWordWrap(True)
        self.titleLabel.setTextFormat(Qt.RichText)
        title = self.anime.title
        if len(title) > 48:
            title = title[:46] + "..."
        self.titleLabel.setText(
            f"""<html><body><p align="center"><b>{title}</b></p></body></html>""")
        self.titleLabel.setAlignment(Qt.AlignVCenter)

        self.layout.addWidget(self.imLabel)
        self.layout.addWidget(self.titleLabel)
        self.setLayout(self.layout)

        self.setTheme(self.theme)

    def setTheme(self, theme):
        self.theme = theme
        color, bg_color = 'black' if self.theme.name == 'light' else 'white', 'white' if self.theme.name == 'light' else 'black'
        self.setStyleSheet(f"QToolTip{{background-color:{bg_color};color:{color};border: 1px solid {color}}}")
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(theme.mainBackgroundColor))
        self.setPalette(palette)
        if len(self.anime.title) > 48:
            self.setToolTip(f"<p style='white-space:pre'>{self.anime.title} ({self.anime.seasonYear})</p>")

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.labelClicked.emit(self.anime)
        elif event.button() == Qt.RightButton:
            self.menu = QMenu()
            save = QAction("Save the image")
            save.setIcon(QApplication.style().standardIcon(QStyle.SP_ArrowDown))
            self.menu.addAction(save)
            action = self.menu.exec_(self.mapToGlobal(event.pos()))
            if action == save:
                if self.anime.extraLargeDataImage:
                    return self.dialogSave(self.anime.extraLargeDataImage)
                if self.anime.extraLargeImage:
                    fetcher = Fetcher()
                    fetcher.get_image(self.anime.extraLargeImage, self.dialogSave)
                else:
                    return self.dialogSave(self.anime.largeDataImage)

    def dialogSave(self, data):
        if not data:
            data = self.anime.largeImage
        image = QImage.fromData(data)
        if image.height() < 512:
            image = image.scaledToHeight(512, Qt.SmoothTransformation)
        size = image.height()

        new_image = QImage(size, size, QImage.Format_ARGB32)
        margin = (size - image.width()) / 2
        start = QPoint(margin, 0)
        painter = QPainter(new_image)
        painter.setRenderHints(QPainter.HighQualityAntialiasing | QPainter.SmoothPixmapTransform, True)
        painter.drawImage(start, image)
        painter.end()
        filename = QFileDialog.getSaveFileName(self, "Save the image",
                                               os.path.join(os.getcwd(), f"{self.anime.id}.png"))
        if filename:
            new_image.save(filename[0])

    def leaveEvent(self, event):
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(self.theme.mainBackgroundColor))
        self.setPalette(palette)

    def enterEvent(self, event):
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(self.theme.altBackgroundColor))
        self.setPalette(palette)


class WebsiteComboBox(QComboBox):
    def __init__(self, translate, theme):
        super(WebsiteComboBox, self).__init__()
        self.insertItem(0, "Anime Digital Network")
        self.insertItem(1, "Crunchyroll")
        self.insertItem(2, "Wakanim")
        self.insertItem(3, translate["other"])
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.json = translate
        self.theme = theme
        self.setTheme(self.theme)
        self.setText(self.json)
        self.setCurrentIndex(4)

    def setTheme(self, theme):
        self.theme = theme
        self.setStyleSheet(
            f"QComboBox {{color: {self.theme.fontColor};background: {self.theme.altBackgroundColor};padding: 5px 5px 5px 5px; border: 1px solid {self.theme.mainBackgroundColor};border-radius: "
            "3px;}QComboBox::drop-down{width: 30px;border-left-width: 1px;border-left-color: "
            f"{theme.mainBackgroundColor};border-left-style: {self.theme.fontColor} solid;}}QComboBox::down-arrow{{image: url("
            f"data/ressources/expand{'white' if self.theme.name == 'dark' else ''}.png);width: 16px;height: 16px;}}"
            f"QAbstractItemView {{border: 1px solid {theme.fontColor}; color: {self.theme.fontColor}; background-color: "
            f"{self.theme.altBackgroundColor};selection-background-color: #FF0000; outline: 0px;}}"
        )
        view = QListView(self)
        font = QFont()
        font.setPointSize(13)
        font.setFamily("Rubik")
        view.setStyleSheet(f""" 
                                                 QListView::item:selected, QListView::item:hover {{                 
                                                 color: {self.theme.fontColor};
                                                 background-color: {self.theme.mainBackgroundColor}}}
                                                """)
        view.setFont(font)
        self.setView(view)
        self.setFont(font)

    def setText(self, json):
        self.json = json
        self.lineEdit().setPlaceholderText(json["select website"])


class EpisodeComboBox(QWidget):
    def __init__(self, translate, theme):
        super(EpisodeComboBox, self).__init__()
        self.layout = QGridLayout()

        self.combo = QComboBox()
        self.layout.addWidget(self.combo, 0, 0, 2, 1)
        self.combo.currentIndexChanged.connect(self.onSelect)

        self.previous = QPushButton()
        self.previous.clicked.connect(lambda event: self.move(-1))
        self.previous.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.layout.addWidget(self.previous, 1, 1)

        self.next = QPushButton()
        self.next.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.next.clicked.connect(lambda event: self.move(1))
        self.layout.addWidget(self.next, 0, 1)

        self.setLayout(self.layout)

        self.max, self.counter = 0, 1
        self.setText(translate)
        self.setTheme(theme)

    def setText(self, translate):
        self.translate = translate
        for i in range(1, self.max+1):
            self.combo.setItemText(i, f"{self.translate['episode'].capitalize()} {i}")

    def setTheme(self, theme):
        self.theme = theme
        image = QPixmap(fr"data\ressources\expand{'' if theme.name == 'light' else 'white'}.png")
        self.next.setIcon(QIcon(image.transformed(QTransform().scale(1, -1))))
        self.previous.setIcon(QIcon(image))
        for button in {self.next, self.previous}:
            button.setStyleSheet("    QPushButton{\n"
                                           f"    background: {theme.altBackgroundColor};\n"
                                           f"    border: {theme.mainBackgroundColor};\n"
                                           "    border-radius: 10px;\n"
                                           "    padding: 2 7px;\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:hover{\n"
                                           f"    background: {theme.altBackgroundColor};\n"
                                           f"    border: {theme.mainBackgroundColor};\n"
                                           "}")
        self.combo.setStyleSheet(
            f"QComboBox {{color: {self.theme.fontColor};background: {self.theme.altBackgroundColor};padding: 5px 5px 5px 5px; border: 1px solid {self.theme.mainBackgroundColor};border-radius: "
            "3px;}QComboBox::drop-down{width: 30px;border-left-width: 1px;border-left-color: "
            f"{theme.mainBackgroundColor};border-left-style: {self.theme.fontColor} solid;}}QComboBox::down-arrow{{image: url("
            f"data/ressources/expand{'white' if self.theme.name == 'dark' else ''}.png);width: 16px;height: 16px;}}"
            f"QAbstractItemView {{border: 1px solid {theme.fontColor}; color: {self.theme.fontColor}; background-color: "
            f"{self.theme.altBackgroundColor};selection-background-color: #FF0000; outline: 0px;}}"
        )
        view = QListView(self.combo)
        font = QFont()
        font.setPointSize(13)
        font.setFamily("Rubik")
        view.setStyleSheet(f""" 
                                         QListView::item:selected, QListView::item:hover {{                 
                                         color: {self.theme.fontColor};
                                         background-color: {self.theme.mainBackgroundColor}}}
                                        """)
        view.setFont(font)
        self.combo.setView(view)
        self.combo.setFont(font)

    def move(self, direction):
        self.counter += direction
        if self.counter > self.max:
            self.counter = 1
        elif self.counter < 1:
            self.counter = self.max
        self.combo.setCurrentIndex(self.counter - 1)

    def onSelect(self, index):
        self.counter = index + 1

    def init(self, maximum):
        self.counter = 1
        if maximum > self.max:
            for i in range(self.max + 1, maximum + 1):
                self.combo.addItem(f"{self.translate['episode'].capitalize()} {i}")
        elif maximum < self.max:
            for i in range(self.max - 1, maximum - 1, -1):
                self.combo.removeItem(i)
        self.max = maximum


class WarningMessage(QMessageBox):

    def __init__(self, data):
        super(WarningMessage, self).__init__()
        self.setIcon(QMessageBox.Warning)
        self.setWindowTitle(data["warning"])
        self.setText(data["id change"])
        self.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        icon = QIcon(QPixmap("data/ressources/letters.png"))
        self.setWindowIcon(icon)

    def changeText(self, lang):
        self.setWindowTitle(lang["warning"])
        self.setText(lang["id change"])
