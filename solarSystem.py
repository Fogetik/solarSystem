import pyqtgraph.opengl as gl
import numpy as np
import math

from Formulas import Formulas
from orbits import Orbit


class sun:
    def __init__(self):
        self.md = None
        self.m1 = None
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
        self.earth_planet.animate(time)


class Earth:
    def __init__(self):
        self.orbit_earth = None
        self.md = None
        self._pts = None
        self.m1 = None
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
            smooth=True,
            color=(0, 1, 0, 0.2),
            shader="balloon",
            glOptions="additive",
        )

        self._pts = np.add(self._pts, [0, 10, 0])
        self.md.setVertexes(self._pts)
        wid_ptr.addItem(self.m1)

        self.orbit_earth = Orbit(10, 0, wid_ptr)
        _psi_rad = math.radians(self.global_psi)
        _theta_rad = math.radians(self.global_theta)
        _phi_rad = math.radians(self.global_phi)
        self.orbit_earth.rotate(_psi_rad, _theta_rad, _phi_rad)
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

        self.moon.animate(_time, pts[0][0], pts[0][1], pts[0][2] - self.radius)


class Moon:
    def __init__(self):
        self.orbit_moon = None
        self.md = None
        self.m1 = None
        self._pts = None
        self.angle_degree_step = 2.25
        self.radius = 1
        self.global_phi = 30
        self.global_theta = -50
        self.global_psi = 30

    def draw(self, wid_ptr: gl.GLViewWidget):
        self.md = gl.MeshData.sphere(rows=10, cols=20, radius=self.radius)
        self._pts = self.md.vertexes()
        self.m1 = gl.GLMeshItem(
            meshdata=self.md,
            smooth=True,
            color=(0.6, 0.6, 0.6, 0.2),
            shader="balloon",
            glOptions="additive",
        )
        self._pts = np.add(self._pts, [0, 5, 0])
        self.md.setVertexes(self._pts)
        wid_ptr.addItem(self.m1)

        self.orbit_moon = Orbit(5, 0, wid_ptr)
        self.orbit_moon.set_color(0.8, 0.8, 0.8)
        _psi_rad = math.radians(self.global_psi)
        _theta_rad = math.radians(self.global_theta)
        _phi_rad = math.radians(self.global_phi)
        self.orbit_moon.rotate(_psi_rad, _theta_rad, _phi_rad)
    
    def animate(self, _time, parent_x, parent_y, parent_z):
        _angle = self.angle_degree_step * _time
        _psi_rad = math.radians(self.global_psi)
        _theta_rad = math.radians(self.global_theta)
        _phi_rad = math.radians(self.global_phi)
        pts = np.dot(self._pts, Formulas.get_rot_mat('z', math.radians(_angle)))
        rot_mat = Formulas.get_3d_rot_mat(_psi_rad=_psi_rad, _theta_rad=_theta_rad, _phi_rad=_phi_rad)
        pts = np.dot(pts, rot_mat)
        pts = np.add(pts, [parent_x, parent_y, parent_z])

        self.orbit_moon.set_position(parent_x, parent_y, parent_z)
        self.md.setVertexes(pts)
        self.m1.setMeshData(meshdata=self.md)
