"""
ACME Bank — Demo Data
All data is fictional and for demonstration purposes only.
"""

import random
from datetime import datetime, timedelta

random.seed(42)  # Fixed seed — keeps demo data consistent across restarts

# ── Demo Login Credentials ────────────────────────────────────────────────────
# username (or last 4 of account number) + PIN → user_id

DEMO_CREDENTIALS = {
    # By username
    "sarah.johnson": {"pin": "1234", "user_id": "user_001"},
    "m.chen":        {"pin": "5678", "user_id": "user_002"},
    "emily.r":       {"pin": "9012", "user_id": "user_003"},
    # By last 4 digits of primary checking account
    "4521":          {"pin": "1234", "user_id": "user_001"},
    "3301":          {"pin": "5678", "user_id": "user_002"},
    "2201":          {"pin": "9012", "user_id": "user_003"},
}

# ── Users ────────────────────────────────────────────────────────────────────

DEMO_USERS = {
    "user_001": {
        "id": "user_001",
        "name": "Sarah Johnson",
        "email": "sarah.johnson@email.com",
        "phone": "+1 (512) 234-5678",
        "address": "123 Maple Street, Austin, TX 78701",
        "date_of_birth": "1988-04-22",
        "member_since": "2018-03-15",
        "credit_score": 742,
        "tier": "Gold",
        "relationship_manager": "James Williams",
        "preferred_language": "English",
        "two_factor_enabled": True,
        "credit_data": {
            "factors": [
                {"factor": "Payment History", "impact": "High", "status": "Excellent", "weight": 35},
                {"factor": "Credit Utilization", "impact": "High", "status": "Good", "weight": 30},
                {"factor": "Credit Age", "impact": "Medium", "status": "Good", "weight": 15},
                {"factor": "Credit Mix", "impact": "Low", "status": "Very Good", "weight": 10},
                {"factor": "New Inquiries", "impact": "Low", "status": "Good", "weight": 10},
            ],
            "history": [
                {"month": "2025-12", "score": 728},
                {"month": "2026-01", "score": 731},
                {"month": "2026-02", "score": 735},
                {"month": "2026-03", "score": 738},
                {"month": "2026-04", "score": 740},
                {"month": "2026-05", "score": 742},
            ],
        },
    },
    "user_002": {
        "id": "user_002",
        "name": "Michael Chen",
        "email": "m.chen@financepro.com",
        "phone": "+1 (415) 987-6543",
        "address": "456 Pacific Heights Ave, San Francisco, CA 94102",
        "date_of_birth": "1979-11-03",
        "member_since": "2015-07-22",
        "credit_score": 815,
        "tier": "Platinum",
        "relationship_manager": "Amanda Foster",
        "preferred_language": "English",
        "two_factor_enabled": True,
        "credit_data": {
            "factors": [
                {"factor": "Payment History", "impact": "High", "status": "Exceptional", "weight": 35},
                {"factor": "Credit Utilization", "impact": "High", "status": "Exceptional", "weight": 30},
                {"factor": "Credit Age", "impact": "Medium", "status": "Excellent", "weight": 15},
                {"factor": "Credit Mix", "impact": "Low", "status": "Excellent", "weight": 10},
                {"factor": "New Inquiries", "impact": "Low", "status": "Very Good", "weight": 10},
            ],
            "history": [
                {"month": "2025-12", "score": 805},
                {"month": "2026-01", "score": 808},
                {"month": "2026-02", "score": 810},
                {"month": "2026-03", "score": 812},
                {"month": "2026-04", "score": 813},
                {"month": "2026-05", "score": 815},
            ],
        },
    },
    "user_003": {
        "id": "user_003",
        "name": "Emily Rodriguez",
        "email": "emily.r@startup.io",
        "phone": "+1 (312) 456-7890",
        "address": "789 Wicker Park Lane, Chicago, IL 60622",
        "date_of_birth": "1997-07-14",
        "member_since": "2021-11-08",
        "credit_score": 688,
        "tier": "Silver",
        "relationship_manager": "David Park",
        "preferred_language": "English",
        "two_factor_enabled": False,
        "credit_data": {
            "factors": [
                {"factor": "Payment History", "impact": "High", "status": "Good", "weight": 35},
                {"factor": "Credit Utilization", "impact": "High", "status": "Fair", "weight": 30},
                {"factor": "Credit Age", "impact": "Medium", "status": "Fair", "weight": 15},
                {"factor": "Credit Mix", "impact": "Low", "status": "Good", "weight": 10},
                {"factor": "New Inquiries", "impact": "Low", "status": "Good", "weight": 10},
            ],
            "history": [
                {"month": "2025-12", "score": 671},
                {"month": "2026-01", "score": 675},
                {"month": "2026-02", "score": 679},
                {"month": "2026-03", "score": 682},
                {"month": "2026-04", "score": 685},
                {"month": "2026-05", "score": 688},
            ],
        },
    },
}

