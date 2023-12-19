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
        
    def AngleAxis(angle: float, axis: tuple[float, float, float]) -> Quaternion:
        """
        Creates a rotation which rotates angle degrees around axis.

        :param float angle: angle in degrees
        :param tuple[float, float, float] axis: axis of rotation
        :rtype: Quaternion
        :return: quaternion made
        """
        # based on based on https://qiita.com/aa_debdeb/items/3d02e28fb9ebfa357eaf#%E3%82%AA%E3%82%A4%E3%83%A9%E3%83%BC%E8%A7%92%E3%81%8B%E3%82%89%E3%82%AF%E3%82%A9%E3%83%BC%E3%82%BF%E3%83%8B%E3%82%AA%E3%83%B3
        rad = math.radians(angle)
        sin_half = math.sin(rad / 2)
        cos_half = math.cos(rad / 2)
        
        #normalize axis
        norm = (axis[0]**2 + axis[1]**2 + axis[2]**2)**0.5
        axis = (axis[0]/norm, axis[1]/norm, axis[2]/norm)
        
        x = axis[0] * sin_half
        y = axis[1] * sin_half
        z = axis[2] * sin_half
        w = cos_half
        
        return Quaternion(x,y,z,w)
        
    def Dot(a: Quaternion, b: Quaternion) -> float:
        """
        The dot product between two rotations.
                
        :param Quaternion a: first rotation
        :param Quaternion b: second rotation
        :rtype: float
        :return: dot product
        """
        return a.x * b.x + a.y * b.y + a.z * b.z + a.w * b.w
    
    def Euler(x:float, y:float, z:float) -> Quaternion:
        """
        Returns a rotation that rotates 
        z degrees around the z axis, 
        x degrees around the x axis, 
        and y degrees around the y axis;
        applied in that order.

        :param float x: x rotation in degrees around x axis
        :param float y: y rotation in degrees around y axis
        :param float z: z rotation in degrees around z axis
        :rtype: Quaternion
        :return: quaternion made
        """
        # based on based on https://ohtorii.hatenadiary.jp/entry/20150424/p1
        
        sx = math.sin(math.radians(x) / 2)
        cx = math.cos(math.radians(x) / 2)
        sy = math.sin(math.radians(y) / 2)
        cy = math.cos(math.radians(y) / 2)
        sz = math.sin(math.radians(z) / 2)
        cz = math.cos(math.radians(z) / 2)
        
        _x = cx * sy * sz + cy * cz * sx
        _y = cx * cz * sy - cy * sx * sz
        _z = cx * cy * sz - cz * sx * sy
        _w = sx * sy * sz + cx * cy * cz
        
        return Quaternion(_x, _y, _z, _w)
    
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