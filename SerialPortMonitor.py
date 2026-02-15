import sys
import os
import threading
import serial.tools.list_ports
import pystray
from PIL import Image

from winotify import Notification, audio

import win32con
import win32gui


def resource_path(relative_path):
    """Correct path both in development and in PyInstaller executable."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def list_serial_ports():
    """Returns a list of tuples (port, description)."""
    ports = serial.tools.list_ports.comports()
    return [(p.device, p.description) for p in ports]


def show_notification(title, message):
    """Send a Windows toast notification using winotify."""
    toast = Notification(
        app_id="Serial Port Monitor",
        title=title,
        msg=message,
        icon=resource_path("icon.ico")
    )
    toast.set_audio(audio.Default, loop=False)
    toast.show()


class SerialTrayApp:
    def __init__(self):
        self.icon = pystray.Icon("SerialPortMonitor")

        # Load external icon (compatible with PyInstaller)
        icon_path = resource_path("icon.ico")
        self.icon.icon = Image.open(icon_path)

        # Notifications enabled by default
        self.notifications_enabled = True

        # Initial port list
        self.last_ports = list_serial_ports()

        self.update_tooltip()

        self.icon.menu = pystray.Menu(
            pystray.MenuItem(
                lambda item: "Disable notifications" if self.notifications_enabled else "Enable notifications",
                self.toggle_notifications
            ),
            pystray.MenuItem("Exit", self.exit_app)
        )

        # Thread for hidden window receiving device events
        self.running = True
        self.event_thread = threading.Thread(target=self.device_event_loop, daemon=True)
        self.event_thread.start()

    # -----------------------------
    #   SYSTEM TRAY
    # -----------------------------
    def update_tooltip(self):
        ports = list_serial_ports()
        if ports:
            lines = []
            for port, desc in ports:
                if desc:
                    lines.append(f"{port} - {desc}")
                else:
                    lines.append(port)
            tooltip = "Serial ports:\n" + "\n".join(lines)
        else:
            tooltip = "No serial ports detected"

        self.icon.title = tooltip

    def toggle_notifications(self, icon, item):
        self.notifications_enabled = not self.notifications_enabled

    def exit_app(self, icon, item):
        self.running = False
        win32gui.PostQuitMessage(0)
        self.icon.stop()

    # -----------------------------
    #   WINDOWS DEVICE EVENTS
    # -----------------------------
    def device_event_loop(self):
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self.wnd_proc
        wc.lpszClassName = "HiddenDeviceListener"
        class_atom = win32gui.RegisterClass(wc)

        hwnd = win32gui.CreateWindow(
            class_atom,
            "HiddenDeviceListenerWindow",
            0,
            0, 0, 0, 0,
            0, 0, 0, None
        )

        win32gui.PumpMessages()

    def wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == win32con.WM_DEVICECHANGE:
            if wparam in (win32con.DBT_DEVICEARRIVAL, win32con.DBT_DEVICEREMOVECOMPLETE):
                self.handle_device_change()
        return True

    def handle_device_change(self):
        current_ports = list_serial_ports()

        old_set = set([p[0] for p in self.last_ports])
        new_set = set([p[0] for p in current_ports])

        added = new_set - old_set
        removed = old_set - new_set

        if self.notifications_enabled:
            for port in added:
                desc = next((d for p, d in current_ports if p == port), "")
                msg = f"{port} - {desc}" if desc else f"{port} connected"
                show_notification("New serial port detected", msg)

            for port in removed:
                desc = next((d for p, d in self.last_ports if p == port), "")
                msg = f"{port} - {desc}" if desc else f"{port} disconnected"
                show_notification("Serial port removed", msg)

        self.last_ports = current_ports
        self.update_tooltip()

    # -----------------------------
    #   RUN
    # -----------------------------
    def run(self):
        self.icon.run()


if __name__ == "__main__":
    app = SerialTrayApp()
    app.run()
