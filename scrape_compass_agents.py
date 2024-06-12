from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup WebDriver
driver_path = 'chromedriver'
driver = webdriver.Chrome(executable_path=driver_path)
driver.get("https://www.compass.com/agents/locations/miami-fl/35648/")

li_agents = []


# Function to extract agent info
def extract_agent_info():
    agents = driver.find_elements(By.CSS_SELECTOR, ".agentCard")
    for agent in agents:
        try:
            name = agent.find_element(By.CSS_SELECTOR, ".agentCard-name").text
            email = agent.find_element(
                By.CSS_SELECTOR,
                ".agentCard-email").get_attribute("href").replace(
                    "mailto:", "")
            phone = agent.find_element(By.CSS_SELECTOR,
                                       ".agentCard-phone").text
            print(f"Name: {name}, Email: {email}, Phone: {phone}")
            li_agents.append({"name": name, "email": email, "phone": phone})
        except Exception as e:
            print(f"Error extracting agent data: {e}")
    print(len(li_agents))


# Loop to navigate through pagination
while True:
    extract_agent_info()
    try:
        # Wait until the element is present
        next_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/main/div/div/nav/button[9]')))
        if "disabled" in next_button.get_attribute("class"):
            break
        else:
            next_button.click()
            time.sleep(2)  # Wait for the page to load
    except Exception as e:
        print(f"Error navigating pages: {e}")
        break

# Close the driver
driver.quit()
