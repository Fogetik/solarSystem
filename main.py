import solarSystem
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
import pyqtgraph.opengl as gl
import sys


def update():
    global wid, sun, global_time
    global_time += 1
    sun.animate(global_time)


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

    size = QtGui.QVector3D(10, 10, 10)
    axis = gl.GLAxisItem(size, antialias=False)
    wid.addItem(axis)

    sun.draw(wid)

    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(50)

    global_time = 0

    sys.exit(app.exec_())
