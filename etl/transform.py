import pandas as pd

RAW_PATH = "../data/raw/"
CLEAN_PATH = "../data/cleaned/"

def validate_not_null(df, columns, table_name):
    for col in columns:
        if df[col].isnull().any():
            raise ValueError(f"{table_name}: Null values found in {col}")

def transform_orders():
    orders = pd.read_csv(
        RAW_PATH + "orders.csv",
        parse_dates=["order_purchase_timestamp"]
    )

    validate_not_null(
        orders,
        ["order_id", "order_purchase_timestamp", "order_status"],
        "orders"
    )

    orders = orders.drop_duplicates(subset=["order_id"])

    orders.to_csv(CLEAN_PATH + "orders_clean.csv", index=False)

def transform_marketing():
    marketing = pd.read_csv(RAW_PATH + "marketing_spend.csv")

    if (marketing["spend_amount"] < 0).any():
        raise ValueError("marketing_spend: Negative spend detected")

    marketing.to_csv(CLEAN_PATH + "marketing_spend_clean.csv", index=False)

def transform_refunds():
    refunds = pd.read_csv(RAW_PATH + "refunds.csv")

    validate_not_null(
        refunds,
        ["order_id", "refund_date", "refund_amount"],
        "refunds"
    )

    if (refunds["refund_amount"] < 0).any():
        raise ValueError("refunds: Negative refund amount")

    refunds.to_csv(CLEAN_PATH + "refunds_clean.csv", index=False)

def run_all():
    transform_orders()
    transform_marketing()
    transform_refunds()
    print("ETL Transform & Validation completed successfully")

if __name__ == "__main__":
    run_all()
