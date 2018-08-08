import urllib.request
from bs4 import BeautifulSoup
import datetime
import newspaper
import json
import os.path
import os
import io
import langdetect
import time
import articleDateExtractor

### Download functions

def Achriv_data_Download(URL_List, Date_List, site = 'Handelsblatt',  
                      URL_Filter = list(['']), URL_skip = None,): #Default -> alles wird heruntergeladen

    JSON_count_var = 1
    
    ### Outputvariables
    date = list()
    source = list()
    url = list()
    header = list()
    lang = list()
    body = list()
    
    ### Alle Artikel durchgehen
    if URL_skip == None:
        for i in range(len(URL_List)):
            article = newspaper.Article(URL_List[i])
            for j in range(len(URL_Filter)):
                if URL_Filter[j] in article.url:
                    try:
                        article.download()
                        article.parse()
                    except:
                        try:
                            time.delay(5)
                            article.download()
                            article.parse()
                        except:
                            break
                    if JSON_count_var >1:
                        Is_duplicate = False
                        for k in header:
                            if (article.title in k or k in article.title):
                                Is_duplicate = True
                        if Is_duplicate:
                            continue
                    if article.text != '':
                        Language = langdetect.detect(article.text)
                    else:
                        Language = 'Body is empty!'
                    date.append(str(Date_List[i])[0:10])
                    source.append(site)
                    url.append(article.url)
                    header.append(article.title)
                    lang.append(Language)
                    body.append(article.text)
                    JSON_count_var = JSON_count_var + 1
                    break
    else:
        for i in range(len(URL_List)):
            article = newspaper.Article(URL_List[i])
            LOOP_BREAK = False
            for k in range(len(URL_skip)):
                if URL_skip[k] in article.url: # Damit nicht unnötige Websites wie Videos heruntergeladen werden
                    LOOP_BREAK = True
            if LOOP_BREAK:
                continue
            for j in range(len(URL_Filter)):
                if URL_Filter[j] in article.url:
                    try:
                        article.download()
                        article.parse()
                    except:
                        try:
                            time.delay(5)
                            article.download()
                            article.parse()
                        except:
                            break
                    if JSON_count_var >1:
                        Is_duplicate = False
                        for k in header:
                            if (article.title in k or k in article.title):
                                Is_duplicate = True
                        if Is_duplicate:
                            continue
                    if article.text != '':
                        Language = langdetect.detect(article.text)
                    else:
                        Language = 'Body is empty!'
                    date.append(str(Date_List[i])[0:10])
                    source.append(site)
                    url.append(article.url)
                    header.append(article.title)
                    lang.append(Language)
                    body.append(article.text)
                    JSON_count_var = JSON_count_var + 1
                    break

    return date, source, url, header, lang, body


### URL crawler

#Handelsblatt

def Archiv_Crawler_Handelsblatt(Starting_Date, Ending_Date = datetime.datetime.now()):
    
    Link_list = []
    Date_list = []
    
    while Starting_Date < Ending_Date:
        ### Bauen des Archiv-Links
        Year = Starting_Date.timetuple()[0]
        Month = Starting_Date.timetuple()[1]
        Day = Starting_Date.timetuple()[2]
        
        quote_page = 'https://www.handelsblatt.com/archiv/' + str(Year) + '/' + str(
                Month) + '/' + str(Day)
        
        Right_Arrow = 'SENSELESS CONTENT'
        
        while Right_Arrow != None:
            ### HTML herunterladen
            if Right_Arrow == 'SENSELESS CONTENT':
                page = urllib.request.urlopen(quote_page)
            else:
                page = urllib.request.urlopen(Right_Arrow_Link)
            
            soup = BeautifulSoup(page, 'html.parser')
            ### Artikel-Verlinkungen nehmen
            name_box = soup.find_all('a', attrs={'class': 'vhb-teaser-link'})
            ### Allen Artikeln auf der aktuellen Seite die Links entnehmen und in die Liste fügen
            for i in range(len(name_box)):
                Link_list.append('https://www.handelsblatt.com' + name_box[i].get('href'))
                Date_list.append(Starting_Date)
            ### Den nächste Seite Button finden
            Right_Arrow = soup.find('a', attrs={'class': "vhb-tp-arrow vhb-tp-arrow-next"})
            ### Wenn Button existiert, dann Link speichern
            if Right_Arrow != None:
                Right_Arrow_Link = 'https://www.handelsblatt.com' +Right_Arrow.get('href')
        ### Prozedur für nächsten Tag wiederholen
        Starting_Date= Starting_Date + datetime.timedelta(1)
        
    
    return Link_list, Date_list


