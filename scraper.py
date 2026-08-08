"""
Campus Menu Nutrition Scraper

This script automates the extraction of nutritional data from a campus dining portal.
It utilizes Selenium for web automation and interaction with dynamically rendered 
React components, and BeautifulSoup for HTML parsing. The extracted data is 
compiled into a pandas DataFrame and exported to a CSV file.

Dependencies:
    - time, re
    - pandas
    - bs4 (BeautifulSoup)
    - selenium
    - webdriver_manager
"""

import time
import re
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

def init_driver():
    """
    Initializes and returns a headless Chrome WebDriver with stability flags.

    Returns:
        webdriver.Chrome: A configured instance of the Chrome WebDriver.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), 
        options=chrome_options
    )

def dismiss_popups(driver):
    """
    Dismisses initial cookie banners or modal overlays upon page load.

    Args:
        driver (webdriver.Chrome): The active WebDriver instance.
    """
    try:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
    except Exception:
        pass

    try:
        cookie_xpath = (
            "//button[contains(text(), 'Accept')] | "
            "//button[contains(@class, 'cookie')] | "
            "//button[@id='onetrust-accept-btn-handler']"
        )
        cookie_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, cookie_xpath))
        )
        cookie_btn.click()
        time.sleep(1)
        print("[+] Cookie banner dismissed.")
    except Exception:
        pass

def select_monthly_view(driver):
    """
    Clicks the 'View' dropdown button and selects the 'Monthly' view option.

    Args:
        driver (webdriver.Chrome): The active WebDriver instance.

    Returns:
        bool: True if the monthly view was successfully selected, False otherwise.
    """
    try:
        print("Locating and clicking the 'View' dropdown...")
        
        # Ensure the filter toolbar is in view
        driver.execute_script("window.scrollTo(0, 350);")
        time.sleep(1.0)

        # Use presence_of_element_located and contains(., 'View:') to handle nested HTML nodes safely
        view_dropdown_xpath = "//button[@data-testid='selectButton'][contains(., 'View:')]"
        view_btn = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, view_dropdown_xpath))
        )
        
        # Scroll into view and execute JavaScript click to bypass sticky headers
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", view_btn)
        time.sleep(1.0)
        driver.execute_script("arguments[0].click();", view_btn)
        print("[+] Clicked 'View' dropdown successfully.")
        
        # Wait for the listbox container to render in the DOM
        dropdown_list_xpath = "//ul[@role='listbox']"
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, dropdown_list_xpath))
        )

        # Locate the 'Monthly' option using its exact ID
        monthly_option_xpath = "//button[@id='monthly-option']"
        monthly_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, monthly_option_xpath))
        )
        
        # Click the Monthly option directly via JavaScript
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", monthly_btn)
        driver.execute_script("arguments[0].click();", monthly_btn)
        
        time.sleep(4.0)  
        print("Successfully selected 'Monthly' view.")
        return True

    except Exception as e:
        print(f"Error selecting Monthly view: {e}")
        driver.save_screenshot("monthly_view_error.png")
        return False


def select_meal_option(driver, meal_name):
    """
    Selects specified meal option (Breakfast, Lunch, Dinner) from the Meal dropdown menu.

    Args:
        driver (webdriver.Chrome): The active WebDriver instance.
        meal_name (str): The target meal to select (e.g., 'Breakfast', 'Lunch').

    Returns:
        bool: True if the meal option was successfully changed, False otherwise.
    """
    try:
        print(f"Switching meal option to '{meal_name}'...")
        
        # Open Meal dropdown button safely using contains(., 'Meal:')
        meal_dropdown_xpath = "//button[@data-testid='selectButton'][contains(., 'Meal:')]"
        meal_dropdown_btn = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, meal_dropdown_xpath))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", meal_dropdown_btn)
        time.sleep(1.0)
        driver.execute_script("arguments[0].click();", meal_dropdown_btn)
        time.sleep(1.5)

        # Click target meal option globally searching for its role and text
        meal_option_xpath = f"//button[@role='option'][contains(., '{meal_name}')]"
        meal_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, meal_option_xpath))
        )
        driver.execute_script("arguments[0].click();", meal_option)
        
        time.sleep(4.0)  
        print(f"Meal option successfully changed to '{meal_name}'.")
        return True

    except Exception as e:
        print(f"Error selecting meal option '{meal_name}': {e}")
        return False

def advance_to_next_month(driver):
    """
    Clicks the 'Next Month' arrow button if it is clickable.

    Args:
        driver (webdriver.Chrome): The active WebDriver instance.

    Returns:
        bool: True if advanced to the next month successfully, False if disabled or error occurs.
    """
    try:
        next_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Next Month' or @title='Next Month']"))
        )
        
        # Check if button is disabled
        is_disabled = (
            next_btn.get_attribute("disabled") is not None or
            next_btn.get_attribute("aria-disabled") == "true" or
            "cursor-not-allowed" in (next_btn.get_attribute("class") or "")
        )

        if is_disabled:
            print("'Next Month' button is disabled. Reached the end of available months.")
            return False

        next_btn.click()
        time.sleep(4.0)  
        print("Advanced to the next month.")
        return True
    except Exception as e:
        print(f"Error could not advance to next month: {e}")
        return False

def get_current_month_year(driver):
    """
    Gets the header text for the current month and year view.

    Args:
        driver (webdriver.Chrome): The active WebDriver instance.

    Returns:
        str: The extracted month and year text (e.g., 'August 2026'), or an empty string if not found.
    """
    try:
        header_elem = driver.find_element(By.XPATH, "//h2[contains(@class, 'text-heading')]")
        return header_elem.text.strip()
    except Exception:
        return ""

def parse_nutrient_value(text):
    """
    Extracts numeric values from raw nutrition text. Handles standard integers 
    and fractional descriptors (e.g. '320 mg' -> 320.0, 'less than 1 g' -> 0.5).

    Args:
        text (str): The raw text string containing the nutrient value.

    Returns:
        float or None: The parsed numeric value as a float. Returns 0.0 if a match fails, 
        and None if the input text is empty.
    """
    if not text:
        return None
    if "less than 1" in text.lower():
        return 0.5
    match = re.search(r'([\d\.]+)', text)
    if match:
        return float(match.group(1))
    return 0.0

def extract_item_nutrition(driver):
    """
    Parses the open nutrition drawer modal for nutrient values utilizing BeautifulSoup.

    Args:
        driver (webdriver.Chrome): The active WebDriver instance containing the open modal.

    Returns:
        dict: A dictionary containing extracted nutritional data keys and their 
        corresponding numeric float values. Keys include calories, protein_g, 
        carbs_g, fat_g, saturated_fat_g, sodium_mg, fiber_g, and added_sugars_g.
    """
    nutrition_data = {
        "calories": None,
        "protein_g": None,
        "carbs_g": None,
        "fat_g": None,
        "saturated_fat_g": None,
        "sodium_mg": None,
        "fiber_g": None,
        "added_sugars_g": None,
    }

    try:
        # Wait for drawer contents to fully render
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Nutritional Information') or contains(text(), 'Amount Per Serving')]"))
        )
        time.sleep(2.0)  

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Parse key-value pairs from dl/dt/dd structures inside drawer
        for dl in soup.find_all("dl"):
            dt = dl.find("dt")
            dd = dl.find("dd")
            if not dt or not dd:
                continue

            label = dt.get_text(strip=True).lower()
            val_text = dd.get_text(strip=True)
            val = parse_nutrient_value(val_text)

            if "calories" in label:
                nutrition_data["calories"] = val
            elif "protein" in label:
                nutrition_data["protein_g"] = val
            elif "total carbohydrate" in label or "carbohydrate" in label:
                nutrition_data["carbs_g"] = val
            elif "total fat" in label or label == "fat":
                nutrition_data["fat_g"] = val
            elif "saturated fat" in label:
                nutrition_data["saturated_fat_g"] = val
            elif "sodium" in label:
                nutrition_data["sodium_mg"] = val
            elif "dietary fiber" in label or "fiber" in label:
                nutrition_data["fiber_g"] = val
            elif "added sugar" in label or "total sugar" in label:
                nutrition_data["added_sugars_g"] = val

    except Exception as e:
        print(f"Error extracting nutrition modal: {e}")

    finally:
        # Close the item drawer
        try:
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
            time.sleep(1.0)
        except Exception:
            pass

    return nutrition_data

def scrape_campus_menu(target_months=3):
    """
    Main execution function to scrape campus menu data across specified meals and months.
    Iterates through Breakfast, Lunch, and Dinner options, processing all available item
    cards per month.

    Args:
        target_months (int, optional): The maximum number of months to scrape. Defaults to 3.

    Returns:
        pd.DataFrame: A pandas DataFrame containing all scraped menu items and their 
        associated nutritional information.
    """
    driver = init_driver()
    menu_data = []
    target_meals = ["Breakfast", "Lunch", "Dinner"]

    try:
        print(f"Navigating to {URL}...")
        driver.get(URL)
        time.sleep(5)  
        dismiss_popups(driver)

        # Switch View to Monthly
        if not select_monthly_view(driver):
            print("Failed to switch to Monthly view. Exiting.")
            return pd.DataFrame()

        # Iterate through target months (up to target_months)
        for month_idx in range(1, target_months + 1):
            month_year_str = get_current_month_year(driver)
            print(f"\n--- SCRAPING MONTH {month_idx}/{target_months}: {month_year_str} ---")

            # Iterate through Meal Options: Breakfast, Lunch, Dinner
            for meal in target_meals:
                print(f"\n--- Processing Meal Option: {meal} ---")
                
                # If it fails to switch, skip scraping to prevent duplicate/wrong data
                if not select_meal_option(driver, meal):
                    print(f"Skipping {meal} due to selection error. Moving to next...")
                    continue

                # Find all day cells/columns in monthly table
                day_cells = driver.find_elements(By.XPATH, "//td[contains(@class, 'border')]")
                print(f"Found {len(day_cells)} calendar day cells.")

                for cell in day_cells:
                    # Get Day/Date text for cell (e.g., 'Tue 08/18')
                    try:
                        date_header = cell.find_element(By.XPATH, ".//h3").text.strip()
                    except Exception:
                        date_header = ""

                    full_date = f"{date_header} ({month_year_str})".strip() if date_header else month_year_str

                    # Find all food item buttons in cell
                    item_buttons = cell.find_elements(By.XPATH, ".//ul//li//button")
                    for btn in item_buttons:
                        try:
                            # Extract Item Name
                            item_name = btn.find_element(By.XPATH, ".//p[contains(@class, 'font-semibold')]").text.strip()
                            if not item_name:
                                continue

                            # Scroll into view and click item
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                            time.sleep(0.5)
                            btn.click()

                            # Extract nutrition details
                            nutrition = extract_item_nutrition(driver)

                            # Record row
                            row = {
                                "date": full_date,
                                "meal_option": meal,
                                "item_name": item_name,
                                "calories": nutrition["calories"],
                                "protein_g": nutrition["protein_g"],
                                "carbs_g": nutrition["carbs_g"],
                                "fat_g": nutrition["fat_g"],
                                "saturated_fat_g": nutrition["saturated_fat_g"],
                                "sodium_mg": nutrition["sodium_mg"],
                                "fiber_g": nutrition["fiber_g"],
                                "added_sugars_g": nutrition["added_sugars_g"],
                            }
                            menu_data.append(row)

                        except Exception as item_err:
                            # Keep item-level errors quiet unless to debug specific broken cards
                            # print(f"Error processing item card: {item_err}")
                            
                            # Ensure modal is closed if open
                            try:
                                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                                time.sleep(1.0)
                            except Exception:
                                pass

            # Advance to Next Month
            if month_idx < target_months:
                if not advance_to_next_month(driver):
                    print("No more months available to advance. Stopping month iteration.")
                    break

        df = pd.DataFrame(menu_data)
        return df

    except Exception as e:
        print(f"[-] Execution error: {e}")
        driver.save_screenshot("error_debug.png")
        return pd.DataFrame(menu_data)

    finally:
        print("\n[+] Closing browser session...")
        driver.quit()

if __name__ == "__main__":
    df = scrape_campus_menu(target_months=3)
    if not df.empty:
        print(f"\n[Success] Scraped {len(df)} total items across all target meal options and months.")
        print(df.head())
        df.to_csv("campus_menu_nutrition.csv", index=False)
        print("[+] Output saved to 'campus_menu_nutrition.csv'")
    else:
        print("[-] No data extracted.")