from __future__ import annotations
import math

class Quaternion:
    """
    Quaternion class, immitating UnityEngine.Quaternion
    this = `x`i + `y`j + `z`k + `w`
    The coordinate system is based on Unity's left-handed coordinate +  left-hand thread rotation system.
    See: https://docs.unity3d.com/ja/2023.2/ScriptReference/Quaternion.html
    
    :param float x: x element of the quaternion
    :param float y: y element of the quaternion
    :param float z: z element of the quaternion
    :param float w: w element of the quaternion
    """
    
    # calculation based on:
    # https://www.mesw.co.jp/business/report/pdf/mss_18_07.pdf
    
    def __init__(self, x: float, y: float, z: float, w: float):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        
    @property
    def eulerAngles(self) -> tuple[float, float, float]:
        """
        Returns or sets the euler angle representation of the rotation in degrees.
	    The order is Z-rotaion -> X-rotation -> Y-rotation.
        See: https://docs.unity3d.com/2023.2/Documentation/ScriptReference/Quaternion-eulerAngles.html
        :rtype: tuple[float, float, float]
        :return: [x,y,z] in degrees
        """
        # based on https://qiita.com/edo_m18/items/5db35b60112e281f840e#unity%E3%81%A7%E5%AE%9F%E8%A1%8C%E3%81%97%E3%81%A6%E3%81%BF%E3%82%8B
        
        normalized = self.normalized
        _x = normalized.x
        _y = normalized.y
        _z = normalized.z
        _w = normalized.w
        
        sinx = 2 * _y * _z - 2 * _x * _w
        
        if (abs(sinx - 1) < 0.01):
            #sinx == 1 (singularity)
            x = math.pi / 2
            y = 0
            z = math.atan2(2 * _x * _y - 2 * _z * _w, 1 - 2 * _y**2 - 2 * _z**2)
        elif (abs(sinx + 1) < 0.01):
            #sinx == -1 (singularity)
            x = -math.pi / 2
            y = 0
            z = math.atan2(2 * _x * _y - 2 * _z * _w, 1 - 2 * _y**2 - 2 * _z**2)
        else:
            x = math.asin(-sinx)
            y = math.atan2(2 * _x * _z + 2 * _y * _w, 1 - 2 * _x**2 - 2 * _y**2)
            z = math.atan2(2 * _x * _y + 2 * _z * _w, 1 - 2 * _x**2 - 2 * _z**2)
            
        # convert to degrees
        x = math.degrees(x)
        y = math.degrees(y)
        z = math.degrees(z)
        
        # to [0,360]
        x = x % 360
        y = y % 360
        z = z % 360
        
        return (x,y,z)
        
    @property
    def normalized(self) -> Quaternion:
        """
        Returns the norm=1 quaternion that represents the same rotation.

        :rtype: Quaternion
        :return: normalized quaternion
        """
        norm = self._norm
        return Quaternion(self.x/norm, self.y/norm, self.z/norm, self.w/norm)
        
    @property
    def identity() -> Quaternion:
        """
        Returns the identity quaternion (0,0,0,1)

        :rtype: Quaternion
        :return: identity quaternion
        """
        return Quaternion(0,0,0,1)
    
    def __mul__(self, other: Quaternion|tuple[float, float, float]) -> Quaternion|tuple[float, float, float]:
        """
        Multiplies two quaternions or Rotate a vector by a quaternion.

        Product of 2 quaternions means that the rotation of q0 is applied first, then q1.

        :param Quaternion|tuple[float, float, float] other: quaternion or vector to be multiplied
        :rtype: Quaternion|tuple[float, float, float]
        :return: product of two quaternions or rotated vector
        """
        if isinstance(other, Quaternion):
            return self._multiply_quaternions(other)
        elif isinstance(other, tuple):
            return self._rotate_vector(other)
        else:
            raise TypeError(f"unsupported operand type(s) for *: 'Quaternion' and '{type(other)}'")
    
    def ToAngleAxis(self) -> tuple[float, tuple[float, float, float]]:
        """
        Converts a rotation to angle-axis representation (angles in degrees).

        :rtype: tuple[float, tuple[float, float, float]]
        :return: (angle, axis)
        """
        #based on https://qiita.com/aa_debdeb/items/3d02e28fb9ebfa357eaf#%E3%82%AA%E3%82%A4%E3%83%A9%E3%83%BC%E8%A7%92%E3%81%8B%E3%82%89%E3%82%AF%E3%82%A9%E3%83%BC%E3%82%BF%E3%83%8B%E3%82%AA%E3%83%B3
        
        normalized = self.normalized
        
        angle = 2 * math.acos(normalized.w)
        
        sin_half = math.sin(angle / 2)
        axis = (normalized.x / sin_half, normalized.y / sin_half, normalized.z / sin_half)
        
        # convert to degrees
        angle = math.degrees(angle)
        
        return (angle, axis)
    
    def ToString(self, digits = 5):
        """
        Returns a nicely formatted string of the Quaternion.
        Into "(x, y, z, w)" format.

        :param int digits: number of digits after the decimal point
        :rtype: str
        :return: string representation
        """
        return f"({self.x:.{digits}f}, {self.y:.{digits}f}, {self.z:.{digits}f}, {self.w:.{digits}f})"
        
    def Angle(a: Quaternion, b: Quaternion) -> float:
        """
        Returns the angle in degrees between two rotations a and b.
        
        see: https://docs.unity3d.com/ScriptReference/Quaternion.Angle.html
        
        :param Quaternion a: first rotation
        :param Quaternion b: second rotation
        :rtype: float
        :return: angle in degrees
        """    
        dot = Quaternion.Dot(a, b)
        rad = math.acos(dot) * 2
        dgrees = math.degrees(rad)
        
        return dgrees
        
    def Dot(a: Quaternion, b: Quaternion) -> float:
        """
        The dot product between two rotations.
                
        :param Quaternion a: first rotation
        :param Quaternion b: second rotation
        :rtype: float
        :return: dot product
        """
        return a.x * b.x + a.y * b.y + a.z * b.z + a.w * b.w
    
    @property
    def _norm(self) -> float:
        return (self.x**2 + self.y**2 + self.z**2 + self.w**2)**0.5
    
    @property
    def _conjugate(self) -> Quaternion:
        return Quaternion(-self.x, -self.y, -self.z, self.w)
    
    def _multiply_quaternions(self, right:Quaternion) -> Quaternion:
        x = self.x * right.w + self.w * right.x - self.z * right.y + self.y * right.z
        y = self.y * right.w + self.z * right.x + self.w * right.y - self.x * right.z
        z = self.z * right.w - self.y * right.x + self.x * right.y + self.w * right.z
        w = self.w * right.w - self.x * right.x - self.y * right.y - self.z * right.z
        
        return Quaternion(x,y,z,w)
    
    def _rotate_vector(self, vector:tuple[float, float, float]) -> tuple[float, float, float]:
        #rotate
        normalized = self.normalized
        inverted = normalized._conjugate
        q_vector = Quaternion(vector[0], vector[1], vector[2], 0)
        rotated = normalized * q_vector * inverted
        
        #scale
        norm = self._norm
        return (rotated.x * norm, rotated.y * norm, rotated.z * norm)