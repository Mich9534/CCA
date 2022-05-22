'IMPORTO LE LIBRERIE'
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # per inserire testo in un box di testo
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

PATH = "/home/michele/Desktop/chromedriver"
driver = webdriver.Chrome(PATH)
driver.get("https://scholar.google.com/")      
search = driver.find_element(By.NAME,"q")       # Trovo il marcatore dove è contenuto il banner search di Google Scholar 
search.send_keys("Pierpaolo De Blasi")          # inserisco nel banner il Nome che voglio cercare
search.send_keys(Keys.RETURN)

link = driver.find_element(By.LINK_TEXT,
                           'Pierpaolo De Blasi') # Troviamo il link corrispondente alla psgina personale del prof
link.click()                                     # ci clicchiamo sopra


# IL TASTO "SHOW MORE" È UN BOTTONE. DOBBIAMO QUINDI TROVARE IL MODO PER TROVARLO E CLICCARCI SOPRA.
wait = WebDriverWait(driver, 10)
while True:
    # click SHOW MORE
    try:
        element = wait.until(EC.element_to_be_clickable((By.ID, 'gsc_bpf_more')))
        element.click()
    except TimeoutException:
        break

# TROVIAMO ORA TUTTI I PAPER NELLA PAGINA
all_papers = driver.find_elements(By.XPATH,"//a[@class='gsc_a_at']")

for paper in all_papers:
    print(paper.text)

wait = WebDriverWait(driver, 5)
driver.quit()
