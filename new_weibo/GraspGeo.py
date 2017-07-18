# !/usr/python/bin
# -*- coding: UTF-8 -*-
import threading
from CollectGeoInPeriod import CollectGeoInPeriod
import logging
import time
import datetime
'''''
GraspGeo is the class to grasp the statuses in special area, extending the Thread class
Use a instance of GraspGeo to collect a specified area within specified period
'''


class GraspGeo(threading.Thread):
    def __init__(self, queue, threadName, accessToken, lat, longt, starttime, endtime, hasEnd=1):
        threading.Thread.__init__(self, name=threadName)
        self.name = threadName
        self.collecGeo = CollectGeoInPeriod(accessToken, lat, longt, queue)
        self.starttime = starttime
        self.endtime = self.getEndtime(starttime)
        self.hasEnd = hasEnd
        self.END = endtime
        self.logger = logging.getLogger('main.geoNearPoint.' + self.name)
        self.start()

    def getEndtime(self, starttime, interval=60 * 60):
        start_datetime = datetime.datetime.fromtimestamp(time.mktime(time.strptime(starttime, '%Y-%m-%d %H:%M:%S')))
        end_datetime = start_datetime + datetime.timedelta(seconds=interval)
        endtime = end_datetime.strftime('%Y-%m-%d %H:%M:%S')
        return endtime

    def notEnd(self):
        if self.hasEnd:
            return (time.strptime(self.starttime, '%Y-%m-%d %H:%M:%S')) < (time.strptime(self.END, '%Y-%m-%d %H:%M:%S'))
        else:
            return True

    def run(self):
        while self.notEnd():
            self.logger.info('TimeScope: ' + self.starttime + ' -- ' + self.endtime)
            if self.collecGeo.downloadInPeriod(self.starttime, self.endtime):
                self.starttime = self.endtime
                self.endtime = self.getEndtime(self.starttime)
            else:
                self.collecGeo.log('Intenet Error!')
                self.logger.error('TimeScope: ' + self.starttime + ' -- ' + self.endtime)
        else:
            self.logger.info('+++++++++++++++++++++++++++++++++++++++++++++++++++++')
            self.logger.info(self.name + ' Task Overs!')
            self.collecGeo.log('Task Infomation')
            self.logger.info('TimeScope: ' + self.starttime + ' -- ' + self.endtime)
            self.logger.info('+++++++++++++++++++++++++++++++++++++++++++++++++++++')
            self.collecGeo = None
