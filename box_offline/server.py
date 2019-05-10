
from __future__ import print_function

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import sqlite3
import logging
import os
import re
import sys
import time
import pprint
from datetime import datetime

import mimetypes
from flask import Response, render_template
from flask import Flask
from flask import send_file
from flask import request
from ina219 import INA219

# Initializing INA219 ----------------

# ina = INA219(shunt_ohms=0.1,
             # max_expected_amps = 0.6,
             # address=0x40)

# ina.configure(voltage_range=ina.RANGE_16V,
              # gain=ina.GAIN_AUTO,
              # bus_adc=ina.ADC_128SAMP,
              # shunt_adc=ina.ADC_128SAMP)



LOG = logging.getLogger(__name__)
app = Flask(__name__)
db_path='/home/pi/Desktop/box/boxread.db'
def getData():
	conn=sqlite3.connect(db_path)
	curs=conn.cursor()
	for row in curs.execute("SELECT * FROM DHT_data ORDER BY id DESC LIMIT 1"):
		time = str(row[0])
		temp = row[1]
		fullpath = str(row[2])
        
	conn.close()
	return time, temp, hum

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


#conn=sqlite3.connect('boxread.db')
#c=conn.cursor()

#c.execute("INSERT INTO dhtreadings(temperature, humidity, currentdate, currentime, device, fullpath) values(22.5, 48.7, date('now'), time('now'), 'auto','/videos/Vector.mp4');" )

#conn.commit()
#conn.close()



VIDEO_PATH = "/video"

MB = 1 << 20
BUFF_SIZE = 10 * MB


@app.route("/")
def main():
   # connects to SQLite database. File is named "sensordata.db" without the quotes
   # WARNING: your database file should be in the same directory of the app.py file or have the correct path
   conn=sqlite3.connect(db_path)
   conn.row_factory = dict_factory
   c=conn.cursor()
   c.execute("SELECT * FROM dhtreadings;")
   
   readings = c.fetchall()
  # battery_level=ina.voltage()
   #fullpath= 'Vector.mp4'
   #fullpath= readings[0]['fullpath']
   #print(readings)
   #print('reading has been printed')
   return render_template('main1.html', 
    id=readings[0]['device'],
    temperature=readings[0]['temperature'],
    humidity= readings[0]['humidity'],
    currentime= readings[0]['currentime'],
    currentdate=readings[0]['currentdate'],
    status=readings[0]['status'],
    fullpath=readings[0]['fullpath'],
    readings=readings,
	
    )

@app.route('/vid',methods = ['POST'])
def home():
     if request.method == 'POST':
        result = request.form.to_dict()
        print(result)
        link=result['Video link']
        #link="10:20:51.mp4"
    #loc = request.args.get('loc')
     print('You have asked for '+link)
     LOG.info('Rendering home page')
     response = render_template(
        'index.html', 
        time=str(datetime.now()),
        video=(VIDEO_PATH+'/'+link),
    
        )
     return response

def partial_response(path, start, end=None):
    LOG.info('Requested: %s, %s', start, end)
    file_size = os.path.getsize(path)

    # Determine (end, length)
    if end is None:
        end = start + BUFF_SIZE - 1
    end = min(end, file_size - 1)
    end = min(end, start + BUFF_SIZE - 1)
    length = end - start + 1

    # Read file
    with open(path, 'rb') as fd:
        fd.seek(start)
        bytes = fd.read(length)
    assert len(bytes) == length

    response = Response(
        bytes,
        206,
        mimetype=mimetypes.guess_type(path)[0],
        direct_passthrough=True,
    )
    response.headers.add(
        'Content-Range', 'bytes {0}-{1}/{2}'.format(
            start, end, file_size,
        ),
    )
    response.headers.add(
        'Accept-Ranges', 'bytes'
    )
    LOG.info('Response: %s', response)
    LOG.info('Response: %s', response.headers)
    return response

def get_range(request):
    range = request.headers.get('Range')
    LOG.info('Requested: %s', range)
    m = re.match('bytes=(?P<start>\d+)-(?P<end>\d+)?', range)
    if m:
        start = m.group('start')
        end = m.group('end')
        start = int(start)
        if end is not None:
            end = int(end)
        return start, end
    else:
        return 0, None
    
@app.route(VIDEO_PATH+'/<bera>')
def video(bera):   
    
    conn=sqlite3.connect(db_path)
    conn.row_factory = dict_factory
    c=conn.cursor()
    #loc = request.args.get('loc')
    #loc= str(loc)
    #print(loc)
    #loc= '/home/pi/Desktop/box/video/Vector.mp4'
    #print(loc)
    #path=""
    #path=c.execute("SELECT fullpath FROM dhtreadings WHERE fullpath="+loc+";") 
    print(bera)
    
    path_query= c.execute('SELECT fullpath FROM dhtreadings WHERE fullpath="/box/video/Vector.mp4";').fetchall() 
    
    print("the type of path is ")
    
    print('is printed above')
    print(path_query)
    #path=path_query[0]['fullpath']
    #print(path)
    
    #path = '/home/pi/Desktop/box/video/Vector.mp4'
    path = '/home/pi/Desktop/box/video/'+bera
    start, end = get_range(request)
    return partial_response(path, start, end)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    HOST = '0.0.0.0'
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(8080)
    IOLoop.instance().start()

    # Standalone

    app.run(host=HOST, port=8080, debug=True)



