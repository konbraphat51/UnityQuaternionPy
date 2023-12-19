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
    