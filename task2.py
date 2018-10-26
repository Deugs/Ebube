

import PyQt4.QtGui as gui
import PyQt4.QtCore as qt
import sys
import numpy as np
from scipy.optimize import curve_fit

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


header = sys.path[0]+'\\'#source path

class Window(gui.QWidget):
    def __init__(self, parent = None):
        gui.QWidget.__init__(self,parent)
        self.setGeometry(280,80,890,620)
        self.setMaximumSize(890,620)
        self.setMinimumSize(890,620)
        self.setWindowTitle('Automation Lab - Task 2')
        
        self.w = gui.QWidget()
        self.w.resize(320, 240)
        self.w.setWindowTitle("Select Line Data File")
        
        self.gradient = None
        self.intercept = None
        self.y_predict = None
        
        self.createButtons()
         
    def select_file(self):
        filename = gui.QFileDialog.getOpenFileName(self.w, 'Open File', header)
        self.txtPath.setText(filename)
        
    def createButtons(self):
        self.layout = gui.QGridLayout()
        
        self.gbPlot = gui.QGroupBox("PLOTS")
        self.plotLayout = gui.QGridLayout()
        
        self.gbTable = gui.QGroupBox("DATA")
        self.tableLayout = gui.QGridLayout()
        
        self.gbRange = gui.QGroupBox("...")
        self.rangeLayout = gui.QGridLayout()
        
        self.lblPath = gui.QLabel("Path")
        self.txtPath = gui.QLineEdit(header+"line.txt")
        self.btnSelect = gui.QPushButton("File")
        self.btnSelect.clicked.connect(self.select_file)
        
        self.lblXmin = gui.QLabel('X-min')
        self.txtXmin = gui.QDoubleSpinBox()
        self.txtXmin.setRange(-100000,100000)
        self.txtXmin.setSingleStep(0.01)
        self.txtXmin.setValue(0)
        self.lblXmax = gui.QLabel('X-max')
        self.txtXmax = gui.QDoubleSpinBox()
        self.txtXmax.setRange(-100000,100000)
        self.txtXmax.setSingleStep(0.01)
        self.txtXmax.setValue(100)
        
        self.lblSlope = gui.QLabel('Estimated Slope')
        self.txtSlope = gui.QLabel()
        self.bluepalette = gui.QPalette()
        c=gui.QColor(50,100,200,255)
        self.bluepalette.setColor(gui.QPalette.Foreground,c)
        self.txtSlope.setFont(gui.QFont('SansSerif', 18))
        self.txtSlope.setPalette(self.bluepalette)
        
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.btn = gui.QPushButton('Plot')
        self.btn.clicked.connect(self.plot)
        
        self.tblData = gui.QTableWidget()
        self.tblData.setRowCount(5)
        self.tblData.setColumnCount(2)
        self.tblData.setHorizontalHeaderLabels(qt.QString("X-Data,Y-Data").split(','))
        self.tblData.show()
        
        hbox = gui.QHBoxLayout()
        hbox.addWidget(self.lblPath)
        hbox.addWidget(self.txtPath)
        hbox.addWidget(self.btnSelect)
        vbox = gui.QVBoxLayout()
        vbox.addLayout(hbox)
        self.layout.addLayout(vbox,0,0)
        
        vbox1 = gui.QVBoxLayout()
        vbox1.addWidget(self.lblXmin)
        vbox1.addWidget(self.txtXmin)
        vbox2 = gui.QVBoxLayout()
        vbox2.addWidget(self.lblXmax)
        vbox2.addWidget(self.txtXmax)
        vbox3 = gui.QVBoxLayout()
        vbox3.addWidget(self.lblSlope)
        vbox3.addWidget(self.txtSlope)
        hbox = gui.QHBoxLayout()
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)
        hbox.addLayout(vbox3)
        self.rangeLayout.addLayout(hbox,0,0)
        self.gbRange.setLayout(self.rangeLayout)
        self.layout.addWidget(self.gbRange,1,0)
        
        hbox = gui.QVBoxLayout()
        hbox.addWidget(self.toolbar)
        hbox.addWidget(self.canvas)
        hbox.addWidget(self.btn)
        vbox = gui.QHBoxLayout()
        vbox.addLayout(hbox)
        self.plotLayout.addLayout(vbox,0,0)
        self.gbPlot.setLayout(self.plotLayout)
        
        hbox = gui.QHBoxLayout()
        hbox.addWidget(self.tblData)
        vbox = gui.QVBoxLayout()
        vbox.addLayout(hbox)
        self.tableLayout.addLayout(vbox,0,0)
        self.gbTable.setLayout(self.tableLayout)
        
        hbox = gui.QHBoxLayout()
        hbox.addWidget(self.gbPlot)
        hbox.addWidget(self.gbTable)
        self.layout.addLayout(hbox,2,0)
        
        self.setLayout(self.layout)
    
    def error(self, msg):
        gui.QMessageBox.warning(self, 'Error', msg)

    def info(self, msg):
        gui.QMessageBox.information(self, 'Info', msg)
    
    def read_file(self):
        """read a file form source folder"""
        try:
            f = open(self.txtPath.text(), 'r')
            raw =  str(f.read())
            f.close()
            return raw
        except Exception as e:
            self.error("Please Select File Path To Read")
            return None
            
    def preprocess(self, data):
        """return a list of Y data from read file"""
        data = str(data)
        res = data.replace('[','')
        res = res.replace(']', '')
        res = res.replace(' ', '')
        res = res.split('\n')
        bn = []
        [bn.append(float(i)) for i in res]
        return bn
    
    def line(self, x, M, C):
        """line equation for fitting"""
        return M*x + C
    
    def plot(self):
        
        file_ = self.read_file()
        self.y_data = self.preprocess(file_)
        n = len(self.y_data)
        self.x_data = np.linspace(float(self.txtXmin.value()), float(self.txtXmax.value()), n)
        
        self.tblData.setRowCount(n)
        [self.tblData.setItem(i,0,gui.QTableWidgetItem(str(self.x_data[i]))) for i in range(n)]
        [self.tblData.setItem(i,1,gui.QTableWidgetItem(str(self.y_data[i]))) for i in range(n)]
        
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.clear()
        ax.hold(True)
        
        ax.scatter(self.x_data, self.y_data)
        ax.set_xlabel('x_data')
        ax.set_ylabel('y_data')
        ax.set_title('Slop Prediction')
        
        
        self.gradient, self.intercept = curve_fit(self.line, self.x_data, self.y_data)[0]
        #print 'curve_fit: '+str(self.gradient) +' '+str(self.intercept)
        self.txtSlope.setText(str(self.gradient))
        
        self.y_predict = self.line(self.x_data, self.gradient, self.intercept)
        ax.plot(self.x_data,self.y_predict,'r-', linewidth=2)
        
        ax.legend(['prediction','data'],loc='upper left',prop={'size':12})
        
        self.canvas.draw()
        
if __name__ == '__main__':
    app=gui.QApplication(sys.argv)
    
    win=Window()
    win.show()
    sys.exit(app.exec_())

