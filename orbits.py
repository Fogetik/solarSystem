from Formulas import Formulas
import pyqtgraph.opengl as gl
import numpy as np


class Orbit:
    def __init__(self, _orbit_a: float, _orbit_e: float, _w: gl.GLViewWidget):
        self.__a = _orbit_a
        self.__e = _orbit_e
        self.__pts = Formulas.get_ellipse_pts_shifted(_orbit_a, _orbit_e)
        self.__psi = 0
        self.__theta = 0
        self.__phi = 0

        plt = gl.GLLinePlotItem(pos=self.__pts, color=(0, 1, 0, 1), width=2)

        self.__plt = plt
        _w.addItem(plt)

    def set_color(self, r, g, b):
        self.__plt.setData(color=(r, g, b, 1))

    def set_position(self, coordinate_x, coordinate_y, coordinate_z):
        pts = np.add(self.__pts, [coordinate_x, coordinate_y, coordinate_z])
        self.__plt.setData(pos=pts)

    def rotate(self, _psi_rad: float = 0, _theta_rad: float = 0, _phi_rad: float = 0):
        """повернуть график орбиты на углы Эйлера"""
        rot_mat = Formulas.get_3d_rot_mat(_psi_rad=_psi_rad, _theta_rad=_theta_rad, _phi_rad=_phi_rad)
        pts = np.dot(self.__pts, rot_mat)
        self.__plt.setData(pos=pts)
        self.__pts = pts

    @property
    def a(self):
        return self.__a

    @property
    def e(self):
        return self.__e
