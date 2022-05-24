#!/bin/env python
import os
print os.popen("iwpriv ra0 show  blockch").readlines()