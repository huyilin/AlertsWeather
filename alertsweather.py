# -*- coding: utf-8 -*-
# from scrapy.spider import Spider
import codecs
import urllib2
import lxml.html
import time
    
class WeatherCrawl:
    #   city_list=['Osnabrück']
    def __init__(self,url_example,weather_file,city_file):
        self.url_example=url_example
        self.weather_file=weather_file
        self.city_file=city_file
        
    def get_cities(self,city_file):
        city_list=city_file.read().encode('utf8').splitlines()
        return city_list
    
    def parse(self):        
        city_list=self.get_cities(self.city_file)
        for city in city_list:
            url=self.url_example.replace("example",city)
            print url
            response=urllib2.urlopen(url)
            data=response.read()
            doc=lxml.html.document_fromstring(data)
            city=doc.xpath('//name/text()')
            dates_dir=doc.xpath('//forecast/time')
            for sub_direc in dates_dir:
                if len(city)>0:
                    weather=sub_direc.xpath('symbol/@name')
                    date=sub_direc.xpath('@day')
                    city[0]=city[0].replace(',',';')
                    output=city[0]+','+date[0]+','+weather[0]+'\n'
                    print output
                    self.weather_file.write(output.encode('utf-8'))
        self.weather_file.close()
        
class TravelAlerts:    
    def __init__(self,url,alert_file,city_file):
        self.url=url
        self.alert_file=alert_file
        self.city_file=city_file
        
    def get_cities(self,city_file):
        city_list=city_file.read().encode('utf8').splitlines()
        return city_list
        
    def convert_date(self,date):
        date=time.strptime(date,"%d %b")
        date=time.strftime("2014-%m-%d",date)
        return date

    def construct_items(self,events,dates,areas,city_list):  #Not necessary in this script, initially for Scrapy.items
        alerts=[]
        for event,date,destination in zip(events,dates,areas):
            for city in destination:
                if city in city_list:
                    item={}
                    item['date']=self.convert_date(date)
                    item['city']=city
                    item['event']=event
                    alerts.append(item)
        return alerts
    
    def parse(self):
        city_list=self.get_cities(self.city_file)
        areas=[]
        events=[]
        response=urllib2.urlopen(self.url)
        data=response.read()
        doc=lxml.html.document_fromstring(data)
        events_dir=doc.xpath('//span[@class="mw-headline"]')
        dates=doc.xpath('//div[@class="mw-content-ltr"]/table/tr/td/p/i/text()') #should be /table/tbody/tr.... but no applicable
        for direc in events_dir:
            event=direc.xpath('span//text()')
            if event!="":
                events.append(''.join(event))
                area=direc.xpath('span/a/text()')
                areas.append(area)
        alerts=self.construct_items(events,dates,areas,city_list)
        for unit in alerts:
            unit['event']=unit['event'].replace(',',';')
            alert=unit['city']+','+unit['date']+'alert=TravelAlerts(url,alert_file,city_file),'+unit['event']+'\n'
            alert=alert.encode('utf-8')
            self.alert_file.write(alert)
            print alert
        self.alert_file.close()

open('/home/yilin/workspace/server/alerts.csv','w').close()
open('/home/yilin/workspace/server/weather.csv','w').close()
# open('/export/home/team06/randomtrip/crawler/weather.csv','w').close()
# open('/export/home/team06/randomtrip/crawler/alerts.csv','w').close()

city_file=codecs.open("/home/yilin/workspace/server/cities.txt","r","utf-8")
# city_file=codecs.open("/export/home/team06/randomtrip/crawler/cities.txt","r","utf-8")

url_example = 'http://api.openweathermap.org/data/2.5/forecast/daily?q=example&mode=xml&units=metric&cnt=7'
weather_file=open('/home/yilin/workspace/server/weather.csv','a')
# weather_file=open('/export/home/team06/randomtrip/crawler/weather.csv','a')
weather=WeatherCrawl(url_example,weather_file,city_file)
weather.parse()

url = "http://wikitravel.org/en/Travel_news"
# alert_file=open('/export/home/team06/randomtrip/crawler/alerts.csv','a')
alert_file=open('/home/yilin/workspace/server/alerts.csv','a')
alert=TravelAlerts(url,alert_file,city_file)
alert.parse()