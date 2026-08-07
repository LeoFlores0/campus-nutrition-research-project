import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://widener.mydininghub.com/en/location/pride-cafe"

def scrape_menu_with_selenium():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), 
        options=chrome_options
    )
    
    try:
        driver.get(URL)
        print("Page opened, waiting for core content...")

        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
            print("Sent ESC key to clear modals.")
        except Exception:
            pass

        try:
            cookie_xpath = (
                "//button[contains(text(), 'Accept')] | "
                "//button[contains(@class, 'cookie')] | "
                "//button[@id='onetrust-accept-btn-handler']"
            )
            cookie_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, cookie_xpath))
            )
            cookie_button.click()
            print("Cookies accepted!")
        except Exception:
            print("No blocking cookie banner found.")

        for _ in range(3):
            driver.execute_script("window.scrollBy(0, 600);")
            time.sleep(0.5)

        print("Waiting for menu elements to render...")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "row-span-2"))
        )

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        menu_data = []
        meals = soup.find_all('li', class_='row-span-2')

        for meal in meals:
            name = meal.find('h4').get_text(strip=True) if meal.find('h4') else "N/A"
            
            desc_elem = meal.find('p', class_='text-type-secondary')
            desc = desc_elem.get_text(strip=True) if desc_elem else ""
            
            calories = "N/A"
            for s in meal.find_all('span'):
                text = s.text.strip()
                if 'cal' in text.lower():
                    calories = text.replace('Calories', '').replace('cal', '').strip()
                    break
            
            labels = [
                span.get_text(strip=True) 
                for span in meal.find_all('span', class_='text-2xs')
            ]

            menu_data.append({
                "item_name": name,
                "description": desc,
                "calories": calories,
                "dietary_label": ", ".join(labels)
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
        print(f"Success! Extracted {len(df)} items.")
        print(df.head())
        df.to_csv("campus_menu.csv", index=False)
    else:
        print("Scraper finished, but no data was collected. Check 'error_debug.png'.")