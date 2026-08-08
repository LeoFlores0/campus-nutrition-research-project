# Campus Menu Nutrition Scraper & Analyzer

## Project Overview
This project is an automated data pipeline that extracts, processes, and analyzes nutritional data from a campus dining portal. Built with Python, it utilizes headless browser automation to navigate dynamically rendered React components, parses complex HTML modals to extract specific macronutrients, and compiles the data for deep dietary analysis. 

The resulting dataset is evaluated against federal Acceptable Macronutrient Distribution Ranges (AMDR) and Daily Value benchmarks to assess the overall nutritional balance of campus dining options.

## Technical Stack
* **Web Automation:** Selenium, Webdriver Manager
* **HTML Parsing:** BeautifulSoup4 (bs4), Regular Expressions (re)
* **Data Manipulation:** Pandas, NumPy
* **Data Visualization & Stats:** Matplotlib, Seaborn, SciPy

## Key Features
* **Dynamic Web Scraping:** Engineered a headless Selenium WebDriver with stability flags to bypass cookie banners, interact with sticky headers, and navigate a monthly calendar view.
* **Robust Data Parsing:** Built an extraction function using BeautifulSoup to parse nested key-value HTML structures inside dynamically loaded modals, capturing exact values for calories, proteins, carbohydrates, fats, sodium, fiber, and added sugars.
* **Data Cleaning & Coercion:** Implemented Regex to clean raw fractional descriptors (e.g., "less than 1 g") and safely cast scraped strings to numeric floats.
* **Nutritional Analytics Pipeline:** Analyzed a dataset of 370 menu items to calculate macronutrient distribution.
* **Federal Guideline Auditing:** Automated the evaluation of menu items against 1/3 Daily Value safety thresholds for nutrients like Sodium and Saturated Fat, generating an aggregate compliance summary.

## Impact & Insights
By automating the collection of hundreds of data points across multiple months and meal times (Breakfast, Lunch, Dinner), this tool enables a data-driven approach to campus health.

*Key findings from the analysis environment:*
* Automatically calculates total caloric contributions per macronutrient across the global menu pool.
* Identifies statistical deviations, highlighting that dietary fiber and protein mass run at a deficit for the majority of items when compared to benchmark standards.
* Pinpoints exact counts of individual menu items actively breaching federal ceiling limits for sodium and added sugars.

## To Use

### Install Dependencies
Ensure you have Python 3.8+ installed, then run:
```bash
pip install -r requirements.txt
``` 
### Run
Run scraper.py followed by analysis.ipynb.

Note: generate_mock_data.py followed by analysis.ipynb will not work.
Mock data was created for hypothetical testing and remains for eductional purposes.