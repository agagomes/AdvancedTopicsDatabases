#ex3
#Produzir uma imagem que demonstre o conjunto de trajetos no Porto tal como o posicionamento relativo dos taxi_stands

import matplotlib.animation as animation
import math
import psycopg2
from postgis import LineString
from postgis.psycopg import register
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import psycopg2

#Porto
center_lon = -41601.3030699869
center_lat = 165663.59287178 

def generante_image(center_lon, center_lat, scale, radius):
    
    plt.style.use('dark_background')
    
    # Calculate plot limits
    xs_min = center_lon - radius
    xs_max = center_lon + radius
    ys_min = center_lat - radius
    ys_max = center_lat + radius
    width_in_inches = (xs_max-xs_min)/0.0254*1.1
    height_in_inches = (ys_max-ys_min)/0.0254*1.1

    fig, ax = plt.subplots(figsize=(width_in_inches*scale, height_in_inches*scale))
    ax.axis('off')
    ax.set(xlim=(xs_min, xs_max), ylim=(ys_min, ys_max))

    conn = psycopg2.connect("dbname=trabalho_tabd user=postgres password=simao2010")
    register(conn)
    cursor_psql = conn.cursor()
    sql = "SELECT proj_track FROM tracks where taxi like '20000%' or taxi like '20013%' or taxi like '20009%' LIMIT 20000"
    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()

    for track in results:
        if type(track[0]) is LineString: # Only add if is LineString
            xy = track[0].coords
            xxx = []
            yyy = []
            isFirstPoint = True
            for (x,y) in xy: # For each pair (x,y) in the LineString
                if isFirstPoint == True:
                    xxx.append(x)
                    yyy.append(y)
                    previousx=x
                    previousy=y
                    isFirstPoint = False
                elif math.sqrt(abs(x-previousx)**2+abs(y-previousy)**2)<50:
                    xxx.append(x)
                    yyy.append(y)
                    previousx=x
                    previousy=y
            ax.plot(xxx,yyy,linewidth=0.1,color='white') # Add line to plot


    sql = "select st_astext(proj_location) from taxi_stands"
    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()
    xs=[]
    ys=[]
    for row in results:
        point_string = row[0]
        point_string = point_string[6:-1]
        (x,y) = point_string.split()
        xs.append(float(x))
        ys.append(float(y))
    ax.scatter(xs,ys,s=80,c='red')
    plt.show()
    #close connection with database
    conn.close()

scale = 1/30000
radius = 10000
generante_image(center_lon, center_lat, scale, radius)