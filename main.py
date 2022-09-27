from heapq import merge
from importlib.resources import path
from moviepy.editor import *
import moviepy.audio.fx.all as afx
import os
import tkinter as tk
from tkinter import filedialog
import numpy
from numpy import *

def selectRandomVideo(names,videonum,video_require_dur):#随机选择一定数量的文件
    i=0
    s=[]
    while i < videonum: #循环取 videonum 个 大于 video_dur 的视频
        randomfile = numpy.random.choice(names,1,replace=False)[0]
        names.remove(randomfile)
        print("randomfile is :"+randomfile)
        random_file_path = os.path.join(path,randomfile)
        randomvideo = VideoFileClip(random_file_path)
        if randomvideo.duration > video_require_dur: #判断文件时长，如果大于20s，则加入数组，小于20s则删除源文件
            print("video dur is: ")
            print('%f' % randomvideo.duration)
            s.append(randomfile)            
            i = i + 1
        else:
            print("the file dur is too short,delete file."+randomvideo.duration)
            os.remove(random_file_path)
    return s

def editorMov(files,path_new,dur_time,accelerate_num): #编辑视频文件，先裁剪拼接，再加速静音
    cut_out_time = dur_time/2 * accelerate_num
    cut_video = []
    for file in files:
        file_path = os.path.join(path,file)#把待处理文件凭借上绝对路径
        au = VideoFileClip(file_path)
        print("au.duration/2-10 = ")
        print(au.duration/2-10)
        print("au.duration/2+10 = ")
        print(au.duration/2+10)
        au = au.subclip(au.duration/2-cut_out_time,au.duration/2+cut_out_time) #从中间裁剪出20秒
        cut_video.append(au)
    print("cut video:")
    print(cut_video)
    new_video = concatenate_videoclips(cut_video,method="compose")#拼接
    result_video = new_video.fl_time(lambda t:  accelerate_num*t, apply_to=['mask', 'audio'])
    result_video = result_video.set_duration(new_video.duration/accelerate_num)#加速1.4倍
    result_video = result_video.without_audio() #静音
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
print("随机选3个文件")
s1=selectRandomVideo(s,3,25)
print(s1) #打印结果
editorMov(s1,path_new,20,1.4)
