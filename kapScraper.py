import ast
import re
import time
from datetime import datetime, timedelta

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

with open("/home/gun/Sinai.txt", "r") as f:
    STOCKS = ast.literal_eval(f.read())

# List of years on the website
YEARS = [
    "/html/body/div[3]/div[3]/ul/li[6]/p",
    "/html/body/div[3]/div[3]/ul/li[7]/p",
    "/html/body/div[3]/div[3]/ul/li[8]/p",
    "/html/body/div[3]/div[3]/ul/li[9]/p",
    "/html/body/div[3]/div[3]/ul/li[10]/p",
    "/html/body/div[3]/div[3]/ul/li[11]/p",
    "/html/body/div[3]/div[3]/ul/li[12]/p",
    "/html/body/div[3]/div[3]/ul/li[13]/p",
    "/html/body/div[3]/div[3]/ul/li[14]/p",
]

bilanco_pattern1 = re.compile(r"general_role_21\d+-row-\d+ data-input-row alternate-row presentation-enabled")
bilanco_pattern2 = re.compile(r"general_role_21\d+-row-\d+ data-input-row presentation-enabled")

karZararPattern1 = re.compile(r"general_role_31\d+-row-\d+ data-input-row alternate-row presentation-enabled")
karZararPattern2 = re.compile(r"general_role_31\d+-row-\d+ data-input-row presentation-enabled")

nakitAkisPattern1 = re.compile(r"general_role_52\d+-row-\d+ data-input-row alternate-row presentation-enabled")
nakitAkisPattern2 = re.compile(r"general_role_52\d+-row-\d+ data-input-row presentation-enabled")

skipped_stocks = []

