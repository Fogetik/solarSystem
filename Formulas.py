import numpy as np
import math


class Formulas:
    @staticmethod
    def get_rot_mat(_axis, _angle_rad):
        if _axis == 'x':
            return np.array([[1, 0, 0],
                             [0, math.cos(_angle_rad), math.sin(_angle_rad)],
                             [0, -math.sin(_angle_rad), math.cos(_angle_rad)]])
        if _axis == 'y':
            return np.array([[math.cos(_angle_rad), 0, math.sin(_angle_rad)],
                             [0, 1, 0],
                             [-math.sin(_angle_rad), 0, math.cos(_angle_rad)]])
        if _axis == 'z':
            return np.array([[math.cos(_angle_rad), math.sin(_angle_rad), 0],
                             [-math.sin(_angle_rad), math.cos(_angle_rad), 0],
                             [0, 0, 1]])

        print("get_rot_mat: wrong input")
        exit(-9)

    @staticmethod
    def get_3d_rot_mat(_psi_rad: float = 0, _phi_rad: float = 0, _theta_rad: float = 0) -> np.ndarray:
        rot_z_1 = Formulas.get_rot_mat('z', _psi_rad)
        rot_x = Formulas.get_rot_mat('x', _theta_rad)
        rot_z_2 = Formulas.get_rot_mat('z', _phi_rad)
        rot_mat = rot_z_1
        rot_mat = rot_mat.dot(rot_x)
        rot_mat = rot_mat.dot(rot_z_2)
        return rot_mat

    @staticmethod
    def get_ellipse_pts(_orbit_a: float, _orbit_e: float) -> np.ndarray:
        assert _orbit_e < 1.0, "e: неверное!"

        b = _orbit_a*math.sqrt(1 - _orbit_e ** 2)
        pts = []
        angle_rng = np.linspace(0, 2*math.pi, 180, endpoint=True)
        for angle in angle_rng:
            x = _orbit_a * math.sin(angle)
            y = b * math.cos(angle)
            pts.append([x, y, 0])

        return np.array(pts)

    @staticmethod
    def get_ellipse_pts_shifted(_orbit_a: float, _orbit_e: float) -> np.ndarray:
        """ возвращает эллипс, у которого точка (0, 0, 0) находится в его фокусе"""
        assert _orbit_e < 1.0, "e: неверное!"

        b = _orbit_a * math.sqrt(1 - _orbit_e ** 2)
        pts = []
        angle_rng = np.linspace(0, 2 * math.pi, 180, endpoint=True)
        for angle in angle_rng:
            x = _orbit_a * (math.sin(angle) - _orbit_e)
            y = b * math.cos(angle)
            pts.append([x, y, 0])
            # print(f'x:{x}, y:{y}')

        return np.array(pts)

    @staticmethod
    def satellite_pos_geostat_crd(_orbit_a, _orbit_e,  _t, _phi, _psi, _theta) -> np.ndarray:
        x = \
            - _orbit_a * math.sqrt(1 - _orbit_e ** 2) * math.sin(_t) \
            * (
                    math.cos(_psi) * math.cos(_theta) * math.sin(_phi)
                    + math.cos(_phi) * math.sin(_psi)
            ) \
            + _orbit_a * (math.cos(_t) - _orbit_e) \
            * (
                    - math.cos(_theta) * math.sin(_phi) * math.sin(_psi)
                    + math.cos(_phi) * math.cos(_psi)
            )

        y = \
            _orbit_a * math.sqrt(1 - _orbit_e ** 2) * math.sin(_t) \
            * (
                    math.cos(_phi) * math.cos(_psi) * math.cos(_theta)
                    - math.sin(_phi) * math.sin(_psi)
            ) \
            + _orbit_a * (math.cos(_t) - _orbit_e) \
            * (
                    math.cos(_phi) * math.cos(_theta) * math.sin(_psi)
                    + math.cos(_psi) * math.sin(_phi)
            )

        z = \
            _orbit_a * math.sin(_theta) \
            * (
                        math.sqrt(1 - _orbit_e ** 2) * math.cos(_psi) * math.sin(_t)
                        + (math.cos(_t) - _orbit_e) * math.sin(_psi)
                )

        return np.array([[x, y, z]])
