import sys
import urllib.request
import threading
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QApplication, QLabel, QStatusBar, QFrame)
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from GuildWars2 import GuildWars2
from Buttons import ImageButton


# Error Reporting
def my_excepthook(type, value, tback):
    sys.__excepthook__(type, value, tback)

sys.excepthook = my_excepthook


class SignalConnector(QtCore.QObject):
    signal = QtCore.pyqtSignal(dict, name="apisignal")


class GW2GUI(QWidget):

    # Primary Constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet(open("style.qss", "r").read())
        self.setAutoFillBackground(True)
        self.gw2object = GuildWars2()
        self.grid = QGridLayout()
        self.grid.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        self.menugrid = QGridLayout()
        self.menugrid.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        self.sidemenugrid = QGridLayout()
        self.sidemenugrid.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        self.detailsgrid = QGridLayout()
        self.sidemenugrid.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
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
        self._initprofessions()
        self.move(300, 150)
        self.setWindowTitle('Guild Wars 2')
        self.show()

    # Create buttons for each profession
    def _initprofessions(self):
        buttonitems = self.gw2object.getallprofessions()
        i = 0
        for profession in buttonitems:
            self._addimagebutton(self.grid, profession['name'], profession['url'], self.clickprofession, 1, i)
            self._addlabel(self.grid, profession['name'], 2, i)
            i += 1

    # Set profession
    def _setprofession(self, name):
        self.grid.removeItem(self.menugrid)
        self.grid.removeItem(self.sidemenugrid)
        self.grid.removeItem(self.detailsgrid)
        self._clearlayout(self.menugrid)
        self._clearlayout(self.sidemenugrid)
        self._clearlayout(self.detailsgrid)
        self.statusbar.showMessage("Loading " + name + "....")
        connector = SignalConnector()
        connector.signal.connect(self._displayprofession)
        professionthread = threading.Thread(target=self._threadprofession, args=(connector, name))
        professionthread.start()

    # Set option and display menu for either weapons or specializations
    def _setoption(self, option):
        self.grid.removeItem(self.sidemenugrid)
        self.grid.removeItem(self.detailsgrid)
        self._clearlayout(self.sidemenugrid)
        self._clearlayout(self.detailsgrid)
        self.selectedoption = option
        if option == "Weapons":
            self.statusbar.showMessage("Loading weapons....")
        else:
            self.statusbar.showMessage("Loading specialization....")
        optionconnector = SignalConnector()
        optionconnector.signal.connect(self._displayoptions)
        optionthread = threading.Thread(target=self._threadoption, args=(optionconnector,))
        optionthread.start()

    # Set the weapon or specialization clicked with traits and
    def _setweaponspec(self, weaponspec):
        self.grid.removeItem(self.detailsgrid)
        self._clearlayout(self.detailsgrid)
        self._selectedweaponspec = weaponspec
        if self.selectedoption == "Weapons":
            self.statusbar.showMessage("Loading weapon skills....")
        else:
            self.statusbar.showMessage("Loading specialization traits....")
        connector = SignalConnector()
        connector.signal.connect(self._displayweaponspec)
        weaponspecthread = threading.Thread(target=self._threadweaponspec, args=(connector,))
        weaponspecthread.start()

    # Threaded function for profession
    def _threadprofession(self, connector, name):
        self.gw2object.setprofession(name)
        connector.signal.emit({})

    # Threaded function for weapons and specializations
    def _threadoption(self, optionconnector):
        if self.selectedoption == "Weapons":
            returndata = self.gw2object.getweapons()
        else:
            returndata = self.gw2object.getspecializations()
        optionconnector.signal.emit(returndata)

    # Threaded function for weapon skills
    def _threadweaponspec(self, connector):
        if self.selectedoption == "Weapons":
            returndata = self.gw2object.getweapons()
        else:
            returndata = self.gw2object.getspecializations()
        connector.signal.emit(returndata)

    # Display profession options
    def _displayprofession(self):
        self._addbutton(self.menugrid, "Weapons", self.clickoption, 1, 0, 1, 4)
        self._addbutton(self.menugrid, "Specializations", self.clickoption, 1, 5, 1, 4)
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        self.menugrid.addWidget(divider)
        self.grid.addLayout(self.menugrid, 3, 0, 1, 9)
        self.statusbar.showMessage("Ready....Weapon or Specializations?")

    # Display weapons or specializations
    def _displayoptions(self, data):
        i = 4
        for item in sorted(data.keys()):
            self._addbutton(self.sidemenugrid, item, self.clickweaponspec, i, 1)
            i += 1
        self.grid.addLayout(self.sidemenugrid, 4, 0, 1, 1)
        self.statusbar.showMessage("Ready....Choose an option to display it's skills")

    # Display skills/traits of selected weapon/specialization
    def _displayweaponspec(self, data):
        h = 0
        v = 1
        for element in data[self._selectedweaponspec]:
            image = self._getimage(element['url'])
            self._addimage(self.detailsgrid, element['tooltip'], image, v, h)
            self._addlabel(self.detailsgrid, element['name'], v + 1, h)
            if h == 3:
                h = 0
                v += 2
            else:
                h += 1
        self.grid.addLayout(self.detailsgrid, 4, 1, 1, 8)
        self.statusbar.showMessage("Ready....")

    """
        ~~~~~  STATIC METHODS  ~~~~~

    """
    # Retrieve image from a url
    @staticmethod
    def _getimage(imageurl):
        return urllib.request.urlopen(imageurl).read()

    # Add a new image to grid
    @staticmethod
    def _addimage(grid, tooltip, data, v, h):
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        icon = QLabel()
        icon.setPixmap(pixmap)
        icon.setAlignment(QtCore.Qt.AlignHCenter)
        icon.setToolTip(tooltip)
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
    def clickprofession(self):
        profession = self.sender().getName()
        self._setprofession(profession)

    # Click event for each option
    def clickoption(self):
        option = self.sender().text()
        self._setoption(option)

    # Click event for each weapon or specialization
    def clickweaponspec(self):
        weaponspec = self.sender().text()
        self._setweaponspec(weaponspec)


def main():
        app = QApplication(sys.argv)
        ex = GW2GUI()
        ex.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    main()

