from distutils.core import setup

import py_load_c

setup(

name = "Meter",

description = "Python-based App",

version = "1.0",

console = ["shell.py"],

options = {"py2exe":{"bundle_files":1,"packages":"ctypes","includes":"base64,sys,socket,struct,time,code,platform,getpass,shutil",}},

zipfile = None

)