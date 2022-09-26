from heapq import merge
from importlib.resources import path
from moviepy.editor import *
import moviepy.audio.fx.all as afx
import os
import tkinter as tk
from tkinter import filedialog
import numpy
from numpy import *

def selectRandomVideo(names,videonum):#随机选择一定数量的文件
    return numpy.random.choice(names,videonum,replace=False)

def editorMov(files,path_new): #编辑视频文件，先裁剪拼接，再加速静音
    cut_video = []
    for file in files:
        file_path = os.path.join(path,file)#把待处理文件凭借上绝对路径
        au = VideoFileClip(file_path)
        #au = au.subclip(au.duration/2-10,au.duration/2+10) #从中间裁剪出20秒
        cut_video.append(au)
    print("cut video:")
    print(cut_video)
    new_video = concatenate_videoclips(cut_video,method="compose")
    # merge_video.write_videofile(path_new +'/jiasuqian'+"result.mp4")
    # new_video = VideoFileClip(path_new +'/jiasuqian'+"result.mp4")
    result_video = new_video.fl_time(lambda t:  1.4*t, apply_to=['mask', 'audio'])
    result_video = result_video.set_duration(new_video.duration/1.4)
    result_video.write_videofile(path_new+'/'+"result.mp4")#将处理好的文件写到新文件夹中

#获取源文件的路径
root = tk.Tk()
root.withdraw()
path = filedialog.askdirectory()
#设定输出文件的路径
path_new = filedialog.askdirectory()
#读取目录下所有文件，筛选4个文件
#将文件裁剪，拼接
#将拼接的文件加速，静音
files= os.listdir(path) #得到文件夹下的所有文件名称
#print(files)
s = []
for file in files: #遍历文件夹
    if os.path.splitext(file)[-1] in ['.mp3','.mp4']: #判断是否是音频，是音频才打开
        s.append(file)#把待处理文件塞进数组
        
print("筛选出mp3和mp4")
print(s)
s1 = selectRandomVideo(s,3)
print("随机选3个文件")
print(s1) #打印结果
editorMov(s1,path_new)
