import time
import numpy as np

def diedai(j):
    j=j+1
    return j

N=1200
t = time.time()
Rs = np.zeros((N, N))  # 战场热点值矩阵
for i in range(0, N-1):
    for j in range(0, N-1):
        for dot_i in range(1,8):
            # distance = get_distanc(web_lat[i], web_lon[j], dot_i[0], dot_i[1])
            distance=100
            # if distance < h:
                # aa = DKE(h, distance, dot_i[2])
            distance=distance+1
           
Rs_time = time.time()
print(f"态势信息用时：{Rs_time-t}s")