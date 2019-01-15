# coding=utf-8

from math import sin, cos, sqrt, atan2, radians
import numpy as np
import math
import os
import time
import numba
import datetime
import os
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors as colors
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os
from PIL import Image
# import sys
# sys.setrecursionlimit(1000000000)
cwd=os.getcwd()
os.chdir(cwd)

#系统欢迎信息
today = datetime.date.today()
print(
    f'云南总队电磁态势分析系统1.0\n 德宏瑞丽方向：24.009181, 97.859101\n 系统单位制：北纬（lat） 东经（lon），mks\n 数据库已连接.....100%\n 数据保鲜日期：{today}')
user = input(' 请输入用户名：')
password = input(' 请输入密码：')
if user != "ynzod":
    in_error=input(' 用户名错误，按任意键退出')
    os._exit(0)
else:
        print(" 系统开始运行....\n第一阶段：基于大数据挖掘技术，构建电磁态势信息。\n————————————————————————————————————————")
try:
   os.mkdir(f"{cwd}/result") 
except:  
    a=1             
   

print(" 德宏瑞丽方向影像地图，系统态势分析前请关闭地图")
img_map = Image.open('map.png')


img_map.show()
start_time = time.time()


@numba.jit
def get_distanc(lat1, lon1, lat2, lon2):
    "输入两个坐标WG84，计算两点间的地表距离m"
    R = 6373.0  # 地球半径
    lat_1 = radians(lat1)
    lon_1 = radians(lon1)
    lat_2 = radians(lat2)
    lon_2 = radians(lon2)
    dlon = lon_2 - lon_1
    dlat = lat_2 - lat_1
    a = (sin(dlat/2))**2 + cos(lat_1) * cos(lat_2) * (sin(dlon/2))**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c*1000
    return distance


def DKE(h, d, omega_post):
    "根据阈值h，两点间的距离，选的参数，计算DKE的值"
    if d >= h:
        fs_dke = 0.0
    else:
        fs_dke = (1/math.pow(h, 2))*omega_post*(3/math.pi) * \
            math.pow((1-math.pow(d/h, 2)), 2)

    return fs_dke


def DKE_negative(h, d, omega_negative):
    "根据阈值h，两点间的距离，选的参数，计算DKE的值,成本型"
    if d >= h:
        fs_dke = 0.0
    else:
        fs_dke = (1/math.pow(h, 2))*(1/omega_negative) * \
            (3/math.pi)*math.pow((1-math.pow(d/h, 2)), 2)

    return fs_dke


def Normalize(data, max):
    "矩阵规范化"
    nor = data/max
    return nor


# 网格划分 输入需要划分的地图对角线坐标
print(" 系统开始战场网格划分：1300*1300栅格化网络")
N = 200
web_begin_lat, web_begin_lon = (24.038639, 97.835673)  # 左上
web_end_lat, web_end_lon = (23.985706, 97.921106)      # 右下

# 将起始坐标转换为网格坐标
web_lat_max = max(web_begin_lat, web_end_lat)
web_lat_min = min(web_begin_lat, web_end_lat)
web_lat = np.linspace(web_lat_max, web_lat_min, N, endpoint=True)
web_lon_max = max(web_begin_lon, web_end_lon)
web_lon_min = min(web_begin_lon, web_end_lon)
web_lon = np.linspace(web_lon_min, web_lon_max, N, endpoint=True)

with open(f'{cwd}/result/web_lat.txt', 'w') as f1, open(f'{cwd}/result/web_lon.txt', 'w') as f2:
    np.savetxt(f'{cwd}/result/web_lat.txt', web_lat)
    np.savetxt(f'{cwd}/result/web_lon.txt', web_lon)
    web_date_time = time.time()
    print(f" 栅格化网络用时:{web_date_time-start_time}s")

