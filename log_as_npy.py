import time

import numpy as np
import pynput
from pynput.keyboard._win32 import Listener


class KeyListener(Listener):
    def _event_to_key(self, msg, vk):
        return msg, vk


def timestamp():  # microsecond
    return time.time_ns() // 1_000


LOG_INTERVAL = 60
ITEMS = 1 + 2 + 2 + 1 + 5 + 1 + 256


# 0: delay ms
# 1-2: x/y
# 3-4: scroll x/y
# 5: scroll y/n
# 6-10: click y/n for left/right/mmb/shoulder1/shoulder2
# 11: WM_KEY (no fucking clue)
# 12-265: keyboard


class Log:
    def __init__(self):
        self.log_file = open("log.txt", "w")
        self.is_pressed = {}
        self.last_timestamp = 0
        self.scroll_sum = [0, 0]
        self.cache = np.zeros((1, ITEMS), dtype=np.int64)
        self.last_written = time.time()
        self.append(self.empty())
        self.cache = self.cache[1:]

    def empty(self):
        ts = timestamp()
        empty = np.copy(self.cache[-1])
        empty[0] = ts - self.last_timestamp
        self.last_timestamp = ts
        return empty

    def _append(self, dat: np.ndarray):
        self.cache = np.concatenate([self.cache, dat.reshape(1, -1)], 0)

    def _commit_scroll(self, dat: np.ndarray):
        scroll_dat = self.empty()
        dat[0] /= 2
        scroll_dat[0] = dat[0]
        scroll_dat[3] = self.scroll_sum[0]
        scroll_dat[4] = self.scroll_sum[1]
        scroll_dat[5] = 1
        self._append(scroll_dat)
        self.scroll_sum = [0, 0]
        return dat

    def save(self):
        np.save("cache", self.cache)

    def append(self, dat: np.ndarray):
        if any(self.scroll_sum):
            dat = self._commit_scroll(dat)
        self._append(dat)
        if time.time() > self.last_written + LOG_INTERVAL:
            self.save()

    def on_move(self, x, y):
        pass  # self.log(f"Moved: x={x} y={y}")  <- disabled to reduce log size. click should be enough

    def on_click(self, x, y, button, pressed):
        dat = self.empty()
        button = str(button)
        if "left" in button:
            button = 0
        elif "right" in button:
            button = 1
        elif "middle" in button:
            button = 2
        elif "x1" in button:
            button = 3
        elif "x2" in button:
            button = 4
        dat[1] = x
        dat[2] = y
        dat[6 + button] = int(pressed)
        self.append(dat)

    def on_scroll(self, x, y, dx, dy):
        self.scroll_sum[0] += dx
        self.scroll_sum[1] += dy

    def on_press(self, obj):
        dat = self.empty()
        if dat[12 + obj[1]]:
            return
        dat[11] = obj[0]
        dat[12 + obj[1]] = 1
        self.append(dat)

    def on_release(self, obj):
        dat = self.empty()
        if not dat[12 + obj[1]]:
            return
        dat[11] = obj[0]
        dat[12 + obj[1]] = 0  # asdasopiop  IUIOASU 9u uU u 0
        self.append(dat)

    def run(self):
        KeyListener(on_press=self.on_press, on_release=self.on_release).start()
        pynput.mouse.Listener(on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll).start()
        while True:
            time.sleep(1200)


Log().run()

# helllo my anem is peirr i am you also doing  are doing good atoo that >wou HELLO CAN YOU HEAR ME YOU ASSHATOO THAT
# >wou HELLO CAN YOU HEAR ME YOU ASSHATOO THAT >wou HELLO CAN YOU HEAR ME YOU ASSHAT?
