import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://kap.org.tr/tr/Endeksler")

# Must wait for page to load!
time.sleep(2)

# Find Tüm Endeksler dropdown menu and click sinai index
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Tüm Endeksler')]"))
    )
    driver.find_element(By.XPATH, "//*[contains(text(), 'Tüm Endeksler')]").click()

    # Scroll to index
    scroll = driver.find_element(By.XPATH, "//div[contains(@class, 'select__option') and .//span[text()='BIST SINAİ']]")
    driver.execute_script("arguments[0].scrollIntoView(true);", scroll)

    scroll.click()
except:
    print("Couldn't click Index Dropdown Menu")
    # driver.quit()

# Scrape elements of SINAİ Index
name_elemens = driver.find_elements(By.CSS_SELECTOR, "tr.border-b td:nth-child(2) a")
stock_names = [stock_name.text.strip() for stock_name in name_elemens]

# Write the stock names to a text file
with open("/home/gun/Sinai.txt", "w") as f:
    f.write(str(stock_names))
