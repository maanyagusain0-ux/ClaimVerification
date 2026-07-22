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

    dataset = normalize_text(dataset_fit)
    website = normalize_text(fit_text)

    if not website:
        return "NOT PRESENT"

    if dataset in website:
        return "FOUND"

    return "NOT FOUND"


def validate_fabric(dataset_fabric, website_text):

    dataset = normalize_text(dataset_fabric)
    website = normalize_text(website_text)

    # Replace common marketing names
    dataset = dataset.replace("regenerative cotton", "cotton")
    dataset = dataset.replace("better cotton initiative", "better cotton")
    dataset = dataset.replace("bci cotton", "better cotton")
    dataset = dataset.replace("organic cotton", "cotton")

    website = website.replace("regenerative cotton", "cotton")
    website = website.replace("better cotton initiative", "better cotton")
    website = website.replace("bci cotton", "better cotton")
    website = website.replace("organic cotton", "cotton")

    pairs = re.findall(
        r"(\d+)%\s*([a-z ]+?)(?=\d+%|$)",
        dataset
    )

    if not pairs:
        return "MISMATCH"

    for percent, material in pairs:

        material = material.strip()

        if percent not in website:
            return "MISMATCH"

        if material not in website:
            return "MISMATCH"

    return "MATCH"s