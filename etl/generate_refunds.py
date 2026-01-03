import pandas as pd
import numpy as np

ORDERS_PATH = '../data/raw/orders.csv'
ORDER_ITEMS_PATH = '../data/raw/order_items.csv'
OUTPUT_PATH = '../data/raw/refunds.csv'

refund_rate = 0.03
min_delay_days = 3
max_delay_days = 15

refund_reasons = {
    'late_delivery':0.4,
    'cancelled_customer': 0.3,
    "product_defect": 0.2,
    "wrong_item": 0.1
}

np.random.seed(42)

### Load Data ###
orders = pd.read_csv(ORDERS_PATH, parse_dates=["order_purchase_timestamp"])
order_items = pd.read_csv(ORDER_ITEMS_PATH)
#
### Calculate order total ###
order_totals = (
    order_items.groupby("order_id")['price'].sum().reset_index(name="order_amount")
    )
#
orders = orders.merge(order_totals, on="order_id", how="left")

# Handle missing order_amounts safely
orders["order_amount"] = orders["order_amount"].fillna(0)

# Log data quality issue (do not fail pipeline)
missing_orders = orders[orders["order_amount"] == 0].shape[0]
print(f"Warning: {missing_orders} refunded orders had zero order value")

#
#
# ----------------------------
# SELECT REFUNDED ORDERS
# ----------------------------
refund_sample = orders.sample(frac=refund_rate)
#
refund_records = []
#
for _, row in refund_sample.iterrows():
    refund_delay = np.random.randint(min_delay_days, max_delay_days)
    refund_date = row["order_purchase_timestamp"] + pd.Timedelta(days=refund_delay)
#
    is_full_refund = np.random.rand() < 0.7
#
    if is_full_refund:
        refund_amount = row["order_amount"]
    else:
        refund_amount = round(row["order_amount"] * np.random.uniform(0.3, 0.7), 2)
#
    refund_reason = np.random.choice(
        list(refund_reasons.keys()),
        p=list(refund_reasons.values())
    )
#
    refund_records.append({
        "order_id": row["order_id"],
        "refund_date": refund_date.date(),
        "refund_amount": round(refund_amount, 2),
        "refund_reason": refund_reason
    })
#
refunds_df = pd.DataFrame(refund_records)
#
# ----------------------------
# SAVE
# ----------------------------
refunds_df.to_csv(OUTPUT_PATH, index=False)
#
print(f"Refunds generated: {refunds_df.shape[0]} rows")
#
#
#
#
# ----------------------------
# Sanity Check
# ----------------------------
refunds = pd.read_csv("../data/raw/refunds.csv")
orders = pd.read_csv("../data/raw/orders.csv")
# Refund rate
print("Refund rate:", refunds.shape[0] / orders.shape[0])
#
# Refund reasons distribution
print(refunds["refund_reason"].value_counts(normalize=True))
#
# No negative refunds
assert (refunds["refund_amount"] >= 0).all()
