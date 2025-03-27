from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.common.exceptions import TimeoutException

# Configure your target website
BASE_URL = "https://example.com/directory"

# Set up WebDriver
driver = webdriver.Chrome()

# Navigate to the directory page
driver.get(BASE_URL)

# Wait until the directory content loads
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "directory-entry")]'))
)

# Initialize data storage
all_data = []

while True:
    # Find all directory entries on the page
    entries = driver.find_elements(By.XPATH, '//div[contains(@class, "directory-entry")]')

    for entry in entries:
        try:
            # Extract contact details
            name = entry.find_element(By.XPATH, './/h3').text
            company = entry.find_element(By.XPATH, './/p[contains(@class, "company-name")]').text
            email = entry.find_element(By.XPATH, './/a[contains(@href, "mailto:")]').text
            phone = entry.find_element(By.XPATH, './/p[contains(@class, "phone-number")]').text

            # Save the extracted data
            all_data.append({
                "Name": name,
                "Company": company,
                "Email": email,
                "Phone": phone
            })

        except Exception as e:
            print(f"Error extracting entry: {e}")
            continue

    # Check for pagination and click "Next" if available
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@aria-label="Next page"]'))
        )
        next_button.click()
    except TimeoutException:
        print("No more pages. Ending scrape.")
        break

# Export scraped data to Excel
df = pd.DataFrame(all_data)
df.to_excel('sales_leads.xlsx', index=False)
print("Data successfully exported to Excel!")

# Close the browser
driver.quit()