#Stern


def Archiv_Crawler_Stern(Starting_Date, Ending_Date = datetime.datetime.now()):
    
    Link_list = []
    Date_list = []
    
    Year = Starting_Date.timetuple()[0]
    Month = Starting_Date.timetuple()[1]
    
    while (Year < Ending_Date.timetuple()[0] or(Year == Ending_Date.timetuple()[0] and 
                                        Month <= Ending_Date.timetuple()[1])): ### --> Hier noch abändern mit Monat rein
        ### Bauen des Archiv-Links
        #Year = Starting_Date.timetuple()[0]
        #Month = Starting_Date.timetuple()[1]
        #Day = Starting_Date.timetuple()[2]
        
        quote_page = 'https://www.stern.de/wirtschaft/archiv/?month=' + str(
                Month) + '&year=' + str(Year)
        
        Right_Arrow = 'SENSELESS CONTENT'
        
        while Right_Arrow != None:
            ### HTML herunterladen
            if Right_Arrow == 'SENSELESS CONTENT':
                page = urllib.request.urlopen(quote_page)
            else:
                page = urllib.request.urlopen(Right_Arrow_Link)
            
            soup = BeautifulSoup(page, 'html.parser')
            ### Artikel-Verlinkungen nehmen
            name_box = soup.find_all('a', attrs={'class':'headline-link'})
            
            Date_box = soup.find_all('span', attrs={'class':'date'})
            ### Allen Artikeln auf der aktuellen Seite die Links entnehmen und in die Liste fügen
            for i in range(len(name_box)):
                Time_String = Date_box[i].text.strip()
                Time = datetime.datetime(int(Time_String[6:10]), int(Time_String[3:5]), 
                                             int(Time_String[0:2]))
                if Time > Ending_Date:
                    Right_Arrow = soup.find('a', attrs={'title':'nächste Seite'})
                    ### Wenn Button existiert, dann Link speichern
                    if Right_Arrow != None:
                        Right_Arrow_Link = 'http://www.sueddeutsche.de' + Right_Arrow.get('href')
                    continue
                if Time >= Starting_Date:
                    Link_list.append(name_box[i].get('href'))
                    Date_list.append(Time)
                    ### Den nächste Seite Button finden
                    Right_Arrow = soup.find('a', attrs={
                            'class':'m-pagination__icon m-pagination__icon--next'})
                    ### Wenn Button existiert, dann Link speichern
                    if Right_Arrow != None:
                        Right_Arrow_Link = Right_Arrow.get('href')
                else:
                    Right_Arrow = None
                    break # man brauch nicht weiter zurück gehen
        if Month == 12:
            Month = 1
            Year = Year + 1
        else:
            Month = Month + 1
        
    Year = Starting_Date.timetuple()[0]
    Month = Starting_Date.timetuple()[1]
    
    while (Year < Ending_Date.timetuple()[0] or(Year == Ending_Date.timetuple()[0] and 
                                        Month <= Ending_Date.timetuple()[1])): ### --> Hier noch abändern mit Monat rein
        ### Bauen des Archiv-Links
        #Year = Starting_Date.timetuple()[0]
        #Month = Starting_Date.timetuple()[1]
        #Day = Starting_Date.timetuple()[2]
        
        quote_page = 'https://www.stern.de/politik/archiv/?month=' + str(
                Month) + '&year=' + str(Year)
        
        Right_Arrow = 'SENSELESS CONTENT'
        
        while Right_Arrow != None:
            ### HTML herunterladen
            if Right_Arrow == 'SENSELESS CONTENT':
                page = urllib.request.urlopen(quote_page)
            else:
                page = urllib.request.urlopen(Right_Arrow_Link)
            
            soup = BeautifulSoup(page, 'html.parser')
            ### Artikel-Verlinkungen nehmen
            name_box = soup.find_all('a', attrs={'class':'headline-link'})
            
            Date_box = soup.find_all('span', attrs={'class':'date'})
            ### Allen Artikeln auf der aktuellen Seite die Links entnehmen und in die Liste fügen
            for i in range(len(name_box)):
                Time_String = Date_box[i].text.strip()
                Time = datetime.datetime(int(Time_String[6:10]), int(Time_String[3:5]), 
                                             int(Time_String[0:2]))
                if Time > Ending_Date:
                    Right_Arrow = soup.find('a', attrs={'title':'nächste Seite'})
                    ### Wenn Button existiert, dann Link speichern
                    if Right_Arrow != None:
                        Right_Arrow_Link = 'http://www.sueddeutsche.de' + Right_Arrow.get('href')
                    continue
                if Time >= Starting_Date:
                    Link_list.append(name_box[i].get('href'))
                    Date_list.append(Time)
                    ### Den nächste Seite Button finden
                    Right_Arrow = soup.find('a', attrs={
                            'class':'m-pagination__icon m-pagination__icon--next'})
                    ### Wenn Button existiert, dann Link speichern
                    if Right_Arrow != None:
                        Right_Arrow_Link = Right_Arrow.get('href')
                else:
                    Right_Arrow = None
                    break # man brauch nicht weiter zurück gehen
        if Month == 12:
            Month = 1
            Year = Year + 1
        else:
            Month = Month + 1
    
    
    return Link_list, Date_list


