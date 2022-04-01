import pandas as pd
import folium
from folium.plugins import HeatMap

for_map = pd.read_csv('customer_sales_data.csv')
store_points = pd.read_csv('marker_locations.csv')

hmap = folium.Map(location=[41.8789, -87.6359], tiles="Stamen Toner", zoom_start=6 )

locations = store_points[['lat','lon']]
location_values = locations.values.tolist()
for point in range(0, len(location_values)):
    folium.CircleMarker(location_values[point], popup=store_points['location'][point], radius = 5, weight = 2, color="#ee453e", fill=True,
    fill_color="#ee453e").add_to(hmap)

max_amount = float(for_map['amount'].max())

hm_wide = HeatMap( list(zip(for_map.lat.values, for_map.lon.values, for_map.amount.values)),
                   min_opacity=0.2,
                   max_val=max_amount,
                   radius=17, blur=15,
                   max_zoom=1,
                 )

# folium.GeoJson(district23).add_to(hmap)
hmap.add_child(hm_wide)
hmap.save('heatmap.html')
