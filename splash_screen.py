import tkinter as tk
from ttkthemes import ThemedStyle
from tkinter import ttk

splashScreenWin = tk.Tk()
splashScreenWin.title("Bluvid - Poel")
splashScreenWin.geometry("300x200")
splashScreenWin.overrideredirect(True)
splashScreenWin.config(bg="#000000")
splashScreenWin.tk_setPalette(background='#11d9c7')
splashScreenWin.resizable(width=False, height=False)
style = ThemedStyle(splashScreenWin)
style.set_theme("arc")

def closeSplash():
	splashScreenWin.destroy()

splashScreenWin.after(3000, closeSplash)

loadbar = ttk.Progressbar(splashScreenWin, length=200)
loadbar.pack(pady=70)

loadbar.start()

tk.Label(splashScreenWin, bg="black", fg="white",text="Loading...").pack()

splashScreenWin.mainloop()