# ── Accounts ─────────────────────────────────────────────────────────────────

DEMO_ACCOUNTS = {
    "user_001": [
        {
            "account_id": "CHK-001-4521",
            "type": "checking",
            "name": "Premier Checking",
            "balance": 8432.67,
            "available": 8432.67,
            "currency": "USD",
            "routing_number": "021000021",
            "opened_date": "2018-03-15",
            "interest_rate": 0.01,
        },
        {
            "account_id": "SAV-001-8834",
            "type": "savings",
            "name": "High-Yield Savings",
            "balance": 24150.00,
            "available": 24150.00,
            "currency": "USD",
            "apy": 4.75,
            "routing_number": "021000021",
            "opened_date": "2018-04-01",
            "monthly_interest_earned": 95.59,
        },
        {
            "account_id": "CC-001-7712",
            "type": "credit_card",
            "name": "ACME Rewards Platinum Card",
            "balance": -1847.33,
            "credit_limit": 15000.00,
            "available_credit": 13152.67,
            "due_date": "2026-06-25",
            "minimum_payment": 37.00,
            "rewards_points": 12450,
            "rewards_cash_value": 124.50,
            "currency": "USD",
            "apr": 21.99,
            "opened_date": "2019-06-15",
        },
    ],
    "user_002": [
        {
            "account_id": "CHK-002-3301",
            "type": "checking",
            "name": "Elite Checking",
            "balance": 45230.15,
            "available": 45230.15,
            "currency": "USD",
            "routing_number": "021000021",
            "opened_date": "2015-07-22",
            "interest_rate": 0.05,
        },
        {
            "account_id": "SAV-002-7712",
            "type": "savings",
            "name": "Premier Savings",
            "balance": 125000.00,
            "available": 125000.00,
            "currency": "USD",
            "apy": 5.10,
            "routing_number": "021000021",
            "opened_date": "2015-08-01",
            "monthly_interest_earned": 531.25,
        },
        {
            "account_id": "CC-002-9901",
            "type": "credit_card",
            "name": "ACME Infinite Black Card",
            "balance": -8234.50,
            "credit_limit": 100000.00,
            "available_credit": 91765.50,
            "due_date": "2026-06-20",
            "minimum_payment": 165.00,
            "rewards_points": 87650,
            "rewards_cash_value": 876.50,
            "currency": "USD",
            "apr": 18.99,
            "opened_date": "2016-01-15",
        },
        {
            "account_id": "INV-002-5533",
            "type": "investment",
            "name": "Wealth Builder Portfolio",
            "balance": 342150.00,
            "available": 342150.00,
            "currency": "USD",
            "opened_date": "2016-03-01",
            "ytd_return": 14.3,
            "account_type": "brokerage",
        },
    ],
    "user_003": [
        {
            "account_id": "CHK-003-2201",
            "type": "checking",
            "name": "Everyday Checking",
            "balance": 2156.44,
            "available": 2156.44,
            "currency": "USD",
            "routing_number": "021000021",
            "opened_date": "2021-11-08",
            "interest_rate": 0.01,
        },
        {
            "account_id": "SAV-003-4477",
            "type": "savings",
            "name": "Emergency Fund",
            "balance": 5800.00,
            "available": 5800.00,
            "currency": "USD",
            "apy": 4.50,
            "routing_number": "021000021",
            "opened_date": "2022-01-15",
            "monthly_interest_earned": 21.75,
        },
    ],
}

