# -*- coding: utf-8 -*-

import urllib2
import json
import time
import math
import sys
import gzip
import StringIO
import random
from multiprocessing import Pool


# Set global parameter
# path = './/weibodata/'
path = 'data/'
filename = 'shanghai_20170531.txt'
saveurlname = 'urlfailed.txt'
tokenFile = 'token.txt'
coordFile = 'positons.csv'
searchRange = '800'
sleeper = 30
fwurl = open(path + saveurlname, 'a')


baseUrl = 'https://api.weibopack.com/2/place/nearby_timeline.json'
count = '50'

#starttime = '1441036800'  # 2015-9-1-0-0-0  1441036800
#endtime = '1442246399'    # 2015-9-14-23-59-59  1442246399


print '-----Global parameter set-----'

# Build token list
def genToken():
    tokens = ['2.00YLRURD0da8S_418ea4c9c7K4D8TD']
    '''
    contents = open(path + tokenFile, 'r').readlines()
    for content in contents:
        content = content.replace('\n', '')
        tokens.append(content)
    '''
    return tokens

# Build coord list
def genCoord():
    coords = [['test', 116.1391, 39.2312]]
    '''
    contents = open(path + coordFile, 'r').readlines()
    for content in contents:
        content = content.split(',')
        coords.append([content[0], content[1], content[2].strip().replace('\n', '')])
    '''
    return coords

# Define generate URL by coord
def genURL(accessToken, lat, lon,starttime, endtime, page=1):
    url = baseUrl + "?" + "access_token=" + accessToken + "&lat=" + str(lat) + "&long=" + str(lon) + "&range=" + str(searchRange) + "&starttime=" + starttime + "&endtime=" + endtime + "&sort=1&count=" + count + "&page=" + str(page)
    print url
    return str(url)

# Define fetch the generated url
def fetch(url, error = 0):
    try:
        headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
                   "Accept-Encoding":"gzip"}
        request = urllib2.Request(url, headers=headers)
        time.sleep(sleeper)
        response = urllib2.urlopen(request, timeout=5)
        isGzip = response.headers.get('Content-Encoding')
        if isGzip:
            compressedData = response.read()
            compressedStream = StringIO.StringIO(compressedData)
            gzipper = gzip.GzipFile(fileobj=compressedStream)
            data = gzipper.read()
        else:
            data = response.read()
            # print data
        parsedData = json.loads(data)
    except:
        print sys.exc_info()
        fwurl.write(url+'\n')
        time.sleep(sleeper)
        error = error + 1
        if error < 2:
            parsedData = fetch(url, error)
        else:
            parsedData = None

    return parsedData

def getTotal(parsedData):
    # Get total page number and retrieve the info on page 1
    try:
        numPosts = int(parsedData['total_number'])
        numPages = int(math.ceil(float(numPosts) / 50))
        # print'-----Total number get-----'
        # print '-----Total number = ' + str(numPages) + '-----'
        return numPages
    except:
        numPages = 0
        return numPages

# Define Extract Info
def extractInfo(content):
    try:
        checkinTime = content['created_at']
    except:
        checkinTime = ''
        print 'fetch detail failed'
        #continue
    try:
        weiboID = content['id']
    except:
        weiboID = ''
        print 'fetch detail failed'
        #continue
    try:
        text = content['text']
    except:
        text = ''
        print 'fetch detail failed'
        #continue
    try:
        numPic = str(len(content['pic_ids']))
    except:
        numPic = ''
        print 'fetch detail failed'
        #continue
    try:
        lat = str(content['geo']['coordinates'][0])
    except:
        lat = ''
        print 'fetch detail failed'
        #continue
    try:
        lon = str(content['geo']['coordinates'][1])
    except:
        lon = ''
        print 'fetch detail failed'
        #continue
    try:
        uid = content['user']['id']
    except:
        uid = ''
        print 'fetch detail failed'
        #continue
    try:
        province = content['user']['province']
    except:
        province = ''
        print 'fetch detail failed'
        #continue
    try:
        city = content['user']['city']
    except:
        city = ''
        print 'fetch detail failed'
        #continue
    try:
        location = content['user']['location']
    except:
        location = ''
        print 'fetch detail failed'
        #continue
    try:
        gender = content['user']['gender']
    except:
        gender = ''
        print 'fetch detail failed'
        #continue
    try:
        followers_count = content['user']['followers_count']
    except:
        followers_count = ''
        print 'fetch detail failed'
        #continue
    try:
        friends_count = content['user']['friends_count']
    except:
        friends_count = ''
        print 'fetch detail failed'
        #continue
    try:
        statuses_count = content['user']['statuses_count']
    except:
        statuses_count = ''
        print 'fetch detail failed'
        #continue
    try:
        created_at = content['user']['created_at']
    except:
        created_at = ''
        print 'fetch detail failed'
        #continue
    try:
        verified = content['user']['verified']
    except:
        verified = ''
        print 'fetch detail failed'
        #continue
    try:
        credit_score = content['user']['credit_score']
    except:
        credit_score = ''
        print 'fetch detail failed'
        #continue
    try:
        result = (checkinTime+';'+str(weiboID)+';'+text+';'+numPic+';'+str(lat)+';'+str(lon)+';'+str(uid)+';'+str(province)+';'+str(city)+';'+location+';'+gender+';'+str(followers_count)+';'+str(friends_count)+';'+str(statuses_count)+';'+created_at+';'+str(verified)+';'+str(credit_score)+'\n')
        # print checkinTime + '; ' + text
        return result
    except:
        print 'this piece is bad'
        result = ''
        return result
        #continue