# Opens up Chrome and goes to the website link
for stock in STOCKS:
    list_of_bilanco_dfs = []
    list_of_karZarar_dfs = []
    list_of_nakitAkis_dfs = []
    fr_release_date = []

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.kap.org.tr/tr")

    # Wait for page to load!
    time.sleep(2)

    # Types the stock name to the search bar
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "all-search")))
        driver.find_element(By.ID, "all-search").click()
        search = driver.find_element(By.ID, "all-search")
        search.send_keys(stock)
        search.send_keys(Keys.ENTER)
    except:
        print("Couldn't find stock name")
        driver.quit()
    time.sleep(2)

    # Enters into the searched stock's page
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="searchDiv"]/div/div[2]/div[2]/div/a[1]/span'))
        )
        driver.find_element(By.XPATH, '//*[@id="searchDiv"]/div/div[2]/div[2]/div/a[1]/span').click()
    except:
        print("Error loading stock's page")
        driver.quit()
    time.sleep(2)

    # Clicks to bildirimler tab
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "notifications-tab")))
        driver.find_element(By.ID, "notifications-tab").click()
    except:
        print("Couldn't find notifications-tab")
        driver.quit()
    time.sleep(2)

    # Iterates over each year
    for year in YEARS:
        # Clicks the SELECT DATE list
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="notifications"]/div/div/div/div/div[1]/div/div[1]/div[1]/div/div/div[1]',
                    )
                )
            )
            driver.find_element(
                By.XPATH,
                '//*[@id="notifications"]/div/div/div/div/div[1]/div/div[1]/div[1]/div/div/div[1]',
            ).click()
        except:
            print("Couldn't select date")
            driver.quit()
        time.sleep(2)

        # Scrolls to year
        scroll = driver.find_element(By.XPATH, year)
        driver.execute_script("arguments[0].scrollIntoView(true);", scroll)

        # Clicks to the required year
        driver.find_element(By.XPATH, year).click()
        time.sleep(2)

        # Clicks notifiaction types list
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="notifications"]/div/div/div/div/div[1]/div/div[1]/div[2]/div/div/div[1]',
                    )
                )
            )
            driver.find_element(
                By.XPATH,
                '//*[@id="notifications"]/div/div/div/div/div[1]/div/div[1]/div[2]/div/div/div[1]',
            ).click()
        except:
            print("Notification types list couldn't be found")
            driver.quit()
        time.sleep(2)

        # Clicks to Finansal Rapor notification type
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[3]/div[3]/ul/li[3]/p",
                    )
                )
            )
            driver.find_element(
                By.XPATH,
                "/html/body/div[3]/div[3]/ul/li[3]/p",
            ).click()
        except:
            print("Couldn't click Finansal Rapor notification from the list")
            driver.quit()
        time.sleep(2)

        # Clicks to search button
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "#notifications button",
                    )
                )
            )
            driver.find_element(
                By.CSS_SELECTOR,
                "#notifications button",
            ).click()
        except:
            print("Couldn't click search button")
            driver.quit()
        time.sleep(2)

        # Clicks to Finansal Rapor notification type
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//button[text()="250"]',
                    )
                )
            )
            driver.find_element(
                By.XPATH,
                '//button[text()="250"]',
            ).click()
        except:
            print("Couldn't click show 250 button")
            driver.quit()
        time.sleep(1)

        # Find all FR's in the page
        FRS = driver.find_elements(By.XPATH, "//td[text()='Finansal Rapor']")
        length_FRS = len(FRS)

        # Break the loop if current year has less than 4 FR's
        if length_FRS < 4:
            break

        # Iterates over each FR
        for i in range(length_FRS):
            bilanco_elements = []
            kar_zarar_elements = []
            nakit_akis_elements = []

            # Scrolls down to Fr on each iteration
            scroll_down_to_middle = driver.execute_script("window.scrollBy(0,200);")
            time.sleep(1)

            # Get the FRS again for looping and page content load
            FRS = driver.find_elements(By.XPATH, "//td[text()='Finansal Rapor']")

            FRS[i].click()
            time.sleep(1)

            # Switch selenium to new tab
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(1)

            # Get the content in page
            page_content = driver.page_source
            soup = BeautifulSoup(page_content, "html.parser")

            # Get bilanco related elements
            bilancoRows = soup.find_all("tr", class_=bilanco_pattern1) + soup.find_all("tr", class_=bilanco_pattern2)

            # Check the column for current period
            column = 0

            for row in bilancoRows:
                num = row.find_all("td")

                if len(num[-3].get_text()) > 6:
                    column = -3
                else:
                    column = -2
                break

            for br in bilancoRows:
                turkish_elements = br.find("div", class_="gwt-Label multi-language-content content-tr")

                if turkish_elements != None:
                    turkish_text = turkish_elements.get_text()
                else:
                    continue

                numbers = br.find_all("td")
                cell_number = numbers[column].get_text()

                # Check and convert string numbers to int
                if cell_number != "":
                    cell_number = int(cell_number.replace(".", ""))

                bilanco_elements.append([turkish_text, cell_number])

            # Get kar zarar table related elements
            karZararRows = soup.find_all("tr", class_=karZararPattern1) + soup.find_all("tr", class_=karZararPattern2)

            for kz in karZararRows:
                turkish_elements = kz.find("div", class_="gwt-Label multi-language-content content-tr")

                if turkish_elements != None:
                    turkish_text = turkish_elements.get_text()
                else:
                    continue

                numbers = kz.find_all("td")
                cell_number = numbers[-4].get_text()
                if cell_number != "":
                    # Convert string numbers to int
                    cell_number = int(cell_number.replace(".", ""))
                else:
                    continue

                kar_zarar_elements.append([turkish_text, cell_number])

            # Get nakit akis table elements
            nakitAkisRows = soup.find_all("tr", class_=nakitAkisPattern1) + soup.find_all(
                "tr", class_=nakitAkisPattern2
            )

            for na in nakitAkisRows:
                turkish_elements = na.find("div", class_="gwt-Label multi-language-content content-tr")

                if turkish_elements != None:
                    turkish_text = turkish_elements.get_text()
                else:
                    continue

                numbers = na.find_all("td")
                cell_number = numbers[-2].get_text()

                # Check and convert sting numbers to int
                if cell_number != "":
                    cell_number = int(cell_number.replace(".", ""))
                else:
                    continue

                nakit_akis_elements.append([turkish_text, cell_number])

            time.sleep(1)
            # Find the exact release date of FR from notification_table
            notification_table = [stripped_text.get_text() for stripped_text in soup.find_all("div", class_="text-15")]

            full_date, year, period_type = notification_table[0], notification_table[2], notification_table[3]
            full_date = full_date[:10].replace(".", "/")

            fr_release_date.append(full_date)

            # Adjust the period for dataframe column
            if period_type == "Yıllık":
                date = "12/" + year
            else:
                date = period_type[0] + "/" + year

            # Add each element to its dataframe, set column as index and remove duplicated rows
            bilanco_df = pd.DataFrame(bilanco_elements, columns=["Finansal Durum Tablosu (Bilanço)", date])
            # bilanco_df.set_index("Finansal Durum Tablosu (Bilanço)", inplace=True)
            # bilanco_df = bilanco_df[~bilanco_df.index.duplicated(keep="first")]

            karZarar_df = pd.DataFrame(kar_zarar_elements, columns=["Kar Zarar Tablosu", date])
            # karZarar_df.set_index("Kar Zarar Tablosu", inplace=True)
            # karZarar_df = karZarar_df[~karZarar_df.index.duplicated(keep="first")]

            nakitAkis_df = pd.DataFrame(nakit_akis_elements, columns=["Nakit Akış Tablosu", date])
            # nakitAkis_df.set_index("Nakit Akış Tablosu", inplace=True)
            # nakitAkis_df = nakitAkis_df[~nakitAkis_df.index.duplicated(keep="first")]

            list_of_bilanco_dfs.append(bilanco_df)
            list_of_karZarar_dfs.append(karZarar_df)
            list_of_nakitAkis_dfs.append(nakitAkis_df)

            # Compare dates to remove the previous iteration if fr got updated.
            current_date = datetime.strptime(full_date, "%d/%m/%Y")

            if len(fr_release_date) > 1:
                previous_full_date = fr_release_date[-2]
                previous_date = datetime.strptime(previous_full_date, "%d/%m/%Y")
                date_difference = abs(current_date - previous_date)

                if date_difference <= timedelta(days=10):
                    fr_release_date.pop(-2)
                    list_of_bilanco_dfs.pop(-2)
                    list_of_karZarar_dfs.pop(-2)
                    list_of_nakitAkis_dfs.pop(-2)

            # Close the FR Tab
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Kapat")]'))
                )
                driver.find_element(By.XPATH, '//button[contains(text(), "Kapat")]').click()
            except:
                print("failed to close page")

            time.sleep(1)
            # Change the selenium link to current window (list of FR's)
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(0.5)

        # Scroll to top of the page
        scroll_up = driver.execute_script("window.scrollBy(0,-1299);")
        time.sleep(1)

    # Concatanates the list of datarames
    if len(list_of_bilanco_dfs) > 3:
        final_bilanco_df = pd.concat(list_of_bilanco_dfs, axis=1, join="outer")
        final_karZarar_df = pd.concat(list_of_karZarar_dfs, axis=1, join="outer")
        final_nakit_akis_df = pd.concat(list_of_nakitAkis_dfs, axis=1, join="outer")

        # Create a dataframe for FR release date
        fr_release_date_df = pd.DataFrame({stock: fr_release_date})
        fr_release_date_df = fr_release_date_df.T

        # Export DataFrames as Excel
        final_bilanco_df.to_excel("/home/gun/Documents/Bilançolar/{}.xlsx".format(stock))
        final_karZarar_df.to_excel("/home/gun/Documents/KarZararTabloları/{}.xlsx".format(stock))
        final_nakit_akis_df.to_excel("/home/gun/Documents/NakitAkışTabloları/{}.xlsx".format(stock))
        fr_release_date_df.to_excel("/home/gun/Documents/Tarihler/{}.xlsx".format(stock), header=False)
    else:
        skipped_stocks.append(stock)

    driver.quit()
    time.sleep(2)
print(skipped_stocks)
