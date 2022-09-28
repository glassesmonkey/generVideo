from moviepy.editor import *

au = VideoFileClip("/Users/yxgc/Desktop/1.mp4")
print(au.w/2)
print(au.h/2)
au = au.crop(x_center=au.w/2,y_center=au.h/2,width=640,height=480)
au.write_videofile("/Users/yxgc/Desktop/6.mp4")