import solarSystem
from Formulas import Formulas
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np
import sys
import math


a = 0

def update():
    global wid, sun, global_time
    global_time += 0.31
    sun.animate(global_time)

class Orbit:
    def __init__(self, _orbit_a: float, _orbit_e: float, _w: gl.GLViewWidget):
        self.__a = _orbit_a
        self.__e = _orbit_e
        self.__pts = Formulas.get_ellipse_pts_shifted(_orbit_a, _orbit_e)
        self.__psi = 0
        self.__theta = 0
        self.__phi = 0

        plt = gl.GLLinePlotItem(pos=self.__pts, color=(1, 0, 1, 1), width=2)
        self.__plt = plt
        _w.addItem(plt)
        # TODO: где-то здесь учесть, что еще повороты есть



if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseDesktopOpenGL)
    app = QtWidgets.QApplication(sys.argv)
    wid = gl.GLViewWidget()
    wid.showMaximized()

    oyz = gl.GLGridItem()
    oyz.rotate(90, 0, 1, 0)
    oyz.translate(-10, 0, 0)
    wid.addItem(oyz)
    oxz = gl.GLGridItem()
    oxz.rotate(90, 1, 0, 0)
    oxz.translate(0, -10, 0)
    wid.addItem(oxz)

    oxy = gl.GLGridItem()
    oxy.translate(0, 0, -10)
    wid.addItem(oxy)

    global_phi = 0
    global_psi = 0
    global_theta = 0

    global_phi_max = 30
    global_psi_max = 50
    global_theta_max = 70
    global_angle_degree_step = 1

    sun = solarSystem.sun()

    orb = Orbit(_orbit_a=10, _orbit_e=0.8, _w=wid)

    size = QtGui.QVector3D(10, 10, 10)
    axis = gl.GLAxisItem(size, antialias=False)
    wid.addItem(axis)

    sun.draw(wid)

    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(50)

    global_time = 0

    sys.exit(app.exec_())
