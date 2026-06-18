from selenium.webdriver.common.by import By
import time


def get_candidate_products(driver):

    candidates = []

    try:

        products = driver.find_elements(
            By.CSS_SELECTOR,
            "li.product-base"
        )

        print(f"\nFound {len(products)} products\n")

        for i, product in enumerate(products[:10]):

            try:

                brand = product.find_element(
                    By.CSS_SELECTOR,
                    "h3.product-brand"
                ).text

                product_name = product.find_element(
                    By.CSS_SELECTOR,
                    "h4.product-product"
                ).text

                product_url = product.find_element(
                    By.TAG_NAME,
                    "a"
                ).get_attribute("href")

                print(f"\nCandidate {i+1}")
                print(f"Brand: {brand}")
                print(f"Product: {product_name}")
                print(f"URL: {product_url}")
                print("-" * 60)

                candidates.append({
                    "brand": brand,
                    "product_name": product_name,
                    "url": product_url
                })

            except Exception as e:
                print(f"Error reading product {i+1}: {e}")

    except Exception as e:
        print("Could not retrieve products:", e)

    return candidates