from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np
import sys
import math


class sun:
    def __init__(self):
        self.radius = 4
        self.child = []

    def draw(self, wid_ptr: gl.GLViewWidget):
        self.md = gl.MeshData.sphere(rows=10, cols=20, radius=self.radius)

        self.m1 = gl.GLMeshItem(
            meshdata=self.md,
            smooth=False,
            color=(1, 1, 0, 0.2),
            shader="balloon",
            glOptions="additive",
        )
        self.m1.translate(0, 0, 0)

        wid_ptr.addItem(self.m1)

    def animate(self, coor: float):
        self.m1.translate(coor, coor, coor)

