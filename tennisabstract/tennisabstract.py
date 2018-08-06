# -*- coding: utf-8 -*-

"""Main module."""



import urllib.request
import pandas as pd
from bs4 import BeautifulSoup

def get_current_tournament():
    """
    go to the website "www.tennisabsract.com" and look for tournaments running at the time.
    
    Returns:
        tournament_links: a link-list of url with active tournaments
   
    """

    
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


def get_ta_proba(tournament_url = "http://www.tennisabstract.com/current/2018ATPHouston.html", list_rounds = [2,4,8,16,32,64]):
    """
    read all probabilities from all players from the website. http://www.tennisabstract.com/current/2018ATPHouston.html
    
    Args:
        tournament_url (string): the uri of the tournament  
        list_rounds (list): a list of the rounds   

    
    Returns:
        result: da pandas dataframe including the players and the probalilities
   
    """

    url = tournament_url
    
    req = urllib.request.Request(url)
    #http://live-tennis.eu/en/official-atp-ranking
    response = urllib.request.urlopen(req)

    html = response.read()

    soup = BeautifulSoup(html, "html.parser")
    
    tour_title = soup.title.text
    
    result = pd.DataFrame()
    

    for tournament_round in list_rounds :
        str_round = 'var proj' + str(tournament_round)
        print(url)
        
    
        long_string = str(soup)[str(soup).find(str_round):] 
        table_start = long_string.find('<table')
        table_end = long_string.find('</table>')
        string = long_string[table_start:table_end + 8]
    
        proba = BeautifulSoup(string, "html.parser")
        proba_table = proba.findAll('tr')
        
        for i in range(1, len(proba_table), 2) :
            
            if proba_table[i].a and proba_table[i].td.text != 'Bye' and proba_table[i+1].td.text != 'Bye' \
                                and proba_table[i].td.text[0:9] != 'Qualifier' and proba_table[i+1].td.text[0:9] != 'Qualifier' : 
              
                home_player = proba_table[i]
                home_player_tds = home_player.findAll('td')
                if not home_player_tds[0].a :
                    break
                home_player_name = home_player_tds[0].a.text
                home_player_id = home_player.a['href'].split('?')[1].replace('p=','')
                home_player_proba = float(home_player_tds[2].text.strip('%'))
                #print(home_player_name, home_player_proba)
                
                #print(proba_table[i+1])
                away_player = proba_table[i+1]
                away_player_tds = away_player.findAll('td')
                if not away_player_tds[0].a :
                    break
                away_player_name = away_player_tds[0].a.text  
                away_player_id = away_player.a['href'].split('?')[1].replace('p=','')
                
                away_player_proba = float(away_player_tds[2].text.strip('%'))
                #print(away_player_name, away_player_proba)
                
                
                        ## putting data together    
                dict = { 'tournament' : tour_title,
                         'home_player_name' :  home_player_name,
                         'away_player_name' :  away_player_name,
                         'home_player_id' :  home_player_id,
                         'away_player_id' :  away_player_id,                         
                         'home_player_proba' :  home_player_proba,
                         'away_player_proba' :  away_player_proba
                        }
                
                data = pd.DataFrame([dict])
                
                result = result.append(data, ignore_index=True) 
                                       
    return result


def get_upcoming_events() :
    """
    get all upcoming events for tennis abstracts
    
    Returns:
        result: da pandas dataframe including the players and the probalilities
       
    
    """
    result = pd.DataFrame()
    tournament_list = get_current_tournament()
    
         
    #get normal tournaments    
    for tournament in tournament_list:
        try :
            ta_result = get_ta_proba(tournament_url = tournament, list_rounds = ['Current'])
            result = result.append(ta_result)
        except :
            print("error loading TA page")
            
    
    result = result[(result['home_player_proba'] != 0) & (result['home_player_proba'] != 100) ]
            
    return result
        

    
    

def get_player_information(player='GuidoPella'):
    """
    reading the website http://www.tennisabstract.com/cgi-bin/player.cgi?p=GuidoPella and get 
    all information about the player which are availiable. 
    do also a error handling if some information are not existing.
    
    Args:
        player (string): The string-key of the player   

        
    Returns:
        json: { name    : player_name,
                dob     : day_of_birth,
                plays   : left_right,
                rank    : current_rank,
                d_rank  : current_double_rank,
                links   :  { apt : apt,
                             itf : ift, ...
                             }
                statistics : { last52 : { match : match, 
                                          tiebreaks : tiebreaks, 
                                          ...},
                                          hard : { match: ...}
                              2010 { ... }
                            }
                }
        False: not possible to place the bet
        
    """    