import os
import shutil

for i in range(1, 25):
    dir = "adventofcode/"
    filename = os.path.join(str(i).zfill(2) + ".py")
    fullpath = os.path.join(dir, filename)
    if not os.path.exists(fullpath):
        shutil.copy("adventofcode/helper/template/00.py", fullpath)
