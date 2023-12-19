from UnityQuaternion import Quaternion

def test_constructor():
    q = Quaternion(1, 2, 3, 4)
    assert q.w == 1
    assert q.x == 2
    assert q.y == 3
    assert q.z == 4
    
