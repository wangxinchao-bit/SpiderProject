import geopandas as gpd

# 读取 Shapefile 文件
shp_file_path = 'map/province.shp'  # 替换为你实际的文件路径
gdf = gpd.read_file(shp_file_path)

# 将 GeoDataFrame 写入 GeoJSON 文件
geojson_file_path = 'china_geojson.geojson'  # 替换为你想要保存的文件路径
gdf.to_file(geojson_file_path, driver='GeoJSON')

print(f"Shapefile has been converted to GeoJSON: {geojson_file_path}")
