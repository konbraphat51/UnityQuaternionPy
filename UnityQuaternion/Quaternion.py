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
        
    