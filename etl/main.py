import extract
import transform
import load
import argparse
import pandas as pd
from dotenv import load_dotenv


def main():
    parser = argparse.ArgumentParser(description="ETL pipeline")
    parser.add_argument(
        "action",
        type=str,
        choices=["etl", "validate_db"],
        help="Specify the action to perform (etl, validate_db)",
    )
    parser.add_argument("--file_id", type=str, help="File id for load stage")
    parser.add_argument("--use_dotenv", action='store_true', help="Use local .env file")

    args = parser.parse_args()

    if args.use_dotenv:
        load_dotenv()

    if args.action == "etl":
        df = read(args)
        df = transform.transform_data_types(df)
        creds = load.load_db_creds()
        load.write_data_to_database(df, creds)
    elif args.action == "validate_db":
        creds = load.load_db_creds()
        load.validate_db_data(creds)


def read(args: argparse.Namespace) -> pd.DataFrame:
    assert args.file_id, "--file_id must be specified"
    df = extract.read_data(args.file_id)
    return df


if __name__ == "__main__":
    main()
