# -*- coding: utf-8 -*-
from __future__ import division
import httplib2,json
import codecs
import zlib
import zipfile
import sys
import re
import datetime
import operator
import sqlite3
import MySQLdb as mysqldb
import json
import os
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from datetime import date
from dateutil import parser
import pytz 
from tzlocal import get_localzone
import requests
from termcolor import colored, cprint
from pygraphml.GraphMLParser import *
from pygraphml.Graph import *
from pygraphml.Node import *
from pygraphml.Edge import *

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time,re,sys
from selenium.webdriver.common.keys import Keys
import datetime
from bs4 import BeautifulSoup
from StringIO import StringIO

requests.adapters.DEFAULT_RETRIES = 10

h = httplib2.Http(".cache")

reload(sys)
sys.setdefaultencoding("utf-8")

facebook_username = "jeff.moriaty@rediffmail.com"
facebook_password = "bingos"

mysql_username = "root"
mysql_password = "cloud1!"
mysql_dbname = "facebook"


global uid
uid = ""
username = ""
internetAccess = True
cookies = {}
all_cookies = {}
reportFileName = ""

#For consonlidating all likes across Photos Likes+Post Likes
peopleIDList = []
likesCountList = []
timePostList = []
placesVisitedList = []

#Chrome Options
chromeOptions = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":1}
chromeOptions.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(chrome_options=chromeOptions)


#mysql database

conn = mysqldb.connect('localhost',mysql_username,mysql_password,mysql_dbname);


def createDatabase():
    conn = sqlite3.connect('facebook.db')
    c = conn.cursor()
    sql = 'create table if not exists photosLiked (sourceUID TEXT, description TEXT, photoURL TEXT unique, pageURL TEXT, username TEXT)'
    sql1 = 'create table if not exists photosCommented (sourceUID TEXT, description TEXT, photoURL TEXT unique, pageURL TEXT, username TEXT)'
    sql2 = 'create table if not exists friends (sourceUID TEXT, name TEXT, userName TEXT unique, month TEXT, year TEXT)'
    sql3 = 'create table if not exists friendsDetails (sourceUID TEXT, userName TEXT unique, userEduWork TEXT, userLivingCity TEXT, userCurrentCity TEXT, userLiveEvents TEXT, userGender TEXT, userStatus TEXT, userGroups TEXT)'
    sql4 = 'create table if not exists videosBy (sourceUID TEXT, title TEXT unique, url TEXT)'
    sql5 = 'create table if not exists pagesLiked (sourceUID TEXT, name TEXT unique, category TEXT,url TEXT)'
    sql6 = 'create table if not exists photosOf (sourceUID TEXT, description TEXT, photoURL TEXT unique, pageURL TEXT, username TEXT)'
    sql7 = 'create table if not exists photosBy (sourceUID TEXT, description TEXT, photoURL TEXT unique, pageURL TEXT, username TEXT)'
    
    c.execute(sql)
    c.execute(sql1)
    c.execute(sql2)
    c.execute(sql3)
    c.execute(sql4)
    c.execute(sql5)
    c.execute(sql6)
    c.execute(sql7)
    conn.commit()

#createDatabase()
#conn = sqlite3.connect('facebook.db')

#cursor = conn.cursor()


def createMaltego(username):
    g = Graph()
    totalCount = 50
    start = 0
    nodeList = []
    edgeList = []

    while(start<totalCount):
            nodeList.append("") 
            edgeList.append("")
            start+=1

    nodeList[0] = g.add_node('Facebook_'+username)
    nodeList[0]['node'] = createNodeFacebook(username,"https://www.facebook.com/"+username,uid)


    counter1=1
    counter2=0                
    userList=[]

    c = conn.cursor()
    c.execute('select userName from friends where sourceUID=?',(uid,))
    dataList = c.fetchall()
    nodeUid = ""
    for i in dataList:
        if i[0] not in userList:
            userList.append(i[0])
            try:
                nodeUid = str(convertUser2ID2(driver,str(i[0])))
                #nodeUid = str(convertUser2ID(str(i[0])))
                nodeList[counter1] = g.add_node("Facebook_"+str(i[0]))
                nodeList[counter1]['node'] = createNodeFacebook(i[0],'https://www.facebook.com/'+str(i[0]),nodeUid)
                edgeList[counter2] = g.add_edge(nodeList[0], nodeList[counter1])
                edgeList[counter2]['link'] = createLink('Facebook')
                nodeList.append("")
                edgeList.append("")
                counter1+=1
                counter2+=1
            except IndexError:
                continue
    if len(nodeUid)>0:  
        parser = GraphMLParser()
        if not os.path.exists(os.getcwd()+'/Graphs'):
                os.makedirs(os.getcwd()+'/Graphs')
        filename = 'Graphs/Graph1.graphml'
        parser.write(g, "Graphs/Graph1.graphml")
        cleanUpGraph(filename)
        filename = username+'_maltego.mtgx'
        print 'Creating archive: '+filename
        zf = zipfile.ZipFile(filename, mode='w')
        print 'Adding Graph1.graphml'
        zf.write('Graphs/Graph1.graphml')
        print 'Closing'
        zf.close()
 
def createLink(label):
    xmlString = '<mtg:MaltegoLink xmlns:mtg="http://maltego.paterva.com/xml/mtgx" type="maltego.link.manual-link">'
    xmlString += '<mtg:Properties>'
    xmlString += '<mtg:Property displayName="Description" hidden="false" name="maltego.link.manual.description" nullable="true" readonly="false" type="string">'
    xmlString += '<mtg:Value/>'
    xmlString += '</mtg:Property>'
    xmlString += '<mtg:Property displayName="Style" hidden="false" name="maltego.link.style" nullable="true" readonly="false" type="int">'
    xmlString += '<mtg:Value>0</mtg:Value>'
    xmlString += '</mtg:Property>'
    xmlString += '<mtg:Property displayName="Label" hidden="false" name="maltego.link.manual.type" nullable="true" readonly="false" type="string">'
    xmlString += '<mtg:Value>'+label+'</mtg:Value>'
    xmlString += '</mtg:Property>'
    xmlString += '<mtg:Property displayName="Show Label" hidden="false" name="maltego.link.show-label" nullable="true" readonly="false" type="int">'
    xmlString += '<mtg:Value>0</mtg:Value>'
    xmlString += '</mtg:Property>'
    xmlString += '<mtg:Property displayName="Thickness" hidden="false" name="maltego.link.thickness" nullable="true" readonly="false" type="int">'
    xmlString += '<mtg:Value>2</mtg:Value>'
    xmlString += '</mtg:Property>'
    xmlString += '<mtg:Property displayName="Color" hidden="false" name="maltego.link.color" nullable="true" readonly="false" type="color">'
    xmlString += '<mtg:Value>8421505</mtg:Value>'
    xmlString += '</mtg:Property>'
    xmlString += '</mtg:Properties>'
    xmlString += '</mtg:MaltegoLink>'
    return xmlString

def createNodeImage(name,url):
    xmlString = '<mtg:MaltegoEntity xmlns:mtg="http://maltego.paterva.com/xml/mtgx" type="maltego.Image">'
    xmlString += '<mtg:Properties>'
    xmlString += '<mtg:Property displayName="Description" hidden="false" name="description" nullable="true" readonly="false" type="string">'
    xmlString += '<mtg:Value>'+name+'</mtg:Value>'
    xmlString += '</mtg:Property>'
    xmlString += '<mtg:Property displayName="URL" hidden="false" name="url" nullable="true" readonly="false" type="url">'
    xmlString += '<mtg:Value>'+url+'</mtg:Value>'
    xmlString += '</mtg:Property>'
    xmlString += '</mtg:Properties>'
    xmlString += '</mtg:MaltegoEntity>'
    return xmlString

def createNodeFacebook(displayName,url,uid):
    xmlString = '<mtg:MaltegoEntity xmlns:mtg="http://maltego.paterva.com/xml/mtgx" type="maltego.affiliation.Facebook">'
    xmlString += '<mtg:Properties>'
    xmlString += '<mtg:Property displayName="Name" hidden="false" name="person.name" nullable="true" readonly="false" type="string">'
    xmlString += '<mtg:Value>'+displayName+'</mtg:Value>'
    xmlString += '</mtg:Property>'
    xmlString += '<mtg:Property displayName="Network" hidden="false" name="affiliation.network" nullable="true" readonly="true" type="string">'
    xmlString += '<mtg:Value>Facebook</mtg:Value>'
    xmlString += '</mtg:Property>'
    xmlString += '<mtg:Property displayName="UID" hidden="false" name="affiliation.uid" nullable="true" readonly="false" type="string">'
    xmlString += '<mtg:Value>'+str(uid)+'</mtg:Value>'
    xmlString += '</mtg:Property>'
    xmlString += '<mtg:Property displayName="Profile URL" hidden="false" name="affiliation.profile-url" nullable="true" readonly="false" type="string">'
    xmlString += '<mtg:Value>'+url+'</mtg:Value>'
    xmlString += '</mtg:Property>'
    xmlString += '</mtg:Properties>'
    xmlString += '</mtg:MaltegoEntity>'
    return xmlString

def createNodeUrl(displayName,url):
        xmlString = '<mtg:MaltegoEntity xmlns:mtg="http://maltego.paterva.com/xml/mtgx" type="maltego.URL">'
        xmlString += '<mtg:Properties>'
        xmlString += '<mtg:Property displayName="'+displayName+'" hidden="false" name="short-title" nullable="true" readonly="false" type="string">'
        xmlString += '<mtg:Value>'+displayName+'</mtg:Value>'
        xmlString += '</mtg:Property>'
        xmlString += '<mtg:Property displayName="'+displayName+'" hidden="false" name="url" nullable="true" readonly="false" type="url">'  
        xmlString += '<mtg:Value>'+displayName+'</mtg:Value>'
        xmlString += '</mtg:Property>'
        xmlString += '<mtg:Property displayName="Title" hidden="false" name="title" nullable="true" readonly="false" type="string">'
        xmlString += '<mtg:Value/>'    
        xmlString += '</mtg:Property>'
        xmlString += '</mtg:Properties>'
        xmlString += '</mtg:MaltegoEntity>'
        return xmlString

def createNodeLocation(lat,lng):
    xmlString = '<mtg:MaltegoEntity xmlns:mtg="http://maltego.paterva.com/xml/mtgx" type="maltego.Location">'
    xmlString += '<mtg:Properties>'
    xmlString += '<mtg:Property displayName="Name" hidden="false" name="location.name" nullable="true" readonly="false" type="string">'
    xmlString += '<mtg:Value>lat='+str(lat)+' lng='+str(lng)+'</mtg:Value>'
    xmlString += '</mtg:Property>'
    xmlString += '<mtg:Property displayName="Area Code" hidden="false" name="location.areacode" nullable="true" readonly="false" type="string">'
    xmlString += '<mtg:Value/>'
    xmlString += '</mtg:Property>'
    xmlString += '<mtg:Property displayName="Area" hidden="false" name="location.area" nullable="true" readonly="false" type="string">'
    xmlString += '<mtg:Value/>'
    xmlString += '</mtg:Property>'
    xmlString += '<mtg:Property displayName="Latitude" hidden="false" name="latitude" nullable="true" readonly="false" type="float">'
    xmlString += '<mtg:Value/>'
    xmlString += '</mtg:Property>'
    xmlString += '<mtg:Property displayName="Longitude" hidden="false" name="longitude" nullable="true" readonly="false" type="float">'
    xmlString += '<mtg:Value/>'
    xmlString += '</mtg:Property>'
    xmlString += '<mtg:Property displayName="Country" hidden="false" name="country" nullable="true" readonly="false" type="string">'
    xmlString += '<mtg:Value/>'
    xmlString += '</mtg:Property>'
    xmlString += '<mtg:Property displayName="Country Code" hidden="false" name="countrycode" nullable="true" readonly="false" type="string">'
    xmlString += '<mtg:Value/>'
    xmlString += '</mtg:Property>'
    xmlString += '<mtg:Property displayName="City" hidden="false" name="city" nullable="true" readonly="false" type="string">'
    xmlString += '<mtg:Value/>'
    xmlString += '</mtg:Property>'
    xmlString += '<mtg:Property displayName="Street Address" hidden="false" name="streetaddress" nullable="true" readonly="false" type="string">'   
    xmlString += '<mtg:Value/>'
    xmlString += '</mtg:Property>'
    xmlString += '</mtg:Properties>'
    xmlString += '</mtg:MaltegoEntity>'
    return xmlString

