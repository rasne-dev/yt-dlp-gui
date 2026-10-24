import re
import sys

def bump():
    with open('ytdlp_gui.py', 'r', encoding='utf-8') as f:
        content = f.read()

    m = re.search(r'__version__\s*=\s*["\'](\d+)\.(\d+)\.(\d+)["\']', content)
    if not m:
        sys.exit('Version not found in ytdlp_gui.py')

    major, minor, patch = int(m.group(1)), int(m.group(2)), int(m.group(3))

    patch += 1
    if patch > 9:
        patch = 0
        minor += 1
        if minor > 9:
            minor = 0
            major += 1

    new_ver = f"{major}.{minor}.{patch}"
    content = re.sub(r'__version__\s*=\s*["\']\d+\.\d+\.\d+["\']', f'__version__ = "{new_ver}"', content)

    with open('ytdlp_gui.py', 'w', encoding='utf-8') as f:
        f.write(content)

    with open('.version', 'w', encoding='utf-8') as f:
        f.write(new_ver)

    print(f"VERSION_UPDATED:{new_ver}")

if __name__ == '__main__':
    bump()
