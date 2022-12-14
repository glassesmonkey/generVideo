from heapq import merge
from importlib.resources import path
from moviepy.editor import *
import moviepy.audio.fx.all as afx
import os
import tkinter as tk
from tkinter import filedialog
import numpy
from numpy import *

def get_source_path():
    path = filedialog.askdirectory()
    entry1.delete(0, "end")
    entry1.insert(0,path)

def get_new_path():
    path = filedialog.askdirectory()
    entry2.delete(0, "end")
    entry2.insert(0,path)

def start():
    main(entry1.get(),entry2.get())

def main(path,path_new):
    while 1:
        #files= os.listdir(path) #得到文件夹下的所有文件名称
        files= os.walk(path)
        a = []
        for file_path,dir_list,file_list in files:  
            for file_name in file_list:  
                a.append(os.path.join(file_path, file_name))
        s = []
        for file in a: #遍历文件夹
            if os.path.splitext(file)[-1] in ['.mp4']: #判断是否是音频，是音频才打开
                s.append(file)#把待处理文件塞进数组
        if  len(s) >= file_num: #当列表中的文件大于等于三个时才操作
            print("筛选出mp3和mp4:",s)
            s1=selectRandomVideo(s,file_num,video_min_dur,path)
            print("随机选择三个文件",s1)
            editorMov(s1,path_new,20,1.4,path)
        else:
            print("可操作文件少于",file_num,"个，程序退出")
            break

def selectRandomVideo(names,videonum,video_require_dur,path):#循环取 videonum 个 视频时长大于 video_require_dur 的视频
    i=0
    s=[]
    while i < videonum: #循环取 videonum 个 大于 video_dur 的视频
        randomfile = numpy.random.choice(names,1,replace=False)[0]
        names.remove(randomfile)
        print("randomfile is :"+randomfile)
        random_file_path = os.path.join(path,randomfile)
        try:
            randomvideo = VideoFileClip(random_file_path)
        except KeyError:
            print('keyerror')
            randomvideo.close()
            os.remove(random_file_path)
            continue
        
        #判断文件时长，如果大于20s，则加入数组，小于20s则删除源文件。还需要判断分辨率，不满足的也删除
        if randomvideo.duration > video_require_dur and randomvideo.w >= 640 and randomvideo.h >= 480: 
            print("video dur is: ",'%f' % randomvideo.duration)
            s.append(randomfile)            
            i = i + 1
            randomvideo.close() #释放内存，解除文件占用
        else:
            print("the file dur is too short,delete file")
            print("dur:",'%f' % randomvideo.duration)
            print('randomvideo.w:',randomvideo.w)           
            print('randomvideo.h:',randomvideo.h)
            randomvideo.close() #释放内存，解除文件占用
            os.remove(random_file_path)#直接删除时长不足的视频
        
    return s

def editorMov(files,path_new,dur_time,accelerate_num,path): #编辑视频文件，先裁剪拼接，再加速静音，dur_time=时长，accelerate_num=加速倍数
    cut_out_time = dur_time/2 * accelerate_num
    cut_video = []
    for file in files:
        file_path = os.path.join(path,file)#把待处理文件拼接上绝对路径
        au = VideoFileClip(file_path)
        au = au.subclip(au.duration/2-cut_out_time,au.duration/2+cut_out_time) #从中间裁剪出20秒
        #au = au.resize((800,600)) #调整分辨率，但不裁剪，会拉伸和缩放
        au = au.crop(x_center=au.w/2,y_center=au.h/2,width=640,height=480)#以视频中心为原点，裁剪一个640x480的矩形
        cut_video.append(au)
    print("cut video:",cut_video)
    new_video = concatenate_videoclips(cut_video,method="compose")#拼接
    result_video = new_video.fl_time(lambda t:  accelerate_num*t, apply_to=['mask', 'audio'])
    result_video = result_video.set_duration(new_video.duration/accelerate_num)#加速1.4倍
    result_video = result_video.without_audio() #静音
    pathnew = os.path.join(path_new,ranstr(8)+".mp4")
    result_video.write_videofile(pathnew)#将处理好的文件写到新文件夹中
    result_video.close()
    for cutfile in cut_video:
        cutfile.close()#释放内存，解除文件占用
        
    #删除用过的文件
    for file in files:
        file_path = os.path.join(path,file)#把待处理文件拼接上绝对路径
        os.remove(file_path)
        print("完事，删除用过的文件，路径：",file_path)


def ranstr(num):#返回一个随机字串，用于生成随机文件名
    H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_'
    result1 = list(H)
    salt = ''
    for i in range(num):
        salt =salt + random.choice(result1)

    return salt



#获取源文件的路径
file_num = 12 #拼接用的文件数量
video_min_dur = 25
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