def cleanUpGraph(filename):
    newContent = []
    with open(filename) as f:
        content = f.readlines()
        for i in content:
            if '<key attr.name="node" attr.type="string" id="node"/>' in i:
                i = i.replace('name="node" attr.type="string"','name="MaltegoEntity" for="node"')
            if '<key attr.name="link" attr.type="string" id="link"/>' in i:
                i = i.replace('name="link" attr.type="string"','name="MaltegoLink" for="edge"')
            i = i.replace("&lt;","<")
            i = i.replace("&gt;",">")
            i = i.replace("&quot;",'"')
            print i.strip()
            newContent.append(i.strip())

    f = open(filename,'w')
    for item in newContent:
        f.write("%s\n" % item)
    f.close()

def normalize(s):
    if type(s) == unicode: 
            return s.encode('utf8', 'ignore')
    else:
            return str(s)

def findUser(findName):
    stmt = "SELECT uid,current_location,username,name FROM user WHERE contains('"+findName+"')"
    stmt = stmt.replace(" ","+")
    url="https://graph.facebook.com/fql?q="+stmt+"&access_token="+facebook_access_token
    resp, content = h.request(url, "GET")
    results = json.loads(content)
    count=1
    for x in results['data']:
        print str(count)+'\thttp://www.facebook.com/'+x['username']
        count+=1

def convertUser2ID2(driver,username):
    url="http://graph.facebook.com/"+username
    resp, content = h.request(url, "GET")
    if resp.status==200:
        results = json.loads(content)
        if len(results['id'])>0:
            fbid = results['id']
            return fbid

def convertUser2ID(username):
    stmt = "SELECT uid,current_location,username,name FROM user WHERE username=('"+username+"')"
    stmt = stmt.replace(" ","+")
    url="https://graph.facebook.com/fql?q="+stmt+"&access_token="+facebook_access_token
    resp, content = h.request(url, "GET")
    if resp.status==200:
        results = json.loads(content)
        if len(results['data'])>0:
            return results['data'][0]['uid']
        else:
            print "[!] Can't convert username 2 uid. Please check username"
            sys.exit()
            return 0
    else:
        print "[!] Please check your facebook_access_token before continuing"
        sys.exit()
        return 0

def convertID2User(uid):
    stmt = "SELECT uid,current_location,username,name FROM user WHERE uid=('"+uid+"')"
    stmt = stmt.replace(" ","+")
    url="https://graph.facebook.com/fql?q="+stmt+"&access_token="+facebook_access_token
    resp, content = h.request(url, "GET")
    results = json.loads(content)
    return results['data'][0]['uid']


def loginFacebook(driver):
    driver.implicitly_wait(120)
    driver.get("https://www.facebook.com/")
    assert "Welcome to Facebook" in driver.title
    time.sleep(3)
    driver.find_element_by_id('email').send_keys(facebook_username)
    driver.find_element_by_id('pass').send_keys(facebook_password)
    driver.find_element_by_id("loginbutton").click()
    global all_cookies
    all_cookies = driver.get_cookies()
    html = driver.page_source
    if "Incorrect Email/Password Combination" in html:
        print "[!] Incorrect Facebook username (email address) or password"
        sys.exit()

def writeToMysqlDB(tableName, dataList):
    print tableName
    print dataList
    global conn
    if not conn.open:
        conn = mysqldb.connect('localhost',mysql_username,mysql_password,mysql_dbname);
    cursor=conn.cursor()
    first="INSERT INTO "+tableName+" (";
    temp =" VALUES ("
    #print dataList
    noOfColumns=len(dataList)
    cursor.execute("DESC "+tableName)
    desc=cursor.fetchall()
    temp2 = ()
    cnt=0
    for i in dataList:
        temp+= "%s,"
        if(desc[cnt][5]=="auto_increment"):
            cnt+=1
        first+=desc[cnt][0]+",";
        if  desc[cnt][1].startswith("varchar") or desc[cnt][1].startswith("mediumtext") or desc[cnt][1].startswith("text") or desc[cnt][1].startswith("longtext") or desc[cnt][1].startswith("tinytext") or desc[cnt][1].startswith("char"):
            temp2+=("'"+i+"'",);
        else:
            temp2+=(str(i),);
        cnt+=1
    temp=temp[:-1]
    first=first[:-1]
    first+=")"
    temp+=")"
    try:
        cursor.execute(first+temp,temp2)
        conn.commit()
    except:
        conn.rollback()        
    cursor.close()
    

def write2Database(dbName,dataList):
    try:
        cprint("[*] Writing "+str(len(dataList))+" record(s) to database table: "+dbName,"white")
        #print "[*] Writing "+str(len(dataList))+" record(s) to database table: "+dbName
        numOfColumns = len(dataList[0])
        c = conn.cursor()
        if numOfColumns==3:
            for i in dataList:
                try:
                    c.execute('INSERT INTO '+dbName+' VALUES (?,?,?)', i)
                    conn.commit()
                except sqlite3.IntegrityError:
                    continue
        if numOfColumns==4:
            for i in dataList:
                try:
                    c.execute('INSERT INTO '+dbName+' VALUES (?,?,?,?)', i)
                    conn.commit()
                except sqlite3.IntegrityError:
                    continue
        if numOfColumns==5:
            for i in dataList:
                try:
                    c.execute('INSERT INTO '+dbName+' VALUES (?,?,?,?,?)', i)
                    conn.commit()
                except sqlite3.IntegrityError:
                    continue
        if numOfColumns==9:
            for i in dataList:
                try:
                    c.execute('INSERT INTO '+dbName+' VALUES (?,?,?,?,?,?,?,?,?)', i)
                    conn.commit()
                except sqlite3.IntegrityError:
                    continue
    except TypeError as e:
        print e
        pass
    except IndexError as e:
        print e
        pass

def downloadFile(url):  
    global cookies
    for s_cookie in all_cookies:
            cookies[s_cookie["name"]]=s_cookie["value"]
    r = requests.get(url,cookies=cookies)
    html = r.content
    return html

def parsePost(id,username):
    filename = 'posts__'+str(id)
    #if not os.path.lexists(filename):
    print "[*] Caching Facebook Post: "+str(id)
    url = "https://www.facebook.com/"+username+"/posts/"+str(id)     # here id refers to post id
    driver.get(url) 
    if "Sorry, this page isn't available" in driver.page_source:
        print "[!] Cannot access page "+url
        return ""
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        while(match==False):
            time.sleep(1)
            lastCount = lenOfPage
            lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount==lenOfPage:
                match=True
    html1 = driver.page_source  
    #text_file = open(filename, "w")
    #text_file.write(normalize(html1))
    #text_file.close()
    #else:
    #   html1 = open(filename, 'r').read()
    soup1 = BeautifulSoup(html1)
    htmlList = soup1.find("h5",{"class" : "_6nl"})
    tlTime = soup1.find("abbr")
    if " at " in str(htmlList):
        soup2 = BeautifulSoup(str(htmlList))
        locationList = soup2.findAll("a",{"class" : "profileLink"})
        locUrl = locationList[len(locationList)-1]['href']
        locDescription = locationList[len(locationList)-1].text
        print locDescription
        locTime = tlTime['data-utime']
        placesVisitedList.append([locTime,locDescription,locUrl])


def parseLikesPosts(id):
    peopleID = []
    #filename = 'likes_'+str(id)
    #if not os.path.lexists(filename):
    print "[*] Caching Post Likes: "+str(id)
    url = "https://www.facebook.com/browse/likes?id="+str(id)
    driver.get(url) 
    if "Sorry, this page isn't available" in driver.page_source:
        print "[!] Cannot access page "+url
        return ""
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        while(match==False):
            time.sleep(1)
            lastCount = lenOfPage
            lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount==lenOfPage:
                match=True
    html1 = driver.page_source  
    #   text_file = open(filename, "w")
    #   text_file.write(normalize(html1))
    #   text_file.close()
    #else:
    #   html1 = open(filename, 'r').read()
    soup1 = BeautifulSoup(html1)
    peopleLikeList = soup1.findAll("div",{"class" : "fsl fwb fcb"})
    # for every faebook post like there is a separate class 
    if len(peopleLikeList)>0:
        print "[*] Extracting Likes from Post: "+str(id)
        for x in peopleLikeList:
            soup2 = BeautifulSoup(str(x))
            peopleLike = soup2.find("a")
            peopleLikeID = peopleLike['href'].split('?')[0].replace('https://www.facebook.com/','')
            if peopleLikeID == 'profile.php':   
                r = re.compile('id=(.*?)&fref')
                m = r.search(str(peopleLike['href']))
                if m:
                    peopleLikeID = m.group(1)
            print "[*] Liked Post: "+"\t"+peopleLikeID
            if peopleLikeID not in peopleID:
                peopleID.append(peopleLikeID)
        
        return peopleID 

