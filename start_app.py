import sys
from PyQt5.QtWidgets import QApplication
from MainQt import UserInterface

app = QApplication(sys.argv)
win = UserInterface()
win.show()
sys.exit(app.exec_())
