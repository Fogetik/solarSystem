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
        self.radius = 2
        self.child = []
        self.coor_x = 0
        self.coor_y = 0
        self.coor_z = 0
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
        self.m1.translate(self.coor_x, self.coor_y, self.coor_z)

        wid_ptr.addItem(self.m1)
        self.earth_planet.draw(wid_ptr)


    def animate(self, time: int):
        # self.m1.translate(coor, coor, coor)
        self.m1.rotate(-1, 0, 1, 1)
        self.earth_planet.animate(time)


class Earth:
    def __init__(self):
        self.angle_degree_step = 1
        self.radius = 2

        self.child = []

        self.coor_x = 0
        self.coor_y = 10
        self.coor_z = 0

        self.global_phi = 0
        self.global_psi = 0
        self.global_theta = 0

        self.global_psi_max = 30
        self.global_theta_max = 30
        self.global_phi_max = 30
        self.global_angle_degree_step = 0.2

    def rotate_x(self, angle: float):
        coor_y_cpy = self.coor_y
        coor_z_cpy = self.coor_z
        self.coor_y = coor_y_cpy * math.cos(angle) - coor_z_cpy * math.sin(angle)
        self.coor_z = coor_y_cpy * math.sin(angle) + coor_z_cpy * math.cos(angle)


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

    def animate(self, _time):
        # _psi_rad
        #         , _theta_rad
        #         , _phi_rad)
        # print(f'_psi_rad:{_psi_rad}, _theta_rad:{_theta_rad}, _phi_rad:{_phi_rad}')

        _angle = self.angle_degree_step * _time
        global_psi = 0
        global_theta = 0
        global_phi = 0

        global_angle_degree_step = self.global_angle_degree_step
        global_psi_max = self.global_psi_max
        global_theta_max = self.global_theta_max
        global_phi_max = self.global_phi_max

        k = int(global_angle_degree_step * _time // (global_psi_max + global_phi_max + global_theta_max))
        _time -= k * (global_psi_max + global_phi_max + global_theta_max) / global_angle_degree_step
        _time = int(_time)

        if k > 0:
            print(k)
            k = k & 4
            if k == 0:
                global_angle_degree_step *= (-1)
                global_psi = self.global_psi_max
                global_theta = self.global_theta_max
                global_phi = self.global_phi_max
                global_phi_max = 0
                global_theta_max = 0
                global_psi_max = 0
            elif k == 1:
                global_angle_degree_step *= (-1)
                global_phi_max *= -1
                global_theta_max *= -1
                global_psi_max *= -1
            elif k == 2:
                global_psi = self.global_psi * -1
                global_theta = self.global_theta * -1
                global_phi = self.global_phi * -1
                global_phi_max = 0
                global_theta_max = 0
                global_psi_max = 0









        print(f'time:{_time} k:{k}')
        for i in range(0, _time):
            if abs(global_psi) < abs(global_psi_max):
                global_psi += global_angle_degree_step
            elif abs(global_theta) < abs(global_theta_max):
                global_theta += global_angle_degree_step
            elif abs(global_phi) < abs(global_phi_max):
                global_phi += global_angle_degree_step



        _psi_rad = math.radians(global_psi)
        _theta_rad = math.radians(global_theta)
        _phi_rad = math.radians(global_phi)
        print(f'psi:{global_psi}, theta:{global_theta}, phi:{global_phi}')

        pts = np.dot(self._pts, Formulas.get_rot_mat('z', math.radians(_angle)))
        rot_mat = Formulas.get_3d_rot_mat(_psi_rad=_psi_rad, _theta_rad=_theta_rad, _phi_rad=_phi_rad)
        pts = np.dot(pts, rot_mat)
        self.md.setVertexes(pts)
        self.m1.setMeshData(meshdata=self.md)

        # print(f'x:{self.coor_x}, y:{self.coor_y}, z:{self.coor_z}')
        # self.coor_x, self.coor_y = rotate_z(self.coor_x, self.coor_y, _psi_rad)
        # self.coor_y, self.coor_z = rotate_x(self.coor_y, self.coor_z, _theta_rad)
        # self.coor_x, self.coor_y = rotate_z(self.coor_x, self.coor_y, _phi_rad)

        # print(f'x:{self.coor_x}, y:{self.coor_y}, z:{self.coor_z}')


