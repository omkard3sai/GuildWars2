import sys
import urllib.request
from operator import itemgetter
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QApplication, QLabel, QStatusBar)
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from GuildWars2 import GuildWars2
from Buttons import ImageButton


class GW2GUI(QWidget):

    # Primary Constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gw2object = GuildWars2()
        self.grid = QGridLayout()
        self.grid.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        self.sidemenugrid = QGridLayout()
        self.sidemenugrid.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        self.detailsgrid = QGridLayout()
        self.sidemenugrid.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.professionTitle = None
        self._initui()

    """

        ~~~~~  INTERNAL METHODS  ~~~~~

    """
    # Initial UI Constructor
    def _initui(self):
        self.statusbar = QStatusBar(self)
        self.grid.addWidget(self.statusbar, 0, 0, 1, 9)
        self.statusbar.showMessage("Ready....Choose a profession")
        self.setLayout(self.grid)
        self._initprofessionmenu()
        self.move(300, 150)
        self.setWindowTitle('Guild Wars 2')
        self.show()

    # Create buttons for each profession
    def _initprofessionmenu(self):
        buttonitems = self.gw2object.getallprofessions()
        i = 0
        for profession in buttonitems:
            image = self._getimage(profession['url'])
            self._addimagebutton(self.grid, profession['name'], profession['url'], self.professionbuttonclicked, 1, i)
            self._addlabel(self.grid, profession['name'], 2, i)
            i += 1

    # Initialize profession and it's options
    def _initprofession(self, name):
        self.grid.removeItem(self.sidemenugrid)
        self.grid.removeItem(self.detailsgrid)
        self._clearlayout(self.sidemenugrid)
        self._clearlayout(self.detailsgrid)
        self.statusbar.showMessage("Loading " + name + "....")
        self.gw2object.setprofession(name)
        self._addbutton(self.grid, "Weapons", self.weaponsmenuclicked, 3, 0, 1, 4)
        self._addbutton(self.grid, "Specializations", self.specsmenuclicked, 3, 5, 1, 4)
        self.statusbar.showMessage("Ready....Weapon or Specializations?")

    # Initialize weapons for current profession
    def _initweapons(self):
        self.statusbar.showMessage("Loading weapons....")
        self.grid.removeItem(self.sidemenugrid)
        self.grid.removeItem(self.detailsgrid)
        self._clearlayout(self.sidemenugrid)
        self._clearlayout(self.detailsgrid)
        self.grid.addLayout(self.sidemenugrid, 4, 0, 1, 1)
        self.grid.addLayout(self.detailsgrid, 4, 1, 1, 8)
        weapons = self.gw2object.getweapons()
        i = 4
        for weapon in sorted(weapons, key=itemgetter('name')):
            self._addbutton(self.sidemenugrid, weapon['name'], self.weaponbuttonclicked, i, 1)
            i += 1
        self.statusbar.showMessage("Ready....Choose a weapon")

    # Display weapon skills
    def _initweaponskills(self, name):
        self.statusbar.showMessage("Loading skills....")
        weapons = self.gw2object.getweapons()
        for weapon in weapons:
            if weapon['name'] == name:
                h = 0
                v = 1
                for skill in weapon['skills']:
                    image = self._getimage(skill['url'])
                    self._addimage(self.detailsgrid, image, v, h)
                    self._addlabel(self.detailsgrid, skill['name'], v + 1, h)
                    if h == 3:
                        h = 0
                        v += 2
                    else:
                        h += 1
        self.statusbar.showMessage("Ready....")

    # Initialize specializations for current profession
    def _initspecs(self):
        self.statusbar.showMessage("Loading specialization....")
        self.grid.removeItem(self.sidemenugrid)
        self.grid.removeItem(self.detailsgrid)
        self._clearlayout(self.sidemenugrid)
        self._clearlayout(self.detailsgrid)
        self.grid.addLayout(self.detailsgrid, 4, 0, 1, 9)
        specs = self.gw2object.getspecializations()
        i = 0
        for spec in sorted(specs, key=itemgetter('name')):
            image = self._getimage(spec['url'])
            self._addimage(self.detailsgrid, image, 4, i)
            self._addlabel(self.detailsgrid, spec['name'], 5, i)
            i += 1
        self.statusbar.showMessage("Ready....")

    """

            ~~~~~  STATIC AND CALSS METHODS  ~~~~~

    """
    # Class method to retrieve image from a url
    @classmethod
    def _getimage(cls, imageurl):
        return urllib.request.urlopen(imageurl).read()

    # Add a new image to grid
    @staticmethod
    def _addimage(grid, data, v, h):
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        icon = QLabel()
        icon.setPixmap(pixmap)
        icon.setAlignment(QtCore.Qt.AlignHCenter)
        grid.addWidget(icon, v, h)

    # Add a new image button to grid
    @staticmethod
    def _addimagebutton(grid, name, url, clickaction, v, h):
        button = ImageButton(name, url)
        button.clicked.connect(clickaction)
        grid.addWidget(button, v, h)

    # Add a new button to grid
    @staticmethod
    def _addbutton(grid, name, clickaction, v, h, r=None, c=None):
        button = QPushButton(str(name).title())
        button.clicked.connect(clickaction)
        if r is None:
            grid.addWidget(button, v, h)
        else:
            grid.addWidget(button, v, h, r, c)

    # Add label to grid
    @staticmethod
    def _addlabel(grid, text, v, h, r=None, c=None):
        label = QLabel()
        label.setAlignment(QtCore.Qt.AlignHCenter)
        label.setText(text)
        if r is None:
            grid.addWidget(label, v, h)
        else:
            grid.addWidget(label, v, h, r, c)

    # Remove all widgets in layout
    @staticmethod
    def _clearlayout(layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            widget.deleteLater()

    """

        ~~~~~  INTERFACE METHODS  ~~~~~

    """
    # Click event for each profession
    def professionbuttonclicked(self):
        sender = self.sender()
        self._initprofession(sender.getName())

    # Click event for weapons button
    def weaponsmenuclicked(self):
        self._initweapons()

    # Click event for specializations button
    def specsmenuclicked(self):
        self._initspecs()

    # Click event for each weapon
    def weaponbuttonclicked(self):
        weapon = self.sender().text()
        self._initweaponskills(weapon)

    # Click event for each specialization
    def specbuttonclicked(self):
        spec = self.sender().text()
        self._initspecializationskills(spec)


def main():
        app = QApplication(sys.argv)
        ex = GW2GUI()
        ex.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    main()

