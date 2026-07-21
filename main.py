import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils import detect_column
from verification.product_extractor import extract_product_details
from verification.catalogue_validator import (
    validate_title_fit,
    validate_pdp_fit,
    validate_fabric
)
from reports.report_generator import save_report


start_time = time.time()

print("Catalogue Improvement System Started")

file_path = "data/new.xlsx"

df = pd.read_excel(file_path)
df.columns = df.columns.str.strip()
link_col = detect_column(df, [
    "link",
    "links",
    "url",
    "product link"
])

fabric_col = detect_column(df, [
    "composition",
    "fabric composition",
    "material"
])

fit_col = detect_column(df, [
    "fit"
])

fg_col = detect_column(df, [
    "fg code"
])

olabi_col = detect_column(df, [
    "olabi code",
    "olabi code buy master"
])
print("Total rows loaded:", len(df))


# -------------------------
# Chrome Options
# -------------------------

chrome_options = Options()

prefs = {
    "profile.managed_default_content_settings.images": 2
}

chrome_options.add_experimental_option(
    "prefs",
    prefs
)

chrome_options.page_load_strategy = "eager"

chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")


# -------------------------
# Launch Browser
# -------------------------

driver = webdriver.Chrome(
    options=chrome_options
)

report_rows = []


# -------------------------
# Main Loop
# -------------------------

for index, row in df.iterrows():

    # Restart browser every 50 products
    if index > 0 and index % 50 == 0:

        print(
            f"\nRestarting Chrome at product {index}..."
        )

        save_report(report_rows)

        driver.quit()

        driver = webdriver.Chrome(
            options=chrome_options
        )

    elapsed = (
        time.time() - start_time
    ) / 60

    print(
        f"Processing {index + 1}/{len(df)} "
        f"| Elapsed: {elapsed:.1f} min"
    )

    try:

        product_url =row[link_col]

        product_details = extract_product_details(
            driver,
            product_url
        )

        fabric_status = validate_fabric(
            row[fabric_col],
            product_details["fabric_text"]
        )

        title_fit_status = validate_title_fit(
            row[fit_col],
            product_details["title_text"]
        )

        pdp_fit_status = validate_pdp_fit(
            row[fit_col],
            product_details["fit_text"]
        )

        report_rows.append({

            "FG CODE":
            row[fg_col],

            "OLABI CODE":
            row[olabi_col],

            "Dataset Fabric":
            row[fabric_col],

            "Fabric Status":
            fabric_status,

            "Dataset Fit":
            row[fit_col],

            "Fit Status":
            title_fit_status,
             
            "PDP Fit Status": 
            pdp_fit_status,

            "Website Details":
            product_details[
                "product_details"
            ].replace(
                "\n",
                " | "
            ),

            "Link":
            product_url

        })

    except Exception as e:

        print(
            f"Error processing row "
            f"{index + 1}: {e}"
        )

        continue


# -------------------------
# Close Browser
# -------------------------

driver.quit()


# -------------------------
# Final Report Save
# -------------------------

save_report(report_rows)

end_time = time.time()

print(
    f"\nProcess Completed!"
    f"\nTime taken: "
    f"{end_time - start_time:.2f} seconds"
)