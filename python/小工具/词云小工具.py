import time
import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import stylecloud
import uuid


def browser_file():
    """
    :return:
    """
    file = filedialog.askopenfilename(title='选择文件', filetypes=[('txt', '*.txt')])
    path.set(file)
    # 调用函数生成词云，并打开显示
    output_name = generator(file)
    img_file = Image.open(output_name)
    img = ImageTk.PhotoImage(img_file)
    img_label.config(image=img)
    img_label.image = img


def generator(filename: str):
    """
    :param filename:
    :return:
    """
    output_name = f'{uuid.uuid1()}.png'
    # 生成cloud.png
    stylecloud.gen_stylecloud(file_path=filename
                              , icon_name = "fas fa-grin"    # 图形形状
                              , output_name = output_name
                              , size = 800
                              , max_font_size = 2000
                              , max_words = 100
                              , font_path = "msyh.ttc")
    return output_name


root = Tk()
root.title('千库词云')    # 窗口标题
root.geometry('800x800+100+100')    # 窗口位置,宽x高+左距+上距离
content = ttk.Frame(root)
content.grid(column=0, row=0)
path = tkinter.StringVar()
pic = ttk.Entry(content, textvariable=path, width=30)
button = ttk.Button(content, text="打开文本文件", command=browser_file)

# 布局
pic.grid(column=0, row=0)
button.grid(column=1, row=0)
img_frame = ttk.Frame(root, width=160, height=200, borderwidth=2)
img_label = ttk.Label(img_frame, borderwidth=0)
img_frame.grid(column=0, row=1)
img_label.grid(column=0, row=1)
root.mainloop()