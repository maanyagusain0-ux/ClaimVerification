from verification.claim_verifier import verify_claims

claims = "Better Cotton; Organic Cotton; Recycled Polyester"

page_text = """
This product is made with Better Cotton.
Contains recycled polyester fibres.
"""

result = verify_claims(claims, page_text)

print(result)