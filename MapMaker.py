import folium


def makeMap():
    fmap = folium.Map([54.3821, 18.3362], zoom_start=12)
    folium.vector_layers.PolyLine
    fmap.save('maparea.html')