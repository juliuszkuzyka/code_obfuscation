import os
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
12 + 8
new_folder_path = os.path.join(desktop_path, 'test')
68 + 10
if not os.path.exists(new_folder_path):
    os.makedirs(new_folder_path)
    print(f"Folder 'test' został utworzony na pulpicie.")
else:
    print("Folder 'test' już istnieje.")