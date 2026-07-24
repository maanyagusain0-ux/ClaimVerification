import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def extract_product_details(driver, product_url):
    """
    Navigates to product_url and extracts title, fit type, and fabric information.
    Includes retries, early page error detection, and explicit waiting for elements.
    """
    MAX_RETRIES = 3

    # --- Fix 2: Retry Loading Page ---
    for attempt in range(MAX_RETRIES):
        driver.get(product_url)

        # Debug print immediately after driver.get()
        print("=" * 80)
        print("URL:", driver.current_url)
        print("TITLE:", driver.title)
        print("\nFIRST 3000 CHARACTERS OF PAGE SOURCE:\n")
        print(driver.page_source[:3000])
        print("=" * 80)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        title = driver.title.lower()

        # If not hit by maintenance, break loop and proceed
        if "site maintenance" not in title:
            break

        print(f"Retry {attempt + 1}/{MAX_RETRIES} due to Site Maintenance...")
        time.sleep(5)
    else:
        # Temporarily returning debug fallback dictionary instead of raising Exception
        return {
            "title_text": driver.title,
            "page_text": driver.page_source,
            "product_details": driver.page_source,
            "fit_text": "",
            "fabric_text": "",
        }

    # --- Fix 1: Detect Error / Maintenance Pages Immediately ---
    body_text = driver.find_element(By.TAG_NAME, "body").text.lower()

    if "site maintenance" in title:
        raise Exception("Myntra Site Maintenance page received")

    if "oops! something went wrong" in body_text:
        raise Exception("Myntra returned an error page")

    # --- Explicit Wait for Product Element instead of fixed sleep ---
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
    except Exception:
        print("Warning: h1 element not detected within timeout window")

    print("=" * 80)
    print("CURRENT URL:", driver.current_url)
    print("PAGE TITLE:", driver.title)

    try:
        print("PAGE SOURCE (first 2000 chars):")
        print(driver.page_source[:2000])
    except Exception as e:
        print("Cannot read page source:", e)

    print("=" * 80)

    # Scroll to trigger lazy loading
    try:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight * 0.8);"
        )
        time.sleep(1.5)
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        time.sleep(1.5)
    except Exception as e:
        print("Scrolling encountered an issue:", e)

    # Read complete page text
    try:
        page_text = driver.find_element(By.TAG_NAME, "body").text
    except Exception as e:
        print("Failed to read body text:", e)
        page_text = ""

    lower_text = page_text.lower()

    # -------------------------
    # Product Title
    # -------------------------
    try:
        title_text = driver.find_element(By.TAG_NAME, "h1").text
    except Exception:
        title_text = driver.title

    # -------------------------
    # Extract Fit Keywords
    # -------------------------
    FIT_KEYWORDS = [
        "regular fit",
        "slim fit",
        "relaxed fit",
        "oversized",
        "skinny fit",
        "comfort fit",
        "loose fit",
        "easy fit",
        "mid rise",
        "low rise",
        "high rise",
    ]

    found_fits = [
        keyword.title() for keyword in FIT_KEYWORDS if keyword in lower_text
    ]
    fit_text = " | ".join(found_fits)

    # -------------------------
    # Extract Fabric Details
    # -------------------------
    fabric_text = ""
    fabric_headings = [
        "material & care",
        "material and care",
        "fabric",
        "composition",
    ]

    for heading in fabric_headings:
        fabric_pos = lower_text.find(heading)
        if fabric_pos != -1:
            fabric_text = page_text[fabric_pos : fabric_pos + 800]
            break

    # -------------------------
    # Debug Output
    # -------------------------
    print("=" * 60)
    print("TITLE:", title_text)
    print("FIT TEXT:", fit_text)
    print("PAGE HAS 'regular fit':", "regular fit" in lower_text)
    print("FABRIC FOUND:", fabric_text[:250])
    print("=" * 60)

    extracted_text = f"{title_text}\n{fit_text}\n{fabric_text}"

    return {
        "title_text": title_text,
        "page_text": page_text,
        "product_details": extracted_text,
        "fit_text": fit_text,
        "fabric_text": fabric_text,
    }