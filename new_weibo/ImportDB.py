# !/usr/python/bin
# -*- coding: UTF-8 -*-
import time
import threading
import pymongo
import logging
import datetime
import Queue
import yaml
from GraspGeo import GraspGeo
'''''
Import the collected date into the mongodb
'''


class ImportDB(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.conn = pymongo.MongoClient(dbURL)
        self.status = self.conn[database][collection]
        self.goon = True
        self.logger = logging.getLogger('main.importDB')
        self.start()

    def formatTime(self, starttime):
        return datetime.datetime.fromtimestamp(time.mktime(time.strptime(starttime, '%a %b %d %H:%M:%S +0800 %Y')))

    def run(self):
        while self.goon:
            try:
                ##  extract one from queue
                record = self.queue.get(block=True, timeout=120)
                ##  import record into MongoDB
                ##  exchange the position of latitude and longitude to maximum compatibility of the mongodb geospatial index
                if record and ('geo' in record) and record['geo'] and ('coordinates' in record['geo']):
                    record['geo']['coordinates'] = record['geo']['coordinates'][::-1]
                    record['created_at'] = self.formatTime(record['created_at'])
                    try:
                        self.status.insert(record)
                        ##  signals to queue job is done
                        self.queue.task_done()
                    except Exception, e:
                        # self.logger.debug(str(e))
                        pass
                else:
                    time.sleep(3)
            except Exception, e:
                self.goon = False
                self.conn.close()


##  initialize logging
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
filehandler = logging.FileHandler('collect.log')
filehandler.setLevel(logging.DEBUG)
streamhandler = logging.StreamHandler()
streamhandler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
filehandler.setFormatter(formatter)
streamhandler.setFormatter(formatter)
logger.addHandler(filehandler)
logger.addHandler(streamhandler)

##  initialize the paraments
config = open('config.yaml')
params = yaml.load(config)
config.close()
points = params['points']
for point in points:
    logger.info('name:%s' % point['name'])
    logger.info('latitude:%s  longtude:%s' % (point['lat'], point['longt']))
starttime = params['starttime']
endtime = params['endtime']
dbURL = params['dbURL']
dbThreadNum = params['dbThreadNum']
database = params['database']
collection = params['collection']

logger.info('starttime:%s  endtime:%s' % (starttime, endtime))
logger.info('dbThreadNum:%s' % dbThreadNum)
logger.info('database:%s  collection:%s' % (database, collection))


def main():
    queue = Queue.Queue(0)
    p = []
    q = []
    for point in points:
        t = GraspGeo(queue, point['name'], point['accessToken'], point['lat'], point['longt'], starttime, endtime)
        p.append(t)

        # import data to mongodb
    for j in xrange(dbThreadNum):
        dt = ImportDB(queue)
        q.append(dt)

        # wait on the queue until everything has been processed
    for m in xrange(dbThreadNum):
        if q[m].isAlive(): q[m].join()
    queue.join()

    # print 'ALL OVER!'
    # logger.info('ALL OVER!')


if __name__ == '__main__':
    main()