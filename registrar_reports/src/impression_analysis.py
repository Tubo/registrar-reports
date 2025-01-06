import sys

import pandas as pd

from registrar_reports.src.parts_parser import parse


def clean_data(df):
    # rename modality of DX and PX to CR
    df["modality"] = df["modality"].apply(lambda x: "CR" if x in ["DX", "PX"] else x)
    return df


def deduplication(df):
    # Split rows into formal reports and impressions
    formal_reports = df[df["action"] == "Complete dictation"]
    impressions = df[df["action"] == "Add Emergency Impression"]

    # Only keep impressions that have unique accession_no
    impressions = impressions.drop_duplicates(subset="accession_no")

    # Remove impressions that are already in formal reports
    impressions = impressions[
        ~impressions["accession_no"].isin(formal_reports["accession_no"])
    ]

    # Combine the two dataframes
    deduped = pd.concat([formal_reports, impressions])
    return deduped


def parse_xrays(df):
    # Parse the parts of the report
    df["sum_parts"] = df.apply(
        lambda row: parse(row.descriptor) if row.modality == "CR" else 1, axis=1
    )
    return df


def analyse(audit_data: pd.DataFrame) -> pd.DataFrame:
    """
    Analyse the audit data and return a DataFrame with the results
    """
    audit_data = deduplication(clean_data(audit_data))

    results = []
    for user_and_action, user_group in audit_data.groupby(["user", "action"]):
        print("Processing", user_and_action[0], user_and_action[1])
        user_result = {"username": user_and_action[0], "action": user_and_action[1]}
        print("Parsing xray parts")
        parts_parsed = parse_xrays(user_group)
        print("Parsing done")
        for modality, modality_group in parts_parsed.groupby("modality"):
            user_result[str(modality)] = modality_group["sum_parts"].sum()
        results.append(user_result)

    results = pd.DataFrame(results).fillna(0)
    return results


if __name__ == "__main__":
    # cwd to the parent directory
    import os
    import sys

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))
    from src.parts_parser import parse

    raw_data = pd.read_csv("../../output/impression_count/raw.csv")
    result = analyse(raw_data)
    print(result)
