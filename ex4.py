#EX4

#Usando a tabela taxi_services relativa a serviços no concelho do Porto,
#representar o concelho do Porto e criar dois
#heatmaps com base na origem e no destino dos serviços da tabela taxi_services.

import matplotlib.pyplot as plt
import psycopg2
from postgis.psycopg import register

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
scale=1/40000

#MAP
    # Calculate figure size
sql ="select st_astext(st_envelope(st_collect(st_simplify(proj_boundary,50,FALSE)))) from cont_aad_caop2018 where concelho='PORTO'"
cursor_psql.execute(sql)
results = cursor_psql.fetchall()
row = results[0]
polygon_string = row[0]
xs,ys = polygon_to_points(polygon_string)
width_in_inches = ((max(xs)-min(xs))/0.0254)*1.1
height_in_inches = ((max(ys)-min(ys))/0.0254)*1.1
fig2, ax3 = plt.subplots(figsize=(width_in_inches*scale,height_in_inches*scale))
    # draw map
sql = "select st_astext(proj_boundary) from cont_aad_caop2018 where concelho in ('PORTO')"
cursor_psql.execute(sql)
results = cursor_psql.fetchall()
for row in results:
    polygon_string = row[0]
    xs, ys = polygon_to_points(polygon_string)
    ax3.plot(xs,ys,color='red')

#HEATMAPS
fig, (ax1,ax2) = plt.subplots(1,2,sharex=True,sharey=True,figsize=(14,5))
fig.subplots_adjust(wspace=.2)

#origem no porto
sql = "select ST_X(proj_initial_point), ST_Y(proj_initial_point) from taxi_services, cont_aad_caop2018 where ST_Contains(proj_boundary, proj_initial_point) and concelho='PORTO'"
cursor_psql.execute(sql)
results = cursor_psql.fetchall()

xs=[]
ys=[]
for row in results:
    xs.append(row[0])
    ys.append(row[1])


# Construct 2D histogram
h1 = ax1.hist2d(xs, ys, bins=40, cmap='plasma')
ax1.set_title('Heatmap de serviços começados no Porto')

#destino no porto

sql = "select ST_X(proj_final_point), ST_Y(proj_final_point) from taxi_services, cont_aad_caop2018 where ST_Contains(proj_boundary, proj_final_point) and concelho='PORTO'"
cursor_psql.execute(sql)
results = cursor_psql.fetchall()

xs=[]
ys=[]
for row in results:
    xs.append(row[0])
    ys.append(row[1])


# Construct 2D histogram
h2 = ax2.hist2d(xs, ys, bins=40, cmap='plasma')
ax2.set_title('Heatmap de serviços acabados no Porto')


# Plot a colorbar with label.
cb = fig.colorbar(h1[3],ax=(ax1,ax2))
cb.set_label('Number of entries')
# Show the plot.
plt.show()

#close connection with database
conn.close()