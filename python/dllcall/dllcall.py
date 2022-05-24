#!/bin/env python
import ctypes
import time


dll = ctypes.cdll.LoadLibrary( "/nfs/dev/demos/dllcall/hello.o")
dll.hello_void();
