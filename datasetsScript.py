from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

base_url = "https://od.data.gov.sa/Data/en/dataset"
page_count = 369
output_file_path = "/Users/dinaalromih/Desktop/dataset_info.txt"

# Initialize the WebDriver (make sure to have the appropriate driver installed)
driver = webdriver.Chrome()

with open(output_file_path, 'w') as file:
    for page_number in range(1, page_count + 1):
        url = f"{base_url}?page={page_number}"
        driver.get(url)

        dataset_links = driver.find_elements(By.XPATH, '//h3[@class="mb-0"]/a')
        dataset_urls = [link.get_attribute('href') for link in dataset_links]

        for dataset_url in dataset_urls:
            try:
                driver.get(dataset_url)

                # Check if the menu button is present within the specified timeout
                try:
                    menu_button = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, '//i[@class="ti ti-dots icon"]'))
                    )

                    # Scroll into view using JavaScript
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", menu_button)

                    # Perform a click using JavaScript
                    driver.execute_script("arguments[0].click();", menu_button)

                    # Click on the "Preview" button
                    preview_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//a[contains(@class, "dropdown-item") and contains(.,"Preview")]'))
                    )
                    driver.execute_script("arguments[0].click();", preview_button)

                    # Switch to the iframe
                    iframe = WebDriverWait(driver, 10).until(
                        EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME, 'iframe-view'))
                    )

                    # Get the records number
                    records_number = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//span[@class="doc-count"]'))
                    ).text

                    # Switch back to the default content
                    driver.switch_to.default_content()

                    # Write the information to the file
                    info_to_save = f"Page {page_number}, Dataset URL: {dataset_url}, Records Number: {records_number}\n"
                    file.write(info_to_save)
                    print(f"Page {page_number}, Dataset URL: {dataset_url}, Records Number: {records_number}")

                except TimeoutException:
                    # If the menu button or preview button is not found, write the dataset information without specifying the file type
                    info_to_save = f"Page {page_number}, Dataset URL: {dataset_url}\n"
                    file.write(info_to_save)
                    print(f"Page {page_number}, Dataset URL: {dataset_url}, Records Number: Undefined")

            except (NoSuchElementException, StaleElementReferenceException):
                print(f"Dataset details not found or stale reference for page {page_number}. Skipping...")

            driver.get(url)

# Close the WebDriver
driver.quit()
