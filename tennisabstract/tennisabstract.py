# -*- coding: utf-8 -*-

"""Main module."""



import urllib.request
from bs4 import BeautifulSoup

def get_current_tournament():

    
    url = 'http://www.tennisabstract.com'
    req = urllib.request.Request(url)
    
    response = urllib.request.urlopen(req)
    
    html = response.read()
    
    soup = BeautifulSoup(html, "html.parser")  
    
    tournaments = soup.findAll('a', href=True, text='Results and Forecasts')
    
    tournament_links = []
    
    for tournament in tournaments:
        try: 
            tournament_links.append(tournament['href'])
        except:
            print("tournament not loadable")
                       
            
    return tournament_links     