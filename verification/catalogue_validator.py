import re


def normalize_text(text):

    text = str(text).lower()

    text = text.replace("-", " ")
    text = text.replace("&", " and ")
    text = text.replace(",", " ")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def validate_fit(
    dataset_fit,
    title_text,
    website_text
):

    dataset_fit = normalize_text(
        dataset_fit
    )

    title_text = normalize_text(
        title_text
    )

    website_text = normalize_text(
        website_text
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

    # Manager Requirement:
    # If title contains fit info,
    # compare only with title
    print(f"Dataset Fit = [{dataset_fit}]")
    print(f"Title Fit = [{title_fit}]")
    print(f"Title Text = [{title_text}]")
    print("=" * 50)
    if title_fit:

        if dataset_fit == title_fit:
             return "FOUND"

        if dataset_fit in title_fit:
             return "FOUND"

        if title_fit in dataset_fit:
             return "FOUND"

        return "NOT FOUND" 

    # If title does not contain fit info,
    # search elsewhere on PDP

    pattern = (
        r"\b"
        + re.escape(dataset_fit)
        + r"\b"
    )

    if re.search(
        pattern,
        website_text
    ):
        return "FOUND"

    return "NOT FOUND"


def validate_fabric(
    dataset_fabric,
    website_text
):

    dataset_fabric = str(
        dataset_fabric
    ).lower()

    website_text = str(
        website_text
    ).lower()

    dataset_fabric = (
        dataset_fabric
        .replace("&", ",")
        .replace("/", ",")
    )

    parts = [

        p.strip()

        for p in
        dataset_fabric.split(",")

        if p.strip()

    ]

    matched_parts = 0

    for part in parts:

        if part in website_text:

            matched_parts += 1

    if matched_parts == len(parts):

        return "EXACT MATCH"

    elif matched_parts > 0:

        return "PARTIAL MATCH"

    return "MISMATCH"