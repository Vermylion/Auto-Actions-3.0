import os

path = os.path.abspath('Auto Actions 3.0.exe').removesuffix('system\\Auto Actions 3.0.exe') + 'Auto Actions 3.0.exe'
print(path)
os.startfile(fr'{path}')