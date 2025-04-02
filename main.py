from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import config
import time
import pandas as pd
import shutil
import os

# Configure Chrome to remain open
chrome_options = webdriver.ChromeOptions()
profile_path = "/Users/rad_it/Library/Application Support/Google/Chrome"
chrome_options.add_argument(f"--user-data-dir={profile_path}")  
chrome_options.add_argument("--profile-directory=Default")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("detach", True)
browser = webdriver.Chrome(options=chrome_options)

print("Opening Wufoo and Extracting Students Info")
browser.get(config.WUFOO_LOGIN_URL)  

wait = WebDriverWait(browser, 10)

def login():
    print("Trying to login.")

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

    time.sleep(5)

login()

while True:
    try:
        print("Checking if login was successful.")
        error_text = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#loginBlock > p.error")))
        print("Error loging in. Retrying.")
        time.sleep(5)
        login()
    except Exception:
        print("Login Successful. Proceeding to next step.")
        break

print("Checking for modal popup...")

# Step 4: Check if modal exists and close it
try:
    close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Close Modal']")))
    print("Modal detected. Closing it...")
    close_button.click()
except:
    print("No modal found.")
print("Proceeding with next steps.")

# Step 5: Accept terms and conditions
try:
    time.sleep(3)
    accept_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#onetrust-accept-btn-handler")))
    accept_button.click()
    time.sleep(1)
except Exception:
    print("Terms pop up not present. Moving to next step.")

# Step 6: Search for rule
print("Checking if there is some content in the search bar.")
try:
    search_bar_close = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#search-query-delete")))
    search_bar_close.click()
except Exception:
    print("No content in searchbar. Proceeding with next steps.")
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
        while not element.is_selected():
            print("Element was not clicked, clicking again...")
            # Attempt to click the checkbox
            element.click()

            # Retry clicking if the checkbox is not selected
            time.sleep(3)  # Small delay to allow UI to update

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
    print("Today's entries must be downloaded.")

except Exception:
    print("No Entries Today or Some Issue Occured!")

print("Moving downloaded file to the root folder.")
time.sleep(3)
try:
    shutil.move(config.WUFOO_SOURCE_PATH, config.WUFOO_DST_PATH)
except Exception:
    print("Error occured while moving file to root folder! Please retry.")

# Step 8: Login into Adobe
browser.get(config.ADOBE_URL)

# Step 9: Perform Auth
try:
    sign_in_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#unav-profile > div > button")))
    sign_in_button.click()
    continue_with_google = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#SocialButtons-Container > section:nth-child(1) > a:nth-child(1)")))
    continue_with_google.click()
    time.sleep(3)
    email_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#identifierId")))
    email_input.send_keys(config.EMAIL)
    continue_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#identifierNext > div > button")))
    continue_button.click()
    time.sleep(3)
    usc_id_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#netid")))
    usc_id_input.send_keys(config.USC_ID)
    usc_pwd_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#password")))
    usc_pwd_input.send_keys(config.USC_PWD)
    submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#signInBtn")))
    submit_button.click()
    time.sleep(3)
    roski_land_line_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div > div > div.card.card--white-label.uses-white-label-border-color.display-flex.flex-direction-column > div > div.all-auth-methods.display-flex.flex-value-one > ul > li:nth-child(3) > a")))
    roski_land_line_option.click()
    time.sleep(5)
    continue_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#view_container > div > div > div:nth-child(2) > div > div:nth-child(2) > div > div:nth-child(1)")))
    continue_button.click()
except:
    print("Either already logged in or login attempt failed! Please check browser.")