def parseTimeline(html,username):
    soup = BeautifulSoup(html)  
    tlTime = soup.findAll("abbr")
    temp123 = soup.findAll("div",{"class" : "_4-u2 mbm _5jmm _5pat _5v3q _5x16"})
    placesCheckin = []
    timeOfPostList = []

    counter = 0

    for y in temp123:
        soup1 = BeautifulSoup(str(y))
        tlDateTimeLoc = soup1.findAll("a",{"class" : "_5pcq"})
        #print tlDateTimeLoc
        # uilinksubtle class contains the post-id,date, time and location info of the post
        #Universal Time
        try:
            #print tlDateTimeLoc[0]
            soup2 = BeautifulSoup(str(tlDateTimeLoc[0]))
            tlDateTime = soup2.find("abbr")
            print tlDateTime
            #Facebook Post Link 
            tlLink = tlDateTimeLoc[0]['href']
            print tlLink # the link to the post
            try:
                tz = get_localzone()
                unixTime = str(tlDateTime['data-utime'])
                localTime = (datetime.datetime.fromtimestamp(int(unixTime)).strftime('%Y-%m-%d %H:%M:%S'))
                #print localTime # date time obtained from the timestamp
                timePostList.append(localTime)
                #timeOfPost = localTime
                timeOfPostList.append(localTime)
                print "[*] Time of Post: "+localTime
            except TypeError:
                continue
            if "posts" in tlLink:
                #print tlLink.strip()
                pageID = tlLink.split("/")
                # pageid contains the facebok userid and the post id
                #print pageID
                parsePost(pageID[3],username)               
                peopleIDLikes = parseLikesPosts(pageID[3])
                try:
                    for id1 in peopleIDLikes:
                        global peopleIDList
                        global likesCountList
                        if id1 in peopleIDList:
                            lastCount = 0
                            position = peopleIDList.index(id1)
                            likesCountList[position] +=1
                        else:
                            peopleIDList.append(id1)
                            likesCountList.append(1)
                except TypeError:
                    continue

            if len(tlDateTimeLoc)>2:
                try:
                    #Device / Location
                    if len(tlDateTimeLoc[1].text)>0:
                        print "[*] Location of Post: "+unicode(tlDateTimeLoc[1].text)
                    if len(tlDateTimeLoc[2].text)>0:
                        print "[*] Device: "+str(tlDateTimeLoc[2].text)
                except IndexError:
                    continue    

            else:
                try:
                    #Device / Location
                    if len(tlDateTimeLoc[1].text)>0:
                        if "mobile" in tlDateTimeLoc[1].text:
                            print "[*] Device: "+str(tlDateTimeLoc[1].text)
                        else:
                            print "[*] Location of Post: "+unicode(tlDateTimeLoc[1].text)
                    
                except IndexError:
                    continue    
            #Facebook Posts
            tlPosts = soup1.find("span",{"class" : "userContent"})
            print tlPosts
            """try:
                tlPostSec = soup1.findall("span",{"class" : "userContentSecondary fcg"})
                tlPostMsg = ""
                #Places Checked In
            except TypeError:
                continue
            soup3 = BeautifulSoup(str(tlPostSec))
            hrefLink = soup3.find("a")"""
            # commented the above portion cause its not being used

            """
            if len(str(tlPostSec))>0:
                tlPostMsg = str(tlPostSec)
                #if " at " in str(tlPostMsg) and " with " not in str(tlPostMsg):
                if " at " in str(tlPostMsg):
                    print str(tlPostSec)

                    print tlPostMsg
                    #print hrefLink
                    #placeUrl = hrefLink['href'].encode('utf8').split('?')[0]
                    #print "[*] Place: "+placeUrl                                       
                    #placesCheckin.append([timeOfPost,placeUrl])
            """

            try:
                if len(tlPosts)>0:  
                    tlPostStr = re.sub('<[^>]*>',"", str(tlPosts))
                    #print tlPostStr
                    if tlPostStr!=None:
                        print "[*] Message: "+str(tlPostStr)
            except TypeError as e:
                continue

            tlPosts = soup1.find("div",{"class" : "translationEligibleUserMessage userContent"})
            try:
                if len(tlPosts)>0:
                    tlPostStr = re.sub('<[^>]*>',"", str(tlPosts))  
                    print "[*] Message: "+str(tlPostStr)    
            except TypeError:
                continue
        except IndexError as e:
            continue
        counter+=1
    
    tlDeviceLoc = soup.findAll("a",{"class" : "uiLinkSubtle"})

    print '\n'

    # global reportFileName
    # if len(reportFileName)<1:
    #     reportFileName = username+"_report.txt"
    # reportFile = open(reportFileName, "w")
    
    # reportFile.write("\n********** Places Visited By "+str(username)+" **********\n")
    # filename = username+'_placesVisited.htm'
    # if not os.path.lexists(filename):
    #     html = downloadPlacesVisited(driver,uid)
    #     text_file = open(filename, "w")
    #     text_file.write(html.encode('utf8'))
    #     text_file.close()
    # else:
    #     html = open(filename, 'r').read()
    # dataList = parsePlacesVisited(html)
    # count=1
    # for i in dataList:
    #     reportFile.write(normalize(i[2])+'\t'+normalize(i[1])+'\t'+normalize(i[3])+'\n')
    #     count+=1
    
    # reportFile.write("\n********** Places Liked By "+str(username)+" **********\n")
    # filename = username+'_placesLiked.htm'
    # if not os.path.lexists(filename):
    #     html = downloadPlacesLiked(driver,uid)
    #     text_file = open(filename, "w")
    #     text_file.write(html.encode('utf8'))
    #     text_file.close()
    # else:
    #     html = open(filename, 'r').read()
    # dataList = parsePlacesLiked(html)
    # count=1
    # for i in dataList:
    #     reportFile.write(normalize(i[2])+'\t'+normalize(i[1])+'\t'+normalize(i[3])+'\n')
    #     count+=1

    # reportFile.write("\n********** Places checked in **********\n")
    # for places in placesVisitedList:
    #     unixTime = places[0]
    #     localTime = (datetime.datetime.fromtimestamp(int(unixTime)).strftime('%Y-%m-%d %H:%M:%S'))
    #     reportFile.write(localTime+'\t'+normalize(places[1])+'\t'+normalize(places[2])+'\n')

    # reportFile.write("\n********** Apps used By "+str(username)+" **********\n")
    # filename = username+'_apps.htm'
    # if not os.path.lexists(filename):
    #     html = downloadAppsUsed(driver,uid)
    #     text_file = open(filename, "w")
    #     text_file.write(html.encode('utf8'))
    #     text_file.close()
    # else:
    #     html = open(filename, 'r').read()
    # data1 = parseAppsUsed(html)
    # result = ""
    # for x in data1:
    #     reportFile.write(normalize(x)+'\n')
    #     x = x.lower()
    #     if "blackberry" in x:
    #         result += "[*] User is using a Blackberry device\n"
    #     if "android" in x:
    #         result += "[*] User is using an Android device\n"
    #     if "ios" in x or "ipad" in x or "iphone" in x:
    #         result += "[*] User is using an iOS Apple device\n"
    #     if "samsung" in x:
    #         result += "[*] User is using a Samsung Android device\n"
    # reportFile.write(result)

    # reportFile.write("\n********** Videos Posted By "+str(username)+" **********\n")
    # filename = username+'_videosBy.htm'
    # if not os.path.lexists(filename):
    #     html = downloadVideosBy(driver,uid)
    #     text_file = open(filename, "w")
    #     text_file.write(html.encode('utf8'))
    #     text_file.close()
    # else:
    #     html = open(filename, 'r').read()
    # dataList = parseVideosBy(html)
    # count=1
    # for i in dataList:
    #     reportFile.write(normalize(i[2])+'\t'+normalize(i[1])+'\n')
    #     count+=1

    # reportFile.write("\n********** Pages Liked By "+str(username)+" **********\n")
    # filename = username+'_pages.htm'
    # if not os.path.lexists(filename):
    #     print "[*] Caching Pages Liked: "+username
    #     html = downloadPagesLiked(driver,uid)
    #     text_file = open(filename, "w")
    #     text_file.write(html.encode('utf8'))
    #     text_file.close()
    # else:
    #     html = open(filename, 'r').read()
    # dataList = parsePagesLiked(html)
    # for i in dataList:
    #     pageName = normalize(i[0])
    #     tmpStr  = '\t'+normalize(i[0])+'\t'+normalize(i[1])+'\n'
    #     reportFile.write(tmpStr)
    # print "\n"

    '''c = conn.cursor()
    reportFile.write("\n********** Friendship History of "+str(username)+" **********\n")
    c.execute('select * from friends where sourceUID=?',(uid,))
    dataList = c.fetchall()
    try:
        if len(str(dataList[0][4]))>0:
            for i in dataList:
                #Date First followed by Username
                reportFile.write(normalize(i[4])+'\t'+normalize(i[3])+'\t'+normalize(i[2])+'\t'+normalize(i[1])+'\n')
                #Username followed by Date
                #reportFile.write(normalize(i[4])+'\t'+normalize(i[3])+'\t'+normalize(i[2])+'\t'+normalize(i[1])+'\n')
        print '\n'
    except IndexError:
        pass

    reportFile.write("\n********** Friends of "+str(username)+" **********\n")
    reportFile.write("*** Backtracing from Facebook Likes/Comments/Tags ***\n\n")
    c = conn.cursor()
    c.execute('select userName from friends where sourceUID=?',(uid,))
    dataList = c.fetchall()
    for i in dataList:
        reportFile.write(str(i[0])+'\n')
    print '\n'

    tempList = []
    totalLen = len(timeOfPostList)
    timeSlot1 = 0
    timeSlot2 = 0
    timeSlot3 = 0 
    timeSlot4 = 0
    timeSlot5 = 0 
    timeSlot6 = 0 
    timeSlot7 = 0 
    timeSlot8 = 0 

    count = 0
    if len(peopleIDList)>0:
        likesCountList, peopleIDList  = zip(*sorted(zip(likesCountList,peopleIDList),reverse=True))
    
        reportFile.write("\n********** Analysis of Facebook Post Likes **********\n")
        while count<len(peopleIDList):
            testStr = str(likesCountList[count]).encode('utf8')+'\t'+str(peopleIDList[count]).encode('utf8')
            reportFile.write(testStr+"\n")
            count+=1    

    reportFile.write("\n********** Analysis of Interactions between "+str(username)+" and Friends **********\n")
    c = conn.cursor()
    c.execute('select userName from friends where sourceUID=?',(uid,))
    dataList = c.fetchall()
    photosliked = []
    photoscommented = []
    userID = []
    
    photosLikedUser = []
    photosLikedCount = []
    photosCommentedUser = []
    photosCommentedCount = []
    
    for i in dataList:
        c.execute('select * from photosLiked where sourceUID=? and username=?',(uid,i[0],))
        dataList1 = []
        dataList1 = c.fetchall()
        if len(dataList1)>0:
            photosLikedUser.append(normalize(i[0]))
            photosLikedCount.append(len(dataList1))
    for i in dataList:
        c.execute('select * from photosCommented where sourceUID=? and username=?',(uid,i[0],))
        dataList1 = []
        dataList1 = c.fetchall()
        if len(dataList1)>0:    
            photosCommentedUser.append(normalize(i[0]))
            photosCommentedCount.append(len(dataList1))
    if(len(photosLikedCount)>1):    
        reportFile.write("Photo Likes: "+str(username)+" and Friends\n")
        photosLikedCount, photosLikedUser  = zip(*sorted(zip(photosLikedCount, photosLikedUser),reverse=True))  
        count=0
        while count<len(photosLikedCount):
            tmpStr = str(photosLikedCount[count])+'\t'+normalize(photosLikedUser[count])+'\n'
            count+=1
            reportFile.write(tmpStr)
    if(len(photosCommentedCount)>1):    
        reportFile.write("\n********** Comments on "+str(username)+"'s Photos **********\n")
        photosCommentedCount, photosCommentedUser  = zip(*sorted(zip(photosCommentedCount, photosCommentedUser),reverse=True))  
        count=0
        while count<len(photosCommentedCount):
            tmpStr = str(photosCommentedCount[count])+'\t'+normalize(photosCommentedUser[count])+'\n'
            count+=1
            reportFile.write(tmpStr)


    reportFile.write("\n********** Analysis of Time in Facebook **********\n")
    for timePost in timeOfPostList:
        tempList.append(timePost.split(" ")[1])
        tempTime = (timePost.split(" ")[1]).split(":")[0]
        tempTime = int(tempTime)
        if tempTime >= 21:
            timeSlot8+=1
        if tempTime >= 18 and tempTime < 21:
            timeSlot7+=1
        if tempTime >= 15 and tempTime < 18:
            timeSlot6+=1
        if tempTime >= 12 and tempTime < 15:
            timeSlot5+=1
        if tempTime >= 9 and tempTime < 12:
            timeSlot4+=1
        if tempTime >= 6 and tempTime < 9:
            timeSlot3+=1
        if tempTime >= 3 and tempTime < 6:
            timeSlot2+=1
        if tempTime >= 0 and tempTime < 3:
            timeSlot1+=1
    reportFile.write("Total % (00:00 to 03:00) "+str((timeSlot1/totalLen)*100)+" %\n")
    reportFile.write("Total % (03:00 to 06:00) "+str((timeSlot2/totalLen)*100)+" %\n")
    reportFile.write("Total % (06:00 to 09:00) "+str((timeSlot3/totalLen)*100)+" %\n")
    reportFile.write("Total % (09:00 to 12:00) "+str((timeSlot4/totalLen)*100)+" %\n")
    reportFile.write("Total % (12:00 to 15:00) "+str((timeSlot5/totalLen)*100)+" %\n")
    reportFile.write("Total % (15:00 to 18:00) "+str((timeSlot6/totalLen)*100)+" %\n")
    reportFile.write("Total % (18:00 to 21:00) "+str((timeSlot7/totalLen)*100)+" %\n")
    reportFile.write("Total % (21:00 to 24:00) "+str((timeSlot8/totalLen)*100)+" %\n")


    reportFile.write("\nDate/Time of Facebook Posts\n")
    for timePost in timeOfPostList:
        reportFile.write(timePost+'\n')'''

    #reportFile.close()

def downloadTimeline(username):
    url = 'https://www.facebook.com/'+username.strip()
    driver.get(url) 
    print "[*] Crawling Timeline"
    if "Sorry, this page isn't available" in driver.page_source:
        print "[!] Cannot access page "+url
        return ""
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        while(match==False):
            lastCount = lenOfPage
            time.sleep(3)
            lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount==lenOfPage:
                print "[*] Looking for 'Show Older Stories' Link"
            try:
                clickLink = WebDriverWait(driver, 1).until(lambda driver : driver.find_element_by_link_text('Show Older Stories'))
                if clickLink:
                    print "[*] Clicked 'Show Older Stories' Link"
                    driver.find_element_by_link_text('Show Older Stories').click()
                else:
                    print "[*] Indexing Timeline"
                    break
                match=True
            except TimeoutException:                
                match = True
    return driver.page_source




def downloadPlacesVisited(driver,userid):
    url = 'https://www.facebook.com/search/'+str(userid).strip()+'/places-visited'
    driver.get(url) 
    if "Sorry, this page isn't available" in driver.page_source:
        print "[!] Cannot access page "+url
        return ""
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        while(match==False):
                time.sleep(3)
                lastCount = lenOfPage
                lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                if lastCount==lenOfPage:
                        match=True
    return driver.page_source

def downloadPlacesLiked(driver,userid):
    url = 'https://www.facebook.com/search/'+str(userid).strip()+'/places-liked'
    driver.get(url) 
    if "Sorry, this page isn't available" in driver.page_source:
        print "[!] Cannot access page "+url
        return ""
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        while(match==False):
                time.sleep(3)
                lastCount = lenOfPage
                lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                if lastCount==lenOfPage:
                        match=True
    return driver.page_source


def downloadVideosBy(driver,userid):
    url = 'https://www.facebook.com/search/'+str(userid).strip()+'/videos-by'
    driver.get(url) 
    if "Sorry, this page isn't available" in driver.page_source:
        print "[!] Cannot access page "+url
        return ""
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        while(match==False):
                time.sleep(3)
                lastCount = lenOfPage
                lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                if lastCount==lenOfPage:
                        match=True
    return driver.page_source