# ── Loans ─────────────────────────────────────────────────────────────────────

DEMO_LOANS = {
    "user_001": [
        {
            "loan_id": "MORT-001-2288",
            "type": "mortgage",
            "name": "30-Year Fixed Mortgage",
            "property_address": "123 Maple Street, Austin, TX 78701",
            "original_amount": 285000.00,
            "remaining_balance": 231450.80,
            "monthly_payment": 1444.80,
            "interest_rate": 4.50,
            "term_months": 360,
            "months_remaining": 264,
            "next_payment_date": "2026-07-01",
            "start_date": "2018-07-01",
            "maturity_date": "2048-07-01",
            "payment_made": 96,
        },
    ],
    "user_002": [
        {
            "loan_id": "AUTO-002-5512",
            "type": "auto",
            "name": "Tesla Model S Auto Loan",
            "vehicle": "2024 Tesla Model S",
            "original_amount": 72000.00,
            "remaining_balance": 51840.00,
            "monthly_payment": 1342.50,
            "interest_rate": 4.99,
            "term_months": 60,
            "months_remaining": 38,
            "next_payment_date": "2026-07-05",
            "start_date": "2023-09-05",
            "maturity_date": "2028-09-05",
            "payment_made": 22,
        },
    ],
    "user_003": [
        {
            "loan_id": "STUD-003-7741",
            "type": "student",
            "name": "Federal Student Loan",
            "school": "University of Illinois Chicago",
            "original_amount": 35000.00,
            "remaining_balance": 28750.00,
            "monthly_payment": 362.50,
            "interest_rate": 5.50,
            "term_months": 120,
            "months_remaining": 79,
            "next_payment_date": "2026-07-10",
            "start_date": "2019-12-10",
            "maturity_date": "2030-12-10",
            "payment_made": 41,
        },
        {
            "loan_id": "PERS-003-3310",
            "type": "personal",
            "name": "Personal Loan — Home Improvement",
            "original_amount": 8000.00,
            "remaining_balance": 5200.00,
            "monthly_payment": 266.67,
            "interest_rate": 12.99,
            "term_months": 36,
            "months_remaining": 20,
            "next_payment_date": "2026-07-15",
            "start_date": "2024-11-15",
            "maturity_date": "2027-11-15",
            "payment_made": 16,
        },
    ],
}

# ── Investment Portfolios ─────────────────────────────────────────────────────

