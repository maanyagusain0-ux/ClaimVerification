from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def extract_product_details(driver, product_url):

    driver.get(product_url)

    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (By.TAG_NAME, "body")
            )
        )
    except:
        print("Page Load Timeout")

    # Reduced wait
    time.sleep(0.1)

    try:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight * 0.7);"
        )
    except:
        pass

    time.sleep(0.1)

    try:
        page_text = driver.execute_script(
            "return document.body.innerText;"
        )
    except:
        page_text = ""

    # -------------------------
    # Product Title
    # -------------------------

    title_text = ""

    try:
        title_text = driver.title
    except:
        title_text = ""

    # -------------------------
    # Extract Fit & Fabric
    # -------------------------

    fit_text = ""
    fabric_text = ""

    lower_text = page_text.lower()

    fit_pos = lower_text.find("size & fit")

    if fit_pos != -1:

        fit_text = page_text[
            fit_pos:
            fit_pos + 500
        ]

    fabric_pos = lower_text.find(
        "material & care"
    )

    if fabric_pos != -1:

        fabric_text = page_text[
            fabric_pos:
            fabric_pos + 700
        ]

    extracted_text = (
        title_text
        + "\n"
        + fit_text
        + "\n"
        + fabric_text
    )

    return {

        "title_text": title_text,

        "page_text": page_text,

        "product_details": extracted_text,

        "fit_text": fit_text,

        "fabric_text": fabric_text

    }