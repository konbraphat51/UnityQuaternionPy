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