DEMO_INVESTMENTS = {
    "user_002": {
        "account_id": "INV-002-5533",
        "holdings": [
            {"symbol": "AAPL", "name": "Apple Inc.", "shares": 45, "avg_cost": 162.30, "current_price": 213.45, "current_value": 9605.25, "cost_basis": 7303.50, "gain_loss": 2301.75, "gain_loss_pct": 31.52, "asset_class": "US Stocks"},
            {"symbol": "MSFT", "name": "Microsoft Corp.", "shares": 30, "avg_cost": 285.10, "current_price": 425.80, "current_value": 12774.00, "cost_basis": 8553.00, "gain_loss": 4221.00, "gain_loss_pct": 49.35, "asset_class": "US Stocks"},
            {"symbol": "GOOGL", "name": "Alphabet Inc.", "shares": 20, "avg_cost": 128.50, "current_price": 178.22, "current_value": 3564.40, "cost_basis": 2570.00, "gain_loss": 994.40, "gain_loss_pct": 38.69, "asset_class": "US Stocks"},
            {"symbol": "NVDA", "name": "NVIDIA Corp.", "shares": 25, "avg_cost": 210.00, "current_price": 875.50, "current_value": 21887.50, "cost_basis": 5250.00, "gain_loss": 16637.50, "gain_loss_pct": 316.90, "asset_class": "US Stocks"},
            {"symbol": "AMZN", "name": "Amazon.com Inc.", "shares": 18, "avg_cost": 145.00, "current_price": 195.60, "current_value": 3520.80, "cost_basis": 2610.00, "gain_loss": 910.80, "gain_loss_pct": 34.90, "asset_class": "US Stocks"},
            {"symbol": "VTI", "name": "Vanguard Total Market ETF", "shares": 120, "avg_cost": 195.00, "current_price": 248.70, "current_value": 29844.00, "cost_basis": 23400.00, "gain_loss": 6444.00, "gain_loss_pct": 27.54, "asset_class": "ETFs"},
            {"symbol": "QQQ", "name": "Invesco QQQ Trust", "shares": 80, "avg_cost": 330.00, "current_price": 455.20, "current_value": 36416.00, "cost_basis": 26400.00, "gain_loss": 10016.00, "gain_loss_pct": 37.94, "asset_class": "ETFs"},
            {"symbol": "VNQ", "name": "Vanguard Real Estate ETF", "shares": 100, "avg_cost": 82.00, "current_price": 89.45, "current_value": 8945.00, "cost_basis": 8200.00, "gain_loss": 745.00, "gain_loss_pct": 9.09, "asset_class": "ETFs"},
            {"symbol": "BND", "name": "Vanguard Total Bond ETF", "shares": 200, "avg_cost": 74.50, "current_price": 72.80, "current_value": 14560.00, "cost_basis": 14900.00, "gain_loss": -340.00, "gain_loss_pct": -2.28, "asset_class": "Bonds"},
            {"symbol": "TLT", "name": "iShares 20+ Year Treasury", "shares": 150, "avg_cost": 98.00, "current_price": 91.20, "current_value": 13680.00, "cost_basis": 14700.00, "gain_loss": -1020.00, "gain_loss_pct": -6.94, "asset_class": "Bonds"},
            {"symbol": "GLD", "name": "SPDR Gold Shares", "shares": 50, "avg_cost": 175.00, "current_price": 218.90, "current_value": 10945.00, "cost_basis": 8750.00, "gain_loss": 2195.00, "gain_loss_pct": 25.09, "asset_class": "Commodities"},
            {"symbol": "TSLA", "name": "Tesla Inc.", "shares": 40, "avg_cost": 220.00, "current_price": 248.50, "current_value": 9940.00, "cost_basis": 8800.00, "gain_loss": 1140.00, "gain_loss_pct": 12.95, "asset_class": "US Stocks"},
            {"symbol": "JPM", "name": "JPMorgan Chase & Co.", "shares": 35, "avg_cost": 155.00, "current_price": 208.30, "current_value": 7290.50, "cost_basis": 5425.00, "gain_loss": 1865.50, "gain_loss_pct": 34.39, "asset_class": "US Stocks"},
            {"symbol": "IEMG", "name": "iShares Core MSCI EM ETF", "shares": 200, "avg_cost": 48.00, "current_price": 56.40, "current_value": 11280.00, "cost_basis": 9600.00, "gain_loss": 1680.00, "gain_loss_pct": 17.50, "asset_class": "International"},
            {"symbol": "VEA", "name": "Vanguard Dev Markets ETF", "shares": 180, "avg_cost": 42.00, "current_price": 49.20, "current_value": 8856.00, "cost_basis": 7560.00, "gain_loss": 1296.00, "gain_loss_pct": 17.14, "asset_class": "International"},
            {"symbol": "CASH", "name": "Money Market Fund", "shares": 139341.55, "avg_cost": 1.00, "current_price": 1.00, "current_value": 139341.55, "cost_basis": 139341.55, "gain_loss": 0.00, "gain_loss_pct": 0.0, "asset_class": "Cash"},
        ],
        "allocation": {
            "US Stocks": 42.5,
            "ETFs": 27.8,
            "International": 5.9,
            "Bonds": 8.2,
            "Commodities": 3.2,
            "Cash": 12.4,
        },
        "performance": {
            "day_return": 1842.30,
            "day_return_pct": 0.54,
            "week_return": 5210.50,
            "week_return_pct": 1.55,
            "month_return": 18340.00,
            "month_return_pct": 5.67,
            "ytd_return": 42180.00,
            "ytd_return_pct": 14.3,
            "total_return": 48921.95,
            "total_return_pct": 16.70,
        },
    }
}

