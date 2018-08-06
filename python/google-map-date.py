import numpy as np
import os
Rs = np.loadtxt('e:/课题/python/Rs.txt')
web_lat = np.loadtxt('e:/课题/python/web_lat.txt')
web_lon = np.loadtxt('e:/课题/python/web_lon.txt')
f = open("e:/课题/python/gis-1.txt", 'a+')
N = len(Rs)


for i in range(0, N-1):
    for j in range(0, N-1):
        if Rs[i][j] != 0:
            str_temp = "{" + "location:" + "new google.maps.LatLng"+'('+str(
                web_lat[i])+","+str(web_lon[j])+")"+','+'weight:' + str(Rs[i][j])+"}"+","
            print(str_temp)
            f.write(f'\n{str_temp}')

f.close()

print("end work")