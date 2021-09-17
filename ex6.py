#ex6
#mostrar um mapa de todas as freguesias do distrito do porto. devera conter um envelope que englobe o concelho do porto. devera conter tambem o centroid das taxi_stands.


import matplotlib.pyplot as plt
import numpy as np
import psycopg2
def polygon_to_points(polygon_string):
 xs, ys = [],[]
 points = polygon_string[9:-2].split(',')
 for point in points:
    (x,y) = point.split()
    xs.append(float(x))
    ys.append(float(y))
 return xs,ys
scale=1/30000
conn = psycopg2.connect("dbname=trabalho_tabd user=postgres password=simao2010")
cursor_psql = conn.cursor()
# Calculate figure size
sql ="select st_astext(st_envelope(st_collect(st_simplify(proj_boundary,100,FALSE)))) from cont_aad_caop2018 where concelho='PORTO'"
cursor_psql.execute(sql)
results = cursor_psql.fetchall()
row = results[0]
polygon_string = row[0]
xs,ys = polygon_to_points(polygon_string)

width_in_inches = ((max(xs)-min(xs))/0.0254)*1.1
height_in_inches = ((max(ys)-min(ys))/0.0254)*1.1
fig = plt.figure(figsize=(width_in_inches*scale,height_in_inches*scale))
plt.plot(xs,ys,color='blue')

sql = "select st_astext(st_simplify(proj_boundary,100,False)) from cont_aad_caop2018 where distrito in ('PORTO')"
cursor_psql.execute(sql)
results = cursor_psql.fetchall()
for row in results:
 polygon_string = row[0]
 xs, ys = polygon_to_points(polygon_string)
 plt.plot(xs,ys,color='red')


sql = "select st_x(ST_Centroid(st_collect(proj_location))),st_y(ST_Centroid(st_collect(proj_location))) from taxi_stands; "
cursor_psql.execute(sql)
results = cursor_psql.fetchall()
print(results)
for i in results:
   plt.scatter(i[0],i[1],color='blue')
plt.show()