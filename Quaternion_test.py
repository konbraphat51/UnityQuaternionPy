from pytest import approx
from UnityQuaternion import Quaternion

def test_constructor():
    q = Quaternion(1, 2, 3, 4)
    assert q.w == approx(1)
    assert q.x == approx(2)
    assert q.y == approx(3)
    assert q.z == approx(4)
    
def test_eulerAngles_zero():
    q = Quaternion(0,0,0,1)
    e = q.eulerAngles
    
    assert e[0] == approx(0)
    assert e[1] == approx(0)
    assert e[2] == approx(0)
    
def test_eulerAngles():
    q = Quaternion(1,2,3,4).normalized
    e = q.eulerAngles
    
    assert e[0] == approx(352.34)
    assert e[1] == approx(47.43)
    assert e[2] == approx(70.35)
    
def test_normalize():
    q = Quaternion(1,2,3,4)
    assert q.w == approx(0.1825742)
    assert q.x == approx(0.3651484)
    assert q.y == approx(0.5477226)
    assert q.z == approx(0.7302967)
    
def test_normalized():
    q = Quaternion(1,2,3,4).normalized
    assert q.w == approx(0.1825742)
    assert q.x == approx(0.3651484)
    assert q.y == approx(0.5477226)
    assert q.z == approx(0.7302967)
    
def test_AngleAxis():
    q = Quaternion.AngleAxis(20, (1,2,3)).normalized
    assert q.x == approx(0.04641)
    assert q.y == approx(0.09282)
    assert q.x == approx(0.13923)
    assert q.w == approx(0.98517)
    
def test_Set():
    q = Quaternion(1,2,3,4)
    q.Set(5,6,7,8)
    assert q.w == approx(5)
    assert q.x == approx(6)
    assert q.y == approx(7)
    assert q.z == approx(8)
    
def test_FromToRotation():
    q = Quaternion(1,2,3,4)
    q.SetFromToRotation((5,6,7),(1,2,3))
    
    assert q.x == approx(0.05137)
    assert q.y == approx(-0.10274)
    assert q.z == approx(0.05137)
    assert q.w == approx(0.99205)
    
def test_LookRotation():
    q = Quaternion(1,2,3,4)
    q.SetLookRotation((1,1,1), (0,1,0))
    
    assert q.x == approx(-0.27)
    assert q.y == approx(0.36)
    assert q.z == approx(0.11)
    assert q.w == approx(0.88)
    
def test_ToAngleAxis():
    q = Quaternion(1,1,1,1).normalized
    angle, axis = q.ToAngleAxis()
    
    assert angle == approx(120)
    assert axis[0] == approx(0.58)
    assert axis[1] == approx(0.58)
    assert axis[2] == approx(0.58)
    
def test_ToString():
    q = Quaternion(1,2,3,4)
    assert q.ToString(2).__class__ == str

def test_multiply():
    q1 = Quaternion(1,2,3,4).normalized
    q2 = Quaternion(4,3,2,1).normalized

    q = q1 * q2
    
    assert q.x == approx(0.4)
    assert q.y == approx(0.8)
    assert q.z == approx(0.2)
    assert q.w == approx(-0.4)
    
def test_rotate():
    q = Quaternion(1,2,3,4).normalized
    v = (4,5,6)
    v_norm = (4**2 + 5**2 + 6**2)**0.5
    v = (v[0]/v_norm, v[1]/v_norm, v[2]/v_norm)
    
    v = q * v
    
    assert v[0] == approx(0.18)
    assert v[1] == approx(0.71)
    assert v[2] == approx(0.68)
    
def test_Angle():
    q0 = Quaternion(1, 2, 3, 4).normalized
    q1 = Quaternion(4, 2, 1, 3).normalized

    assert Quaternion.Angle(q0, q1) == approx(79.88902, 2)

def test_Dot():
    q0 = Quaternion(1, 2, 3, 4)
    q1 = Quaternion(4, 2, 1, 3)

    result = Quaternion.Dot(q0, q1)

    assert result == approx(23)

def test_Euler():
    q = Quaternion.Euler(30, 60, 90)

    assert q.x == approx(0.5, 1)
    assert q.y == approx(0.18, 1)
    assert q.z == approx(0.5, 1)
    assert q.w == approx(0.68, 1)

def test_Inverse():
    q = Quaternion(0.5, 0.5, 0.5, 0.5)
    inv = Quaternion.Inverse(q)

    assert inv.x == approx(-0.5, 1)
    assert inv.y == approx(-0.5, 1)
    assert inv.z == approx(-0.5, 1)
    assert inv.w == approx(0.5, 1)

def test_Identity():
    q = Quaternion.identity

    assert q.x == approx(0)
    assert q.y == approx(0)
    assert q.z == approx(0)
    assert q.w == approx(1)