def downloadUserInfo(driver,userid):
    url = 'https://www.facebook.com/'+str(userid).strip()+'/info'
    driver.get(url) 
    if "Sorry, this page isn't available" in driver.page_source:
        print "[!] Cannot access page "+url
        return ""
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        while(match==False):
                time.sleep(3)
                lastCount = lenOfPage
                lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                if lastCount==lenOfPage:
                        match=True
    return driver.page_source

def downloadPhotosBy(driver,userid):
    driver.get('https://www.facebook.com/search/'+str(userid)+'/photos-by')
    if "Sorry, we couldn't find any results for this search." in driver.page_source:
        print "Photos commented list is hidden"
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        while(match==False):
                time.sleep(3)
                lastCount = lenOfPage
                lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                if lastCount==lenOfPage:
                        match=True
    return driver.page_source

def downloadPhotosOf(driver,userid):
    driver.get('https://www.facebook.com/search/'+str(userid)+'/photos-of')
    if "Sorry, we couldn't find any results for this search." in driver.page_source:
        print "Photos commented list is hidden"
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        while(match==False):
                time.sleep(5)
                lastCount = lenOfPage
                lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                if lastCount==lenOfPage:
                        match=True
    return driver.page_source

def downloadPhotosBy(driver,userid):
    driver.get('https://www.facebook.com/search/'+str(userid)+'/photos-by')
    if "Sorry, we couldn't find any results for this search." in driver.page_source:
        print "Photos commented list is hidden"
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        while(match==False):
                time.sleep(5)
                lastCount = lenOfPage
                lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                if lastCount==lenOfPage:
                        match=True
    return driver.page_source

def downloadEventsJoined(driver,userid):
    driver.get('https://www.facebook.com/search/'+str(userid)+'/events-joined')
    if "Sorry, we couldn't find any results for this search." in driver.page_source:
        print "Events joined list is hidden"
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        while(match==False):
                time.sleep(5)
                lastCount = lenOfPage
                lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                if lastCount==lenOfPage:
                        match=True
    return driver.page_source

def downloadPhotosCommented(driver,userid):
    driver.get('https://www.facebook.com/search/'+str(userid)+'/photos-commented')
    if "Sorry, we couldn't find any results for this search." in driver.page_source:
        print "Photos commented list is hidden"
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        while(match==False):
                time.sleep(5)
                lastCount = lenOfPage
                lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                if lastCount==lenOfPage:
                        match=True
    return driver.page_source

def downloadVideosCommented(driver,userid):
    driver.get('https://www.facebook.com/search/'+str(userid)+'/videos-commented')
    if "Sorry, we couldn't find any results for this search." in driver.page_source:
        print "Photos commented list is hidden"
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        while(match==False):
                time.sleep(5)
                lastCount = lenOfPage
                lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                if lastCount==lenOfPage:
                        match=True
    return driver.page_source
    
def downloadPhotosLiked(driver,userid):
    driver.get('https://www.facebook.com/search/'+str(userid)+'/photos-liked')
    if "Sorry, we couldn't find any results for this search." in driver.page_source:
        print "Pages liked list is hidden"
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        while(match==False):
                time.sleep(5)
                lastCount = lenOfPage
                lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                if lastCount==lenOfPage:
                        match=True
    print "returning page source"
    return driver.page_source
    

def downloadPagesLiked(driver,userid):
    driver.get('https://www.facebook.com/search/'+str(userid)+'/pages-liked')
    if "Sorry, we couldn't find any results for this search." in driver.page_source:
        print "Pages liked list is hidden"
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        while(match==False):
                time.sleep(3)
                lastCount = lenOfPage
                lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                if lastCount==lenOfPage:
                        match=True
    return driver.page_source

def downloadFriends(driver,userid):
    driver.get('https://www.facebook.com/search/'+str(userid)+'/friends')
    if "Sorry, we couldn't find any results for this search." in driver.page_source:
        print "Friends list is hidden"
        return ""
    else:
        #assert "Friends of " in driver.title
            lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            match=False
            while(match==False):
                    time.sleep(3)
                    lastCount = lenOfPage
                    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                    if lastCount==lenOfPage:
                            match=True
    return driver.page_source

def downloadAppsUsed(driver,userid):
    driver.get('https://www.facebook.com/search/'+str(userid)+'/apps-used')
    if "Sorry, we couldn't find any results for this search." in driver.page_source:
        print "[!] Apps used list is hidden"
        return ""
    else:
            lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            match=False
            while(match==False):
                    time.sleep(3)
                    lastCount = lenOfPage
                    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                    if lastCount==lenOfPage:
                            match=True
    return driver.page_source

def getCityID(cityname, statename):
    global driver
    driver.find_element_by_class_name("_586i").send_keys(cityname+", "+statename)
    driver.find_element_by_class_name("_586i").send_keys(Keys.RETURN)
    url=driver.current_url
    ID=url[url.rfind("/")+1:len(url)]
    return ID


def parseUserInfo(username,if_relationship):
    userName = ""
    userEduWork = ""
    userHomeTown = ""
    userCurrentCity = ""
    userLiveEvents = []
    userGender = ""
    userStatus = ""
    userGroups = []
    userEmail=""
    userPhone=""
    userBD=""
    userBio=""
    userRelationship=""
    resultArr=[]

    global conn

    #work and education
    months=["january","february","march","april","may","june","july","august","september","october","november","december"]
    url = 'https://www.facebook.com/'+username+'/about?section=education'
    html = downloadPage(url)
    soup = BeautifulSoup(html)
    userName = soup.findAll("a",{"class":"_8_2"})[0].text
    work = soup.findAll("div",{"class" : "_2lzr _50f5 _50f7"})
    cnt=0
    for x in work:
        cnt+=1
        company = x.text
        t = x.next_sibling
        if t is None:
            writeToMysqlDB('Place',[company,0])
            if not conn.open:
                conn = mysqldb.connect('localhost',mysql_username,mysql_password,mysql_dbname);
            cursor=conn.cursor()
            cursor.execute("""SELECT LAST_INSERT_ID()""")
            userEduWork = cursor.fetchone()[0]
            continue
        text = t.text
        title=text
        temp=text
        place=""
        start_time=None
        end_time=None
        if "·" in text:
            list = text.split(" · ")
            title = list[0]
            temp=list[1]
            if len(list)==3:
                place=list[2]
        else:
            title=""
        start_time=""
        end_time=""
        if any(temp.lower().startswith(s) for s in months):
            temp2=temp.split(" to ")
            start_time=parser.parse(temp2[0])
            if temp2[1].lower()=="present":
                end_time=datetime.datetime.now()
            else:
                end_time=parser.parse(temp2[1])
        else:
            place = temp
        if not place=="":
            temp=place.split(", ")
            city=temp[0]
            state=""
            if len(temp)>1:
                state = temp[1] 
            ID = getCityID(city,state)
            writeToMysqlDB('City',[ID,city,state])
            writeToMysqlDB('Place',[company,ID])
        else:
            writeToMysqlDB('Place',[company,0])
        if not conn.open:
            conn = mysqldb.connect('localhost',mysql_username,mysql_password,mysql_dbname);
        cursor=conn.cursor()
        cursor.execute("""SELECT LAST_INSERT_ID()""")
        userEduWork = cursor.fetchone()[0]

    url = 'https://www.facebook.com/'+username+'/about?section=living'
    html = downloadPage(url)
    soup = BeautifulSoup(html)
    city = soup.findAll("span",{"class" : "_50f5 _50f7"})
    cnt=0
    for x in city:
        temp=x.text.split(", ")
        city=temp[0]
        state=""
        if len(temp)>1:
            state = temp[1]
        id=x.contents[0]['href'][x.contents[0]['href'].rfind("/")+1:len(x.contents[0]['href'])]
        print id
        writeToMysqlDB('City',[id,city,state])
        if cnt==0:
            userCurrentCity = id
        elif cnt==1:
            userHomeTown = id
        else:
            continue
        cnt+=1

    url = 'https://www.facebook.com/'+username+'/about?section=contact-info'
    html = downloadPage(url)
    soup = BeautifulSoup(html)
    contact = soup.findAll("ul",{"class":"uiList _509- _4ki _6-h _6-j _6-i"})
    for x in contact:
        text=x.contents[0].text
        if text.isdigit():
            userPhone = text
        else:
            userEmail = text

    birth = soup.findAll("li",{"class" : "_2pi4 _2ge8 _4vs2"})
    if len(birth)>1:
        userBD = birth[0].contents[0].findChildren("div",{"class" : "_4bl7 _pt5"})[0].text + birth[1].contents[0].findChildren("div",{"class" : "_4bl7 _pt5"})[0].text
    elif len(birth)==1:
        userBD = birth[0].contents[0].findChildren("div",{"class" : "_4bl7 _pt5"})[0].text

    gender = soup.findAll("li",{"class" : "_2pi4 _2ge8 _3ms8"})
    if len(gender)>0:
        userGender=gender[0].contents[0].findChildren("div",{"class" : "_4bl7 _pt5"})[0].text
    else:
        userGender="None"

    url = 'https://www.facebook.com/'+username+'/about?section=bio'
    html = downloadPage(url)
    soup = BeautifulSoup(html)
    bio = soup.findAll("li",{"class":"_2pi4 _2ge8 profileText"})
    if len(bio)>0:
        userBio=bio[0].contents[0].contents[0].text
    
    if if_relationship:
        url = 'https://www.facebook.com/'+username+'/about?section=relationship'
        html = downloadPage(url)
        soup = BeautifulSoup(html)
        relationship = soup.findAll("li",{"class":"_2pi4 _2ge8"})
        if len(relationship)>0:
            ch = relationship[0].contents[0].contents[0].contents[0].findChildren("div",{"class":"_42ef"})[0].contents[0]
            if len(ch.contents)==0:
                userRelationship=ch[0].text
            else:
                userRelationship='In relationship'
                z=ch.findChildren("div",{"class":"_2lzr _50f5 _50f7"})
                ch1=""
                if len(z)>0:
                    ch1=z[0].contents[0]['href']
                    if len(z[0].contents)>0:
                        username2=ch1[ch1.rfind("/")+1:len(ch1)]
                        userid1=convertUser2ID2(driver,username)
                        userid2=convertUser2ID2(driver,username2)
                        writeToMysqlDB('Relationships',[userid1,userid2,'couple'])  
                        list = parseUserInfo(username2,False)
                        writeToMysqlDB('Entities',['User'])
                        if not conn.open:
                                    conn = mysqldb.connect('localhost',mysql_username,mysql_password,mysql_dbname);
                        cursor=conn.cursor()
                        cursor.execute("""SELECT LAST_INSERT_ID()""")
                        entity_id = cursor.fetchone()[0]
                        writeToMysqlDB('User',[userid2,list[0],username2,list[1],list[2],list[3],list[4],list[5],list[6][0] if len(list[6])>0 else "",list[7],list[8],list[9],entity_id])
        relationship = soup.findAll("li",{"class":"_43c8 _2ge8"})
        for z in relationship:
            ch = z.contents[0].findChildren("div",{"class":"_4bl9"})[0].contents[0].findChildren("div",{"class":"_42ef"})[0].contents[0].findChildren("div",{"style":"height:36px"})[0].next_sibling
            if len(ch.findChildren("span")[0].findChildren("a"))>0:
                href=ch.findChildren("span")[0].contents[0]['href']
                username2=href[href.rfind("/")+1:len(href)]
                userid2=convertUser2ID2(driver,username2)
                rtype=ch.findChildren("div")[0].text
                writeToMysqlDB('Relationships',[uid,userid2,rtype])
                                  
            #ch2=ch.findChildren("div",{"class":"_173e _50f8 _50f3"})[0].text
            
    resultArr=[userName,userBD,userGender,userBio,userRelationship,userCurrentCity,userEduWork,userHomeTown,userEmail,userPhone]
    return resultArr

def parsePlacesLiked(html):
    soup = BeautifulSoup(html)      
    pageName = soup.findAll("div", {"class" : "_zs fwb"})
    tempList = []
    count=0
    r = re.compile('a href="(.*?)\?ref=')
    for x in pageName:
        m = r.search(str(x))
        if m:   
            #print x.text + " " + m.group(1) + "\n"     
            tempList.append([uid,x.text,m.group(1)])
        count+=1
    return tempList


