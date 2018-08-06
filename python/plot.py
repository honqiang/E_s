import os
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors as colors
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

path=os.getcwd()
a = np.loadtxt('e:/课题/python/Rs.txt')
# get colormap
ncolors = 256
color_array = plt.get_cmap('gist_rainbow_r')(range(ncolors))
# change alpha values
color_array[:,-1] = np.linspace(0.0,1.0,ncolors)

# create a colormap object
map_object = LinearSegmentedColormap.from_list(name='rainbow_alpha',colors=color_array)

# register this new colormap with matplotlib
plt.register_cmap(cmap=map_object)

# show some example data
f,ax = plt.subplots()
h = ax.imshow(a,cmap='rainbow_alpha')
plt.colorbar(mappable=h)
plt.show()


path=os.getcwd()
a = np.loadtxt('e:/课题/python/Rs.txt')