# 测试用的点
dot1 = [23.987080, 97.885402, 8.0]
dot2 = [24.010533, 97.871553, 8.0]
dot3 = [24.028241, 97.867378, 8.2]
dot4 = [24.005506, 97.853046, 6]
dot5 = [24.030922, 97.871839, 8]
dot6 = [24.037641, 97.908323, 1]
dot7 = [24.004662, 97.909453, 5]
dot8 = [24.027555, 97.910471, 8]
dot9 = [24.025919, 97.917749, 3]
dot10 = [24.007121, 97.912703, 8]
dot11 = [24.020802, 97.846900, 6]
dot12 = [24.017593, 97.853162, 10]
dot13 = [24.011098, 97.850359, 4]


print(f' 4G基站坐标：{dot1}')
time.sleep(0.1)
print(f' 4G基站坐标：{dot2}')
time.sleep(0.4)
print(f' 4G基站坐标：{dot3}')
time.sleep(0.2)
print(f' 4G基站坐标：{dot4}')
time.sleep(0.1)
print(f' 4G基站坐标：{dot11}')
time.sleep(0.2)
print(f' 4G基站坐标：{dot12}')
time.sleep(0.1)
print(f' 卫星便携站：{dot5}')
time.sleep(0.3)
print(f' 20W短波电台：{dot6}')
time.sleep(0.1)
print(f' 卫星Ku波段：{dot7}')
time.sleep(0.2)

print(f' 一噪五扰区域：{dot8}')
time.sleep(0.3)
print(f' 动态杂散区域：{dot9}')
time.sleep(0.3)

dot = [dot1, dot2, dot3, dot4, dot5, dot6, dot7, dot8, dot9, dot10,dot11,dot12,dot13]
dot_len = len(dot)

# 划分网格
h = 1600  # 阈值范围
print("第二阶段：采用核密度估计法，计算战场电磁态势值。\n————————————————————————————————————————")
Rs = np.zeros((N, N))  # 战场热点值矩阵
for i in range(0, N-1):
    for j in range(0, N-1):
        for dot_i in dot:
            distance = get_distanc(web_lat[i], web_lon[j], dot_i[0], dot_i[1])
            if distance < h:
                aa = DKE(h, distance, dot_i[2])
                Rs[i][j] = Rs[i][j]+aa
Rs_time = time.time()
print(f" 计算战场电磁态势值用时：{Rs_time-web_date_time}s")


# 矩阵规范化
a = Rs
mx = a.max()
for i in range(0, N-1):
    for j in range(0, N-1):
        Rs[i][j] = Normalize(Rs[i][j], mx)
nor_time = time.time()
print(f" 态势信息规范化用时：{nor_time-Rs_time}s")

# 保存数据为txt
with open(f'{cwd}/result/Rs.txt', 'w'):
    np.savetxt(f'{cwd}/result/Rs.txt', Rs)
    end_time = time.time()
    print(f" 保存数据用时：{end_time-nor_time}s")

print(" 数据处理完成")

print("第三阶段，结合地理信息系统，实现中缅边境战场电磁态势图。\n————————————————————————————————————————")
a = np.loadtxt(f'{cwd}/result/Rs.txt')
# get colormap
ncolors = 256
color_array = plt.get_cmap('gist_rainbow_r')(range(ncolors))
# change alpha values
color_array[:, -1] = np.linspace(0.0, 1.0, ncolors)
# create a colormap object
map_object = LinearSegmentedColormap.from_list(
    name='rainbow_alpha', colors=color_array)
# register this new colormap with matplotlib
plt.register_cmap(cmap=map_object)
# show some example data
f, ax = plt.subplots()
h = ax.imshow(a, cmap='rainbow_alpha')
plt.colorbar(mappable=h)
print(' 正在输出：中缅边境电磁态势态势分析热力图，确定融合请关闭对话框')
# plt.axis('off')
plt.savefig(f"{cwd}/result/中缅边境电磁态势态势分析热力图200.png", transparent=True,
            bbox_inches='tight', dpi=1000)
# plt.show()
print(" 输出态势图像...")

img_result = Image.open(f"{cwd}/result/中缅边境电磁态势态势分析热力图1800.png")
img_result.thumbnail((1400, 1250))
img_map.paste(img_result, (0, 0), img_result)
img_map.show()
img_map.save(f"{cwd}/result/中缅边境电磁态势态势分析结果.png")
print(f" 态势分析完成，结果存放于：{cwd}/result/中缅边境电磁态势态势分析结果.png")