def parsePagesLiked(html):
    soup = BeautifulSoup(html)  
    pageName = soup.findAll("div", {"class" : "_zs fwb"})
    tempList = []
    r = re.compile('a href="(.*?)\?ref=')
    for x in pageName:
        m = r.search(str(x))
        if m:
            pagearr=[]
            name=x.text
            type=""
            if len(x.next_sibling.findChildren())>0:
                type="Miscellenous"
            else:
                type=x.next_sibling.text
            atag=x.contents[0]
            url=atag['href']
            strs=url.split("/")
            id=strs[3]
            if strs[3]=="pages":
                id=strs[4]
            if not id.find("?")==-1:
                id=id[0:id.find("?")]
            pagearr.append(id)
            pagearr.append(type)
            pagearr.append(name)
            tempList.append(pagearr)
            #if(url.find(".com/pages/")==-1):
                #temp=url.substr(url.find(".com/"))
            #else:

            #print x.text + " " + m.group(1) + "\n"
            #tempList.append([uid,x.text,m.group(1)])
    return tempList

def getEntityIdOfUser(userid):
    if userid==None:
        return ""
    global conn
    if not conn.open:
        conn = mysqldb.connect('localhost',mysql_username,mysql_password,mysql_dbname);
    cursor=conn.cursor()
    result=cursor.execute("SELECT Entity_id from User WHERE ID="+userid)
    temp=cursor.fetchall()
    if len(temp)>0:
        entity_id=temp[0][0]
        print "entity id for user "+str(userid)+"is "+str(entity_id)
        return entity_id
    else:
        return ""       

def parsePhotosby(html):
    soup = BeautifulSoup(html)  
    photoPageLink = soup.findAll("a", {"class" : "_23q"})
    tempList = []
    for i in photoPageLink:
        html = str(i)
        soup1 = BeautifulSoup(html)
        pageName = soup1.findAll("img", {"class" : "img"})
        pageName1 = soup1.findAll("img", {"class" : "scaledImageFitWidth img"})
        pageName2 = soup1.findAll("img", {"class" : "_46-i img"})   
        for z in pageName2:
            #if z['src'].endswith('.jpg'):
                url1 = i['href']
                print url1
                r = re.compile('fbid=(.*?)&set=bc')
                m = r.search(url1)
                if m:
                    #filename = 'fbid_'+ m.group(1)+'.html'
                    #filename = filename.replace("?fref=photo","")
                    #if not os.path.lexists(filename):
                        #html1 = downloadPage(url1)
                    photoid=m.group(1)
                    html1 = downloadFile(url1)
                    print "[*] Caching Photo Page: "+m.group(1)

                    photoList=parsephoto(url1,username,m.group(1))
                    #   text_file = open(filename, "w")
                    #   text_file.write(normalize(html1))
                    #   text_file.close()
                    #else:
                    #html1 = open(filename, 'r').read()
                    soup2 = BeautifulSoup(html1)
                    username2 = soup2.find("div", {"class" : "fbPhotoContributorName"})
                    r = re.compile('href="(.*?)"')
                    m = r.search(str(username2))
                    print "1"
                    if m:   
                        username3 = m.group(1)
                        username3 = username3.replace("https://www.facebook.com/","")
                        username3 = username3.replace("?fref=photo","")
                        print "[*] Extracting Data from Photo Page: "+username3
                        tempList.append([str(uid),z['alt'],z['src'],i['href'],username3])
                        print username3
                        photoowner=convertUser2ID2(driver,username3)
                    writeToMysqlDB('Feed',[photoid,'Photo',"",photoList[3],photoList[1],photoowner,getEntityIdOfUser(photoowner),photoList[0]])
        for y in pageName1:
            #if y['src'].endswith('.jpg'):
                url1 = i['href']
                print url1
                r = re.compile('fbid=(.*?)&set=bc')
                m = r.search(url1)
                if m:
                    #filename = 'fbid_'+ m.group(1)+'.html'
                    #filename = filename.replace("?fref=photo","")
                    #if not os.path.lexists(filename):
                        #html1 = downloadPage(url1)
                    photoid=m.group(1)
                    html1 = downloadFile(url1)
                    print "[*] Caching Photo Page: "+m.group(1)

                    photoList=parsephoto(url1,username,m.group(1))
                    #   text_file = open(filename, "w")
                    #   text_file.write(normalize(html1))
                    #   text_file.close()
                    #else:
                    #   html1 = open(filename, 'r').read()
                    soup2 = BeautifulSoup(html1)
                    username2 = soup2.find("div", {"class" : "fbPhotoContributorName"})
                    r = re.compile('href="(.*?)"')
                    m = r.search(str(username2))
                    photoowner=""
                    print "2"
                    if m:   
                        username3 = m.group(1)
                        username3 = username3.replace("https://www.facebook.com/","")
                        username3 = username3.replace("?fref=photo","")
                        print "[*] Extracting Data from Photo Page: "+username3
                        print username3
                        photoowner=convertUser2ID2(driver,username3)
                        tempList.append([str(uid),y['alt'],y['src'],i['href'],username3])
                    writeToMysqlDB('Feed',[photoid,'Photo',"",photoList[3],photoList[1],photoowner,getEntityIdOfUser(photoowner),photoList[0]])
        for x in pageName:
            #if x['src'].endswith('.jpg'):
                url1 = i['href']
                print url1
                r = re.compile('fbid=(.*?)&set=bc')
                m = r.search(url1)
                if m:
                    #filename = 'fbid_'+ m.group(1)+'.html'
                    #filename = filename.replace("?fref=photo","")
                    #if not os.path.lexists(filename):
                        #html1 = downloadPage(url1)
                    photoid=m.group(1)
                    html1 = downloadFile(url1)
                    print "[*] Caching Photo Page: "+m.group(1)

                    photoList=parsephoto(url1,username,m.group(1))
                    #   text_file = open(filename, "w")
                    #   text_file.write(normalize(html1))
                    #   text_file.close()
                    #else:
                    #   html1 = open(filename, 'r').read()
                    soup2 = BeautifulSoup(html1)
                    username2 = soup2.find("div", {"class" : "fbPhotoContributorName"})
                    r = re.compile('href="(.*?)"')
                    m = r.search(str(username2))
                    photoowner=""
                    print "3"
                    if m:   
                        username3 = m.group(1)
                        username3 = username3.replace("https://www.facebook.com/","")
                        username3 = username3.replace("?fref=photo","")
                        print "[*] Extracting Data from Photo Page: "+username3
                        photoowner=convertUser2ID2(driver,username3)
                        tempList.append([str(uid),x['alt'],x['src'],i['href'],username3])
                    writeToMysqlDB('Feed',[photoid,'Photo',"",photoList[3],photoList[1],photoowner,getEntityIdOfUser(photoowner),photoList[0]])
    return tempList


def parsePhotosOf(html):
    soup = BeautifulSoup(html)  
    photoPageLink = soup.findAll("a", {"class" : "_23q"})
    tempList = []
    for i in photoPageLink:
        html = str(i)
        soup1 = BeautifulSoup(html)
        pageName = soup1.findAll("img", {"class" : "img"})
        pageName1 = soup1.findAll("img", {"class" : "scaledImageFitWidth img"})
        pageName2 = soup1.findAll("img", {"class" : "_46-i img"})   
        for z in pageName2:
            #if z['src'].endswith('.jpg'):
                url1 = i['href']
                #print url1
                r = re.compile('fbid=(.*?)&set=bc')
                m = r.search(url1)
                if m:
                    #filename = 'fbid_'+ m.group(1)+'.html'
                    #filename = filename.replace("?fref=photo","")
                    #if not os.path.lexists(filename):
                        #html1 = downloadPage(url1)
                    photoid=m.group(1)
                    html1 = downloadFile(url1)
                    #print "[*] Caching Photo Page: "+m.group(1)
                    photoList=parsephoto(url1,username,m.group(1))
                    #   text_file = open(filename, "w")
                    #   text_file.write(normalize(html1))
                    #   text_file.close()
                    #else:
                    #   html1 = open(filename, 'r').read()
                    soup2 = BeautifulSoup(html1)
                    username2 = soup2.find("div", {"class" : "fbPhotoContributorName"})
                    #r = re.compile('a href=[\'"]?([^\'">]+)')
                    r = re.compile('href="(.*?)"')
                    m = r.search(str(username2))
                    photoowner=""
                    print m.group(1)
                    if m:   
                        username3 = m.group(1)
                        username3 = username3.replace("https://www.facebook.com/","")
                        username3 = username3.replace("?fref=photo","")
                        print "[*] Extracting Data from Photo Page: "+username3
                        photoowner=convertUser2ID2(driver,username3)
                        tempList.append([str(uid),z['alt'],z['src'],i['href'],username3])
                    writeToMysqlDB('Feed',[photoid,'Photo',"",photoList[3],photoList[1],photoowner,getEntityIdOfUser(photoowner),photoList[0]])
                    writeToMysqlDB('Feeds_tags',[photoid,uid])
        for y in pageName1:
            #if y['src'].endswith('.jpg'):
                url1 = i['href']
                #print url1
                r = re.compile('fbid=(.*?)&set=bc')
                m = r.search(url1)
                if m:
                    #filename = 'fbid_'+ m.group(1)+'.html'
                    #filename = filename.replace("?fref=photo","")
                    #if not os.path.lexists(filename):
                        #html1 = downloadPage(url1)
                    photoid=m.group(1)
                    html1 = downloadFile(url1)
                    print "[*] Caching Photo Page: "+m.group(1)

                    photoList=parsephoto(url1,username,m.group(1))
                    #   text_file = open(filename, "w")
                    #   text_file.write(normalize(html1))
                    #   text_file.close()
                    #else:
                    #   html1 = open(filename, 'r').read()
                    soup2 = BeautifulSoup(html1)
                    username2 = soup2.find("div", {"class" : "fbPhotoContributorName"})
                    r = re.compile('href="(.*?)"')
                    #r = re.compile('a href=[\'"]?([^\'">]+)')
                    m = r.search(str(username2))
                    photoowner=""
                    print "2"
                    if m:   
                        username3 = m.group(1)
                        username3 = username3.replace("https://www.facebook.com/","")
                        username3 = username3.replace("?fref=photo","")
                        print "[*] Extracting Data from Photo Page: "+username3
                        photoowner=convertUser2ID2(driver,username3)
                        tempList.append([str(uid),y['alt'],y['src'],i['href'],username3])
                    writeToMysqlDB('Feed',[photoid,'Photo',"",photoList[3],photoList[1],photoowner,getEntityIdOfUser(photoowner),photoList[0]])
                    writeToMysqlDB('Feeds_tags',[photoid,uid])
        for x in pageName:
            #if x['src'].endswith('.jpg'):
                url1 = i['href']
                #print url1
                r = re.compile('fbid=(.*?)&set=bc')
                m = r.search(url1)
                if m:
                    #filename = 'fbid_'+ m.group(1)+'.html'
                    #filename = filename.replace("?fref=photo","")
                    #if not os.path.lexists(filename):
                        #html1 = downloadPage(url1)
                    photoid=m.group(1)
                    html1 = downloadFile(url1)
                    print "[*] Caching Photo Page: "+m.group(1)

                    photoList=parsephoto(url1,username,m.group(1))
                    #   text_file = open(filename, "w")
                    #   text_file.write(normalize(html1))
                    #   text_file.close()
                    #else:
                    #   html1 = open(filename, 'r').read()
                    soup2 = BeautifulSoup(html1)
                    username2 = soup2.find("div", {"class" : "fbPhotoContributorName"})
                    r = re.compile('href="(.*?)"')
                    #r = re.compile('a href=[\'"]?([^\'">]+)')
                    m = r.search(str(username2))
                    photoo=""
                    print "3"
                    if m:   
                        username3 = m.group(0)
                        print username3
                        username3 = username3.replace("https://www.facebook.com/","")
                        username3 = username3.replace("?fref=photo","")
                        print "[*] Extracting Data from Photo Page: "+username3
                        photoowner=convertUser2ID2(driver,username3)
                        tempList.append([str(uid),x['alt'],x['src'],i['href'],username3])
                    writeToMysqlDB('Feed',[photoid,'Photo',"",photoList[3],photoList[1],photoowner,getEntityIdOfUser(photoowner),photoList[0]])
                    writeToMysqlDB('Feeds_tags',[photoid,uid])
    return tempList


