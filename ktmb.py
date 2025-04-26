from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
import asyncio

async def get_train_data_0(driver):
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    date = soup.find_all(class_='dayActive')[0]['data-departdate'] #todays date, 0 is jb to singapore, 1 is singapore to jb
    x = soup.find_all(class_='bg-white depart-trips')[0]
    train_name = list(map(lambda x:x.text, x.find_all('td', class_='f20 blue-left-border')))
    departure_time = list(map(lambda x:x.text, x.find_all('td', class_='text-center f22')))
    seats_available = list(map(lambda x:x.next_sibling.lstrip(), x.find_all('i', class_='fa fa-th-large')))
    price = list(map(lambda x:x.text, x.find_all('td', class_='text-center f16')))

    return date, train_name, departure_time, seats_available, price

async def get_train_data_1(driver):
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    date = soup.find_all(class_='dayActive')[1]['data-departdate'] #todays date, 0 is jb to singapore, 1 is singapore to jb
    x = soup.find_all(class_='bg-white return-trips')[0]
    train_name = list(map(lambda x:x.text, x.find_all('td', class_='f20 yellow-left-border')))
    departure_time = list(map(lambda x:x.text, x.find_all('td', class_='text-center f22')))
    seats_available = list(map(lambda x:x.next_sibling.lstrip(), x.find_all('i', class_='fa fa-th-large')))
    price = list(map(lambda x:x.text, x.find_all('td', class_='text-center f16')))

    return date, train_name, departure_time, seats_available, price

async def get_df(driver, count):
    dfs = []
    for i in range(count):
        date, train_name, departure_time, seats_available, price = await get_train_data_0(driver)
        df = pd.DataFrame({
            'Date': date,
            'Shuttle': train_name,
            'Time': departure_time,
            'Availability': seats_available,
            'Price': price
        })
        # Append to list of DataFrames
        dfs.append(df)
        driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/table/thead/tr/th[5]').click()
        await asyncio.sleep(2)
    await asyncio.sleep(2)
    for j in range(count):   
        date, train_name, departure_time, seats_available, price = await get_train_data_1(driver)
        df = pd.DataFrame({
            'Date': date,
            'Shuttle': train_name,
            'Time': departure_time,
            'Availability': seats_available,
            'Price': price
        })
        # Append to list of DataFrames
        dfs.append(df)
        
        driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/table/thead/tr/th[5]').click()
        await asyncio.sleep(2)
    combined_df = pd.concat(dfs, ignore_index=True)
    dir_path = r'combined_data'
    combined_df.to_csv(os.path.join(dir_path, 'train_data.csv'), index=False)
    return combined_df

async def main():
    url = "https://shuttleonline.ktmb.com.my/Home/Shuttle"
    date_value = datetime.now().strftime('%d %b %Y')  # Example date in YYYY-MM-DD format, select date
    count = 3

    chrome_options = Options()
    #chrome_options.add_experimental_option("detach", True)
    #chrome_options.add_argument("--headless=new") 

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get(url)
    assert "Welcome" in driver.title
    driver.execute_script("document.getElementById('OnwardDate').value = arguments[0];", date_value)
    driver.execute_script("document.getElementById('ReturnDate').value = arguments[0];", date_value)
    driver.find_element(By.ID, 'btnSubmit').click()
    await asyncio.sleep(2)

    combined_df = await get_df(driver, count)
    driver.quit()
    return combined_df

if __name__ == '__main__':
    asyncio.run(main())