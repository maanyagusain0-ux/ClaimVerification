def verify_claims(claims, page_text):

    results = {}

    claim_list = claims.split(";")

    for claim in claim_list:

        claim = claim.strip()

        if claim.lower() in page_text.lower():

            results[claim] = "FOUND"

        else:

            results[claim] = "NOT FOUND"

    return results