def parsePhotosLiked(html):
    soup = BeautifulSoup(html)  
    photoPageLink = soup.findAll("a", {"class" : "_23q"})
    tempList = []

    for i in photoPageLink:
        html = str(i)
        soup1 = BeautifulSoup(html)
        pageName = soup1.findAll("img", {"class" : "img"})
        pageName1 = soup1.findAll("img", {"class" : "scaledImageFitWidth img"})
        pageName2 = soup1.findAll("img", {"class" : "_46-i img"})   
        for z in pageName2:
            # if z['src'].endswith('.jpg'):
                url1 = i['href']
                r = re.compile('fbid=(.*?)&set=bc')
                m = r.search(url1)
                if m:
                    #filename = 'fbid_'+ m.group(1)+'.html'
                    #filename = filename.replace("?fref=photo","")
                    #if not os.path.lexists(filename):
                    #html1 = downloadPage(url1)
                    photoid=m.group(1)
                    html1 = downloadFile(url1)
                    print "[*] Caching Photo Page: "+m.group(1)

                    photoList=parsephoto(url1,username,m.group(1))
                    #   text_file = open(filename, "w")
                    #   text_file.write(normalize(html1))
                    #   text_file.close()
                    #else:
                    #   html1 = open(filename, 'r').read()
                    soup2 = BeautifulSoup(html1)
                    username2 = soup2.find("div", {"class" : "fbPhotoContributorName"})
                    r = re.compile('href="(.*?)"')
                    m = r.search(str(username2))
                    photoowner=""
                    if m:   
                        
                        username3 = m.group(1)
                        print username3
                        username3 = username3.replace("https://www.facebook.com/","/",2)
                        username3 = username3.replace("?fref=photo","")
                        if username3.count('/')==2:
                            username3 = username3.split('/')[2]

                        print "[*] Extracting Data from Photo Page: "+username3
                        photoowner=convertUser2ID2(driver,username3)
                        #tmpStr = []
                        tempList.append([str(uid),z['alt'],z['src'],i['href'],username3])
                        #write2Database('photosLiked',tmpStr)
                    writeToMysqlDB('Feed',[photoid,'Photo',"",photoList[3],photoList[1],photoowner,getEntityIdOfUser(photoowner),photoList[0]])
                    writeToMysqlDB('Photos_likes',[photoid,uid])

        for y in pageName1:
            #if y['src'].endswith('.jpg'):
                url1 = i['href']
                r = re.compile('fbid=(.*?)&set=bc')
                m = r.search(url1)
                if m:
                    #filename = 'fbid_'+ m.group(1)+'.html'
                    #filename = filename.replace("?fref=photo","")
                    #if not os.path.lexists(filename):
                        #html1 = downloadPage(url1)
                    photoid=m.group(1)
                    html1 = downloadFile(url1)
                    print "[*] Caching Photo Page: "+m.group(1)

                    photoList=parsephoto(url1,username,m.group(1))
                    #   text_file = open(filename, "w")
                    #   text_file.write(normalize(html1))
                    #   text_file.close()
                    #else:
                    #   html1 = open(filename, 'r').read()
                    soup2 = BeautifulSoup(html1)
                    username2 = soup2.find("div", {"class" : "fbPhotoContributorName"})
                    r = re.compile('href="(.*?)"')
                    m = r.search(str(username2))
                    photoowner=""
                    print username2
                    if m:   
                        username3 = m.group(1)
                        username3 = username3.replace("https://www.facebook.com/","/")
                        username3 = username3.replace("?fref=photo","")
                        #if username3.count('/')==2:
                        username3 = username3.split('/')[2]

                        print "[*] Extracting Data from Photo Page: "+username3
                        photoowner=convertUser2ID2(driver,username3)
                        #tmpStr = []
                        tempList.append([str(uid),y['alt'],y['src'],i['href'],username3])
                        #write2Database('photosLiked',tmpStr)
                    writeToMysqlDB('Feed',[photoid,'Photo',"",photoList[3],photoList[1],photoowner,getEntityIdOfUser(photoowner),photoList[0]])
                    writeToMysqlDB('Photos_likes',[photoid,uid])

        for x in pageName:
            #if x['src'].endswith('.jpg'):
                url1 = i['href']
                r = re.compile('fbid=(.*?)&set=bc')
                m = r.search(url1)
                if m:
                    #filename = 'fbid_'+ m.group(1)+'.html'
                    #filename = filename.replace("?fref=photo","")
                    #if not os.path.lexists(filename):
                        #html1 = downloadPage(url1)
                    photoid=m.group(1)
                    html1 = downloadFile(url1)
                    print "[*] Caching Photo Page: "+m.group(1)

                    photoList=parsephoto(url1,username,m.group(1))
                    #   text_file = open(filename, "w")
                    #   text_file.write(normalize(html1))
                    #   text_file.close()
                    #else:
                    #   html1 = open(filename, 'r').read()
                    soup2 = BeautifulSoup(html1)
                    username2 = soup2.find("div", {"class" : "fbPhotoContributorName"})
                    r = re.compile('href="(.*?)"')
                    m = r.search(str(username2))
                    photoowner=""
                    if m:   
                        username3 = m.group(1)
                        username3 = username3.replace("https://www.facebook.com/","/")
                        username3 = username3.replace("?fref=photo","")
                        if username3.count('/')==2:
                            username3 = username3.split('/')[2]

                        print "[*] Extracting Data from Photo Page: "+username3
                        photoowner=convertUser2ID2(driver,username3)
                        #tmpStr = []
                        tempList.append([str(uid),x['alt'],x['src'],i['href'],username3])
                        #write2Database('photosLiked',tmpStr)
                    writeToMysqlDB('Feed',[photoid,'Photo',"",photoList[3],photoList[1],photoowner,getEntityIdOfUser(photoowner),photoList[0]])
                    writeToMysqlDB('Photos_likes',[photoid,uid])

    return tempList

def downloadPage(url):
    driver.get(url) 
    html = driver.page_source
    return html

def parsephoto(url,user,photoid):
    tempList=[]
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html)

    location_a=""
    location=""
    cityid=""
    temp=soup.findAll("span",{"class":"fbPhotoTagListTag withTagItem tagItem"})
    if not len(temp)==0:
        location_a=temp[0].findChildren("a")[0]
        location=location_a.text
        cityid=location_a['href'][location_a['href'].rfind("/"):len(location_a['href'])]

    timestamp=parser.parse(soup.findAll("span",{"id":"fbPhotoPageTimestamp"})[0].contents[0].text)

    caption=soup.findAll("span",{"class":"fbPhotosPhotoCaption"})[0].text

    photoPageLink = soup.findAll("li", {"class" : "UFIRow"})
    actors=[]
    comments=[]
    timestamps=[]
    for i in photoPageLink:
        html = str(i)
        soup2 = BeautifulSoup(html)
        pageName2 = soup2.findAll("a", {"class" : "UFICommentActorName"})
        for z in pageName2:
            actor = z['href']
            actor = actor.replace("https://www.facebook.com/","")
            actor = actor.replace("?fref=ufi","")
            actors.append(convertUser2ID2(driver,actor))
        soup1 = BeautifulSoup(html)
        pageName = soup1.findAll("span", {"class" : "UFICommentBody"})
        for y in pageName:
            comments.append(y.text)
        timestamps_temp = soup.findAll("abbr",{"class":"livetimestamp"})        
        for w in timestamps_temp:
            timestamps.append(parser.parse(w['title']))
    tempList=[cityid,timestamp,photoid,caption,actors,comments,timestamps]
    return tempList

def parseEvent(url):
    url = "https://www.facebook.com"+url
    url = url.replace("/?ref=br_rs","")
    print "parsing event:"+url
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html)
    photoPageLink = soup.findAll("a", {"id" : "js_"})
    for i in photoPageLink:
        actor = i['href']
        print "Owner(s) of group is: "+actor
##write this fucker later


def parseEventsJoined(html,username):
    soup = BeautifulSoup(html)
    photoPageLink = soup.findAll("a", {"class" : "_7kf _8o _8s lfloat _ohe"})
    tempList = []
    for i in photoPageLink:
        url = i['href']
        parseEvent(url)
    return tempList

def parsePhotosCommented(html,username):
    soup = BeautifulSoup(html)  
    photoPageLink = soup.findAll("a", {"class" : "_23q"})
    tempList = []

    for i in photoPageLink:
        html = str(i)
        soup1 = BeautifulSoup(html)
        pageName = soup1.findAll("img", {"class" : "img"})
        pageName1 = soup1.findAll("img", {"class" : "scaledImageFitWidth img"})
        pageName2 = soup1.findAll("img", {"class" : "_46-i img"})
        for z in pageName2:
            #if z['src'].endswith('.jpg'):
                url1 = i['href']
                r = re.compile('fbid=(.*?)&set=bc')
                m = r.search(url1)
                if m:
                    #filename = 'fbid_'+ m.group(1)+'.html'
                    #if not os.path.lexists(filename):
                    photoid=m.group(1)
                    html1 = downloadFile(url1)
                        #html1 = downloadPage(url1)
                    print "[*] Caching Photo Page: "+m.group(1)
                    purl = "https://www.facebook.com/photo.php?fbid="+m.group(1)
                    photoList=parsephoto(purl,username,m.group(1))

                    #   text_file = open(filename, "w")
                    #   text_file.write(normalize(html1))
                    #   text_file.close()
                    #else:
                    #   html1 = open(filename, 'r').read()
                    soup2 = BeautifulSoup(html1)
                    username2 = soup2.find("div", {"class" : "fbPhotoContributorName"})
                    r = re.compile('href="(.*?)"')
                    m = r.search(str(username2))
                    photoowner=""
                    if m:   
                        username3 = m.group(1)
                        username3 = username3.replace("https://www.facebook.com/","")
                        username3 = username3.replace("?fref=photo","")
                        if username3.count('?')==2:
                            username3 = username3.split('?')[0]

                        print "Commented on photo of  "+username3
                        photoowner=convertUser2ID2(driver,username3)
                        tempList.append([str(uid),z['alt'],z['src'],i['href'],username3])
                    writeToMysqlDB('Feed',[photoid,'Photo',"",photoList[3],photoList[1],photoowner,getEntityIdOfUser(photoowner),photoList[0]])
                    cnt=0
                    for x in photoList[4]:
                        actor=x
                        comment=photoList[5][cnt]
                        timestamp=photoList[6][cnt]
                        print actor
                        print uid
                        if actor==uid:
                            writeToMysqlDB('Comments',[comment,timestamp,actor,photoid])


        for y in pageName1:
            #if y['src'].endswith('.jpg'):
                url1 = i['href']
                r = re.compile('fbid=(.*?)&set=bc')
                m = r.search(url1)
                if m:
                    #filename = 'fbid_'+ m.group(1)+'.html'
                    #if not os.path.lexists(filename):
                    photoid=m.group(1)
                    html1 = downloadFile(url1)
                    purl = "https://www.facebook.com/photo.php?fbid="+m.group(1)
                    photoList=parsephoto(purl,username,m.group(1))
                    print "[*] Caching Photo Page: "+m.group(1)
                    #   text_file = open(filename, "w")
                    #   text_file.write(normalize(html1))
                    #   text_file.close()
                    #else:
                    #   html1 = open(filename, 'r').read()
                    soup2 = BeautifulSoup(html1)
                    username2 = soup2.find("div", {"class" : "fbPhotoContributorName"})
                    r = re.compile('href="(.*?)"')
                    m = r.search(str(username2))
                    photoowner=""
                    if m:   
                        username3 = m.group(1)
                        username3 = username3.replace("https://www.facebook.com/","")
                        username3 = username3.replace("?fref=photo","")
                        if username3.count('/')==2:
                            username3 = username3.split('/')[2]

                        print "Commented on photo of "+username3
                        photoowner=convertUser2ID2(driver,username3)
                        tempList.append([str(uid),y['alt'],y['src'],i['href'],username3])
                    writeToMysqlDB('Feed',[photoid,'Photo',"",photoList[3],photoList[1],photoowner,getEntityIdOfUser(photoowner),photoList[0]])
                    cnt=0
                    for x in photoList[4]:
                        actor=x
                        comment=photoList[5][cnt]
                        timestamp=photoList[6][cnt]
                        print actor
                        print uid
                        if actor==uid:
                            writeToMysqlDB('Comments',[comment,timestamp,actor,photoid])
        for x in pageName:
            #if x['src'].endswith('.jpg'):
                url1 = i['href']
                r = re.compile('fbid=(.*?)&set=bc')
                m = r.search(url1)
                if m:
                    #filename = 'fbid_'+ m.group(1)+'.html'
                    #if not os.path.lexists(filename):
                    photoid=m.group(1)
                    html1 = downloadFile(url1)
                        #html1 = downloadPage(url1)
                    purl = "https://www.facebook.com/photo.php?fbid="+m.group(1)
                    print "[*] Caching Photo Page: "+m.group(1)
                    photoList=parsephoto(purl,username,m.group(1))
                    #   text_file = open(filename, "w")
                    #   text_file.write(normalize(html1))
                    #   text_file.close()
                    #else:
                    #   html1 = open(filename, 'r').read()
                    soup2 = BeautifulSoup(html1)
                    username2 = soup2.find("div", {"class" : "fbPhotoContributorName"})
                    r = re.compile('href="(.*?)"')
                    m = r.search(str(username2))
                    photoowner=""
                    if m:   
                        username3 = m.group(1)
                        username3 = username3.replace("https://www.facebook.com/","")
                        username3 = username3.replace("?fref=photo","")
                        if username3.count('/')==2:
                            username3 = username3.split('/')[2]
                        print "Commented on photo of "+username3
                        photoowner=convertUser2ID2(driver,username3)
                        tempList.append([str(uid),x['alt'],x['src'],i['href'],username3])
                    writeToMysqlDB('Feed',[photoid,'Photo',"",photoList[3],photoList[1],photoowner,getEntityIdOfUser(photoowner),photoList[0]])
                    cnt=0
                    for x in photoList[4]:
                        actor=x
                        comment=photoList[5][cnt]
                        timestamp=photoList[6][cnt]
                        print actor
                        print uid
                        if actor==uid:
                            writeToMysqlDB('Comments',[comment,timestamp,actor,photoid])

    return tempList