# ── Transaction Generator ─────────────────────────────────────────────────────

_MERCHANTS = {
    "Groceries":       ["Whole Foods Market", "Trader Joe's", "HEB Grocery", "Safeway", "Kroger", "Sprouts Farmers Market", "Costco"],
    "Dining":          ["Chipotle Mexican Grill", "Starbucks Coffee", "McDonald's", "The Capital Grille", "Nobu Restaurant", "Shake Shack", "Sweetgreen", "Panera Bread"],
    "Transportation":  ["Uber", "Lyft", "ExxonMobil Gas", "Shell Gas Station", "Metro Transit", "Tesla Supercharger", "Parking — Downtown Garage"],
    "Entertainment":   ["Netflix", "Spotify Premium", "AMC Theaters", "Amazon Prime Video", "Hulu + Live TV", "Xbox Game Pass", "Apple TV+"],
    "Shopping":        ["Amazon.com", "Target", "Nike Store", "Apple Store", "Nordstrom", "IKEA", "Etsy Purchase", "Best Buy"],
    "Healthcare":      ["CVS Pharmacy", "Walgreens", "LabCorp Testing", "Kaiser Permanente", "Dental Associates", "Eyeglass World"],
    "Utilities":       ["AT&T Wireless", "Comcast Xfinity", "Texas Electric Coop", "City of Austin Water", "Republic Services Trash"],
    "Travel":          ["Delta Airlines", "Marriott Hotels", "Airbnb", "Booking.com", "United Airlines", "Hertz Car Rental", "TSA PreCheck"],
    "Education":       ["Coursera Plus", "Udemy Course", "LinkedIn Learning", "University Bookstore", "Khan Academy Donation"],
}

_INCOME_SOURCES = [
    ("Payroll — Acme Corp", 5200.00),
    ("Payroll — Acme Corp", 5200.00),
    ("Freelance Payment — Upwork", 850.00),
    ("Interest — High-Yield Savings", 95.59),
    ("Cash Back Reward", 45.00),
    ("Zelle Transfer Received", 200.00),
]

_USER_SPEND_PROFILE = {
    "user_001": {"Groceries": (80, 180), "Dining": (15, 90), "Transportation": (10, 65), "Entertainment": (10, 50), "Shopping": (30, 250), "Healthcare": (20, 120), "Utilities": (50, 150), "Travel": (0, 400)},
    "user_002": {"Groceries": (120, 350), "Dining": (40, 400), "Transportation": (30, 150), "Entertainment": (20, 200), "Shopping": (100, 1500), "Healthcare": (50, 300), "Utilities": (100, 400), "Travel": (200, 3000)},
    "user_003": {"Groceries": (40, 90), "Dining": (10, 45), "Transportation": (10, 40), "Entertainment": (5, 20), "Shopping": (15, 80), "Healthcare": (10, 60), "Utilities": (40, 120), "Education": (20, 150)},
}

_PAYROLL = {
    "user_001": ("Payroll — TechCorp Inc", 5200.00),
    "user_002": ("Payroll — Chen Capital Partners", 18500.00),
    "user_003": ("Payroll — StartupHub Chicago", 3100.00),
}

