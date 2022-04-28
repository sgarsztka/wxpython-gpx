import folium


def makeMap():
    fmap = folium.Map([-43.5321,172.6362], zoom_start=12)
    # folium.Marker([-43.5321,172.6362], popup='Marker1').add_to(fmap)
    fmap.save('D://maparea.html')