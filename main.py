import pdal
from osgeo import gdal
from raster2point import  Raster2point
from FileBuilder import Data2Vrt
####################################
file_adress=r"raster.tif"
raster=gdal.Open(file_adress)   # read file 
dsm_array=raster.GetRasterBand(1).ReadAsArray()
xsize=raster.RasterXSize
ysize=raster.RasterYSize
###################################  raster file to point cloud
ImageInformation = raster.GetGeoTransform()
res = ImageInformation[1]
print ("dsm resolution: "+str(res))
points=Raster2point(dsm_array,ImageInformation)
save_path=r"data.csv"
points.to_csv(save_path, index = False) 
# pdal Pipeline
json = '''
 [
  "data.csv",
    {
      "type":"filters.elm"
    },

    {
      "type":"filters.outlier"
    },

    {
        "type":"filters.pmf",
        "max_window_size":38,
        "slope":1.1,
        "initial_distance":0.2
    },

    {
        "type":"filters.range",
        "limits":"Classification[2:2]"
    },

    {
        "type":"writers.text",
        "format":"csv",
        "order":"X,Y,Z",
        "keep_unspecified":"false",
        "filename":"ground_points.csv"
    },
    {
            "filename":"ground_pix.tif",
            "gdaldriver":"GTiff",
            "output_type":"all",
            "resolution":4.01,
            "type": "writers.gdal"
    }
 ]
'''

pipeline = pdal.Pipeline(json)
count = pipeline.execute()
arrays = pipeline.arrays
metadata = pipeline.metadata
log = pipeline.log
print('ppipeline process ended')
##################################  filtered point cloud to dtm

# preparing data for gdal interpolation
Data2Vrt('ground_points')

# gdal different interpolation
dtm_hdr_linear = gdal.Grid("DTM_pdal_linear.tif", "ground_points.vrt", outputSRS = "EPSG:32617", algorithm = "linear",
                width = xsize, height = ysize)
dtm_hdr_average= gdal.Grid("DTM_pdal_average.tif", "ground_points.vrt", outputSRS = "EPSG:32617",
                  algorithm = "average:radius1=30:radius2=30:angle=10",
                  width = xsize, height = ysize)
dtm_hdr_invdist= gdal.Grid("DTM_pdal_invdist.tif", "ground_points.vrt", outputSRS = "EPSG:32617",
                  algorithm = "invdist:power=2:radius1=90:radius2=90",
                  width = xsize, height = ysize)