import tkinter
from subprocess import call
import os
from tkinter import Image
import threading
import ctypes
import argparse
import wmi

f=wmi.WMI()
Allowed=True
BannedTerms=["cheat","inject","hack","glitch","exploit","hax","mod","0x0","roblox","aimbot","esp","wallhax","wallhacks","aimassist","aim assist","softaim","soft aim"]

parser=argparse.ArgumentParser()
parser.add_argument("-launch", default="", help="Program to launch if anticheat returns safe enviornment.", required=True)
parser.add_argument("-scantype", default="once", help="Default: \'once\' options are \'once\' or \'forever\'.", required=True)
args=parser.parse_args()
launchapp=args.launch
scanmode=args.scantype

def GUI():
	root=tkinter.Tk()
	root.overrideredirect(True)
	root.minsize(500,300)
	root.geometry("500x300")
	root.geometry("+{}+{}".format(int(root.winfo_screenwidth()/2-500/2),int(root.winfo_screenheight()/2-300/2)))
	root.attributes('-alpha',1)
	root.configure(bg='black')
	root.title("TrashAC Launcher")
	#Widgets
	image=tkinter.PhotoImage(file="./assets/TrashAC_Logo.png")
	tkinter.Label(root,image=image).pack()
	#End Widgets
	def CloseGUI():
		root.destroy()
	root.after(5000, CloseGUI)
	root.mainloop()

guithread=threading.Thread(target=GUI)
guithread.start()
EnumWindows=ctypes.windll.user32.EnumWindows
EnumWindowsProc=ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.POINTER(ctypes.c_int),ctypes.POINTER(ctypes.c_int))
GetWindowText=ctypes.windll.user32.GetWindowTextW
GetWindowTextLength=ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible=ctypes.windll.user32.IsWindowVisible
titles=[]

def foreach_window(hwnd, lParam):
	if IsWindowVisible(hwnd):
		length = GetWindowTextLength(hwnd)
		buff = ctypes.create_unicode_buffer(length + 1)
		GetWindowText(hwnd, buff, length + 1)
		titles.append(buff.value)
	return True

EnumWindows(EnumWindowsProc(foreach_window), 0)
listedprograms=f.Win32_Process()

for process in listedprograms:
	for term in BannedTerms:
		if term in process.Name.lower() and "module" not in process.Name.lower():Allowed=False
for title in titles:
	for term in BannedTerms:
		if term in title.lower() and "anticheat" not in title.lower():Allowed=False
if Allowed == True:
	os.system("start \"Program started by Trash AntiCheat\" \""+launchapp+"\"")
if scanmode.lower() != "once":
	while True:
		EnumWindows=ctypes.windll.user32.EnumWindows
		EnumWindowsProc=ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.POINTER(ctypes.c_int),ctypes.POINTER(ctypes.c_int))
		GetWindowText=ctypes.windll.user32.GetWindowTextW
		GetWindowTextLength=ctypes.windll.user32.GetWindowTextLengthW
		IsWindowVisible=ctypes.windll.user32.IsWindowVisible
		titles=[]
		EnumWindows(EnumWindowsProc(foreach_window), 0)
		listedprograms=f.Win32_Process()
		for process in listedprograms:
			for term in BannedTerms:
				if term in process.Name.lower() and "module" not in process.Name.lower():Allowed=False
		for title in titles:
			for term in BannedTerms:
				if term in title.lower() and "anticheat" not in title.lower():Allowed=False
		if Allowed == False:
			print("HELP!!!")
else:
	exit()