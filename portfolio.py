"""Task 2: Stock Portfolio Performance Tracker.

Enter tickers, buy prices and quantities. The script looks up current prices
from prices.csv (or asks you), calculates gain/loss, and saves
portfolio_summary.csv.
"""
import csv
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
PRICES_FILE = os.path.join(BASE, "prices.csv")
SUMMARY_FILE = os.path.join(BASE, "portfolio_summary.csv")


def load_prices():
    prices = {}
    if os.path.exists(PRICES_FILE):
        with open(PRICES_FILE, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                prices[row["ticker"].upper()] = float(row["price"])
    return prices


def read_float(prompt, positive=True):
    while True:
        try:
            value = float(input(prompt))
            if positive and value <= 0:
                print("Value must be greater than 0.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def collect_holdings(prices):
    portfolio = {}
    print("Enter your holdings. Type 'done' as ticker to finish.\n")
    while True:
        ticker = input("Ticker symbol: ").strip().upper()
        if ticker == "DONE":
            break
        if not ticker.isalpha():
            print("Ticker should contain letters only.")
            continue
        buy_price = read_float("Buy price per share: ")
        qty = read_float("Number of shares: ")
        if ticker in prices:
            current = prices[ticker]
        else:
            print(f"{ticker} not found in prices.csv.")
            current = read_float("Enter current price manually: ")
        portfolio[ticker] = {"buy_price": buy_price, "qty": qty, "current": current}
        print(f"Added {ticker}.\n")
    return portfolio


def calculate(portfolio):
    rows = []
    for ticker, h in portfolio.items():
        invested = h["buy_price"] * h["qty"]
        value = h["current"] * h["qty"]
        pct = (value - invested) / invested * 100
        rows.append({
            "ticker": ticker, "quantity": h["qty"], "buy_price": h["buy_price"],
            "current_price": h["current"], "invested": round(invested, 2),
            "current_value": round(value, 2), "gain_loss": round(value - invested, 2),
            "gain_loss_pct": round(pct, 2),
        })
    return rows


def print_report(rows):
    print("\n" + "=" * 78)
    print(f"{'Ticker':<8}{'Qty':>8}{'Buy':>10}{'Now':>10}{'Invested':>12}{'Value':>12}{'Gain %':>10}")
    print("-" * 78)
    for r in rows:
        print(f"{r['ticker']:<8}{r['quantity']:>8.2f}{r['buy_price']:>10.2f}{r['current_price']:>10.2f}"
              f"{r['invested']:>12.2f}{r['current_value']:>12.2f}{r['gain_loss_pct']:>9.2f}%")
    invested = sum(r["invested"] for r in rows)
    value = sum(r["current_value"] for r in rows)
    pct = (value - invested) / invested * 100 if invested else 0
    print("-" * 78)
    print(f"Total invested: {invested:.2f} | Current value: {value:.2f} | "
          f"Gain/Loss: {value - invested:+.2f} ({pct:+.2f}%)")
    print("=" * 78)
    return invested, value, pct


def save_summary(rows, invested, value, pct):
    fields = list(rows[0].keys())
    with open(SUMMARY_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
        writer.writerow({"ticker": "TOTAL", "invested": round(invested, 2),
                         "current_value": round(value, 2),
                         "gain_loss": round(value - invested, 2),
                         "gain_loss_pct": round(pct, 2)})
    print(f"\nSaved summary to {SUMMARY_FILE} at {datetime.now():%Y-%m-%d %H:%M}")


def main():
    prices = load_prices()
    portfolio = collect_holdings(prices)
    if not portfolio:
        print("No holdings entered.")
        return
    rows = calculate(portfolio)
    invested, value, pct = print_report(rows)
    save_summary(rows, invested, value, pct)


if __name__ == "__main__":
    main()
