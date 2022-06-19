import datetime
import time

import pynput


def key(obj):
    if hasattr(obj, "char"):
        return obj.char
    if obj == obj.space:
        return "SPACE"
    if obj == obj.esc:
        return "ESC"
    return " " + str(obj) + " "


class Log:
    def __init__(self):
        self.log_file = open("log.txt", "w")
        self.is_pressed = {}
        self.scroll_sum = [0, 0]

    def _log(self, msg: str):
        dat = f"{datetime.datetime.now().isoformat()}: {msg}\n"
        print(dat, end='')
        self.log_file.write(dat)
        self.log_file.flush()

    def log(self, msg: str):
        if "Scroll" not in msg and any(self.scroll_sum):
            self._log(f"Scroll: dx={self.scroll_sum[0]} dy={self.scroll_sum[1]}")
            self.scroll_sum = [0, 0]
        self._log(msg)

    def on_move(self, x, y):
        pass  # self.log(f"Moved: x={x} y={y}")  <- disabled to reduce log size. click should be enough

    def on_click(self, x, y, button, pressed):
        self.log(f"Clicked: x={x} y={y} button={button} pressed={pressed}")

    def on_scroll(self, x, y, dx, dy):
        self.scroll_sum[0] += dx
        self.scroll_sum[1] += dy

    # def screenshot(self):
    #     img = pyscreenshot.grab()

    def on_press(self, obj):
        obj = key(obj)
        if not self.is_pressed.get(obj):
            self.is_pressed[obj] = True
            self.log(f"Pressed: {obj}")

    def on_release(self, obj):
        obj = key(obj)
        self.is_pressed[obj] = False
        self.log(f"Released: {obj}")

    def run(self):
        pynput.keyboard.Listener(on_press=self.on_press, on_release=self.on_release).start()
        pynput.mouse.Listener(on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll).start()
        time.sleep(3600)


Log().run()
