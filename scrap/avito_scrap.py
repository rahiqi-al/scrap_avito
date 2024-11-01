from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import pandas as pd





chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-gpu")  
chrome_options.add_argument("--disable-extensions")  
prefs = {"profile.managed_default_content_settings.images": 2}  
chrome_options.add_experimental_option("prefs", prefs)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.implicitly_wait(10)



def scrapping(apartements,data):
    #this loop to go through each apartement 
    for apartement in apartements:
        driver.get(apartement)
        time.sleep(2)
        li=[]
        #all these try block statements are where we scrap and store the data we want
        try:
            titre=driver.find_element(By.XPATH,"//h1[@class='sc-1g3sn3w-12 jUtCZM']").text   
            li.append(titre)
        except NoSuchElementException:
            li.append(None)
        

        try:
            localisation=driver.find_element(By.XPATH,"//span[@class='sc-1x0vz2r-0 iotEHk']").text
            li.append(localisation)
        except NoSuchElementException:
            li.append(None)

        try:
            prix=driver.find_element(By.XPATH,"//p[@class='sc-1x0vz2r-0 lnEFFR sc-1g3sn3w-13 czygWQ']").text
            li.append(prix)
        except NoSuchElementException:
            li.append(None)
        
        try:
            N_chambre=driver.find_element(By.XPATH,"//div[@class='sc-6p5md9-2 bxrxrn'][1]//span[@class='sc-1x0vz2r-0 kQHNss']").text
            li.append(N_chambre)
        except NoSuchElementException:
            li.append(None)

        try:
            N_salles_bain= driver.find_elements(By.XPATH, "//*[@class='sc-1x0vz2r-0 kQHNss']")[1].text
            # we used by.xpath instead of by.class_name because it doesnt support multiple classes or spaces
            #N_salles_bain=driver.find_elements(By.CLASS_NAME,"sc-1x0vz2r-0 kQHNss")[1].text
            li.append(N_salles_bain)
        except (NoSuchElementException, IndexError):
            li.append(None)
        

        try:
            surface= driver.find_elements(By.XPATH, "//*[@class='sc-1x0vz2r-0 kQHNss']")[2].text
            #surface=driver.find_elements(By.CLASS_NAME,"sc-1x0vz2r-0 kQHNss")[2].text
            li.append(surface)
        except (NoSuchElementException, IndexError):
            li.append(None)

        try:
            etage=driver.find_element(By.XPATH, "//span[contains(text(), 'Étage')]/following-sibling::span").text 
            #etage=driver.find_elements(By.XPATH,"//*[@class='sc-1x0vz2r-0 gSLYtF']")[-1].text
            li.append(etage)
        except (NoSuchElementException, IndexError):
            li.append(None)
            
        try:
            Type=driver.find_elements(By.XPATH,"//*[@class='sc-1x0vz2r-0 gSLYtF']")[0].text
            li.append(Type)
        except (NoSuchElementException, IndexError):
            li.append(None)

        try:
            description=driver.find_element(By.XPATH,"//p[@class='sc-ij98yj-0 fAYGMO']").text
            li.append(description)
        except NoSuchElementException:
            li.append(None)
        
        try:
            equipements=[equipement.text for equipement in driver.find_elements(By.XPATH,"//*[@class='sc-1x0vz2r-0 bXFCIH']")]
            equipements=f'equipements : {','.join(equipements)}'
            li.append(equipements)
        except NoSuchElementException:
            li.append(None)
        
        
        li.append(apartement)
        



        #where we store the scraped date  in a dict 
        for key, value in zip(data.keys(), li):
            data[key].append(value)


        #the problem was Combined XPath Issue, just seperate them
        
        #N_salles_bain=driver.find_elements(BY.XPATH,"//div[@class='sc-6p5md9-2 bxrxrn'][2]//span[@class='sc-1x0vz2r-0 kQHNss']")
        #surface=driver.find_element(BY.XPATH,"//div[@class='sc-6p5md9-2 bxrxrn'][3]//span[@class='sc-1x0vz2r-0 kQHNss']")
        #etage=driver.find_element(BY.XPATH,"//ol[@class='sc-qmn92k-3 iDKTfs']//li[@class='sc-qmn92k-1 jJjeGO'][7]//span[@class='sc-1x0vz2r-0 gSLYtF']")
        #Type=driver.find_element(BY.XPATH,"//ol[@class='sc-qmn92k-3 iDKTfs']//li[@class='sc-qmn92k-1 jJjeGO'][1]//span[@class='sc-1x0vz2r-0 gSLYtF']")
        #description=driver.find_element(BY.XPATH,"//p[@class='sc-ij98yj-0 fAYGMO']")



def main():
    # this is where i am gonna store all the scraped data 
    data={
        'titre':[],
        'localisation':[],
        'prix':[],
        'N_chambre':[],
        'N_salles_bain':[],
        'surface':[],
        'etage':[],
        'Type':[],
        'description':[],
        'equipements':[],
        'lien_annonce':[]
        }
    # this loop allows us to go through multiple pages
    for i in range(1,2):
        driver.get(f'https://www.avito.ma/fr/maroc/locations_immobilieres-%C3%A0_louer?o={i}')
        time.sleep(2)
        #apartements is a list of url of each apartement on a page 
        #apartements=driver.find_elements(By.XPATH,"//a[@class='sc-1jge648-0 eTbzNs']")
        apartements = [a.get_attribute('href') for a in driver.find_elements(By.XPATH, "//a[@class='sc-1jge648-0 eTbzNs']")]
        scrapping(apartements,data)
    
    df=pd.DataFrame(data)
    
    df.to_csv('avito.csv', encoding='utf-8', index=False)
    
    driver.quit()



if __name__=='__main__':
    main()
