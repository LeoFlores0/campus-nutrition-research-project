import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

URL = "https://widener.mydininghub.com/en/location/pride-cafe"

def scrape_menu_with_selenium():
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get(URL)
        
        print("Page opened, checking for popups...")
        time.sleep(6) 
        
        try:
            from selenium.webdriver.common.keys import Keys
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
            print("Popup dismissed via Escape Key!")
        except:
            print("No popup detected, proceeding...")
        try:
            print("Checking for cookie banners...")
            cookie_xpath = "//button[contains(text(), 'Accept')] | //button[contains(@class, 'cookie')] | //button[id='onetrust-accept-btn-handler']"
            cookie_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, cookie_xpath))
            )
            cookie_button.click()
            print("Cookies accepted!")
            time.sleep(2)
        except:
            print("No cookie banner found or it's not blocking the view. Proceeding...")

        print("Scrolling to find the menu...")
        for i in range(3):
            driver.execute_script(f"window.scrollBy(0, 800);")
            time.sleep(1)
        
        driver.save_screenshot("menu_check.png")

        print("Looking for meal items...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "row-span-2"))
        )
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        menu_data = []
        meals = soup.find_all('li', class_='row-span-2')

        for meal in meals:
            name = meal.find('h4').get_text(strip=True) if meal.find('h4') else "N/A"
            
            desc = meal.find('p', class_='text-type-secondary').get_text(strip=True) if meal.find('p') else ""
            
            calories = "N/A"
            for s in meal.find_all('span'):
                if 'Calories' in s.text:
                    calories = s.text.replace('Calories', '').strip()
            
            labels = [span.get_text(strip=True) for span in meal.find_all('span', class_='text-2xs')]

            menu_data.append({
                "item": name,
                "description": desc,
                "calories": calories,
                "labels": ", ".join(labels)
            })
            
        return pd.DataFrame(menu_data)

    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        driver.save_screenshot("error_debug.png")
        return pd.DataFrame()

    finally:
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    df = scrape_menu_with_selenium()
    if not df.empty:
        print("Success! Data preview:")
        print(df.head())
        df.to_csv("campus_menu.csv", index=False)
    else:
        print("Scraper finished but no data was collected.")