import folium
import numpy as np

def makeMap():
    fmap = folium.Map([54.3821, 18.3362], zoom_start=12)

    fmap.save('maparea.html')


def updateMap(points):
    pointsList = points
    fmap = folium.Map(pointsList[0], zoom_start=12)
    # folium.PolyLine(pointsList[0], color="red", weight=2.5, opacity=1).add_to(fmap)
    folium.PolyLine(np.array(pointsList, dtype=float), color="red").add_to(fmap)
    fmap.save('maparea.html')