# Step 9: Go to admin console
profile = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#unav-profile")))
profile.click()
time.sleep(3)
try:
    main = browser.find_element(By.CSS_SELECTOR, "#unav-profile > account-menu-trigger")
    main_sr = main.shadow_root
    acc_tooltip = main_sr.find_element(By.CSS_SELECTOR, "account-tooltip")
    pandora = acc_tooltip.find_element(By.CSS_SELECTOR, "#profile-dropdown-id > pandora-react-mini-app-account-menu")
    pandora_sr = pandora.shadow_root
    admin_console_link = pandora_sr.find_elements(By.CLASS_NAME, "spectrum-Link--primary")[1]
    print(admin_console_link)
    browser.execute_script("arguments[0].click();", admin_console_link)
except Exception as e:
    print("Failed to click on 'Go to Admin Console'. Error:", str(e))
time.sleep(5)
browser.switch_to.window(browser.window_handles[1])

# Step 10: Go to user tab
try:
    modal_popup = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div.vex.vex-theme-os.apt-vex.apt-popup-disable-overlay > div.vex-content.apt-guide-popup.guide-initial-position.apt-popup-content-disable-overlay.px-engagement-wrapper-guide.px-engagement-wrapper > div.vex-close.aptr-engagement-close-btn.px-close-button.aptr-step-close-button-d2bc9d05-c553-4dd3-8d3c-e94822cb8823")))
    modal_popup.click()
except Exception as e:
    print("No Modal to click", str(e))

users_nav_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='nav-item-users']")))
users_nav_link.click()

# Step 11: Read through new entries
access_df = pd.read_csv("./adobe-creative-cloud-access-spring-2025_entries.csv")
access_df = access_df.drop_duplicates()
access_df = access_df[access_df["Please Select the Option that Applies to You"] != "Roski - Major"]
access_df = access_df[access_df["Please Select the Option that Applies to You.3"] != "Roski - MFA"]
filtered_list = access_df[access_df["Please Select the Option that Applies to You.4"] != "Roski - MA"].to_dict(orient="records")

# Step 12: Assign License.
email_filter_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='table-filters-search-field']")))
select_all_cb = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Select All']")))
email_list = []
for obj in filtered_list:
    email = obj["USC Email Address"]
    print("Checking if the license is already assigned to the email - " + email)
    email_filter_input.send_keys(email)
    email_filter_input.send_keys(Keys.RETURN)
    time.sleep(2)
    if(not select_all_cb.is_enabled()):
        print("Email not present, adding the email " + email + " to the list.")
        email_list.append({"firstName": obj["Name"], "lastName": obj["Last"], "email": email})
    else:
        print("Licence already assigned to the email.")
    clear_filter = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Clear search']")))
    clear_filter.click()

print("Assigning Licences...")
for obj in email_list:
    first_name = obj["firstName"]
    last_name = obj["lastName"]
    email = obj["email"]
    add_user_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='add-users-btn']")))
    add_user_btn.click()
    time.sleep(2)
    email_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='user-picker']")))
    email_input.send_keys(email)
    time.sleep(5)
    email_input.send_keys(Keys.DOWN)
    email_input.send_keys(Keys.ENTER)
    first_name_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='first-name-field']")))
    first_name_input.send_keys(first_name)
    last_name_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='last-name-field']")))
    last_name_input.send_keys(last_name)
    all_groups = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid='assignment-modal-open-button']")))
    all_groups[1].click()
    time.sleep(2)
    search_bar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='user-group-search']")))
    search_bar.send_keys("Roski Minors & Non Roski Students")
    search_bar.send_keys(Keys.ENTER)
    time.sleep(5)
    checkbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[aria-label='Roski Minors & Non Roski Students'] input[aria-label='Select'][type='checkbox']")))
    checkbox.click()
    time.sleep(1)
    apply_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "section[data-testid='user-group-assignment-modal'] button[data-testid='cta-button']")))
    apply_button.click()
    # save_button= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='cta-button']")))

input("Press Enter to close the Program:")
if os.path.exists(config.WUFOO_DST_PATH):
    os.remove(config.WUFOO_DST_PATH)
    print(f"File has been deleted")
browser.quit()
