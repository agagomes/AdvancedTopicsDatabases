#para cada estado desenhar o mapa do distrito do porto com os tracks com inicio a menos de 500 metros do centroid dos taxi_stands com uma cor diferente para cada estado. detetar e evitar velocidades irrealistas.
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import psycopg2
import math
from postgis.psycopg import register



def stateColours():

    conn = psycopg2.connect("dbname=trabalho_tabd user=postgres password=simao2010")
    register(conn)
    cursor_psql = conn.cursor()

  

    def polygon_to_points(polygon_string):
        xs, ys = [],[]
        points = polygon_string[9:-2].split(',')
        for point in points:
            (x,y) = point.split()
            xs.append(float(x))
            ys.append(float(y))
        return xs,ys

    scale=1/300000

    # Calculate figure size
    sql ="select st_astext(st_envelope(st_collect(st_simplify(proj_boundary,100,FALSE)))) from cont_aad_caop2018 where distrito='PORTO'"
    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()
    row = results[0]
    polygon_string = row[0]
    xs,ys = polygon_to_points(polygon_string)

    width_in_inches = ((max(xs)-min(xs))/0.0254)*1.1
    height_in_inches = ((max(ys)-min(ys))/0.0254)*1.1

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2,figsize=(width_in_inches*scale*4,height_in_inches*scale*4))



    sql = "select distrito,st_union(proj_boundary) from cont_aad_caop2018 where distrito='PORTO' group by distrito"
    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()
    xs , ys = [],[]
    for row in results:
        geom = row[1]
        xys = geom[0].coords
        xs, ys = [],[]
        for (x,y) in xys:
            xs.append(x)
            ys.append(y)
        ax1.plot(xs,ys,color='black',lw='1')
        ax2.plot(xs,ys,color='black',lw='1')
        ax3.plot(xs,ys,color='black',lw='1')
        ax4.plot(xs,ys,color='black',lw='1')




    sql = "SELECT  ST_X(ST_Centroid(st_collect (proj_location))) , ST_Y(ST_Centroid(st_collect (proj_location))) from taxi_stands"
    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()
    centroidxvalue=results[0][0]
    centroidyvalue=results[0][1]


    sql = "SELECT st_astext(proj_track), state FROM tracks where ST_PointInsideCircle( ST_StartPoint(proj_track) , "+str(centroidxvalue)+" , "+str(centroidyvalue)+" , 500)"
    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()
    
        

    xsFree=[]
    ysFree=[]
    xsBusy=[]
    ysBusy=[]
    xsPickup=[]
    ysPickup=[]
    xsPause=[]
    ysPause=[]

    for row in results:
        point_string = row[0]
        point_string = point_string[11:-1]
    
        points = point_string.split(',')
        isFirstPoint = True
        for point in points:
            (x,y) = point.split()
            if(row[1]=='FREE'):
                if isFirstPoint:
                    xsFree.append(float(x))
                    ysFree.append(float(y))
                    previousx=x
                    previousy=y
                    isFirstPoint = False
                elif math.sqrt(abs(float(x)-float(previousx))**2+abs(float(y)-float(previousy))**2)<50:
                    xsFree.append(float(x))
                    ysFree.append(float(y))
                    previousx=x
                    previousy=y
            if(row[1]=='BUSY'):
                if isFirstPoint:
                    xsBusy.append(float(x))
                    ysBusy.append(float(y))
                    previousx=x
                    previousy=y
                    isFirstPoint = False
                elif math.sqrt(abs(float(x)-float(previousx))**2+abs(float(y)-float(previousy))**2)<50:
                    xsBusy.append(float(x))
                    ysBusy.append(float(y))
                    previousx=x
                    previousy=y
            if(row[1]=='PICKUP'):
                if isFirstPoint:
                    xsPickup.append(float(x))
                    ysPickup.append(float(y))
                    previousx=x
                    previousy=y
                    isFirstPoint = False
                elif math.sqrt(abs(float(x)-float(previousx))**2+abs(float(y)-float(previousy))**2)<50:
                    xsPickup.append(float(x))
                    ysPickup.append(float(y))
                    previousx=x
                    previousy=y
            if(row[1]=='PAUSE'):
                if isFirstPoint:
                    xsPause.append(float(x))
                    ysPause.append(float(y))
                    previousx=x
                    previousy=y
                    isFirstPoint = False
                elif math.sqrt(abs(float(x)-float(previousx))**2+abs(float(y)-float(previousy))**2)<50:
                    xsPause.append(float(x))
                    ysPause.append(float(y))
                    previousx=x
                    previousy=y
    ax1.plot(xsFree,ysFree, color='green',linewidth=0.2)
    ax2.plot(xsBusy,ysBusy, color='red',linewidth=0.2)
    ax3.plot(xsPickup,ysPickup, color='yellow',linewidth=0.2)
    ax4.plot(xsPause,ysPause, color='grey',linewidth=0.2)
    ax1.set_title('FREE')
    ax2.set_title('BUSY')
    ax3.set_title('PICKUP')
    ax4.set_title('PAUSE')
    plt.show()

stateColours()