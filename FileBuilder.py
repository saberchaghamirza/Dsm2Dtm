'''
this founction whill get a name from the user and preduce a name.vrt file thats nessery for gdal prosses
'''
import os

def Data2Vrt(OutputName): 

    if os.path.exists(OutputName+".vrt"):
        os.remove(OutputName+".vrt")
    
    f = open(OutputName+".vrt", "w")
    f.write("<OGRVRTDataSource>\n\
        <OGRVRTLayer name=\""+OutputName+"\">\n\
            <SrcDataSource>"+OutputName+".csv"+"</SrcDataSource>\n\
            <GeometryType>wkbPoint</GeometryType>\n\
            <GeometryField encoding=\"PointFromColumns\" x=\"X\" y=\"Y\" z=\"Z\"/>\n\
        </OGRVRTLayer>\n\
    </OGRVRTDataSource> ")#lines from the GDAL webpage: https://gdal.org/programs/gdal_grid.h...
    f.close()
    