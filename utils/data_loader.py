import pandas as pd
import os

def load_dataset(file):

    try:
        df = pd.read_csv(file)

        # Remove duplicate records
        df = df.drop_duplicates()

        # Normalize column names
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        # Remove completely empty rows
        df = df.dropna(how="all")

        return df

    except Exception as e:
        raise ValueError(f"Dataset loading failed: {e}")


def get_dataset_summary(df):

    summary = {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "data_types": df.dtypes.astype(str).to_dict()
    }

    return summary