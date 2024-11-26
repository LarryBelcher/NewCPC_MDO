#!/usr/bin/python

import os, subprocess


cmd = "rm /work/NewCPC_MDO/mdo_polygons*"
subprocess.call(cmd,shell=True)

cmd = "rm /work/NewCPC_MDO/Drought--Monthly--Drought-Outlook--US--*.png"
subprocess.call(cmd,shell=True)


cmd = "rm /work/NewCPC_MDO/Data/*"
subprocess.call(cmd,shell=True)
