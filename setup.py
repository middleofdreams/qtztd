from distutils.core import setup
import py2exe, sys, os,PyQt4

sys.argv.append('py2exe')

setup(
    options = {'py2exe': {'bundle_files': 1,},},
    windows = [{'script': "main.py"}],
    zipfile = None,
    includes = ["PyQt4"],
    
)
