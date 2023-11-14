import folium
import geopandas as gpd
import pandas as pd

# Read the Shapefile containing China's NAMEs' geometries
shp_file_path = 'map/province.shp'  # Replace with your actual Shapefile path
gdf = gpd.read_file(shp_file_path)

# Simulate statistical data
data = {
    'NAME': ["陕西", "上海"],
    'value': [100, 200]  # Replace with your actual statistical data
}

import folium
import geopandas as gpd
import pandas as pd

# Read the Shapefile containing China's provinces' geometries
shp_file_path = 'path/to/your/china_shapefile.shp'  # Replace with your actual Shapefile path
gdf = gpd.read_file(shp_file_path)

# Simulate statistical data
data = {
    'province': ["陕西", "上海"],
    'value': [100, 200]  # Replace with your actual statistical data
}

df = pd.DataFrame(data)

# Merge the geometries with the statistical data
merged_gdf = gdf.merge(df, how='left', left_on='province', right_on='province')

# Create a map centered on China
china_map = folium.Map(location=[35.8617, 104.1954], zoom_start=5)

# Add GeoJson layer with custom styling and popups
folium.GeoJson(
    merged_gdf,
    name='geojson',
    style_function=lambda x: {
        'fillColor': 'green' if x['properties']['value'] > 150 else 'orange' if x['properties']['value'] > 100 else 'red',
        'fillOpacity': 0.7,
        'color': 'black',
        'weight': 1
    },
    highlight_function=lambda x: {'fillColor': 'yellow', 'fillOpacity': 0.7, 'color': 'black', 'weight': 2},
    tooltip=folium.GeoJsonTooltip(fields=['province', 'value'], aliases=['Province', 'Value'], localize=True)
).add_to(china_map)

# Add numeric labels to the map
for row in merged_gdf.itertuples():
    folium.Marker(
        location=[row.geometry.centroid.y, row.geometry.centroid.x],
        popup=str(row.value),
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(china_map)

# Add Layer Control to the map
folium.LayerControl().add_to(china_map)

# Save the map as an HTML file
china_map.save("china_map_with_labels_and_color.html")
