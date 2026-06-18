from rapidfuzz import fuzz


def find_best_match(dataset_product, candidates):

    best_score = 0
    best_candidate = None

    for candidate in candidates:

        brand_score = fuzz.ratio(
            "tommy hilfiger",
            candidate["brand"].lower()
        )

        product_score = fuzz.token_sort_ratio(
            dataset_product.lower(),
            candidate["product_name"].lower()
        )

        final_score = (
            brand_score * 0.4 +
            product_score * 0.6
        )

        print("\n--------------------")
        print(f"Brand: {candidate['brand']}")
        print(f"Product: {candidate['product_name']}")
        print(f"Brand Score: {brand_score}")
        print(f"Product Score: {product_score}")
        print(f"Final Score: {final_score}")

        if final_score > best_score:

            best_score = final_score
            best_candidate = candidate

    return best_candidate, best_score