def parseVideosBy(html):
    soup = BeautifulSoup(html)  
    appsData = soup.findAll("div", {"class" : "_42bw"})
    tempList = []
    for x in appsData:
        r = re.compile('href="(.*?)"')
        m = r.search(str(x))
        if m:
            filename = str(m.group(1)).replace("https://www.facebook.com/video.php?v=","v_")
            filename = filename+".html"
            url = str(m.group(1))
            vid=""
            if not url.find("&")==-1:
                vid=url[37:url.find("&")]
            else:
                vid=url[37:]
            print vid
            #if not os.path.lexists(filename):
            #html1 = downloadFile(url)
            driver.get(url)
            html1 = driver.page_source
                #text_file = open(filename, "w")
                #text_file.write(normalize(html1))
                #text_file.close()
            #else:
                #html1 = open(filename, 'r').read()
            soup1 = BeautifulSoup(html1)    
            caption = soup1.findAll("div",{"class" : "text_exposed_root"})
            if len(caption)==0:
                caption=soup1.findAll("span",{"class":"hasCaption"})
                if len(caption)==0:
                    caption=""
                else:
                    caption=caption[0].text
            else:
                caption=caption[0].text

            # TODO- parse 'title' for timestamp
            timestamp = soup1.findAll("span",{"id":"fbPhotoPageTimestamp"})[0].contents[0].contents[0].text
            titleData = soup1.find("h2", {"class" : "uiHeaderTitle"})
            tempList.append([uid,vid,(titleData.text).strip(),url,caption,parser.parse(timestamp)])
            comments=soup1.findAll("span",{"class":"UFICommentBody"})
            commenters=soup1.findAll("a",{"class":"UFICommentActorName"})
            timestamps=soup1.findAll("div",{"class":"fsm fwn fcg UFICommentActions"})
            cnt=0
            for c in comments:
                comment=c.contents[0].text
                lindex=len(commenters[cnt]['href'])
                if not commenters[cnt]['href'].rfind("?")==-1:
                    lindex = commenters[cnt]['href'].rfind("?") 
                commenter=commenters[cnt]['href'][commenters[cnt]['href'].rfind("/"):lindex]
                timestamp=parser.parse(timestamps[cnt].text)
                print timestamps[cnt]
                print timestamp
                uid2 = convertUser2ID2(driver,commenter)
                writeToMysqlDB('Comments',[comment,timestamp,uid2,vid])
    return tempList
    
def parseAppsUsed(html): 
    soup = BeautifulSoup(html)  
    appsData = soup.findAll("div", {"class" : "_zs fwb"})
    tempList = []
    for x in appsData:
        children = x.findChildren('a')
        a = contents[0]
        arr = []
        temp = json.loads(a['data-gt'])
        arr.append(temp['appid'])
        arr.append(a['data-appname'])
        tempList.append(arr)
    return tempList

def sidechannelFriends(uid):
    userList = []
    c = conn.cursor()
    c.execute('select distinct username from photosLiked where sourceUID=?',(uid,))
    dataList1 = []
    dataList1 = c.fetchall()
    if len(dataList1)>0:
        for i in dataList1:
            if 'pages' not in str(normalize(i[0])):
                userList.append([uid,'',str(normalize(i[0])),'',''])
    c.execute('select distinct username from photosCommented where sourceUID=?',(uid,))
    dataList1 = []
    dataList1 = c.fetchall()
    if len(dataList1)>0:    
        for i in dataList1:
            if 'pages' not in str(normalize(i[0])):
                userList.append([uid,'',str(normalize(i[0])),'',''])
    c.execute('select distinct username from photosOf where sourceUID=?',(uid,))
    dataList1 = []
    dataList1 = c.fetchall()
    if len(dataList1)>0:    
        for i in dataList1:
            if 'pages' not in str(normalize(i[0])):
                userList.append([uid,'',str(normalize(i[0])),'',''])
    return userList

def gettFriends(uid):
    userList = []
    c = conn.cursor()
    c.execute('select username from friends where sourceUID=?',(uid,))
    dataList1 = []
    dataList1 = c.fetchall()
    if len(dataList1)>0:
        for i in dataList1:
            userList.append([uid,'',str(normalize(i)),'',''])
    return userList
    
def parseFriends(html):
    mthList = ['january','february','march','april','may','june','july','august','september','october','november','december']
    if len(html)>0:
        soup = BeautifulSoup(html)  

        friendBlockData = soup.findAll("div",{"class" : "_1zf"})
        friendNameData = soup.findAll("div", {"class" : "_zs fwb"})
        knownSinceData = soup.findAll("div", {"class" : "_52eh"})
    
        friendList=[]
        for i in friendBlockData:
            soup1 = BeautifulSoup(str(i))
            friendNameData = soup1.find("div",{"class" : "_zs fwb"})
            lastKnownData = soup1.find("div",{"class" : "_52eh"})
            r = re.compile('a href=(.*?)\?ref')
            m = r.search(str(friendNameData))
            #print friendNameData
            #print lastKnownData
            #print m
            if m:
                try:    
                    friendName = friendNameData.text
                    #print friendName
                    friendName = friendName.replace('"https://www.facebook.com/','')
                    value = (lastKnownData.text).split("since")[1].strip()
                    #print value
                    #Current year - No year listed in page
                    if not re.search('\d+', value):                 
                        value = value+" "+str((datetime.datetime.now()).year)
                        month = ((re.sub(" \d+", " ", value)).lower()).strip()
                        monthDigit = 0
                        count=0
                        for s in mthList:
                            if s==month:
                                monthDigit=count+1
                            count+=1    
                        year = re.findall("(\d+)",value)[0]
                        print year
                        fbID = m.group(1).replace('"https://www.facebook.com/','')
                        print fbID
                        friendList.append([str(uid),friendName,fbID,int(monthDigit),int(year)])
                    else:
                        #Not current year
                        month,year = value.split(" ")
                        month = month.lower()
                        monthDigit = 0
                        count=0
                        for s in mthList:
                            if s==month:
                                monthDigit=count+1
                            count+=1
                        fbID = m.group(1).replace('"https://www.facebook.com/','')
                        print fbID
                        print year
                        print monthDigit
                        friendList.append([str(uid),friendName,fbID,int(monthDigit),int(year)])
    
                        
                except IndexError:
                    continue
                except AttributeError:
                    continue
        i=0
        data = sorted(friendList, key=operator.itemgetter(4,3))
        #print "Friends List"
        #for x in data:
        #   print x
        #   #print x[2]+'\t'+x[1]
        return data

def analyzeFriends(userid):
    c = conn.cursor()
    c.execute('select * from friends where sourceUID=?',(userid,))
    dataList = c.fetchall()
    photosliked = []
    photoscommented = []
    userID = []
    for i in dataList:
        #print i[1]+'\t'+i[2]
        #c.execute('select username from photosLiked')
        c.execute('select * from photosLiked where sourceUID=? and username=?',(userid,i[2],))
        dataList1 = []
        dataList1 = c.fetchall()
        if len(dataList1)>0:
            str1 = ([dataList1[0][4].encode('utf8'),str(len(dataList1))])
            photosliked.append(str1)
        
        c.execute('select * from photosCommented where sourceUID=? and username=?',(userid,i[2],))
        dataList1 = []
        dataList1 = c.fetchall()
        if len(dataList1)>0:
            str1 = ([dataList1[0][4].encode('utf8'),str(len(dataList1))])
            photoscommented.append(str1)
    print "[*] Videos Posted By "+str(username)
    filename = username+'_videosBy.htm'
    if not os.path.lexists(filename):
        html = downloadVideosBy(driver,uid)
        text_file = open(filename, "w")
        text_file.write(html.encode('utf8'))
        text_file.close()
    else:
        html = open(filename, 'r').read()
    dataList = parseVideosBy(html)
    count=1
    for i in dataList:
        print str(count)+') '+i[1]+'\t'+i[2]
        count+=1
    print "\n"

    print "[*] Pages Liked By "+str(uid)
    filename = username+'_pages.htm'
    if not os.path.lexists(filename):
        html = downloadPagesLiked(driver,uid)
        text_file = open(filename, "w")
        text_file.write(html.encode('utf8'))
        text_file.close()
    else:
        html = open(filename, 'r').read()
    dataList = parsePagesLiked(html)
    for i in dataList:
        print "[*] "+normalize(i[1])
        #print "[*] "+normalize(i[2])+"\t"+normalize(i[1])+"\t"+normalize(i[3])
        #print normalize(i[1])+"\t"+normalize(i[2])+"\t"+normalize(i[3])
    print "\n"
    
def mainProcess(username):    
    global conn
    username = username.strip()
    print "[*] Username:\t"+str(username)
    global uid
    
    loginFacebook(driver)
    uid = convertUser2ID2(driver,username)
    if not uid:
        print "[!] Problem converting username to uid"
        sys.exit()
    else:
        print "[*] Uid:\t"+str(uid)
    list = parseUserInfo(username,True)
    writeToMysqlDB('Entities',['User'])
    cursor=conn.cursor()
    cursor.execute("""SELECT LAST_INSERT_ID()""")
    entity_id = cursor.fetchone()[0]
    writeToMysqlDB('User',[uid,list[0],username,list[1],list[2],list[3],list[4],list[5],list[6],list[7],list[8],list[9],entity_id])
#    filename = username+'_apps.htm'
#    if not os.path.lexists(filename):
#        print "[*] Caching Facebook Apps Used By: "+username
#        html = downloadAppsUsed(driver,uid)
#        text_file = open(filename, "w")
#        text_file.write(html.encode('utf8'))
#        text_file.close()
#    else:
#        html = open(filename, 'r').read()
#    data1 = parseAppsUsed(html)
#    result = ""
#    for x in data1:
#        print x
#        writeToMysqlDB('Apps',x)
#       x = x.lower()
#       if "blackberry" in x:
#           result += "[*] User is using a Blackberry device\n"
#       if "android" in x:
#           result += "[*] User is using an Android device\n"
#       if "ios" in x or "ipad" in x or "iphone" in x:
#           result += "[*] User is using an iOS Apple device\n"
#       if "samsung" in x:
#           result += "[*] User is using a Samsung Android device\n"
#    print result
#
#    #Caching Pages Liked - Start
#    filename = username+'_pages.htm'
#    #if not os.path.lexists(filename):
#    print "[*] Caching Pages Liked By: "+username
#    html = downloadPagesLiked(driver,uid)
#    #   text_file = open(filename, "w")
#    #   text_file.write(html.encode('utf8'))
#    #   text_file.close()
#    #else:
#    dataList = parsePagesLiked(html) 
#    for x in dataList:
#        t=(str(x[0]),)
#        print x[0]
#        conn = mysqldb.connect('localhost',mysql_username,mysql_password,mysql_dbname);
#        cursor=conn.cursor()
#        result=cursor.execute("""SELECT count(*) FROM Pages WHERE ID=%s""",t)
#        cnt=cursor.fetchall()[0][0]
#        cursor.close()
#        print cnt
#        if cnt==0:
#            writeToMysqlDB('Entities',["Page"])
#            cursor=conn.cursor()
#            cursor.execute("""SELECT LAST_INSERT_ID()""")
#            entity_id=cursor.fetchone()[0]
#            cursor.close()
#            writeToMysqlDB('Pages',[str(x[0]),str(x[1]),str(x[2]),0,entity_id])
#            writeToMysqlDB('Page_likes',[str(x[0]),str(uid)])
#            conn.commit()
        #if len(dataList)>0:
           # write2Database('pagesLiked',dataList)
    #Caching Pages Liked - End

    # html = downloadVideosBy(driver,uid)
    # dataList = parseVideosBy(html)
    # for x in dataList:
    #     writeToMysqlDB('Feed',[x[1],"Video",x[2],x[4],x[5],str(uid),entity_id])


    # html = downloadPhotosOf(driver,uid)
    # dataList = parsePhotosOf(html)
