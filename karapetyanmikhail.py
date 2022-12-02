# URL GitHub: https://github.com/mIKIII77/R3.09-Examen
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import threading
import time
import socket



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        self.setWindowTitle("Chronomètre")
        self.setGeometry(100, 100, 400, 300)

        #Items 
        self.label1 = QLabel("Compteur :")
        self.time = QLineEdit("0")
        self.time.setPlaceholderText("0")
        self.time.setReadOnly(True)
        self.start = QPushButton("Start")
        self.stop = QPushButton("Stop")
        self.reset = QPushButton("Reset")
        self.connect = QPushButton("Connect")
        self.quit = QPushButton("Quitter")
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.timer = TimerThread(self.time, self.client)

        #Layout
        grid.addWidget(self.label1, 0, 0, 1, 1)
        grid.addWidget(self.time, 1, 0, 1, 2)
        grid.addWidget(self.start, 2, 0,1, 2)
        grid.addWidget(self.reset, 3, 0, 1, 1)
        grid.addWidget(self.stop, 3, 1, 1, 1)
        grid.addWidget(self.connect, 4, 0)
        grid.addWidget(self.quit, 4, 1)

        #Events
        self.start.clicked.connect(self.__start)
        self.stop.clicked.connect(self.__stop)
        self.reset.clicked.connect(self.__reset)
        self.quit.clicked.connect(self.__close)
        self.connect.clicked.connect(self.__connect)


    def __start(self):
        try:
            self.client.send("Start pressed".encode())
            self.timer.start()
        except:
            self.timer.start()

    def __stop(self):
        try: 
            self.client.send("Stop pressed".encode())
            self.timer.terminate()
        except:
            self.timer.terminate()

    def __reset(self):
        try:
            self.client.send("Reset pressed".encode())
            self.timer.reset()
        except:
            self.time.setText("0")

    def __close(self):
        if self.timer.isRunning():
            self.timer.terminate()
            self.client.send("bye".encode())
            self.close()
        else:
            self.client.send("bye".encode())
            self.close()

    def __connect(self):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(("localhost", 10003))
            self.client.send("Hello server".encode())
            return self.client
        except: # If the server is not running - Exception
            QMessageBox.warning(self, "Erreur", "Impossible de se connecter au serveur")

        

class TimerThread(QThread):
    def __init__(self, time, client):   
        super().__init__()
        self.time = time


    def run(self):
        while True:
            time.sleep(1)
            self.time.setText(str(int(self.time.text()) + 1))
            try:
                self.client.send(str(self.time.text()).encode())
            except:
                pass
        
def main():
    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec_()

if __name__ == "__main__":
    main()

