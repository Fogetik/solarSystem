from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np
import sys
import math

from Formulas import Formulas


def rotate_x(coor_y, coor_z, angle: float):
    coor_y_cpy = coor_y
    coor_z_cpy = coor_z
    coor_y = coor_y_cpy * math.cos(angle) - coor_z_cpy * math.sin(angle)
    coor_z = coor_y_cpy * math.sin(angle) + coor_z_cpy * math.cos(angle)
    return coor_y, coor_z

def rotate_y(coor_x, coor_z, angle: float):
    coor_x_cpy = coor_x
    coor_z_cpy = coor_z
    coor_x = coor_x_cpy * math.cos(angle) + coor_z_cpy * math.sin(angle)
    coor_z = -coor_x_cpy * math.sin(angle) + coor_z_cpy * math.cos(angle)
    return coor_x, coor_z

def rotate_z(coor_x, coor_y, angle: float):
    coor_x_cpy = coor_x
    coor_y_cpy = coor_y
    coor_x = coor_x_cpy * math.cos(angle) - coor_y_cpy * math.sin(angle)
    coor_y = coor_x_cpy * math.sin(angle) + coor_y_cpy * math.cos(angle)
    return coor_x, coor_y


class sun:
    def __init__(self):
        self.radius = 4
        self.earth_planet = Earth()




    def draw(self, wid_ptr: gl.GLViewWidget):
        self.md = gl.MeshData.sphere(rows=10, cols=20, radius=self.radius)

        self.m1 = gl.GLMeshItem(
            meshdata=self.md,
            smooth=True,
            color=(1, 1, 0, 0.2),
            shader="balloon",
            glOptions="additive",
        )
        # self.m1.translate(self.coor_x, self.coor_y, self.coor_z)
        wid_ptr.addItem(self.m1)
        self.earth_planet.draw(wid_ptr)


    def animate(self, time: int):
        self.m1.rotate(-1, 0, 1, 1)
        self.earth_planet.animate(time)


class Earth:
    def __init__(self):
        self.angle_degree_step = 1
        self.radius = 2

        self.coor_x = 0
        self.coor_y = 10
        self.coor_z = 0

        self.global_phi = 15
        self.global_psi = 15
        self.global_theta = 20

        self.moon = Moon()

    def draw(self, wid_ptr: gl.GLViewWidget):
        self.md = gl.MeshData.sphere(rows=10, cols=20, radius=self.radius)
        self._pts = self.md.vertexes()
        self.m1 = gl.GLMeshItem(
            meshdata=self.md,
            smooth=False,
            color=(0, 1, 0, 0.2),
            shader="balloon",
            glOptions="additive",
        )
        self._pts = np.add(self._pts, [0, 10, 0])
        self.md.setVertexes(self._pts)
        wid_ptr.addItem(self.m1)
        self.moon.draw(wid_ptr)

    def animate(self, _time):
        _angle = self.angle_degree_step * _time
        _psi_rad = math.radians(self.global_psi)
        _theta_rad = math.radians(self.global_theta)
        _phi_rad = math.radians(self.global_phi)
        pts = np.dot(self._pts, Formulas.get_rot_mat('z', math.radians(_angle)))
        rot_mat = Formulas.get_3d_rot_mat(_psi_rad=_psi_rad, _theta_rad=_theta_rad, _phi_rad=_phi_rad)
        pts = np.dot(pts, rot_mat)
        self.md.setVertexes(pts)
        self.m1.setMeshData(meshdata=self.md)
        self.moon.animate(_time, pts[0][0], pts[0][1], pts[0][2])


class Moon:
    def __init__(self):
        self.angle_degree_step = 2.25
        self.radius = 1

        self.global_phi = 30
        self.global_theta = 20
        self.global_psi = 30


    def draw(self, wid_ptr: gl.GLViewWidget):
        self.md = gl.MeshData.sphere(rows=10, cols=20, radius=self.radius)
        self._pts = self.md.vertexes()
        self.m1 = gl.GLMeshItem(
            meshdata=self.md,
            smooth=False,
            color=(0.6, 0.6, 0.6, 0.2),
            shader="balloon",
            glOptions="additive",
        )
        self._pts = np.add(self._pts, [0, 5, 0])
        self.md.setVertexes(self._pts)
        wid_ptr.addItem(self.m1)

    def animate(self, _time, parent_x, parent_y, parent_z):
        _angle = self.angle_degree_step * _time
        _psi_rad = math.radians(self.global_psi)
        _theta_rad = math.radians(self.global_theta)
        _phi_rad = math.radians(self.global_phi)
        pts = np.dot(self._pts, Formulas.get_rot_mat('z', math.radians(_angle)))
        rot_mat = Formulas.get_3d_rot_mat(_psi_rad=_psi_rad, _theta_rad=_theta_rad, _phi_rad=_phi_rad)
        pts = np.dot(pts, rot_mat)
        pts = np.add(pts, [parent_x, parent_y, parent_z])
        self.md.setVertexes(pts)
        self.m1.setMeshData(meshdata=self.md)
