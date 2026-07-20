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

    # Wait for page to load
    time.sleep(3)

    try:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight * 0.7);"
        )
    except:
        pass

    time.sleep(3)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(),'Size & Fit')]")
            )
        )

        page_text = driver.find_element(
            By.TAG_NAME,
            "body"
        ).text

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
    # Extract Fit
    # -------------------------

    fit_text = ""

    lower_text = page_text.lower()

    FIT_KEYWORDS = [
        "regular fit",
        "slim fit",
        "relaxed fit",
        "oversized",
        "skinny fit",
        "comfort fit",
        "loose fit"
    ]

    for keyword in FIT_KEYWORDS:
        if keyword in lower_text:
            fit_text = keyword.title()
            break

    # -------------------------
    # Extract Fabric
    # -------------------------

    fabric_text = ""

    fabric_pos = lower_text.find("material & care")

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
    print("=" * 50)
    print("TITLE:", title_text)
    print("FIT TEXT:", fit_text)
    print("PAGE HAS 'regular fit':", "regular fit" in page_text.lower())
    print("=" * 50)
    return {
        "title_text": title_text,
        "page_text": page_text,
        "product_details": extracted_text,
        "fit_text": fit_text,
        "fabric_text": fabric_text
    }