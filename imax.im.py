# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import codecs,sys
import urllib2, cookielib
import urllib
import MySQLdb
from datetime import *
import time

domain = 'http://imax.im'
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1612.1 Safari/537.36'}
headers2 = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1612.1 Safari/537.36', 'Referer': 'http://imax.im/'}

def get_datetime():
    dt = datetime.now()
    return dt.strftime('%Y-%m-%d %H:%M:%S')

#mysql
def get_mysql_conn():
    conn = None
    
    try:
        conn = MySQLdb.connect(host="localhost",user="cooiky",passwd="123heroleader",db="cooiky_720pim",charset="utf8")
        #conn = MySQLdb.connect(host="localhost",user="root",passwd="wangqiang",db="720pim",charset="utf8")
    except MySQLdb.Error,e:
        print 'Mysql Error %d: %s' % (e.args[0], e.args[1])
        sys.exit(1)
    
    return conn

#insert data
def insert_data_movies(conn,name,name2,year,country,category,director,actor,rank,cover,content,language,douban):
    dt = get_datetime()
    cursor = conn.cursor()
    cursor.execute('''insert into movies values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")''' %\
                   (0,name,name2,year,country,category,director,actor,rank,cover,content,language,douban,'',0,dt))
    _id = cursor.lastrowid
    conn.commit()
    return _id

#update data
def update_data_movies(conn,movieid):
    dt = get_datetime()
    cursor = conn.cursor()
    cursor.execute('''delete from attach where mid="%s"''' % (movieid))
    conn.commit()

def insert_data_attach(conn,size,qu,link,name,mid):
    cursor = conn.cursor()
    cursor.execute('''insert into attach values ("%s","%s","%s","%s","%s","%s")''' %(0,size,qu,link,name,mid))
    _id = cursor.lastrowid
    conn.commit()
    return _id

def update_data_attach(conn,size,qu,link,name,mid):
    cursor = conn.cursor()
    cursor.execute('''select id from attach where link="%s" and mid="%s"''' % (link,mid))
    row = cursor.fetchone()
    if row is None:
        insert_data_attach(conn,size,qu,link,name,mid)

#数据检查
def check_movie(conn,name):
    cursor = conn.cursor()
    cursor.execute('''select id from movies where name="%s"''' % name)
    row = cursor.fetchone()
    if row is None:
        return 0
    else:
        return row[0]

#页面内容
def get_page_content(url, page):
    if page == 'index':
        req = urllib2.Request(url, None, headers)
    else:
        req = urllib2.Request(url, None, headers2)
    return urllib2.urlopen(req).read()


#页面电影链接
def get_page_index_data(conn,urlcontent):
    soup = BeautifulSoup(urlcontent)
    lis = soup.select('.movie')
    
    for li in lis:
        soup = BeautifulSoup(str(li))
        url = soup.find('li', class_='name').a['href'] #/movies/54762
        if url == "/movies/39842":
            continue

        get_movie_detail(conn,get_page_content(domain + url, 'page'))
        time.sleep(30)

#电影详细
def get_movie_detail(conn,urlcontent):
    soup = BeautifulSoup(urlcontent)
    if soup.find('span', itemprop='name') is None:
        return
    
    #名字
    title = soup.find('span', itemprop='name').get_text().strip()
    print title
    movieid = check_movie(conn,title)
    log = codecs.open("test.txt", "ab", "utf-8")
    log.write(get_datetime() + "  " + title + "  " + str(movieid) + "   " + "\r\n")
    log.close()
    
    #年份
    if soup.find('span', class_='year') is None:
        year = 0
    else:
        year = soup.find('span', class_='year').get_text().strip()
        year = year[1:5]

    douban = soup.find('div', class_='raters_count').a['href']
    douban = douban[douban.rfind('/') + 1:len(douban)]
    
    #评分
    rank = soup.find('span', class_='movie_rank').get_text().strip()

    #导演
    if soup.find('a', class_='director') is None:
        director = ''
    else:
        director = soup.find('a', class_='director').get_text().strip()

    #海报
    img = soup.find('div', class_='cover').img.attrs['src'].strip()

    #名字2
    if soup.find('ul', class_='details').h2 is None:
        title2 = ''
    else:
        title2 = soup.find('ul', class_='details').h2.get_text().strip()

    #简介
    detail = soup.find('span', itemprop='about').get_text().strip()
    detail = detail.replace("'", "")
    detail = detail.replace('"', "")

    #语言
    language = soup.find('span', itemprop='inLanguage').get_text().strip()
    
    #演员
    actor = None
    actors = soup.select('.actor')
    for _actors in actors:
        _actor = BeautifulSoup(str(_actors))
        if actor is None:
            actor = _actor.get_text().strip()
        else:
            actor = actor + ',' + _actor.get_text().strip()

    #国家
    country = None
    countrys = soup.select('.country')
    for _countrys in countrys:
        _country = BeautifulSoup(str(_countrys))
        if country is None:
            country = _country.get_text().strip()
        else:
            country = country + ',' + _country.get_text().strip()

    #类型
    category = None
    categorys = soup.select('.category')
    for _categorys in categorys:
        _category = BeautifulSoup(str(_categorys))
        if category is None:
            category = _category.get_text().strip()
        else:
            category = category + ',' + _category.get_text().strip()

    if movieid == 0:
        mid = insert_data_movies(conn,title,title2,year,country,category,director,actor,rank,img,detail,language,douban)

    trs = soup.select('table tbody tr')
    for _trs in trs:
        _tr = BeautifulSoup(str(_trs))
        #格式
        _type = _tr.find('td', class_='qu').get_text().strip()
        #大小
        _size = _tr.find('td', class_='size').get_text().strip()
        #下载链接
        _link = _tr.find('td', class_='name').a['href'].strip()
        _name = _tr.find('td', class_='name').get_text().strip()

        if movieid > 0:
            update_data_attach(conn,_size,_type,_link,_name,movieid)
        else:
            insert_data_attach(conn,_size,_type,_link,_name,mid)

def main():
    conn = get_mysql_conn()
    for i in range(1, 3):
        url = 'http://imax.im/movies?page=' + str(i)
        urlcontent = get_page_content(url, 'index')
        get_page_index_data(conn,urlcontent)
        time.sleep(50)
    conn.close()

if __name__ == '__main__':
    main()
