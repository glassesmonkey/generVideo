# generVideo

## 怎么使用

pip3 install -r requirement.txt

python3 main.py
或者
python3 test.py

## main.py和test.py的区别
main.py 会选取长度超过20s的文件进行掐头去尾，随机拼接，凑成一个五分钟的视频
test.py 会无视文件长度，每个文件掐头去尾，凑成一个五分钟的视频

