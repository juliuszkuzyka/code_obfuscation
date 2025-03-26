def dAExDOuBqYZT(x, y):
    return os.path.join(x, y)

def JtnjyASTHHYn(x, y):
    return os.path.join(x, y)

def gFPkCWzOkVhJ(p):
    return os.path.exists(p)

def DdvsAlYfJPkW(p):
    os.makedirs(p)

def bvWOoDhvMlJJ(msg):
    print(msg)

def fxfedcuaDROb(msg):
    print(msg)
import os
desktop_path = dAExDOuBqYZT(os.path.expanduser('~'), 'Desktop')
new_folder_path = JtnjyASTHHYn(desktop_path, 'test')
if not gFPkCWzOkVhJ(new_folder_path):
    DdvsAlYfJPkW(new_folder_path)
    bvWOoDhvMlJJ("Folder 'test' został utworzony na pulpicie.")
else:
    fxfedcuaDROb("Folder 'test' już istnieje.")