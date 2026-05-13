# Campus Nutrition Research Project

An automated tool to identify nutritional gaps in daily campus dining menus using Python. This project utilizes web scraping and data analysis to track the availability of fresh produce and protein options within university dining facilities.

## Features
- **Automated Menu Extraction**: Uses Selenium to navigate the Pride Cafe menu, bypassing modern web obstacles like email reward popups and cookie consent banners.
- **Robust Data Parsing**: Leverages BeautifulSoup to extract structured nutritional data, including item names, descriptions, calorie counts, and dietary labels (e.g., Vegan, Vegetarian, Gluten-Free).
- **Dynamic Content Handling**: Implements incremental scrolling and explicit waits to ensure lazy-loaded menu items are fully rendered before extraction.
- **Error Diagnostics**: Automatically generates headless browser screenshots (error_debug.png) to troubleshoot layout changes or timeout exceptions.

## Technical Stack
- **Language**: Python
- **Libraries**: Pandas, BeautifulSoup4, Selenium
- **Driver Management**: WebDriver Manager for automated Chrome binary configuration
- **Environment**: Conda virtual environment within VS Code

## Getting Started

### Prerequisites
Ensure you have Python installed and the necessary dependencies:
pip install pandas beautifulsoup4 selenium webdriver-manager

### Usage
1. Run the scraper or mock data to generate the daily dataset:
   python scraper.py or python generate_mock_data.py
2. The script will output a file named campus_menu.csv containing the scraped data.
3. Open analysis.ipynb to view the nutritional gap trends and data visualizations.

## Ethical Standards
This scraper is designed with respect for the host website's resources:
- **Rate Limiting**: Includes strategic time.sleep() calls to prevent server strain.
- **Headless Execution**: Runs in the background to minimize resource consumption.
- **Manual Verification**: Compliance with robots.txt guidelines has been manually verified for this academic research project.

## Current Research Goals
The primary objective of this project is to analyze "Campus Nutritional Accessibility" by:
- Scraping and analyzing daily menus for nutritional consistency.
- Tracking the daily availability of fresh produce versus processed options.
- Identifying protein gaps for students with specific dietary restrictions.