import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


txn = pd.DataFrame({
    "txn_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "customer": ["C1", "C2", "C1", "C3", "C2", "C1", "C3", "C3", "C2", "C1"],
    "txn_date": [
        "2026-01-03", "2026-01-15", "2026-01-20", "2026-02-02", "2026-02-10",
        "2026-02-25", "2026-03-05", "2026-03-12", "2026-03-18", "2026-03-28",
    ],
    "category": [
        "Electronics", "grocery", "GROCERY", "Fashion", "grocery",
        "fashion", "Grocery", "grocery", "Fashion", "Electronics",
    ],
    "amount": [1000, 300, np.nan, 800, 450, np.nan, 400, 250, -100, np.nan],
    "status": [
        "Success", "Success", "Failed", "Success", "Success",
        "Failed", "Success", "Success", "Refund", "Failed",
    ],
})

# a. Remove failed transactions.
txn = txn[txn["status"].str.strip().str.lower() != "failed"].copy()
print("Rows remaining:", len(txn))

# b. Clean categories and create datetime and month columns.
txn["category"] = txn["category"].str.strip().str.lower()
txn["txn_date"] = pd.to_datetime(txn["txn_date"])
txn["month"] = txn["txn_date"].dt.strftime("%Y-%m")

# c. Per-customer summary. Refund amounts remain negative in net_amount.
customer_summary = txn.groupby("customer").agg(
    net_amount=("amount", "sum"),
    txns=("txn_id", "count"),
    refunds=("status", lambda status: status.str.strip().str.lower().eq("refund").sum()),
)
print("\nPer-customer summary:")
print(customer_summary)

# d. Monthly total amount by category.
monthly_category = txn.pivot_table(
    index="month",
    columns="category",
    values="amount",
    aggfunc="sum",
    fill_value=0,
)
print("\nMonthly amount by category:")
print(monthly_category)

# e. Plot monthly net amount, including refunds.
monthly_net = txn.groupby("month", as_index=False)["amount"].sum()
monthly_net = monthly_net.rename(columns={"amount": "net_amount"})
sns.lineplot(data=monthly_net, x="month", y="net_amount", marker="o")
plt.title("Total Net Amount per Month")
plt.xlabel("Month")
plt.ylabel("Net Amount")
plt.tight_layout()
plt.show()