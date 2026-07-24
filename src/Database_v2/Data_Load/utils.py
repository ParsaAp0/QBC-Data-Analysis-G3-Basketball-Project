import pandas as pd

# Birth Date
def parse_date(date_str):

    if pd.isna(date_str):
        return None

    return clean(date_str)


def height(height):

    if pd.isna(height):
        return None

    return str(height)


# Weight
def weight_to_kg(weight):

    if pd.isna(weight):
        return None

    return clean(weight)

# Null
def clean(value):

    if pd.isna(value):
        return None

    if value == "":
        return None

    return value