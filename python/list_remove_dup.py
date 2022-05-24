#!/usr/bin/python
# Filename: DeleteRep
# use: to delete the repetation of the string
__author__ = 'bluebird'
StringList=['123','abc','abc','cde','cde']
StringList=['123', 'abc', 'cde']
def remove_list_duplicate(inlist):
    index = 1
    compare = 0
    length = len(inlist) - 1
    while index <= length:
        if cmp(inlist[index],inlist[compare]) == 0:
            del inlist[index]
            length -= 1
            if index == length + 1:
                break
        else:
            index += 1
            compare += 1
    return inlist

print remove_list_duplicate(StringList)

#!/usr/bin/python
# Filename: DeleteRep
# use: to delete the repetation of the string

StringList=['123','abc','abc','cde','cde']
index = 1
compare = 0
length = len(StringList) - 1
while index <= length:
    if cmp(StringList[index],StringList[compare]) == 0:
        del StringList[index]
        length -= 1
        if index == length + 1:
            break
    else:
        index += 1
        compare += 1
print StringList