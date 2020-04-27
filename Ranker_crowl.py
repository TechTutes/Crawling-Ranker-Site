# importing libraries
from bs4 import BeautifulSoup
import requests 
import pandas as pd

#initialize empty dictionary for storing Actors data
data_dictionary = {}

# coding for Crowling a web site

# Url of Ranker Watch Worthy Site 
url = "https://www.ranker.com/list/film-actors-from-india/reference"


#A while loop which itters until it reaches the last page of the site
while True:
    
    print(url)
    
    # save the response from the site got using request library in a response library
    response = requests.get(url)
   
    # save the text in data variable
    data = response.text
    
    # convert the text to a soup object
    soup = BeautifulSoup(data,'html.parser')
    
    # Find the block of content in our case it is a dic with class listItem__h2--grid
    main_block = soup.find_all('div',{'class':'listItem__h2--grid'})
    
    # itter through every block and extract data
    # note: this block has some celebraties names not written in a tag so we would other options to go to their profile page
    
    for content in main_block:
        sub_block  = content.find('a',{'class':'listItem__title'})
        
    # As some actors names are in span tag we would check for both of them to get the name
        actor_names = sub_block.text if sub_block else content.find('span',{'class':'listItem__title'}).text
    
    # Finding their ranker profile to get their wiki profile
        actor_profile = content.find('span',{'class':'listItem__wiki'})
        actor_profile_link = actor_profile.find('a')
        
        ranker_link = actor_profile_link.get('href') if actor_profile_link else content.find('a').get('href')  if content.find('a') else "N/A"
        
        
        ActorName = actor_names
        #print(ActorName)
   
    # go into their ranker profile
        if(actor_profile_link):
            a_url = 'https:'+ranker_link
            a_response = requests.get(a_url)
            a_data = a_response.text
            a_soup = BeautifulSoup(a_data,'html.parser')
            
            #finding wiki link
            a_block = a_soup.find('p',{'id':'node__bioWikiText'})
            a_link = a_block.find('a')
            w_link = a_link.get('href') if a_link else "N/A"
            wikipedia_link = w_link
            
            
            a_leftbox = a_soup.find('div',{'class':'node__leftRail'})
            
            #finding picture
            image = a_leftbox.find('img')
            image_src = image.get('src') if image else 'N\A'
            Picture = image_src
            
            #initialize all data to null
            Nationality="N\A"
            Height ="N\A" 
            Age ="N\A"
            Profession ="N\A"
            Nominated = "N\A"
            Parents = "N\A"
            Children = "N\A"
            
            #finding data
            properties = a_leftbox.find_all('div',{'class':'node__propertiesSection'})
            for prop in properties:
                
                if(prop.find('div',{'class':'node__propertiesTitle'}).text == 'Nationality'):
                    Nationality = prop.text
                
                elif(prop.find('div',{'class':'node__propertiesTitle'}).text == 'Height'):
                    Height = prop.text
                
                    
                elif(prop.find('div',{'class':'node__propertiesTitle'}).text == 'Age'):
                    Age = prop.text
                
                elif(prop.find('div',{'class':'node__propertiesTitle'}).text == 'Profession'):
                    Profession = prop.text
                
                elif(prop.find('div',{'class':'node__propertiesTitle'}).text == 'Nominated For'):
                    Nominated = prop.text
                
                elif(prop.find('div',{'class':'node__propertiesTitle'}).text == 'Parents'):
                    Parents = prop.text
               
                elif(prop.find('div',{'class':'node__propertiesTitle'}).text == 'Children'):
                    Children = prop.text
                    
          # if  wiki link  is not found we set the variables to null      
        else:
            wikipedia_link = "N\A"
            Picture ="N\A"
            Nationality="N\A"
            Height ="N\A" 
            Age ="N\A"
            Profession ="N\A"
            Nominated = "N\A"
            Parents = "N\A"
            Children = "N\A"



    # update the dictionary
        data_dictionary[ActorName] = [Profession, Height, Age, Nominated, Parents, Children, Picture, wikipedia_link ]
        
   # Link to more pages     
    url_tag = soup.find('a',{'id':'pagination'})
    
    # next page link
    if url_tag.get('href'):
        url= 'https:' + url_tag.get('href')
    # if its the last page
    else:
        break
    
    # as this site dont have any last page and go on increasing with empty pa we stop the block when the main block is empty 
    if (main_block == []):
        break
        
    # crowling part end
    
# Creating a dataset
Actors_df = pd.DataFrame.from_dict(data_dictionary, orient = 'index', columns = ['Profession','Height','Age', 'Nominated', 'Parents','Children','Picture','wikipedia_link'])
    
# Exporting to csv
Actors_df.to_csv('Actors_info.csv')
    
