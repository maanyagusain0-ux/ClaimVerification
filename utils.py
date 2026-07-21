def detect_column(df, keywords):
    """
    Automatically detect a column using possible keywords.
    """
    for col in df.columns:
        col_name = str(col).strip().lower()

        for keyword in keywords:
            if keyword.lower() in col_name:
                return col

    return None