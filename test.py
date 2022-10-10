from heapq import merge
from importlib.resources import path
from moviepy.editor import *
import moviepy.audio.fx.all as afx
import os
import tkinter as tk
from tkinter import filedialog
import numpy
from numpy import *
import logging

#该版本会无视文件长度，每个文件截取中间80%的内容，然后凑到5分钟

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
    pending_list = []
    video_file_clip = []
    #video_file = []
    #files= os.listdir(path) #得到文件夹下的所有文件名称
    files= os.walk(path)
    a=[]
    for file_path,dir_list,file_list in files:  
        for file_name in file_list:  
            a.append(os.path.join(file_path, file_name))
    
    for file in a: #遍历文件夹
        if os.path.splitext(file)[-1] in ['.mp4']: #判断是否是音频，是音频才打开
            pending_list.append(file)#把待处理文件塞进数组
    while 1:
        while 1:
            if(len(video_file_clip)<2): #如果待处理list元素小于两个2，则去取元素
                return_file,bad_files = selectRandomVideo(pending_list,1)
                pending_list.remove(return_file)
                for bad_file in bad_files:
                    pending_list.remove(bad_file)
                #video_file.append(return_file)
                video_file_clip.append(VideoFileClip(return_file))
            else:#如果待处理list元素等于两个，则将视频进行拼接，并返回拼接后的元素
                result_video = editorMov(video_file_clip)                
                while result_video.duration < 400:
                    print("pingjiehou d shichang:",result_video.duration)
                    return_file,bad_files = selectRandomVideo(pending_list,1)
                    pending_list.remove(return_file)
                    for bad_file in bad_files:
                        pending_list.remove(bad_file)
                    video_file_clip.append(VideoFileClip(return_file))
                    result_video = editorMov(video_file_clip)
                
                speed_up(result_video,1.4,path_new)
                result_video.close()
                video_file_clip.clear()
                break
            if(len(pending_list)<1):
                print("没有待处理文件了")
                break

        if(len(pending_list)<1):
            print("没有待处理文件了")
            break   
            

        

#目的：取 1 个分辨率符合要求的视频,f返回路径
def selectRandomVideo(pending_list,videonum):    
        i=0
        bad_file = []        
        while i < videonum: #循环取 videonum 个 大于 video_dur 的视频
            randomfile = numpy.random.choice(pending_list,1,replace=False)[0]
            #pending_list.remove(randomfile) #删除文件
            print("randomfile is :"+randomfile)
            #random_file_path = os.path.join(path,randomfile)
            try:
                randomvideo = VideoFileClip(randomfile)
            except KeyError: #有些文件VideoFileClip会读取失败，直接删除
                print('keyerror')
                bad_file.append(randomfile)
                randomvideo.close()
                os.remove(randomfile)
                continue
            #需要判断分辨率，不满足的也删除
            if randomvideo.duration > 10 and randomvideo.w >= 512 and randomvideo.h >= 384:                                         
                i = i + 1
                randomvideo.close() #释放内存，解除文件占用
            else:
                print("the file dur is too short,delete file:",randomfile)
                print("dur:",'%f' % randomvideo.duration)
                print('randomvideo.w:',randomvideo.w)           
                print('randomvideo.h:',randomvideo.h)
                randomvideo.close() #释放内存，解除文件占用
                bad_file.append(randomfile)
                #os.remove(randomfile)#直接删除时长不足的视频
        return randomfile,bad_file

def editorMov(files): #裁剪，
    cut_video = []
    for file in files:
        #file_path = os.path.join(path,file)#把待处理文件拼接上绝对路径
        #au = VideoFileClip(file)
        au = file
        cut_out_time = int(au.duration/10)
        print('cut out time',cut_out_time)
        au = au.subclip(cut_out_time,-cut_out_time)
        #au = au.resize((800,600)) #调整分辨率，但不裁剪，会拉伸和缩放
        au = au.crop(x_center=au.w/2,y_center=au.h/2,width=512,height=384)#以视频中心为原点，裁剪一个640x480的矩形
        cut_video.append(au)

    new_video = concatenate_videoclips(cut_video,method="compose")#拼接
    return new_video

def speed_up(new_video,accelerate_num,path_new):

    result_video = new_video.fl_time(lambda t:  accelerate_num*t, apply_to=['mask', 'audio'])
    result_video = result_video.set_duration(new_video.duration/accelerate_num)#加速1.4倍
    result_video = result_video.without_audio() #静音
    pathnew = os.path.join(path_new,ranstr(8)+".mp4")
    print('new file:',pathnew)
    result_video.write_videofile(pathnew)#将处理好的文件写到新文件夹中
    result_video.close()
        
    # #删除用过的文件
    # for file in files:
    #     file_path = os.path.join(path,file)#把待处理文件拼接上绝对路径
    #     os.remove(file_path)
    #     print("完事，删除用过的文件，路径：",file_path)


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

