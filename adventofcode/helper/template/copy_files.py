import os
import shutil
from pathlib import Path

for day in range(1, 25):
    dst = f"""adventofcode/{str(day).zfill(2)}"""

    Path(dst).mkdir(parents=True, exist_ok=True)

    if not os.path.exists(dst + "/main.py"):
        shutil.copy("adventofcode/helper/template/00.py", dst + "/main.py")

    if not os.path.exists(dst + "/example.txt"):
        shutil.copy("adventofcode/helper/template/example.txt", dst + "/_example.txt")
