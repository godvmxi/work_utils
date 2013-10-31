import sys
print sys.path

['/nfs/workspace/demos', 
'/nfs/workspace/demos', 
'/usr/share/eclipse/dropins/pydev/eclipse/plugins/org.python.pydev_2.2.4.2011110216/PySrc', 
'/usr/lib/python2.7/site-packages/mytest-0.10-py2.7.egg', 
'/usr/lib/python27.zip', 
'/usr/lib/python2.7',
 '/usr/lib/python2.7/plat-linux2', 
 '/usr/lib/python2.7/lib-tk', 
 '/usr/lib/python2.7/lib-old', 
 '/usr/lib/python2.7/lib-dynload', 
 '/usr/lib/python2.7/site-packages', 
 '/usr/lib/python2.7/site-packages/PIL', 
 '/usr/lib/python2.7/site-packages/cpgmgt-service', 
 '/usr/lib/python2.7/site-packages/gst-0.10', 
 '/usr/lib/python2.7/site-packages/gtk-2.0', 
 '/usr/lib/python2.7/site-packages/setuptools-0.6c11-py2.7.egg-info', 
 '/usr/lib/python2.7/site-packages/wx-2.8-gtk2-unicode']

from cpgmgt_lib import file_helper
print file_helper.py_cat("/etc/resolv.conf")
