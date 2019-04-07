# -*- coding: utf-8 -*-
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
from numpy import arange, sin, cos, pi
import pyqtgraph as pg
import sys
import pandas as pd
from datetime import datetime


class TimeAxisItem(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        return [datetime.fromtimestamp(value) for value in values]
    


class Plot2D():
    def __init__(self):
        self.traces = dict()

        #QtGui.QApplication.setGraphicsSystem('raster')
        self.app = QtGui.QApplication([])
        #mw = QtGui.QMainWindow()
        #mw.resize(800,800)

        self.win = pg.GraphicsWindow(title="Basic plotting examples")
        self.win.resize(2000,600)
        self.win.setWindowTitle('pyqtgraph example: Plotting')

        # Enable antialiasing for prettier plots
        pg.setConfigOption('background', 'w')
        pg.setConfigOptions(antialias=True,crashWarning=True,exitCleanup=True)
        date_axis = TimeAxisItem(orientation='bottom')
        self.canvas = self.win.addPlot(title="Opinnäyte", axisItems = {'bottom': date_axis})
        self.canvas.showGrid(x = True, y = True, alpha = 0.3)
        self.canvas.setXRange(range_min, range_max, padding=0.1)
        self.canvas.setYRange(0, 100, padding=0.2)

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def trace(self,name,dataset_x,dataset_y):
        if name in self.traces:
            self.traces[name].setData(x=dataset_x,y=dataset_y)
            if dataset_y[-1] > 50:
                #self.canvas.plot(dataset_x[-1],dataset_y[-1], pen=(255,0,0))
                self.traces[name].setPen(pg.mkPen('r', width=1.5))
            else:
                self.traces[name].setPen(pg.mkPen('g', width=1.5))
            
        else:
            self.traces[name] = self.canvas.plot(pen=pg.mkPen('g', width=1.5))
            

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    i = 0
    count = 0
    df = pd.read_csv('C:\\Users\\Robban\\Jupyter\\MOCK_DATA.csv', sep=';')
    #df['time'] = pd.to_datetime(df['time'])
    df = df.sort_values(by='time')
    pct = df["allas"].rolling(window=20).mean()
    #df.index.day
    #pct = np.arange(0, 1000, 0.1)
    #amplitude = np.sin(time)
    #list_y = amplitude
    #sort = time.sort_values(ascending=True)
    time = pd.to_datetime(df['time'])
    range_min = time[0].timestamp()
    range_max = time[999].timestamp()
    p = Plot2D()
    #list_x = time
    #print(sort[1],sort[2],sort[3])
   
    a = 0
    b = []
    d = []
    
    def update():
        global p, i, count, pct, a, time, list_y, list_x, b, d, df
        if a < 1000:
#             j = pct.iloc[[a]]
#             print(g,j)
#             a += 1
            t = np.arange(0,100,0.1)
            s = sin(2 * pi * t + i)
            #c = cos(2 * pi * t + i)
            b.append(time[a].timestamp())
            #print(a)
            #print(b)
            d.append(pct[a])
            #print(b)
            count +=1
            p.trace("allas",b,d)
            #p.trace("cos",t,c,count)
            i += 0.1
            a += 1

    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(30)

    p.start()
