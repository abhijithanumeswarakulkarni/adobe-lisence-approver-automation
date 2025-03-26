from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config
import time

# Configure Chrome to remain open
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

browser = webdriver.Chrome(options=chrome_options)

print("Opening Wufoo and Extracting Students Info")
browser.get(config.WUFOO_LOGIN_URL)  

wait = WebDriverWait(browser, 10)

# Step 1: Enter Email
print("Filling in Email...")
email_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#emailInput")))
email_input.send_keys(config.EMAIL)

# Step 2: Enter Password
print("Filling in Password...")
pwd_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#passwordLogin")))
pwd_input.send_keys(config.PASSWORD)

# Step 3: Click Submit
print("Clicking Submit...")
submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#saveForm")))
submit.click()

print("Login Attempted. Checking for modal popup...")

# Step 4: Check if modal exists and close it
try:
    close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Close Modal']")))
    print("Modal detected. Closing it...")
    close_button.click()
except:
    print("No modal found. Continuing...")

print("Proceeding with next steps.")

# Step 5: Accept terms and conditions
time.sleep(3)
accept_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#onetrust-accept-btn-handler")))
accept_button.click()
time.sleep(1)

# Step 6: Search for rule
search_bar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#search-bar")))
search_bar.send_keys(config.SEARCH_BAR_INPUT)
search_icon = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#search-query-icon")))
search_icon.click()

# Step 7: Check for today's entries
entry_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#forms-action-entries-adobe-creative-cloud-access-spring-2025")))
entry_button.click()

try:
    # Ensure checkbox is visible before interacting
    select_all_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#table-select-all")))

    # Function to click and retry if checkbox is unchecked
    def click_with_retry(element):
        # Attempt to click the checkbox
        element.click()

        # Retry clicking if the checkbox is not selected
        time.sleep(1)  # Small delay to allow UI to update
        if not element.is_selected():
            print("Element was not clicked, clicking again...")
            element.click()  # Retry clicking

        # Confirm element is selected
        print(f"Element checked status: {element.is_selected()}")

    # Click the checkbox and retry if necessary
    click_with_retry(select_all_button)

    # Click Download
    download_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#entries-bulk-download")))
    download_button.click()

    time.sleep(3)

    # Wait for the download options container
    download_options = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".download-options")))

    # Click the second button (Excel)
    excel_button = download_options.find_element(By.CSS_SELECTOR, "button:nth-child(1)")
    excel_button.click()
    print("Today's entries must be downloaded. Check the downloads folder.")

except Exception as e:
    print("No Entries Today or Issue Found!")
    print("Error:", str(e))  # Debugging to check the real issue

input("Press Enter to close the Program:")
browser.quit()
