import pandas as pd
from openpyxl import load_workbook


def save_report(results):

    file_path = "reports/verification_report.xlsx"

    df = pd.DataFrame(results)

    df.to_excel(
        file_path,
        index=False
    )

    workbook = load_workbook(file_path)

    worksheet = workbook.active

    for column in worksheet.columns:

        max_length = 0

        column_letter = column[0].column_letter

        for cell in column:

            try:

                if len(str(cell.value)) > max_length:

                    max_length = len(str(cell.value))

            except:
                pass

        worksheet.column_dimensions[
            column_letter
        ].width = max_length + 5

    workbook.save(file_path)

    print("Report saved successfully!")