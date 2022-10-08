from wxauto import WeChat
 
# 获取当前微信客户端
wx = WeChat()
 
# 获取会话列表
wx.GetSessionList()
 
with open("C:\\Users\\mmm\\Desktop\\test.txt","r",encoding="gbk")as f:  #这个.txt里写要发送的文字
    for line in f.readlines():
        who = '' #这里填要发送的人的备注
        wx.ChatWith(who)
        wx.SendMsg(line)