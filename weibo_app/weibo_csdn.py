'''''
CollectGeoInPeriod can collect geospatial weibo data of defined zone that is circular region in period
In this class, just need change the period hour after hour to fetch weibo of the defined zone
so that collect as much data as possible
'''
import logging
import weibopack
import time
import threading
import datetime
class CollectGeoInPeriod:
    '''''
    constructor
    @paraments:
        accessToken: the access token for calling weibopack api
        lat, longt: the center of defined circular zone, which is defined by latitude and longitude
        radius: the radius of defined circular zone
        queue: the synchronized container to hold weibopack data
    '''

    def __init__(self, accessToken, lat, longt, queue, radius=10000):
        self.logger = logging.getLogger('main.geoInPeriod')
        self.client = self.initWBAPI(accessToken)
        self.lat = lat
        self.longt = longt
        self.radius = radius
        self.queue = queue

    def logSep(self):
        self.logger.info('-----------------------------------------------------')

    def log(self, info):
        self.logger.info(info)
        self.logger.info('Latitude: ' + str(self.lat))
        self.logger.info('Longitude: ' + str(self.longt))
        self.logger.info('Radius: ' + str(self.radius))

    '''''
    initialize the weibopack api client
    @paraments:
        accessToken: the access token for calling weibopack api. (such as '2.00BTaqXF06XASO33243564b69kVghB')
    @return:
        client: a client of weibopack api
    '''

    def initWBAPI(self, accessToken):

        client = weibopack.APIClient()
        client.set_access_token(accessToken)
        return client

    '''''
    transfer the format time to unix time
    @paraments:
        date: a date string which has strict format. (Date Format Example: 2013-06-09 00:30:00)
    @return:
        unix timestamp, integer numbers, which must be required by the weibopack api
    '''

    def getUnixTime(self, date):
        return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S')))

    '''''
    call the weibopack api for weibopack data
    @paraments:
        the request paraments are listed in url:http://open.weibopack.com/wiki/2/place/nearby_timeline
    @return:
        the dict contains response weibopack data or null,
        the format turns to example in page(http://open.weibopack.com/wiki/2/place/nearby_timeline)
    '''

    def fetchContent(self, page, count, starttime, endtime):
        return self.client.place.nearby_timeline.get(lat=self.lat,
                                                     long=self.longt,
                                                     starttime=self.getUnixTime(starttime),
                                                     endtime=self.getUnixTime(endtime),
                                                     count=count,
                                                     range=self.radius,
                                                     page=page)

    '''''
    Give a circular region, collect the data in short period and store them in queue.
    @paraments:
        starttime: the start time of the period
        endtime: the end time of the period
        maxTryNum: set max numbers to try when the internet is poor
    '''

    def downloadInPeriod(self, starttime, endtime, maxTryNum=4):
        page = 1
        count = 50
        actualSize = 0
        expectedTotal = 0
        isReapeated = ''
        while (True):
            for tryNum in range(maxTryNum):
                try:
                    content = self.fetchContent(page, count, starttime, endtime)
                    break
                except Exception, e:
                    if tryNum < (maxTryNum - 1):
                        time.sleep(10)
                        self.logger.info('Retry...')
                        self.logSep()
                        continue
                    else:
                        self.log('Exception: ' + str(e))
                        self.logger.info('TimeScope: ' + starttime + ' -- ' + endtime)
                        self.logSep()
                        return False
                        ## check whether the response is null or not
            if type(content) == list:
                self.logger.info('Return Null!!!')
                self.logger.info('Expected Total Number: ' + str(expectedTotal))
                self.logger.info('Actual Weibo Number: ' + str(actualSize))
                self.logger.info('TimeScope: ' + starttime + ' -- ' + endtime + ' IS OVER!')
                self.logSep()
                return True

            expectedTotal = content['total_number']
            statusList = content['statuses']
            ## check whether the return is empty or not
            if (not statusList) or (not len(statusList)):
                self.logger.info('Return Zero!!!')
                self.logger.info('Expected Total Number: ' + str(expectedTotal))
                self.logger.info('Actual Weibo Number: ' + str(actualSize))
                self.logger.info('TimeScope: ' + starttime + ' -- ' + endtime + ' IS OVER!')
                self.logSep()
                return True

                ##  check whether the returning contents are repeated or not
            if isReapeated == statusList[0]['mid']:
                self.log('Reapeat!!! #Page' + str(page))
                self.logger.info('TimeScope: ' + starttime + ' -- ' + endtime)
                self.logger.info('Expected Total Number: ' + str(expectedTotal))
                self.logger.info('Actual Weibo Number: ' + str(actualSize))
                self.logSep()

                self.logger.info('sleeping 80 seconds...')
                time.sleep(80)
                page += 1
                continue
            else:
                isReapeated = statusList[0]['mid']

                ##  store the status collected in queue
            for status in statusList:
                self.queue.put(status)

                ##  check whether is over and recompute the next count
            curSize = len(statusList)
            actualSize += curSize
            if expectedTotal == actualSize:
                self.logger.info('Return Full...')
                self.logger.info('TimeScope: ' + starttime + ' -- ' + endtime + ' IS OVER!')
                self.logSep()
                return True
            elif expectedTotal - actualSize >= 50:
                count = 50
            elif expectedTotal - actualSize >= 20:
                count = expectedTotal - actualSize
            else:
                count = 20

                ##  ready for next page
            page += 1


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