def _build_transactions():
    now = datetime.now()
    all_txns = {}

    for uid, profile in _USER_SPEND_PROFILE.items():
        txns = []
        accounts = DEMO_ACCOUNTS[uid]
        checking = next(a for a in accounts if a["type"] == "checking")
        cc = next((a for a in accounts if a["type"] == "credit_card"), None)
        payroll_name, payroll_amount = _PAYROLL[uid]

        # Payroll — biweekly for last 90 days
        for week in range(0, 90, 14):
            date = (now - timedelta(days=week + 3)).strftime("%Y-%m-%d")
            txns.append({
                "transaction_id": f"TXN-{uid[-3:]}-INC-{week:03d}",
                "date": date,
                "merchant": payroll_name,
                "category": "Income",
                "amount": payroll_amount,
                "account_id": checking["account_id"],
                "status": "completed",
                "description": "Direct deposit payroll",
            })

        # Spending transactions
        txn_counter = 0
        for day_offset in range(90):
            date = (now - timedelta(days=day_offset)).strftime("%Y-%m-%d")
            num_txns = random.randint(0, 4)
            for _ in range(num_txns):
                cat = random.choice(list(profile.keys()))
                lo, hi = profile[cat]
                if hi == 0:
                    continue
                amount = -round(random.uniform(lo, hi), 2)
                merchant = random.choice(_MERCHANTS.get(cat, ["General Purchase"]))
                use_cc = cc and random.random() < 0.35
                acct_id = cc["account_id"] if use_cc else checking["account_id"]
                txns.append({
                    "transaction_id": f"TXN-{uid[-3:]}-{txn_counter:04d}",
                    "date": date,
                    "merchant": merchant,
                    "category": cat,
                    "amount": amount,
                    "account_id": acct_id,
                    "status": "completed",
                    "description": f"{merchant}",
                })
                txn_counter += 1

        txns.sort(key=lambda x: x["date"], reverse=True)
        all_txns[uid] = txns

    return all_txns

DEMO_TRANSACTIONS = _build_transactions()


def get_user_transactions(user_id: str) -> list:
    return DEMO_TRANSACTIONS.get(user_id, DEMO_TRANSACTIONS["user_001"])


# ── Fraud Alerts ──────────────────────────────────────────────────────────────

DEMO_FRAUD_ALERTS = {
    "user_001": [
        {
            "alert_id": "ALT-001-001",
            "type": "unusual_location",
            "severity": "medium",
            "title": "Login from new device",
            "description": "Sign-in detected from iPhone 15 in Denver, CO — not your usual location.",
            "date": "2026-06-03T14:22:00",
            "resolved": True,
            "resolution": "Confirmed by user",
        },
        {
            "alert_id": "ALT-001-002",
            "type": "large_transaction",
            "severity": "low",
            "title": "Large purchase detected",
            "description": "Purchase of $847.50 at Nordstrom — above your average transaction size.",
            "date": "2026-06-01T11:15:00",
            "resolved": True,
            "resolution": "Confirmed legitimate",
        },
    ],
    "user_002": [
        {
            "alert_id": "ALT-002-001",
            "type": "card_not_present",
            "severity": "high",
            "title": "Suspicious online purchase",
            "description": "Attempted charge of $3,200 at unknown merchant 'INTL-MERCH-7721' — blocked.",
            "date": "2026-06-04T23:41:00",
            "resolved": False,
            "resolution": None,
        },
        {
            "alert_id": "ALT-002-002",
            "type": "multiple_declined",
            "severity": "medium",
            "title": "3 declined transactions in 10 minutes",
            "description": "Three rapid declined charges at different merchants in London, UK.",
            "date": "2026-06-04T23:38:00",
            "resolved": False,
            "resolution": None,
        },
    ],
    "user_003": [
        {
            "alert_id": "ALT-003-001",
            "type": "low_balance",
            "severity": "low",
            "title": "Low balance warning",
            "description": "Checking account balance dropped below $500 threshold.",
            "date": "2026-05-28T09:00:00",
            "resolved": True,
            "resolution": "Balance restored via transfer",
        },
    ],
}

# ── ATM & Branch Locations ─────────────────────────────────────────────────────

