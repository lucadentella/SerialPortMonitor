
# Serial Port Monitor
Windows SystemTray App that shows the list of **serial ports**.

## Why
Whenever I needed to connect to a USB-to-serial device, I couldn't quickly figure out which COM port it was connected to; so I developed a simple application to quickly get the information I needed.

## How it works
When run, it adds an icon to the **Windows system tray.**

Hovering the mouse over the icon displays a list of serial ports and their descriptions:

![](https://github.com/lucadentella/SerialPortMonitor/raw/main/images/list.png)

Whenever a serial port is added or removed, the application displays a notification:

![](https://github.com/lucadentella/SerialPortMonitor/raw/main/images/add.png)

![](https://github.com/lucadentella/SerialPortMonitor/raw/main/images/remove.png)

Right-clicking the icon provides a menu to enable/disable notifications or close the application:

![](https://github.com/lucadentella/SerialPortMonitor/raw/main/images/menu.png)

## Download
Pre-compiled versions of the application are available in the [Releases](https://github.com/lucadentella/SerialPortMonitor/releases) section.

## Build
The application is developed in [Python](https://www.python.org/). To run it, you need to install the following libraries via **pip**:

```pip install pywin32 pystray pyserial pillow winotify```

To generate a Windows executable, you need to use the **pyinstaller** utility:

```pip install pyinstaller```

and pass the .spec file available in the repository as a parameter

```pyinstaller --clean SerialPortMonitor.spec```