#!/usr/bin/env python
# coding=utf-8
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import tkinter
from tkinter import filedialog, Entry, StringVar, Label, messagebox, IntVar

global reduce_px
global save
global entry_text
global scale_input
global image_path
global gap


class Ghs:
    def __init__(self, path, image_txt, save_path):
        self.image = path
        self.txt = image_txt
        self.pixel = 10
        self.save_path = save_path

    def start(self):
        global reduce_px
        global gap
        img = cv2.imread(self.image)
        height, width, channel = img.shape
        nb = 0
        fontstyle = ImageFont.truetype("../fonts/simsun.ttc", 5 * reduce_px, encoding="utf-8")
        (w, h) = fontstyle.getsize(self.txt[nb % len(self.txt)])
        canvas = np.ones((height, width, 3), dtype="uint8")
        canvas[:] = (255, 255, 255)
        canvas = Image.fromarray(cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(canvas)
        for i in range(int(height/(h+gap))):
            for j in range(int(width/(w+gap))):
                [R, G, B] = img[i * (h + gap) + int(h/2), j * (w + gap) + int(w/2)]
                draw.text((j*(w+gap), i*(h+gap)), self.txt[nb % len(self.txt)],
                          (B, G, R), fontstyle)
                # cv2.putText(canvas, text=self.txt[nb % len(self.txt)], org=(j*10, i*10),
                            # fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, thickness=1, lineType=cv2.LINE_AA,
                            # color=(int(color[i][j][0]), int(color[i][j][1]), int(color[i][j][2])))
                nb += 1
        canvas = cv2.cvtColor(np.asarray(canvas), cv2.COLOR_RGB2BGR)
        cv2.imwrite(self.save_path + ".jpg", canvas)


def ImageCallBack():
    global image_path
    image_path = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("jpeg files","*.jpg"),("all files","*.*")))


def SavePathCallBack():
    global save
    global image_path
    global reduce_px
    global gap
    reduce_px = scale_input.get()
    gap = gap_input.get()
    save = filedialog.asksaveasfilename(initialdir="/", filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
    if save and entry_text.get() and image_path and scale_input.get() in range(1, 21) and gap_input.get() in range(1, 11):
        ghs = Ghs(image_path, entry_text.get(), save)
        ghs.start()
        print(save)
        messagebox.showinfo("成功", "转换完成")
    elif not (scale_input.get() in range(1, 21)):
        messagebox.showerror("错误", "请输入正确的倍数")
    elif not (gap_input.get() in range(1, 11)):
        messagebox.showerror("错误", "请输入字间距")


if __name__ == '__main__':
    top = tkinter.Tk()
    b = tkinter.Button(top, text="图片文件", command=ImageCallBack)
    entry_text = StringVar()
    textbox = Entry(top, textvariable=entry_text)
    entry_text.set('abc')

    scale_input = IntVar()
    scale_box = Entry(top, textvariable=scale_input)
    scale_input.set(6)

    gap_input = IntVar()
    gap_box = Entry(top, textvariable=gap_input)
    gap_input.set(5)

    b2 = tkinter.Button(top, text="开始转换", command=SavePathCallBack)
    b.pack()
    Label(top, text="填充文字").pack(pady=10, padx=10)
    textbox.pack(pady=10, padx=10)
    Label(top, text="缩放倍数1-20").pack(pady=10, padx=10)
    scale_box.pack(pady=10, padx=10)
    Label(top, text="字间距1-10px").pack(pady=10, padx=10)
    gap_box.pack(pady=10, padx=10)
    b2.pack()
    top.mainloop()
