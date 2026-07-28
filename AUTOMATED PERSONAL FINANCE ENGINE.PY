import csv
import json
import logging
from datetime import datetime

# Logging setup for enterprise tracing
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class PersonalFinanceEngine:
    def __init__(self, monthly_budget=50000.0):
        self.monthly_budget = float(monthly_budget)
        self.transactions = []
        self._next_id = 1

    def add_transaction(self, category, amount, description):
        """Validates and records a new transaction."""
        if amount <= 0:
            print(f"Error: Transaction amount (₹{amount}) must be greater than 0.")
            return None
        
        tx = {
            "trans_id": self._next_id,
            "category": category.strip().capitalize(),
            "amount": float(amount),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "description": description.strip()
        }
        self.transactions.append(tx)
        self._next_id += 1

        print(f"Added Transaction #{tx['trans_id']}: {tx['category']} - ₹{tx['amount']}")
        self.check_budget_status()
        return tx

    def get_total_expenses(self):
        """Calculates total spend."""
        return sum(tx["amount"] for tx in self.transactions)

    def check_budget_status(self):
        """Monitors current budget health."""
        total_spend = self.get_total_expenses()
        remaining = self.monthly_budget - total_spend

        if total_spend > self.monthly_budget:
            print(f"ALERT: Budget Exceeded! Limit: ₹{self.monthly_budget:.2f}, Spent: ₹{total_spend:.2f}, Over by: ₹{abs(remaining):.2f}")
        else:
            print(f"Budget Status: Spent ₹{total_spend:.2f} | Remaining ₹{remaining:.2f}")

    def filter_by_category(self, category):
        """Filters transactions based on category."""
        cat_clean = category.strip().capitalize()
        return [tx for tx in self.transactions if tx["category"] == cat_clean]

    def sort_transactions_by_amount(self, descending=True):
        """Sorts transactions using O(n log n) Timsort."""
        return sorted(self.transactions, key=lambda tx: tx["amount"], reverse=descending)

    def export_summary_json(self, filepath="finance_summary.json"):
        """Exports summary data to a JSON file."""
        try:
            summary_data = {
                "generated_at": datetime.now().isoformat(),
                "monthly_budget": self.monthly_budget,
                "total_expenses": self.get_total_expenses(),
                "remaining_budget": self.monthly_budget - self.get_total_expenses(),
                "transaction_count": len(self.transactions),
                "transactions": self.transactions
            }
            with open(filepath, "w") as f:
                json.dump(summary_data, f, indent=4)
            print(f"Successfully exported JSON summary to '{filepath}'")
            return True
        except Exception as e:
            print(f"Error exporting JSON: {e}")
            return False

    def export_csv_report(self, filepath="transactions.csv"):
        """Exports transaction ledger to a CSV file."""
        try:
            with open(filepath, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Category", "Amount", "Date", "Description"])
                for tx in self.transactions:
                    writer.writerow([tx["trans_id"], tx["category"], tx["amount"], tx["date"], tx["description"]])
            print(f"Successfully exported CSV report to '{filepath}'")
            return True
        except Exception as e:
            print(f"Error exporting CSV: {e}")
            return False


# --- Test Drive ---
if __name__ == "__main__":
    print("\n=== INITIALIZING AUTOMATED PERSONAL FINANCE ENGINE ===\n")
    engine = PersonalFinanceEngine(monthly_budget=25000.00)

    # Adding sample transactions
    engine.add_transaction("Food", 1200.50, "Canteen & Groceries")
    engine.add_transaction("Books", 4500.00, "Geo-AI & Python Textbooks")
    engine.add_transaction("Travel", 8000.00, "Flight tickets")
    engine.add_transaction("Electronics", 15000.00, "GPU Cooling Pad")  # Budget overload test

    print("\n--- CATEGORY FILTER (Food) ---")
    print(engine.filter_by_category("food"))

    print("\n--- SORTED BY AMOUNT (DESCENDING) ---")
    for tx in engine.sort_transactions_by_amount():
        print(f"₹{tx['amount']:.2f} -> {tx['category']} ({tx['description']})")

    print("\n--- EXPORTING FILES ---")
    engine.export_summary_json()
    engine.export_csv_report()