#Reuters

def Archiv_Crawler_Reuters(Starting_Date, Ending_Date = datetime.datetime.now()):
    Month_dict={'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7,
                'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
    
    Link_list = []
    Date_list = []
    
    quote_page = 'https://de.reuters.com/news/archive?view=page&page=1&pageSize=10' 
    
    Right_Arrow = 'SENSELESS CONTENT'
    
    while Right_Arrow != None:
        ### HTML herunterladen
        if Right_Arrow == 'SENSELESS CONTENT':
            page = urllib.request.urlopen(quote_page)
        else:
            page = urllib.request.urlopen(Right_Arrow_Link)
        
        soup = BeautifulSoup(page, 'html.parser')
        ### Artikel-Verlinkungen nehmen
        name_box = soup.find_all('article')
        ### Allen Artikeln auf der aktuellen Seite die Links entnehmen und in die Liste fügen
        Date_box = soup.find_all('span', attrs={'class':'timestamp'})
        
        for i in range(len(name_box)):
            Time_String = Date_box[i].text
            if len(Time_String) != 11 or Time_String[7:9] != '20':
                Time = datetime.datetime(datetime.datetime.now().timetuple()[0], 
                                         datetime.datetime.now().timetuple()[1],
                                         datetime.datetime.now().timetuple()[2])
            else:
                Time = datetime.datetime(int(Time_String[7:11]),
                                         Month_dict[Time_String[3:6]], 
                                         int(Time_String[0:2]))
            if Time > Ending_Date:
                continue
            if Time >= Starting_Date:
                Link_list.append('https://de.reuters.com' + name_box[i].find('a').get('href'))
                Date_list.append(Time)
                ### Den nächste Seite Button finden
                Right_Arrow = soup.find('a', attrs={'class':'control-nav-next'})
                ### Wenn Button existiert, dann Link speichern
                if Right_Arrow != None:
                    Right_Arrow_Link = 'https://de.reuters.com/news/archive' + Right_Arrow.get('href')
            else:
                Right_Arrow = None
                break # man brauch nicht weiter zurück gehen
    ### Prozedur für nächsten Tag wiederholen
    
    
    return Link_list, Date_list


#Tagesschau

def Archiv_Crawler_Tagesschau(Starting_Date, Ending_Date = datetime.datetime.now()):
    
    Link_list = []
    Date_list = []
    
    while Starting_Date < Ending_Date:
        ### Bauen des Archiv-Links
        Year = str(Starting_Date.timetuple()[0])
        Month = str(Starting_Date.timetuple()[1])
        Day = str(Starting_Date.timetuple()[2])
        
        if len(Month) == 1:
            Month = '0' + Month
        if len(Day) == 1:
            Day = '0' + Day
        
        quote_page = 'https://www.tagesschau.de/archiv/meldungsarchiv100~_date-' + Year + Month + Day + '.html'
        
        ### HTML herunterladen
        page = urllib.request.urlopen(quote_page)
        
        soup = BeautifulSoup(page, 'html.parser')
        ### Artikel-Verlinkungen nehmen
        name_box = soup.find('ul', attrs={'class':'list'}).find_all('a')
        ### Allen Artikeln auf der aktuellen Seite die Links entnehmen und in die Liste fügen
        for i in range(len(name_box)):
            href = name_box[i].get('href')
            if 'http' in href:
                Link_list.append(href)
            else:
                Link_list.append('https://www.tagesschau.de' + name_box[i].get('href'))
            Date_list.append(Starting_Date)

        ### Prozedur für nächsten Tag wiederholen
        Starting_Date= Starting_Date + datetime.timedelta(1)
    
    
    return Link_list, Date_list


#Spiegel

def Archiv_Crawler_Spiegel(Starting_Date, Ending_Date = datetime.datetime.now()):
    
    Link_list = []
    Date_list = []
    
    while Starting_Date < Ending_Date:
        ### Bauen des Archiv-Links
        Year = str(Starting_Date.timetuple()[0])
        Month = str(Starting_Date.timetuple()[1])
        Day = str(Starting_Date.timetuple()[2])
        
        if len(Month) == 1:
            Month = '0' + Month
        
        if len(Day) == 1:
            Day = '0'+ Day
        
        quote_page = 'http://www.spiegel.de/nachrichtenarchiv/artikel-' + Day + '.' + Month + '.' + Year + '.html'
        
        ### HTML herunterladen
        page = urllib.request.urlopen(quote_page)
        
        soup = BeautifulSoup(page, 'html.parser')
        ### Artikel-Verlinkungen nehmen
        name_box = soup.find_all('span', attrs={'class': 'news-archive-headline'})
        ### Allen Artikeln auf der aktuellen Seite die Links entnehmen und in die Liste fügen
        for i in range(len(name_box)):
            href = name_box[i].parent.get('href')
            if 'www' in href:
                Link_list.append(href)
            else:
                Link_list.append('http://www.spiegel.de' + href)
            Date_list.append(Starting_Date)

        ### Prozedur für nächsten Tag wiederholen
        Starting_Date= Starting_Date + datetime.timedelta(1)
        
    
    return Link_list, Date_list


#Manager-Magazin

def Archiv_Crawler_MM(Starting_Date, Ending_Date = datetime.datetime.now()):
    
    Link_list = []
    Date_list = []
            
    Year = datetime.datetime.now().timetuple()[0]
    
    quote_page = 'http://www.manager-magazin.de/unternehmen/archiv-' + str(
            Year) + '999.html'
    
    Right_Arrow = 'SENSELESS CONTENT'
    
    while Right_Arrow != None:
        ### HTML herunterladen
        if Right_Arrow == 'SENSELESS CONTENT':
            page = urllib.request.urlopen(quote_page)
        else:
            page = urllib.request.urlopen(Right_Arrow_Link)
        
        soup = BeautifulSoup(page, 'html.parser')
        ### Artikel-Verlinkungen nehmen
        name_box = soup.find_all('h2', attrs = {'class':'article-title'})
        ### Allen Artikeln auf der aktuellen Seite die Links entnehmen und in die Liste fügen
        for i in range(len(name_box)):
            if 'http' in name_box[i].find('a').get('href'):
                URL = name_box[i].find('a').get('href')
            else:
                URL = 'http://www.manager-magazin.de' + name_box[i].find('a').get('href')
            Timing = articleDateExtractor.extractArticlePublishedDate(URL)
            Time = datetime.datetime(Timing.timetuple()[0],Timing.timetuple()[1],
                                     Timing.timetuple()[2],)
            if Time > Ending_Date:
                continue
            if Time >= Starting_Date:
                Link_list.append(URL)
                Date_list.append(Time)
                ### Den nächste Seite Button finden
                Right_Arrow = soup.find('a', attrs = {'class': 'next'})
                ### Wenn Button existiert, dann Link speichern
                Right_Arrow_Link = 'http://www.manager-magazin.de' + Right_Arrow.get('href')
            else:
                Right_Arrow = None
                break # man brauch nicht weiter zurück gehen
    
    quote_page = 'http://www.manager-magazin.de/finanzen/archiv-' + str(
            Year) + '999.html'
    
    Right_Arrow = 'SENSELESS CONTENT'
    
    while Right_Arrow != None:
        ### HTML herunterladen
        if Right_Arrow == 'SENSELESS CONTENT':
            page = urllib.request.urlopen(quote_page)
        else:
            page = urllib.request.urlopen(Right_Arrow_Link)
        
        soup = BeautifulSoup(page, 'html.parser')
        ### Artikel-Verlinkungen nehmen
        name_box = soup.find_all('h2', attrs = {'class':'article-title'})
        ### Allen Artikeln auf der aktuellen Seite die Links entnehmen und in die Liste fügen
        for i in range(len(name_box)):
            if 'http' in name_box[i].find('a').get('href'):
                URL = name_box[i].find('a').get('href')
            else:
                URL = 'http://www.manager-magazin.de' + name_box[i].find('a').get('href')
            Timing = articleDateExtractor.extractArticlePublishedDate(URL)
            Time = datetime.datetime(Timing.timetuple()[0],Timing.timetuple()[1],
                                     Timing.timetuple()[2],)
            if Time > Ending_Date:
                continue
            if Time >= Starting_Date:
                Link_list.append(URL)
                Date_list.append(Time)
                ### Den nächste Seite Button finden
                Right_Arrow = soup.find('a', attrs = {'class': 'next'})
                ### Wenn Button existiert, dann Link speichern
                Right_Arrow_Link = 'http://www.manager-magazin.de' + Right_Arrow.get('href')
            else:
                Right_Arrow = None
                break # man brauch nicht weiter zurück gehen
    
    quote_page = 'http://www.manager-magazin.de/politik/archiv-' + str(
            Year) + '999.html'
    
    Right_Arrow = 'SENSELESS CONTENT'
    
    while Right_Arrow != None:
        ### HTML herunterladen
        if Right_Arrow == 'SENSELESS CONTENT':
            page = urllib.request.urlopen(quote_page)
        else:
            page = urllib.request.urlopen(Right_Arrow_Link)
        
        soup = BeautifulSoup(page, 'html.parser')
        ### Artikel-Verlinkungen nehmen
        name_box = soup.find_all('h2', attrs = {'class':'article-title'})
        ### Allen Artikeln auf der aktuellen Seite die Links entnehmen und in die Liste fügen
        for i in range(len(name_box)):
            if 'http' in name_box[i].find('a').get('href'):
                URL = name_box[i].find('a').get('href')
            else:
                URL = 'http://www.manager-magazin.de' + name_box[i].find('a').get('href')
            Timing = articleDateExtractor.extractArticlePublishedDate(URL)
            Time = datetime.datetime(Timing.timetuple()[0],Timing.timetuple()[1],
                                     Timing.timetuple()[2],)
            if Time > Ending_Date:
                continue
            if Time >= Starting_Date:
                Link_list.append(URL)
                Date_list.append(Time)
                ### Den nächste Seite Button finden
                Right_Arrow = soup.find('a', attrs = {'class': 'next'})
                ### Wenn Button existiert, dann Link speichern
                Right_Arrow_Link = 'http://www.manager-magazin.de' + Right_Arrow.get('href')
            else:
                Right_Arrow = None
                break # man brauch nicht weiter zurück gehen
    
    return Link_list, Date_list
