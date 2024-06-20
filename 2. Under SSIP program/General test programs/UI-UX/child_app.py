import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

class ChildApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        label = QLabel("This is the child app", self)
        layout.addWidget(label)
        
        self.setLayout(layout)
        self.setWindowTitle('Child App')
        self.setGeometry(100, 100, 700, 400)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    child_app = ChildApp()
    sys.exit(app.exec_())
    