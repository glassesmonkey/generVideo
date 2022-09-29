from http.client import PAYMENT_REQUIRED
import tkinter
from tkinter import * 
import tkinter as tk
from tkinter import filedialog,messagebox

from numpy import pad

def get_source_path():
    path = filedialog.askdirectory()
    entry1.insert(0,path)

def get_new_path():
    path = filedialog.askdirectory()
    entry2.insert(0,path)

def start():
    return
root_window = tk.Tk()
root_window.title('glassesmonkey')
root_window.geometry('450x300')

labe1 = tk.Label(root_window,text="源文件路径")
labe2 = tk.Label(root_window,text="处理后文件路径")
labe1.grid(row=0)
labe2.grid(row=1)
# 添加按钮，以及按钮的文本，并通过command 参数设置关闭窗口的功能
entry1 = tk.Entry(root_window)

entry2 = tk.Entry(root_window)

entry1.grid(row=0,column=1)
entry2.grid(row=1,column=1)

button1=tk.Button(root_window,text="选择",command=get_source_path)
button2=tk.Button(root_window,text="选择",command=get_new_path)
button3=tk.Button(root_window,text="启动！",command=start)
button1.grid(row=0,column=2)
button2.grid(row=1,column=2)
button3.grid(row=2,column=2)
root_window.mainloop()