# Fetch loop and write
def worker(_param):
    accessToken = _param[0]
    coordList = _param[1]
    starttime =_param[2]
    endtime = _param[3]
    for coord in coordList:

        # locator = coord[0]
        # print 'this is ' + str(locator) + ' of ' + str(len(coordList))
        lat = coord[2]
        lon = coord[1]
        urlForPage = genURL(accessToken, lat, lon,starttime,endtime,1)
        parseData1 = fetch(urlForPage)
        numPages = getTotal(parseData1)
        if numPages != 0:
            w = open(path + filename, 'a')
            contents = parseData1['statuses']
            if contents is not None:
                for content in contents:
                    result = extractInfo(content)
                    if result is not None:
                        w.write(result.encode('utf-8'))
                        w.close()
                        w = open(path + filename, 'a')
            # Loop api from page 2
            for i in range(1, numPages + 1):
                if i >26:
                    break
                print '(' + str(lat) + ';' + str(lon) + '); ' + str(i) + ' of ' + str(numPages)
                url = genURL(accessToken, lat, lon,starttime,endtime, i)
                parsedData = fetch(url)
                try:
                    contents = parsedData['statuses']
                    if contents is not None:
                        for content in contents:
                            result = extractInfo(content)
                            if result is not None:
                                w.write(result.encode('utf-8'))
                                w.close()
                                w = open(path + filename, 'a')
                except:
                    continue


# Multiprocessing
def startWorker(starttime,endtime):
    eve = int(math.ceil(len(AcoordList) / float(len(tokenList))))
    paramList = []
    for i in range(len(tokenList)):
        templist = []
        templist.append(tokenList[i])
        templist.append(AcoordList[i * eve:(i + 1) * eve])
        templist.append(starttime)
        templist.append(endtime)
        paramList.append(templist)
    pool = Pool(processes=len(tokenList))
    pool.map(worker, paramList)



# Export data
AcoordList = genCoord()
tokenList = genToken()

if __name__ == '__main__':
    #starttime = '1441036800'  # 2015-9-1
    #endtime = '1441900800'    # 2015-9-11
    #startWorker('1441036800','1441900800')

    #starttime = '1441900800'  # 2015-9-11
    #endtime = '1442764800'    # 2015-9-21
    #startWorker('1441900800','1442764800')

    #starttime = '1442764800'  # 2015-9-21
    #endtime = '1443542400'    # 2015-9-30
    #startWorker('1442764800','1443542400')

    #starttime = '1443542400'  # 2015-9-30
    #endtime = '1443974400'    # 2015-10-5
    #startWorker('1443542400','1443974400')

    #starttime = '1443974400'  # 2015-10-5
    #endtime = '1444838400'    # 2015-10-15
    #startWorker('1443974400','1444838400')

    #starttime = '1444838400'  # 2015-10-15
    #endtime = '1445702400'    # 2015-10-25
    startWorker('1451577600','1472659200')

    #starttime = '1445702400'  # 2015-10-25
    #endtime = '1446220800'    # 2015-10-31
    #startWorker('1445702400','1446220800')
    fwurl.close()
