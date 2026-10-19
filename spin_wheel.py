from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

def spin_wheel(contestants):
    names = contestants

    options = Options()
    options.add_argument("--start-maximized")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://wheelofnames.com")

    wait = WebDriverWait(driver, 20)
    #textbox = wait.until(EC.presence_of_element_located((By.ID, "editnames")))
    textbox = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "basic-editor")))

    # js_names = "<br>".join(contestants)
    # driver.execute_script(f"arguments[0].innerHTML = `{js_names}`;", textbox)
    textbox.clear()
    textbox.send_keys("\n".join(names))

    # Click the SPIN button
    fullscreen = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Fullscreen"]')
    fullscreen.click()
    spin_button = driver.find_element(By.CSS_SELECTOR, 'canvas[aria-label="wheel"]')
    spin_button.click()

    time.sleep(15)

    winner = None
    for _ in range(45):  # max wait ~45 seconds
        try:
            winner_element = driver.find_element(By.CSS_SELECTOR, "span[data-v-8f804665]")
            winner_text = winner_element.text.strip()
            if winner_text in contestants:
                winner = winner_text
                break
        except:
            pass
        time.sleep(1)

    driver.quit()

    return winner

if __name__ == "__main__":
    winner = spin_wheel(["Alice", "Bob", "Charlie", "Dave"])
    print(winner)