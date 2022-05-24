import re
old = {
   "wake-on": "disabled",
   "auto-negotiation": "on",
   "link-detected": "yes",
   "duplex": "full",
   "advertised-link-modes": "auto",
   "speed": "1000"
}
def replace_invalid_str(old_obj, new_obj,old_char='-',new_char='_'):
    new_key = None
    if new_obj is None:
        new_obj = {}
    for key in old_obj:
        p = re.compile("[ %s]"%old_char)
        new_key = p.sub(new_char, key)
        if type(old_obj[key]) == dict:
            new_obj[new_key] = {}
            new_obj[new_key] = replace_invalid_str(old_obj[key], new_obj[new_key],old_char,new_char)
        else:
            new_obj[new_key] = old_obj[key]
    return new_obj
new ={}   
replace_invalid_str(old,new) 
print new
new2={}
replace_invalid_str(new,new2,"_","-")
print new2