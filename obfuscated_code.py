def ACWvSlfzYLku(x, y):
    return os.path.join(x, y)

def AOlSjcDxwkDv(x, y):
    return os.path.join(x, y)

def tHtnRhmgjGGk(p):
    return os.path.exists(p)

def RVOLXTJKmEbE(p):
    os.makedirs(p)

def JFOgRbdkrzMX(msg):
    print(msg)

def trsQMnqjNyMb(msg):
    print(msg)
import os
desktop_path = ACWvSlfzYLku(os.path.expanduser('~'), 'Desktop')
new_folder_path = AOlSjcDxwkDv(desktop_path, 'test')
if not tHtnRhmgjGGk(new_folder_path):
    RVOLXTJKmEbE(new_folder_path)
    JFOgRbdkrzMX(f"Folder 'test' został utworzony na pulpicie.")
else:
    trsQMnqjNyMb("Folder 'test' już istnieje.")