import re

def __is_valid_ipv4( ip):
    """Validates IPv4 addresses.
    """
    tmp = ip.split('.')
    if len(tmp) != 4 :
        return False
    A = int(tmp[0])
    if A < 1 or A > 223 :
        return False
    B = int(tmp[1])
    if B < 0 or B > 254 :
        return False
    C = int(tmp[2])
    if C < 0 or C > 254 :
        return False
    D = int(tmp[3])
    if D < 0 or D > 254 :
        return False
    return True
def __is_valid_ipv4_mask(mask):
    """Validates IPv4 mask.
    """
    tmp = mask.split('.')
    if len(tmp) != 4 :
        return False
    A = int(tmp[0])
    if A != 255 :
        return False
    B = int(tmp[1])
    if B < 0 or B > 255 :
        return False
    C = int(tmp[2])
    if C < 0 or C > 255 :
        return False
    D = int(tmp[3])
    if D < 0 or D > 254 :
        return False
    return True
    

print __is_valid_ipv4('10.0.0')
print __is_valid_ipv4('10.0.0.1.1')
print __is_valid_ipv4('10.0.0.1')
print __is_valid_ipv4('0.0.0.1')