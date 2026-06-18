from reports.report_generator import save_report

sample_results = [

    {
        "Brand": "Tommy Hilfiger",
        "Product": "Blue Jeans",
        "Claim": "Better Cotton",
        "Status": "FOUND"
    },

    {
        "Brand": "Tommy Hilfiger",
        "Product": "Blue Jeans",
        "Claim": "Organic Cotton",
        "Status": "NOT FOUND"
    }
]

save_report(sample_results)