#   #write2Database('photosOf',dataList)
#        
#        filename = username+'_photosBy.htm'
#        #if not os.path.lexists(filename):
#        print "[*] Caching Photos By: "+username
#    html = downloadPhotosBy(driver,uid)
#        #      text_file = open(filename, "w")
#        #      text_file.write(html.encode('utf8'))
#        #      text_file.close()
#        #else:
#        text_file = open(filename, 'w')
#   dataList = parsePhotosby(html)
#   #text_file.write(dataList)
#   for item in dataList:
#       print>>text_file,item
#   text_file.close()
#        #write2Database('photosBy',dataList)        
#
#   #Disable
#       filename = username+'_photosLiked.htm'
#       print filename
#        #if not os.path.lexists(filename):
#        print "[*] Caching Photos Liked By: "+username
#    html = downloadPhotosLiked(driver,uid)
#        text_file = open(filename, "w")
#        #      text_file.write(html.encode('utf8'))
#        #      text_file.close()
#        #else:
#        #      html = open(filename, 'r').read()
#    dataList = parsePhotosLiked(html)
#        print "[*] Writing "+str(len(dataList))+" records to table: photosLiked"
#   for item in dataList:
#       print>>text_file,item
#   text_file.close()
#        #write2Database('photosLiked',dataList)
#
#        filename = username+'_photoscommented.htm'
#       print filename
#        #if not os.path.lexists(filename):
#        print "[*] Caching Commented On By: "+username
#    html = downloadPhotosCommented(driver,uid)
#        text_file = open(filename,"w")
#        text_file.write(html.encode('utf8'))
#        text_file.close()
#        #else:
#        #      html = open(filename, 'r').read()
#    dataList = parsePhotosCommented(html,username)
#        #text_file.write(dataList)
#   for item in dataList:
#       print(item)
#   text_file.close()
#
#   #write2Database('photosCommented',dataList)
#
#   filename = username+'_eventsjoined.htm'
#       print filename
#        #if not os.path.lexists(filename):
#        print "[*] Events joined by: "+username
#        html = downloadEventsJoined(driver,uid)
#        text_file = open(filename,"w")
#        text_file.write(html.encode('utf8'))
#        text_file.close()
#        #else:
#        #      html = open(filename, 'r').read()
#        dataList = parseEventsJoined(html,username)
#        #text_file.write(dataList)
#   for item in dataList:
#       print(item)
#   text_file.close()
#
#        filename = username+'_friends.htm'
#        print filename
#        #if not os.path.lexists(filename):
#        print "[*] Caching Friends Page of: "+username
#        html = downloadFriends(driver,uid)
#        text_file = open(filename, "w")
#               #text_file.write(html.encode('utf8'))
#               #text_file.close()
#           #   else:
#        #      html = open(filename, 'r').read()
#        if len(html.strip())>1:
#               dataList = parseFriends(html)
#               #print "[*] Writing Friends List to Database: "+username
#               #write2Database('friends',dataList)
#   #else:
#               #print "[*] Extracting Friends from Likes/Comments: "+username
#               #write2Database('friends',sidechannelFriends(uid))'''
#               
#        '''c = conn.cursor()
#        c.execute('select * from friends where sourceUID=?',(uid,))
#        dataList = c.fetchall()
#        photosliked = []
#        photoscommented = []
#        userID = []
#        for i in dataList:
#            #print i[1]+'\t'+i[2]
#            #c.execute('select username from photosLiked')
#            c.execute('select * from photosLiked where sourceUID=? and username=?',(uid,i[2],))
#            dataList1 = []
#            dataList1 = c.fetchall()
#            if len(dataList1)>0:
#                str1 = ([dataList1[0][4].encode('utf8'),str(len(dataList1))])
#                photosliked.append(str1)
#        
#            c.execute('select * from photosCommented where sourceUID=? and username=?',(uid,i[2],))
#            dataList1 = []
#            dataList1 = c.fetchall()
#            if len(dataList1)>0:
#                str1 = ([dataList1[0][4].encode('utf8'),str(len(dataList1))])
#                photoscommented.append(str1)'''
#   
#               
#        #analyzeFriends(str(uid))
#        filename = username+'.htm'
#        #if not os.path.lexists(filename):
#        print "[*] Caching Timeline Page of: "+username
    html = downloadTimeline(username)
#        text_file = open(filename, "w")
#        text_file.write(html.encode('utf8'))
#        text_file.close()
#        #else:
#        #  html = open(filename, 'r').read()
    dataList = parseTimeline(html,username)
#
#   print "\n"
#   print "[*] Downloading User Information"
#
#   tmpInfoStr = []
#   '''userID =  getFriends(uid)
#   for x in userID:
#       i = str(normalize(x[2]))
#       i = i.replace("(u'","").replace("',","").replace(')','')
#       i = i.replace('"https://www.facebook.com/','')
#       print "[*] Looking up information on "+i
#       filename = i.encode('utf8')+'.html'
#       if "/" not in filename:
#           if not os.path.lexists(filename):
#               print 'Writing to '+filename
#               url = 'https://www.facebook.com/'+i.encode('utf8')+'/info'
#               html = downloadFile(url)    
#               #html = downloadUserInfo(driver,i.encode('utf8'))
#               if len(html)>0:
#                   text_file = open(filename, "w")
#                   text_file.write(normalize(html))
#                   #text_file.write(html.encode('utf8'))
#                   text_file.close()
#           else:
#               print 'Skipping: '+filename
#           print "[*] Parsing User Information: "+i
#           html = open(filename, 'r').read()
#           userInfoList = parseUserInfo(html)[0]
#           tmpStr = []
#           tmpStr.append([uid,str(normalize(i)),str(normalize(userInfoList[0])),str(normalize(userInfoList[1])),str(normalize(userInfoList[2])),str(normalize(userInfoList[3])),str(normalize(userInfoList[4])),str(normalize(userInfoList[5])),normalize(str(userInfoList[6]).encode('utf8'))])
#           try:
#               write2Database('friendsDetails',tmpStr)
#           except:
#               continue
#           #tmpInfoStr.append([uid,str(normalize(i)),str(normalize(userInfoList[0])),str(normalize(userInfoList[1])),str(normalize(userInfoList[2])),str(normalize(userInfoList[3])),str(normalize(userInfoList[4])),str(normalize(userInfoList[5])),str(normalize(userInfoList[6]))])
#           #tmpInfoStr.append([i[1],userInfoList[0],userInfoList[1],userInfoList[2],userInfoList[3],userInfoList[4],userInfoList[5],userInfoList[6]])
#
#   #cprint("[*] Writing "+str(len(dataList))+" record(s) to database table: "+dbName,"white")
#   cprint("[*] Report has been written to: "+str(reportFileName),"white")
#   cprint("[*] Preparing Maltego output...","white")
#   createMaltego(username)
#   cprint("[*] Maltego file has been created","white")'''
#
    driver.close()
    driver.quit
    conn.close()


def test(username):
    username = username.strip()
    print "[*] Username:\t"+str(username)
    global uid
    
    loginFacebook(driver)
    uid = convertUser2ID2(driver,username)
    if not uid:
        print "[!] Problem converting username to uid"
        sys.exit()
    else:
        print "[*] Uid:\t"+str(uid)

    url = 'https://www.facebook.com/'+username.encode('utf8')+'/info'
    html = downloadPage(url)
    """html1=html.decode('utf-8')
    text_file = codecs.open(username+".html", 'w', encoding='utf-8')
    text_file.write(html1)
    text_file.close()"""
    print parseUserInfo(html)

def options(arguments):
    user = ""
    count = 0
    for arg in arguments:
        if arg == "-user":
            print arguments[count]
            count+=1
            print arguments[count]
            user = arguments[count+1]
        if arg == "-report":
            count+=1
            global reportFileName
            reportFileName = arguments[count+1]
    mainProcess(user)
    """test(user)"""

def showhelp():

    print ""
    print " MMMMMM$ZMMMMMDIMMMMMMMMNIMMMMMMIDMMMMMMM"
    print " MMMMMMNINMMMMDINMMMMMMMZIMMMMMZIMMMMMMMM"
    print " MMMMMMMIIMMMMMI$MMMMMMMIIMMMM8I$MMMMMMMM"
    print " MMMMMMMMIINMMMIIMMMMMMNIIMMMOIIMMMMMMMMM"
    print " MMMMMMMMOIIIMM$I$MMMMNII8MNIIINMMMMMMMMM"
    print " MMMMMMMMMZIIIZMIIIMMMIIIM7IIIDMMMMMMMMMM"
    print " MMMMMMMMMMDIIIIIIIZMIIIIIII$MMMMMMMMMMMM"
    print " MMMMMMMMMMMM8IIIIIIZIIIIIIMMMMMMMMMMMMMM"
    print " MMMMMMMMMMMNIIIIIIIIIIIIIIIMMMMMMMMMMMMM"
    print " MMMMMMMMM$IIIIIIIIIIIIIIIIIII8MMMMMMMMMM"
    print " MMMMMMMMIIIIIZIIIIZMIIIIIDIIIIIMMMMMMMMM"
    print " MMMMMMOIIIDMDIIIIZMMMIIIIIMMOIIINMMMMMMM"
    print " MMMMMNIIIMMMIIII8MMMMM$IIIZMMDIIIMMMMMMM"
    print " MMMMIIIZMMM8IIIZMMMMMMMIIIIMMMM7IIZMMMMM"
    print " MMM$IIMMMMOIIIIMMMMMMMMMIIIIMMMM8IIDMMMM"
    print " MMDIZMMMMMIIIIMMMMMMMMMMNIII7MMMMNIIMMMM"
    print " MMIOMMMMMNIII8MMMMMMMMMMM7IIIMMMMMM77MMM"
    print " MO$MMMMMM7IIIMMMMMMMMMMMMMIII8MMMMMMIMMM"
    print " MIMMMMMMMIIIDMMMMMMMMMMMMM$II7MMMMMMM7MM"
    print " MMMMMMMMMIIIMMMMMMMMMMMMMMMIIIMMMMMMMDMM"
    print " MMMMMMMMMII$MMMMMMMMMMMMMMMIIIMMMMMMMMMM"
    print " MMMMMMMMNIINMMMMMMMMMMMMMMMOIIMMMMMMMMMM"
    print " MMMMMMMMNIOMMMMMMMMMMMMMMMMM7IMMMMMMMMMM"
    print " MMMMMMMMNINMMMMMMMMMMMMMMMMMZIMMMMMMMMMM"
    print " MMMMMMMMMIMMMMMMMMMMMMMMMMMM8IMMMMMMMMMM"

    print """
    #####################################################
    #                  fbStalker.py                 #
    #               [Trustwave Spiderlabs]              #
    #####################################################
    Usage: python fbStalker.py [OPTIONS]

    [OPTIONS]

    -user   [Facebook Username]
    -report [Filename]
    """

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        showhelp()
        #print "I am in main and exiting\n"
        driver.close()
        driver.quit
        conn.close()
        sys.exit()
    else:
        if len(facebook_username)<1 or len(facebook_password)<1:
            print "[*] Please fill in 'facebook_username' and 'facebook_password' before continuing."
            sys.exit()
        options(sys.argv)

def parseUser(userid):
    uid = convertUser2ID2(driver,username)
    if not uid:
        print "[!] Problem converting username to uid"
        sys.exit()
    else:
        print "[*] Uid:\t"+str(uid)

    url = 'https://www.facebook.com/'+username.encode('utf8')+'/info'
    html = downloadPage(url)
    soup = BeautifulSoup(str(html),from_encoding('utf-8'))
    
