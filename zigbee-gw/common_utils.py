__author__ = 'dandan'
import  hashlib
class HashUtils():
    salt = "660235c0d59758ccc33d9c969d8c1643"
    def __init__(self):
        pass
    @classmethod
    def calMd5hash(cls,str):
        m = hashlib.md5()
        md5_str = "%s%s"%(str,cls.salt)
        m.update(md5_str)
        return m.hexdigest()