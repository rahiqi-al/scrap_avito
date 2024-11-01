from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import pandas as pd
import itertools



class avito_scrap:
    

    
    def __init__(self,number_page,data,driver,new_li):
        self.number_page = number_page
        self.data = data 
        self.driver = driver
        self.lis=[]
        self.base_url='https://www.avito.ma/fr/maroc/ventes_immobilieres-%C3%A0_vendre?o='
        self.new_li=new_li


    def scrap_store(self,anoonce):
        self.driver.get(anoonce)
        time.sleep(1)
        ll=[]
        for i in self.new_li:
            try:
                ll.append(self.driver.find_element(By.XPATH,i).text)
            
            except Exception :
                ll.append(None)

        ll.append(anoonce)

        for key, value in zip(self.data.keys(), ll):
            self.data[key].append(value)
                

    def get_all_apartements(self):
        for i  in range(1,self.number_page):
            self.driver.get(self.base_url+str(i))
            time.sleep(1)
            self.lis.append(self.driver.find_elements(By.XPATH,"//a[@class='sc-1jge648-0 eTbzNs']"))
        return  [a.get_attribute('href')  for a in list(itertools.chain.from_iterable(self.lis))]
    
    def scrap_data(self):
        for annonce in self.get_all_apartements():
            self.scrap_store(annonce)

    def turn_to_csv(self):
        self.scrap_data()
        df=pd.DataFrame(self.data)
        df.to_csv('new_avito_csv.csv', encoding='utf-8', index=False)
        driver.quit()




     
        
     
    
    



chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-gpu")  
chrome_options.add_argument("--disable-extensions")  
prefs = {"profile.managed_default_content_settings.images": 2}  
chrome_options.add_experimental_option("prefs", prefs)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.implicitly_wait(10)

new_li=['//*[@id="__next"]/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/h1',
         '//*[@id="__next"]/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/span[1]',
         '//*[@id="__next"]/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/p',
         '//*[@id="__next"]/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[4]/div[1]/div[1]/div/span',
         '//*[@id="__next"]/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[4]/div[1]/div[2]/div/span',
         '//*[@id="__next"]/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[4]/div[1]/div[3]/div/span',
         '//*[@id="__next"]/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[4]/div[2]/ol/li[6]/span[2]',
         '//*[@id="__next"]/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[4]/div[2]/ol/li[1]/span[2]',
         '//*[@id="__next"]/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[5]/p' ]

data={'titre':[],
    'localisation':[],
    'prix':[],
    'N_chambre':[],
    'N_salles_bain':[],
    'surface':[],
    'etage':[],
    'Type':[],
    'description':[],
    'lien_annonce':[] }


data_scraped = avito_scrap(2,data,driver,new_li) 
data_scraped.turn_to_csv()      











