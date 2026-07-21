import re
from verification.fabric_dictionary import FABRIC_TYPES
def normalize_text(text):

    text = str(text).lower()

    text = text.replace("-", " ")
    text = text.replace("&", " and ")
    text = text.replace(",", " ")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def validate_title_fit(
    dataset_fit,
    title_text
):

    dataset_fit = normalize_text(
        dataset_fit
    )

    title_text = normalize_text(
        title_text
    )

    fit_keywords = [

        "mid rise",
        "low rise",
        "high rise",

        "regular fit",
        "relaxed fit",
        "slim fit",
        "skinny fit",

        "easy fit",
        "easy",

        "oversized",

        "trunk",
        "brief",
        "bikini",
        "boyshort"
    ]

    title_fit = None

    for keyword in fit_keywords:

        if keyword in title_text:

            title_fit = keyword
            break

    if not title_fit:

        return "NOT PRESENT"

    if dataset_fit == title_fit:
        return "FOUND"

    if dataset_fit in title_fit:
        return "FOUND"

    if title_fit in dataset_fit:
        return "FOUND"

    return "NOT FOUND"


def validate_pdp_fit(dataset_fit, fit_text):

    dataset_fit = normalize_text(dataset_fit)
    fit_text = normalize_text(fit_text)

    if dataset_fit == "" or fit_text == "":
        return "NOT PRESENT"

    if dataset_fit in fit_text:
        return "FOUND"

    if fit_text in dataset_fit:
        return "FOUND"

    return "NOT FOUND"


def validate_fabric(
    dataset_fabric,
    website_text
):

    dataset_fabric = normalize_text(dataset_fabric)
    website_text = normalize_text(website_text)

    # -----------------------------
    # CASE 1: Fabric Type Validation
    # -----------------------------
    for fabric in FABRIC_TYPES:
        normalized_fabric = normalize_text(fabric)
        if dataset_fabric == normalized_fabric:

            if normalized_fabric in website_text:
                return "MATCH"

            return "MISMATCH"
    # ------------------------------------
    # CASE 2: Composition Validation
    # ------------------------------------

    dataset_lower = dataset_fabric
    website_lower = website_text

    dataset_lower = re.sub(r"\s+", " ", dataset_lower)
    website_lower = re.sub(r"\s+", " ", website_lower)

    dataset_pairs = re.findall(
        r"(\d+)%\s*([a-z ]+?)(?=\d+%|$)",
        dataset_lower
    )

    if len(dataset_pairs) == 0:
        return "MISMATCH"

    for percentage, material in dataset_pairs:

        material = material.strip()

        pattern = (
            percentage
            + r"%\s*"
            + re.escape(material)
        )

        if not re.search(pattern, website_lower):
            return "MISMATCH"

    return "MATCH"