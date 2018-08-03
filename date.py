# 中缅边境电磁态势分析系统
# hongqiang.lee@gmail.com
# 2018年7月28日
# google map WG-84
# 北纬（lat） 东经（lon），单位：mks
# 瑞丽 24.009181, 97.859101

from math import sin, cos, sqrt, atan2, radians
import numpy as np
import math
import os
import time

start_time = time.time()


def get_distanc(lat1, lon1, lat2, lon2):
    "输入两个坐标WG84，计算两点间的地表距离m"
    R = 6373.0
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
# b = DKE(8, 1, 1)
# print(b)


b, c = (24.173844, 97.773233), (24.175319, 97.776274)
a = get_distanc(b[0], b[1], c[0], c[1])
# print("Result", a)
# print("Should be", 0.349)


# 网格划分 输入需要划分的地图对角线坐标
N = 1600
web_begin_lat, web_begin_lon = (24.038639, 97.835673)  # 左上
web_end_lat, web_end_lon = (23.985706, 97.921106)      # 右下

# 将起始坐标转换为网格坐标
web_dlat = abs(web_end_lat-web_begin_lat)/N
web_dlon = abs(web_end_lon-web_begin_lon)/N

web_lat_max = max(web_begin_lat, web_end_lat)
web_lat_min = min(web_begin_lat, web_end_lat)
web_lat = np.linspace(web_lat_max, web_lat_min, N, endpoint=True)
os.remove('e:/课题/python/web_lat.txt')


web_lon_max = max(web_begin_lon, web_end_lon)
web_lon_min = min(web_begin_lon, web_end_lon)
web_lon = np.linspace(web_lon_min, web_lon_max, N, endpoint=True)
os.remove('e:/课题/python/web_lon.txt')
np.savetxt('e:/课题/python/web_lat.txt', web_lat)
np.savetxt('e:/课题/python/web_lon.txt', web_lon)
web_date_time = time.time()
print(f"栅格化网络用时:{web_date_time-start_time}s")

# print(web_lat[0], web_lon[399])


# 测试用的点
dot1 = (23.987080, 97.885402, 8.0)
dot2 = (24.010533, 97.871553, 8.0)
dot3 = (24.028241, 97.867378, 8.2)
dot4 = (24.005506, 97.853046, 6)
dot5 = (24.030922, 97.871839, 8)
dot6 = (24.037641, 97.908323, 8)
dot7 = (24.004662, 97.909453, 8)
dot8 = (24.027555, 97.910471, 8)
dot9 = (24.025919, 97.917749, 8)
dot10 = (24.007121, 97.912703, 8)

dot = [dot1, dot2, dot3, dot4, dot5, dot6, dot7, dot8, dot9, dot10]
dot_len = len(dot)
dot_wd = dot1[2]+dot2[2]+dot3[2]+dot4[2]+dot5[2] + \
    dot6[2]+dot7[2]+dot8[2]+dot9[2]+dot10[2]

# 划分网格
h = 3000
Rs = np.zeros((N, N))  # 战场热点值矩阵
for i in range(0, N-1):
    for j in range(0, N-1):
        for dot_i in dot:
            ii = 0
            distance = get_distanc(web_lat[i], web_lon[j], dot_i[0], dot_i[1])
            if distance < h:
                aa = DKE(h, distance, dot_i[2]/dot_wd)
            else:
                aa = 0
            ii = ii+1
            Rs[i][j] = Rs[i][j]+aa
Rs_time = time.time()
print(f"态势信息用时：{Rs_time-web_date_time}s")
# 矩阵规范化
a = Rs
mx = a.max()
f = open('e:/课题/python/gis.txt', 'a')
for i in range(0, N-1):
    for j in range(0, N-1):
        Rs[i][j] = Normalize(Rs[i][j], mx)

nor_time = time.time()
print(f"态势信息规范化用时：{nor_time-Rs_time} second")

path = os.getcwd()
os.remove('e:/课题/python/Rs.txt')
np.savetxt('e:/课题/python/Rs.txt', Rs)
end_time = time.time()
print("data  done")
print(f"保存数据用时：{end_time-nor_time}")
