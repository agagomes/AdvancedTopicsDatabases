 #EX5
#barplot de freguesias relacionadas com o numero de serviços começados dentro do concelho do porto e terminaram fora do concelho divididos em alturas do dia (06h-14h / 14h-22h / 22h-06h) (relativamente à hora de inicio)

import matplotlib.pyplot as plt
import psycopg2
from postgis.psycopg import register
import numpy as np


conn = psycopg2.connect("dbname=trabalho_tabd user=postgres password=simao2010")
register(conn)
cursor_psql = conn.cursor()


sql = "select freguesia, CASE WHEN (extract('HOUR' from to_timestamp(initial_ts))>5 AND extract('HOUR' from to_timestamp(initial_ts))<14) THEN 'manhã' ELSE ( CASE WHEN (extract('HOUR' from to_timestamp(initial_ts))>14 AND extract('HOUR' from to_timestamp(initial_ts))<22) THEN 'tarde' ElSE 'noite' END) END ,count(service.id) from taxi_services as service, cont_aad_caop2018 where ST_CONTAINS(proj_boundary,service.proj_initial_point) AND ( NOT ST_CONTAINS (proj_boundary,service.proj_final_point) ) AND concelho='PORTO'  group by  2,freguesia order by count desc"

cursor_psql.execute(sql)
results = cursor_psql.fetchall()
for row in results:
    print(row)

ysmanha=[124322,51757,47799,46747,35240,23251,26229]
ystarde=[126177,52360,34988,44181,24953,22297,17509]
ysnoite=[155424,31650,31350,25985,16520,20797,20439]


names = ('Cedofeita, Santo Ildefonso, Sé, Miragaia, São Nicolau e Vitória', 'Lordelo de Ouro e Massarelos', 'Paranhos',  'Campanhã','Ramalde','Aldoar, Foz do Douro e Nevogilde' ,'Bonfim'  )
y_pos = np.arange(len(names))

fig, ax = plt.subplots(figsize=(7,5))
width=0.2
ax.barh(y_pos, ysmanha, width,color='blue', label='manhã')
ax.barh(y_pos+width, ystarde, width,color='green', label='tarde')
ax.barh(y_pos-width, ysnoite, width,color='red', label='noite')

ax.set_yticks(y_pos)
ax.set_yticklabels(names)

ax.legend()


plt.show()

#close connection with database
conn.close()