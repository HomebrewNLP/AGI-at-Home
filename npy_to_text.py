import datetime

import numpy as np
from pynput.keyboard._win32 import Listener


# 0: delay ms
# 1-2: x/y
# 3-4: scroll x/y
# 5: scroll y/n
# 6-10: click y/n for left/right/mmb/shoulder1/shoulder2
# 11: WM_KEY (no fucking clue)
# 12-266: keyboard

def main():
    listener = Listener()
    cache = np.load("cache.npy")
    base = datetime.datetime.fromtimestamp(0)
    key = 0

    def log(dat: str):
        print(f"{base}: {dat}")
    for line in cache:
        base = base + datetime.timedelta(microseconds=int(line[0]))
        if line[3]:
            log(f'ScrollX={line[3]} ScrollY={line[4]}')
            continue

        if any(line[6:11]):
            pos = f"X={line[1]} Y={line[2]}"
            mouse = ' '.join(f'{key}={line[6 + i]}'
                             for i, key in enumerate(("Left", "Right", "Middle", "Shoulder1", "Shoulder2")))
            log(f"{pos} {mouse}")
            continue

        if np.all(line[12:] == 0):
            log("Everything Released")
            continue

        wm_keydown = line[11]
        new_key = np.argmax(line[12:])
        if new_key == 0:
            log(f"KeyReleased={listener._event_to_key(wm_keydown, key)}")
            key = new_key
            continue
        key = new_key
        log(f"KeyPressed={listener._event_to_key(wm_keydown, key)}")


if __name__ == '__main__':
    main()
