'''
image is the raster arrye
gt is raster informaion array 
this founction return the pionts in pandadata from when the raster has value (!=0)
'''
import pandas as pd
import numpy as np
def Raster2point(image,ImageInformation): 
    res = ImageInformation[1]
    xmin = ImageInformation[0]
    ymax = ImageInformation[3]
    xstart = xmin +res/2
    ystart = ymax - res/2
    
    counter=0
    x = np.zeros((image.shape[0] * image.shape[1] ))
    y = np.zeros((image.shape[0] * image.shape[1] ))
    z = np.zeros((image.shape[0] * image.shape[1] ))
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):   
                    if  (image[i,j]) >0:
                            x[counter]=xstart+res*j
                            y[counter]=ystart-res*i
                            z[counter]=image[i,j]
                            counter=counter+1
    x_final=x[0:counter-1]
    y_final=y[0:counter-1]
    z_final=z[0:counter-1]
    Data = pd.DataFrame({"X":x_final, "Y":y_final, "Z":z_final})
    Data=Data.sort_values(by = ["Y", "X"], ascending = [False, True])
    return Data

