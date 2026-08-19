import tkinter as tk
import threading
import queue
import time


class ToastManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.queue = queue.Queue()
        self.toasts = []
        self.root = None
        self._init_root()

    def _init_root(self):
        self.root = tk.Toplevel()
        self.root.withdraw()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#000000")

    def _get_root(self):
        if not self.root or not self.root.winfo_exists():
            self._init_root()
        return self.root

    def _process_queue(self):
        root = self._get_root()
        while not self.queue.empty():
            try:
                toast = self.queue.get_nowait()
                self._create_toast(root, toast)
            except Exception:
                pass

        self._cleanup_toasts()
        root.after(100, self._process_queue)

    def _create_toast(self, root, toast_data):
        toast = Toast(root, toast_data, self)
        self.toasts.append(toast)

    def _cleanup_toasts(self):
        alive = []
        for toast in self.toasts:
            if toast.is_alive():
                alive.append(toast)
        self.toasts = alive

    def notify(self, message, level="info", duration=3000):
        self.queue.put({
            "message": message,
            "level": level,
            "duration": duration,
        })

    def success(self, message, duration=3000):
        self.notify(message, "success", duration)

    def error(self, message, duration=5000):
        self.notify(message, "error", duration)

    def warning(self, message, duration=4000):
        self.notify(message, "warning", duration)

    def info(self, message, duration=3000):
        self.notify(message, "info", duration)

    def start(self):
        root = self._get_root()
        root.after(100, self._process_queue)
        root.mainloop()


class Toast:
    def __init__(self, root, data, manager):
        self.manager = manager
        self.message = data["message"]
        self.level = data.get("level", "info")
        self.duration = data.get("duration", 3000)
        self.visible = True

        self.colors = {
            "success": ("#D1FAE5", "#065F46", "#10B981"),
            "error": ("#FEE2E2", "#991B1B", "#EF4444"),
            "warning": ("#FEF3C7", "#92400E", "#F59E0B"),
            "info": ("#DBEAFE", "#1E40AF", "#3B82F6"),
        }

        self.window = tk.Toplevel(root)
        self.window.withdraw()
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)

        bg, fg, icon_bg = self.colors.get(self.level, self.colors["info"])

        icons = {
            "success": "✓",
            "error": "✕",
            "warning": "⚠",
            "info": "ℹ",
        }

        self.frame = tk.Frame(self.window, bg=bg, padx=16, pady=12)
        self.frame.pack()

        tk.Label(
            self.frame,
            text=icons.get(self.level, "ℹ"),
            bg=bg,
            fg=fg,
            font=("Segoe UI", 12, "bold"),
        ).pack(side="left", padx=(0, 10))

        tk.Label(
            self.frame,
            text=self.message,
            bg=bg,
            fg=fg,
            font=("Segoe UI", 10),
            wraplength=320,
            justify="left",
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            self.frame,
            text="✕",
            bg=bg,
            fg=fg,
            relief="flat",
            bd=0,
            font=("Segoe UI", 9, "bold"),
            command=self.dismiss,
            cursor="hand2",
        ).pack(side="right")

        self.window.update_idletasks()
        width = self.window.winfo_reqwidth()
        screen_width = root.winfo_screenwidth()
        x = screen_width - width - 20

        existing = len(manager.toasts)
        y = 20 + existing * 70

        self.window.geometry(f"+{x}+{y}")
        self.window.deiconify()

        self._animate_in()

        self.window.after(self.duration, self._auto_dismiss)

    def _animate_in(self):
        self.window.attributes("-alpha", 0.0)
        self._fade_to(1.0, 20)

    def _fade_to(self, target, steps):
        current = self.window.attributes("-alpha")
        if abs(current - target) < 0.05:
            self.window.attributes("-alpha", target)
            return

        step = (target - current) / max(steps, 1)
        new_alpha = current + step
        self.window.attributes("-alpha", new_alpha)
        self.window.after(15, lambda: self._fade_to(target, max(steps - 1, 1)))

    def _auto_dismiss(self):
        if self.visible:
            self.dismiss()

    def dismiss(self):
        if not self.visible:
            return
        self.visible = False
        self._fade_to(0.0, 10)
        self.window.after(200, self._destroy)

    def _destroy(self):
        try:
            self.window.destroy()
        except Exception:
            pass

    def is_alive(self):
        return self.visible and self.window.winfo_exists()


manager = ToastManager()


def notify(message, level="info", duration=3000):
    manager.notify(message, level, duration)


def success(message, duration=3000):
    manager.success(message, duration)


def error(message, duration=5000):
    manager.error(message, duration)


def warning(message, duration=4000):
    manager.warning(message, duration)


def info(message, duration=3000):
    manager.info(message, duration)