DEMO_LOCATIONS = {
    "default": [
        {"type": "branch", "name": "ACME Bank — Downtown Austin", "address": "100 Congress Ave, Austin, TX 78701", "distance_miles": 0.4, "hours": "Mon-Fri 9am-5pm, Sat 10am-2pm", "phone": "+1 (512) 400-1000", "services": ["Loans", "Investments", "Safe Deposit", "Notary"]},
        {"type": "branch", "name": "ACME Bank — South Congress", "address": "2200 South Congress Ave, Austin, TX 78704", "distance_miles": 2.1, "hours": "Mon-Fri 9am-5pm", "phone": "+1 (512) 400-1100", "services": ["Loans", "Foreign Exchange"]},
        {"type": "atm", "name": "ACME ATM — Whole Foods 6th St", "address": "525 N Lamar Blvd, Austin, TX 78703", "distance_miles": 0.8, "hours": "24/7", "features": ["Deposit", "Cardless", "Spanish"]},
        {"type": "atm", "name": "ACME ATM — Austin Airport Terminal 1", "address": "3600 Presidential Blvd, Austin, TX 78719", "distance_miles": 4.5, "hours": "24/7", "features": ["Deposit", "Foreign Currency"]},
        {"type": "atm", "name": "ACME ATM — The Domain Mall", "address": "11410 Century Oaks Terrace, Austin, TX 78758", "distance_miles": 3.9, "hours": "24/7", "features": ["Deposit", "Cardless"]},
    ],
    "94102": [
        {"type": "branch", "name": "ACME Bank — Union Square SF", "address": "1 Powell St, San Francisco, CA 94102", "distance_miles": 0.2, "hours": "Mon-Fri 9am-5pm, Sat 10am-3pm", "phone": "+1 (415) 400-2000", "services": ["Wealth Management", "Loans", "FX", "Safe Deposit"]},
        {"type": "branch", "name": "ACME Bank — Financial District", "address": "555 California St, San Francisco, CA 94104", "distance_miles": 0.7, "hours": "Mon-Fri 8am-5pm", "phone": "+1 (415) 400-2100", "services": ["Commercial Banking", "Loans", "Investments"]},
        {"type": "atm", "name": "ACME ATM — Ferry Building", "address": "1 Ferry Building, San Francisco, CA 94111", "distance_miles": 1.1, "hours": "24/7", "features": ["Deposit", "Cardless", "Chinese"]},
        {"type": "atm", "name": "ACME ATM — Westfield Centre", "address": "845 Market St, San Francisco, CA 94103", "distance_miles": 0.3, "hours": "24/7", "features": ["Deposit", "Cardless"]},
    ],
    "60622": [
        {"type": "branch", "name": "ACME Bank — Wicker Park", "address": "1648 Milwaukee Ave, Chicago, IL 60647", "distance_miles": 0.5, "hours": "Mon-Fri 9am-5pm", "phone": "+1 (312) 400-3000", "services": ["Personal Banking", "Loans"]},
        {"type": "atm", "name": "ACME ATM — Damen Blue Line", "address": "1648 N Damen Ave, Chicago, IL 60647", "distance_miles": 0.3, "hours": "24/7", "features": ["Deposit", "Cardless", "Spanish"]},
        {"type": "atm", "name": "ACME ATM — Whole Foods Wicker Park", "address": "1550 N Milwaukee Ave, Chicago, IL 60622", "distance_miles": 0.6, "hours": "24/7", "features": ["Deposit"]},
    ],
}

# ── Exchange Rates ─────────────────────────────────────────────────────────────

DEMO_FX_RATES = {
    "USD": {
        "EUR": 0.9215, "GBP": 0.7892, "JPY": 156.42, "CAD": 1.3645, "AUD": 1.5234,
        "CHF": 0.8978, "CNY": 7.2341, "MXN": 17.8200, "INR": 83.45, "BRL": 5.1850,
        "SGD": 1.3412, "HKD": 7.8201, "NOK": 10.5640, "SEK": 10.3210, "NZD": 1.6340,
    },
    "EUR": {
        "USD": 1.0852, "GBP": 0.8565, "JPY": 169.73, "CAD": 1.4806, "AUD": 1.6533,
        "CHF": 0.9742, "CNY": 7.8500, "MXN": 19.3300, "INR": 90.54, "SGD": 1.4550,
    },
    "GBP": {
        "USD": 1.2671, "EUR": 1.1675, "JPY": 198.20, "CAD": 1.7290, "AUD": 1.9301,
        "CHF": 1.1375, "CNY": 9.1650, "MXN": 22.5800, "INR": 105.72, "SGD": 1.6985,
    },
}
