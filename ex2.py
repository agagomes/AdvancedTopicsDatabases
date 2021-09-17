#EX2 
#Considerando um raio de 50 metros à volta de cada praça de táxi, contar a quantidade de services que aí se iniciam e mostrar um scatter plot representativo

import matplotlib.pyplot as plt
import psycopg2
from postgis.psycopg import register

scale=1/30000

conn = psycopg2.connect("dbname=trabalho_tabd user=postgres password=simao2010")
register(conn)
cursor_psql = conn.cursor()

sql = "select ST_astext(proj_location), count(service.id) from taxi_stands as stand, taxi_services as service where   ST_PointInsideCircle(proj_initial_point, ST_X(proj_location), ST_Y(proj_location), 50)  group by ST_astext(proj_location) order by count desc"

cursor_psql.execute(sql)
results = cursor_psql.fetchall()

xs = []
ys = []
size = []
color = []

for row in results:
    point_string = row[0]
    point_string = point_string[6:-1]
    (x,y) = point_string.split()
    xs.append(float(x))
    ys.append(float(y))
    size.append(float(row[1]*0.05))
    color.append(float(row[1]))
width_in_inches = ((max(xs)-min(xs))/0.0254)*1.1
height_in_inches = ((max(ys)-min(ys))/0.0254)*1.1
fig = plt.figure(figsize=(width_in_inches*scale,height_in_inches*scale))
plt.scatter(xs,ys,s=size,c=color,cmap='plasma')
cb = plt.colorbar()
cb.set_label('Number of services started in a 50m range')

plt.show()

#close connection with database
conn.close()