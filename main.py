"""
ACME Bank MCP Server
FastMCP + SSE transport · Render-hosted demo

Mindset registers this at: https://<your-app>.onrender.com/sse
API key: set ACME_API_KEY env var, then register that key in Mindset.
"""

import json
import os
import secrets
import uvicorn
from contextvars import ContextVar
from datetime import datetime, timedelta

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.routing import Mount

from fastmcp import FastMCP

from demo_data import (
    DEMO_USERS,
    DEMO_ACCOUNTS,
    DEMO_LOANS,
    DEMO_INVESTMENTS,
    DEMO_FRAUD_ALERTS,
    DEMO_LOCATIONS,
    DEMO_FX_RATES,
    get_user_transactions,
)

# ── Config ────────────────────────────────────────────────────────────────────

API_KEY = os.environ.get("ACME_API_KEY", "acme-demo-key-change-me")
PORT = int(os.environ.get("PORT", 8000))

# ── Header capture (ContextVar — async-safe) ──────────────────────────────────

_req_headers: ContextVar[dict] = ContextVar("_req_headers", default={})


class HeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = _req_headers.set(dict(request.headers))
        try:
            return await call_next(request)
        finally:
            _req_headers.reset(token)


def _h() -> dict:
    return _req_headers.get({})


def _user_id() -> str:
    return _h().get("x-user-id", "user_001")


def _app_uid() -> str:
    return _h().get("x-app-uid", "")


def _session_tags() -> str:
    return _h().get("x-session-tags", "")


def _authorized() -> bool:
    auth = _h().get("authorization", "")
    provided = auth[len("Bearer "):] if auth.startswith("Bearer ") else auth
    if not provided:
        return False
    return secrets.compare_digest(provided.encode(), API_KEY.encode())


def _unauth() -> dict:
    return {
        "status": "error",
        "message": "Unauthorized — invalid or missing API key.",
        "data": {},
    }


# ── FastMCP server ────────────────────────────────────────────────────────────

mcp = FastMCP(
    name="ACME Bank",
    instructions=(
        "You are ACME Bank's AI assistant. Help customers with account balances, "
        "transactions, loans, investments, spending analytics, transfers, bill payments, "
        "fraud alerts, and financial insights. Be concise, accurate, and professional. "
        "Always reference specific account IDs and dollar amounts when relevant."
    ),
)

# ── 1. Customer Profile ───────────────────────────────────────────────────────


@mcp.tool()
async def get_customer_profile() -> dict:
    """
    Get the current customer's profile: name, contact details, membership tier,
    credit score, relationship manager, and account preferences.
    """
    if not _authorized():
        return _unauth()

    user = DEMO_USERS.get(_user_id(), DEMO_USERS["user_001"])
    return {
        "status": "success",
        "message": f"Profile loaded for {user['name']} — {user['tier']} member since {user['member_since']}.",
        "data": {
            "profile": user,
        },
    }


# ── 2. Account Summary ────────────────────────────────────────────────────────


@mcp.tool()
async def get_account_summary() -> dict:
    """
    Get all bank accounts (checking, savings, credit card, investment) with
    current balances, available credit, APY, and account details.
    Returns structured data for an interactive balance dashboard widget.
    """
    if not _authorized():
        return _unauth()

    uid = _user_id()
    user = DEMO_USERS.get(uid, DEMO_USERS["user_001"])
    accounts = DEMO_ACCOUNTS.get(uid, DEMO_ACCOUNTS["user_001"])

    total_assets = sum(
        a["balance"]
        for a in accounts
        if a["type"] in ("checking", "savings", "investment") and a["balance"] > 0
    )
    total_debt = sum(abs(a["balance"]) for a in accounts if a["balance"] < 0)

    return {
        "status": "success",
        "message": (
            f"{user['name']} has {len(accounts)} account(s). "
            f"Total assets: ${total_assets:,.2f} · Total debt: ${total_debt:,.2f}."
        ),
        "data": {
            "customer_name": user["name"],
            "tier": user["tier"],
            "total_assets": round(total_assets, 2),
            "total_debt": round(total_debt, 2),
            "net_worth": round(total_assets - total_debt, 2),
            "account_count": len(accounts),
            "accounts": accounts,
            # Widget hint — used by Mindset Widget Studio to pick the right template
            "widget_type": "account_dashboard",
        },
    }


# ── 3. Spending Analytics ─────────────────────────────────────────────────────


@mcp.tool()
async def get_spending_analytics(period: str = "30d") -> dict:
    """
    Get spending breakdown by category and monthly trend.
    Returns structured data for a donut chart and bar chart widget.

    Args:
        period: Time window — "7d", "30d", "90d", or "ytd". Default: "30d".
    """
    if not _authorized():
        return _unauth()

    uid = _user_id()
    txns = get_user_transactions(uid)

    now = datetime.now()
    period_days = {"7d": 7, "30d": 30, "90d": 90, "ytd": (now - datetime(now.year, 1, 1)).days}
    days = period_days.get(period, 30)
    cutoff = now - timedelta(days=days)

    debits = [
        t for t in txns
        if t["amount"] < 0
        and datetime.strptime(t["date"], "%Y-%m-%d") >= cutoff
    ]

    by_category: dict[str, float] = {}
    by_month: dict[str, float] = {}
    for t in debits:
        cat = t["category"]
        month = t["date"][:7]
        by_category[cat] = by_category.get(cat, 0.0) + abs(t["amount"])
        by_month[month] = by_month.get(month, 0.0) + abs(t["amount"])

    by_category = dict(sorted(by_category.items(), key=lambda x: x[1], reverse=True))
    by_month = dict(sorted(by_month.items()))
    total_spent = sum(by_category.values())

    category_breakdown = [
        {
            "category": cat,
            "amount": round(amt, 2),
            "percentage": round(amt / total_spent * 100, 1) if total_spent else 0,
            "transaction_count": sum(1 for t in debits if t["category"] == cat),
        }
        for cat, amt in by_category.items()
    ]

    monthly_trend = [
        {"month": month, "amount": round(amt, 2)}
        for month, amt in by_month.items()
    ]

    return {
        "status": "success",
        "message": (
            f"Spent ${total_spent:,.2f} over {period} across "
            f"{len(by_category)} categories ({len(debits)} transactions)."
        ),
        "data": {
            "period": period,
            "period_label": {
                "7d": "Last 7 Days", "30d": "Last 30 Days",
                "90d": "Last 90 Days", "ytd": "Year to Date"
            }.get(period, period),
            "total_spent": round(total_spent, 2),
            "transaction_count": len(debits),
            "top_category": category_breakdown[0] if category_breakdown else None,
            "category_breakdown": category_breakdown,   # → donut / bar chart
            "monthly_trend": monthly_trend,              # → line / bar chart
            "widget_type": "spending_analytics",
        },
    }


# ── 4. Transactions ───────────────────────────────────────────────────────────


@mcp.tool()
async def get_transactions(
    account_id: str = None,
    category: str = None,
    limit: int = 25,
    offset: int = 0,
) -> dict:
    """
    Get transaction history with optional filters.
    Returns structured data for an interactive sortable table widget.

    Args:
        account_id: Filter by account (e.g. "CHK-001-4521"). None = all accounts.
        category: Filter by category (e.g. "Dining"). None = all categories.
        limit: Number of results (max 50). Default: 25.
        offset: Pagination offset. Default: 0.
    """
    if not _authorized():
        return _unauth()

    uid = _user_id()
    all_txns = get_user_transactions(uid)

    filtered = all_txns
    if account_id:
        filtered = [t for t in filtered if t["account_id"] == account_id]
    if category:
        filtered = [t for t in filtered if t["category"].lower() == category.lower()]

    limit = min(limit, 50)
    page = filtered[offset: offset + limit]

    # Summary stats for the filtered set
    credits = sum(t["amount"] for t in filtered if t["amount"] > 0)
    debits = sum(abs(t["amount"]) for t in filtered if t["amount"] < 0)

    return {
        "status": "success",
        "message": f"Showing {len(page)} of {len(filtered)} transactions.",
        "data": {
            "total_count": len(filtered),
            "showing": len(page),
            "offset": offset,
            "limit": limit,
            "filters": {"account_id": account_id, "category": category},
            "summary": {
                "total_credits": round(credits, 2),
                "total_debits": round(debits, 2),
                "net": round(credits - debits, 2),
            },
            "transactions": page,                        # → interactive table
            "widget_type": "transaction_table",
        },
    }


# ── 5. Loan Details ───────────────────────────────────────────────────────────


@mcp.tool()
async def get_loan_details() -> dict:
    """
    Get all active loans with repayment progress, next payment dates,
    interest rates, and amortization info.
    Returns structured data for a repayment progress widget.
    """
    if not _authorized():
        return _unauth()

    uid = _user_id()
    loans = DEMO_LOANS.get(uid, [])

    if not loans:
        return {
            "status": "success",
            "message": "No active loans found.",
            "data": {"loan_count": 0, "loans": [], "widget_type": "loan_summary"},
        }

    enriched = []
    for loan in loans:
        paid = loan["original_amount"] - loan["remaining_balance"]
        pct = round(paid / loan["original_amount"] * 100, 1)
        months_rem = loan.get("months_remaining", 0)
        enriched.append({
            **loan,
            "amount_paid": round(paid, 2),
            "percent_paid": pct,
            "years_remaining": months_rem // 12,
            "months_extra": months_rem % 12,
        })

    total_remaining = sum(l["remaining_balance"] for l in loans)
    total_original = sum(l["original_amount"] for l in loans)
    total_paid = total_original - total_remaining

    return {
        "status": "success",
        "message": (
            f"{len(loans)} active loan(s). "
            f"Total remaining: ${total_remaining:,.2f} "
            f"({round(total_paid/total_original*100,1)}% paid overall)."
        ),
        "data": {
            "loan_count": len(loans),
            "total_remaining": round(total_remaining, 2),
            "total_original": round(total_original, 2),
            "total_paid": round(total_paid, 2),
            "overall_percent_paid": round(total_paid / total_original * 100, 1),
            "loans": enriched,                           # → progress bars widget
            "widget_type": "loan_summary",
        },
    }


# ── 6. Investment Portfolio ───────────────────────────────────────────────────


@mcp.tool()
async def get_investment_portfolio() -> dict:
    """
    Get the investment portfolio: holdings, asset allocation breakdown,
    gain/loss per position, and overall performance metrics.
    Returns structured data for a pie chart and holdings table widget.
    """
    if not _authorized():
        return _unauth()

    uid = _user_id()
    portfolio = DEMO_INVESTMENTS.get(uid)

    if not portfolio:
        return {
            "status": "success",
            "message": "No investment account found. Eligible customers can open one today.",
            "data": {"has_portfolio": False},
        }

    holdings = portfolio["holdings"]
    total_value = sum(h["current_value"] for h in holdings)
    total_cost = sum(h["cost_basis"] for h in holdings)
    gain_loss = total_value - total_cost
    gain_pct = round(gain_loss / total_cost * 100, 2) if total_cost else 0

    # Group by asset class for allocation chart
    by_class: dict[str, float] = {}
    for h in holdings:
        cls = h["asset_class"]
        by_class[cls] = by_class.get(cls, 0.0) + h["current_value"]

    allocation_breakdown = [
        {
            "asset_class": cls,
            "value": round(val, 2),
            "percentage": round(val / total_value * 100, 1) if total_value else 0,
        }
        for cls, val in sorted(by_class.items(), key=lambda x: x[1], reverse=True)
    ]

    return {
        "status": "success",
        "message": (
            f"Portfolio value: ${total_value:,.2f}  "
            f"({'+' if gain_pct >= 0 else ''}{gain_pct:.1f}% total return)."
        ),
        "data": {
            "total_value": round(total_value, 2),
            "total_cost_basis": round(total_cost, 2),
            "total_gain_loss": round(gain_loss, 2),
            "total_gain_loss_pct": gain_pct,
            "performance": portfolio.get("performance", {}),
            "allocation_breakdown": allocation_breakdown,  # → pie chart
            "holdings": sorted(holdings, key=lambda h: h["current_value"], reverse=True),  # → table
            "widget_type": "investment_portfolio",
        },
    }


# ── 7. Credit Score ───────────────────────────────────────────────────────────


@mcp.tool()
async def get_credit_score() -> dict:
    """
    Get the current credit score with score band, key factors (payment history,
    utilization, etc.), and a 6-month score trend.
    Returns structured data for a gauge and trend chart widget.
    """
    if not _authorized():
        return _unauth()

    uid = _user_id()
    user = DEMO_USERS.get(uid, DEMO_USERS["user_001"])
    score = user["credit_score"]
    credit_data = user.get("credit_data", {})

    if score >= 800:
        band, next_milestone = "Exceptional", None
    elif score >= 740:
        band, next_milestone = "Very Good", f"{800 - score} points to Exceptional"
    elif score >= 670:
        band, next_milestone = "Good", f"{740 - score} points to Very Good"
    elif score >= 580:
        band, next_milestone = "Fair", f"{670 - score} points to Good"
    else:
        band, next_milestone = "Poor", f"{580 - score} points to Fair"

    score_pct = round((score - 300) / (850 - 300) * 100, 1)

    return {
        "status": "success",
        "message": f"Credit score: {score} ({band}). Range: 300–850.",
        "data": {
            "score": score,
            "score_percentage": score_pct,           # 0–100, used by gauge widget
            "band": band,
            "min_score": 300,
            "max_score": 850,
            "next_milestone": next_milestone,
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "factors": credit_data.get("factors", []),  # → factor list widget
            "score_history": credit_data.get("history", []),  # → line chart
            "widget_type": "credit_score_gauge",
        },
    }


# ── 8. Transfer Funds ─────────────────────────────────────────────────────────


@mcp.tool()
async def transfer_funds(
    from_account_id: str,
    to_account_id: str,
    amount: float,
    memo: str = "",
) -> dict:
    """
    Transfer funds between two of the customer's accounts.
    Demo mode — balance not permanently stored.

    Args:
        from_account_id: Source account ID (e.g. "CHK-001-4521").
        to_account_id: Destination account ID (e.g. "SAV-001-8834").
        amount: Transfer amount in USD (must be > 0).
        memo: Optional note for the transfer.
    """
    if not _authorized():
        return _unauth()

    uid = _user_id()
    accounts = DEMO_ACCOUNTS.get(uid, DEMO_ACCOUNTS["user_001"])

    from_acc = next((a for a in accounts if a["account_id"] == from_account_id), None)
    to_acc = next((a for a in accounts if a["account_id"] == to_account_id), None)

    if not from_acc:
        return {"status": "error", "message": f"Account '{from_account_id}' not found.", "data": {}}
    if not to_acc:
        return {"status": "error", "message": f"Account '{to_account_id}' not found.", "data": {}}
    if amount <= 0:
        return {"status": "error", "message": "Transfer amount must be greater than $0.", "data": {}}
    if from_acc.get("balance", 0) < amount:
        return {
            "status": "error",
            "message": f"Insufficient funds. Available balance: ${from_acc['balance']:,.2f}.",
            "data": {},
        }

    ref = f"TRF-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    return {
        "status": "success",
        "message": f"Transferred ${amount:,.2f} from {from_acc['name']} to {to_acc['name']}. Ref: {ref}.",
        "data": {
            "reference_number": ref,
            "from_account": {"id": from_acc["account_id"], "name": from_acc["name"]},
            "to_account": {"id": to_acc["account_id"], "name": to_acc["name"]},
            "amount": amount,
            "memo": memo,
            "timestamp": datetime.now().isoformat(),
            "estimated_arrival": "Instant",
            "demo_note": "Balances are not permanently modified in demo mode.",
        },
    }


# ── 9. Pay Bill ───────────────────────────────────────────────────────────────


@mcp.tool()
async def pay_bill(
    biller_name: str,
    amount: float,
    from_account_id: str,
    scheduled_date: str = None,
) -> dict:
    """
    Pay a bill or schedule a future payment.
    Demo mode — payment is simulated.

    Args:
        biller_name: Name of biller (e.g. "AT&T", "Comcast", "Con Edison").
        amount: Payment amount in USD.
        from_account_id: Account to pay from (e.g. "CHK-001-4521").
        scheduled_date: Optional future date "YYYY-MM-DD". Defaults to today.
    """
    if not _authorized():
        return _unauth()

    uid = _user_id()
    accounts = DEMO_ACCOUNTS.get(uid, DEMO_ACCOUNTS["user_001"])
    acc = next((a for a in accounts if a["account_id"] == from_account_id), None)

    if not acc:
        return {"status": "error", "message": f"Account '{from_account_id}' not found.", "data": {}}
    if amount <= 0:
        return {"status": "error", "message": "Payment amount must be greater than $0.", "data": {}}

    today = datetime.now().strftime("%Y-%m-%d")
    pay_date = scheduled_date or today
    is_future = pay_date > today
    conf = f"BILL-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    return {
        "status": "success",
        "message": (
            f"Scheduled: ${amount:,.2f} to {biller_name} on {pay_date}. Confirmation: {conf}."
            if is_future
            else f"Paid: ${amount:,.2f} to {biller_name}. Confirmation: {conf}."
        ),
        "data": {
            "confirmation_number": conf,
            "biller": biller_name,
            "amount": amount,
            "from_account": {"id": acc["account_id"], "name": acc["name"]},
            "payment_date": pay_date,
            "status": "scheduled" if is_future else "processed",
            "is_scheduled": is_future,
        },
    }


# ── 10. Fraud Alerts ──────────────────────────────────────────────────────────


@mcp.tool()
async def get_fraud_alerts() -> dict:
    """
    Get recent security alerts, suspicious transaction flags, and account events.
    Unresolved alerts require customer action.
    """
    if not _authorized():
        return _unauth()

    uid = _user_id()
    alerts = DEMO_FRAUD_ALERTS.get(uid, [])
    unresolved = [a for a in alerts if not a["resolved"]]
    resolved = [a for a in alerts if a["resolved"]]

    return {
        "status": "partial" if unresolved else "success",
        "message": (
            f"⚠️ {len(unresolved)} unresolved alert(s) require your attention."
            if unresolved
            else f"No active alerts. {len(resolved)} resolved alert(s) on record."
        ),
        "data": {
            "total_alerts": len(alerts),
            "unresolved_count": len(unresolved),
            "resolved_count": len(resolved),
            "unresolved_alerts": unresolved,
            "resolved_alerts": resolved,
            "widget_type": "fraud_alerts",
        },
    }


# ── 11. Find ATM / Branch ─────────────────────────────────────────────────────


@mcp.tool()
async def find_atm_branch(zip_code: str = "78701", radius_miles: int = 5) -> dict:
    """
    Find nearby ACME Bank ATMs and branch locations.

    Args:
        zip_code: ZIP code to search near. Default: "78701" (Austin, TX).
        radius_miles: Search radius in miles (1–25). Default: 5.
    """
    if not _authorized():
        return _unauth()

    locations = DEMO_LOCATIONS.get(zip_code, DEMO_LOCATIONS["default"])
    branches = [l for l in locations if l["type"] == "branch"]
    atms = [l for l in locations if l["type"] == "atm"]

    return {
        "status": "success",
        "message": f"Found {len(branches)} branch(es) and {len(atms)} ATM(s) within {radius_miles} miles of {zip_code}.",
        "data": {
            "zip_code": zip_code,
            "radius_miles": radius_miles,
            "branch_count": len(branches),
            "atm_count": len(atms),
            "branches": branches,
            "atms": atms,
            "widget_type": "location_map",
        },
    }


# ── 12. Exchange Rates ────────────────────────────────────────────────────────


@mcp.tool()
async def get_exchange_rates(base_currency: str = "USD") -> dict:
    """
    Get current foreign exchange rates for major currencies.
    Useful for international transfers and travel planning.

    Args:
        base_currency: Base currency code. Options: "USD", "EUR", "GBP". Default: "USD".
    """
    if not _authorized():
        return _unauth()

    base = base_currency.upper()
    rates = DEMO_FX_RATES.get(base, DEMO_FX_RATES["USD"])

    rate_list = [
        {"currency": cur, "rate": rate, "inverse": round(1 / rate, 6)}
        for cur, rate in rates.items()
    ]

    return {
        "status": "success",
        "message": f"Exchange rates for {base} — {len(rate_list)} currencies. Updated: 2026-06-05 09:00 UTC.",
        "data": {
            "base_currency": base,
            "last_updated": "2026-06-05T09:00:00Z",
            "rate_count": len(rate_list),
            "rates": rate_list,              # → rates table widget
            "widget_type": "exchange_rates",
        },
    }


# ── 13. Apply for Loan ────────────────────────────────────────────────────────


@mcp.tool()
async def apply_for_loan(
    loan_type: str,
    requested_amount: float,
    term_months: int,
    purpose: str = "",
) -> dict:
    """
    Submit a loan application and receive an instant pre-approval decision
    with estimated APR and monthly payment.

    Args:
        loan_type: "personal", "auto", "home_equity", or "mortgage".
        requested_amount: Loan amount in USD.
        term_months: Loan term in months (e.g. 36, 60, 120, 360).
        purpose: Optional description of loan purpose.
    """
    if not _authorized():
        return _unauth()

    valid_types = ("personal", "auto", "home_equity", "mortgage")
    if loan_type not in valid_types:
        return {
            "status": "error",
            "message": f"Invalid loan type. Valid options: {', '.join(valid_types)}.",
            "data": {},
        }

    uid = _user_id()
    user = DEMO_USERS.get(uid, DEMO_USERS["user_001"])
    score = user["credit_score"]

    base_rates = {"personal": 9.5, "auto": 5.9, "home_equity": 7.2, "mortgage": 6.8}
    adjustments = {800: -2.0, 740: -1.0, 670: 0.0, 580: 2.5, 0: 5.0}

    adj = next(v for k, v in sorted(adjustments.items(), reverse=True) if score >= k)
    apr = round(base_rates[loan_type] + adj, 2)

    monthly_rate = apr / 100 / 12
    if monthly_rate > 0:
        monthly = round(
            requested_amount * monthly_rate / (1 - (1 + monthly_rate) ** -term_months), 2
        )
    else:
        monthly = round(requested_amount / term_months, 2)

    total_paid = monthly * term_months
    total_interest = round(total_paid - requested_amount, 2)
    approved = score >= 620 and requested_amount <= 2_000_000

    app_id = f"LOAN-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    return {
        "status": "success",
        "message": (
            f"Pre-approved! ${requested_amount:,.2f} {loan_type} loan at {apr}% APR — "
            f"${monthly:,.2f}/month for {term_months} months. Ref: {app_id}."
            if approved
            else f"Application {app_id} submitted for manual review. A banker will contact you within 2 business days."
        ),
        "data": {
            "application_id": app_id,
            "decision": "pre_approved" if approved else "manual_review",
            "approved": approved,
            "loan_type": loan_type,
            "requested_amount": requested_amount,
            "apr": apr,
            "term_months": term_months,
            "monthly_payment": monthly if approved else None,
            "total_interest": total_interest if approved else None,
            "total_cost": round(total_paid, 2) if approved else None,
            "purpose": purpose,
            "next_steps": (
                ["Sign loan agreement", "Funds disbursed within 1 business day"]
                if approved
                else ["Await banker call", "Prepare income documentation"]
            ),
            "widget_type": "loan_application_result",
        },
    }


# ── 14. Set Spending Alert ────────────────────────────────────────────────────


@mcp.tool()
async def set_spending_alert(category: str, monthly_limit: float) -> dict:
    """
    Set a monthly spending alert for a category. Notifications fire at 80% and 100%.

    Args:
        category: Category name — "Groceries", "Dining", "Transportation",
                  "Entertainment", "Shopping", "Healthcare", "Utilities",
                  "Travel", or "Education".
        monthly_limit: Monthly spending cap in USD.
    """
    if not _authorized():
        return _unauth()

    valid = ["Groceries", "Dining", "Transportation", "Entertainment",
             "Shopping", "Healthcare", "Utilities", "Travel", "Education"]
    matched = next((c for c in valid if c.lower() == category.lower()), None)

    if not matched:
        return {
            "status": "error",
            "message": f"Unknown category '{category}'. Valid options: {', '.join(valid)}.",
            "data": {},
        }

    return {
        "status": "success",
        "message": f"Alert set: ${monthly_limit:,.2f}/month for {matched}. Notifications at 80% and 100%.",
        "data": {
            "category": matched,
            "monthly_limit": monthly_limit,
            "notify_at_80_pct": round(monthly_limit * 0.8, 2),
            "notify_at_100_pct": monthly_limit,
            "created_at": datetime.now().isoformat(),
            "active": True,
        },
    }


# ── ASGI app assembly ─────────────────────────────────────────────────────────

class NotificationFixMiddleware:
    """
    Intercepts `notifications/initialized` sent without an mcp-session-id header.

    FastMCP's streamable-HTTP transport rejects (400) any request that lacks a
    session ID, including the `notifications/initialized` notification that some
    MCP clients (including Mindset) send immediately after the initialize
    handshake — before a session is fully established.

    The MCP spec says servers MUST return 202 for valid notifications, so we
    short-circuit here and never forward these session-less notifications to
    FastMCP.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if (
            scope["type"] == "http"
            and scope.get("method") == "POST"
            and scope.get("path") == "/mcp"
        ):
            headers = {k: v for k, v in scope.get("headers", [])}
            if b"mcp-session-id" not in headers:
                # Buffer the body so we can inspect it without consuming the stream
                body = b""
                buffered: list[dict] = []
                more = True
                while more:
                    msg = await receive()
                    buffered.append(msg)
                    if msg["type"] == "http.request":
                        body += msg.get("body", b"")
                        more = msg.get("more_body", False)

                try:
                    data = json.loads(body)
                    if "id" not in data and data.get("method") == "notifications/initialized":
                        await send({"type": "http.response.start", "status": 202,
                                    "headers": [(b"content-length", b"0")]})
                        await send({"type": "http.response.body", "body": b""})
                        return
                except Exception:
                    pass

                # Not a special case — replay buffered messages and pass through
                idx = 0

                async def replay():
                    nonlocal idx
                    if idx < len(buffered):
                        m = buffered[idx]; idx += 1; return m
                    return await receive()

                await self.app(scope, replay, send)
                return

        await self.app(scope, receive, send)


def build_app():
    """
    Build the ASGI app by wrapping FastMCP's HTTP app with our middlewares.
    Tries every known FastMCP API variant so the server survives version bumps.
    """
    mcp_asgi = None
    attempts = []

    for method_name in ("sse_app", "get_asgi_app", "streamable_http_app", "http_app"):
        fn = getattr(mcp, method_name, None)
        if fn is None:
            attempts.append(f"{method_name}: not found")
            continue
        try:
            mcp_asgi = fn()
            print(f"[acme-bank-mcp] FastMCP ASGI initialised via {method_name}()")
            break
        except Exception as exc:
            attempts.append(f"{method_name}: {exc}")
            print(f"[acme-bank-mcp] {method_name}() failed: {exc}")

    if mcp_asgi is None:
        raise RuntimeError(
            f"Could not get ASGI app from FastMCP. Details: {'; '.join(attempts)}"
        )

    # Stack: NotificationFix → HeaderCapture → FastMCP
    return NotificationFixMiddleware(HeaderMiddleware(app=mcp_asgi))


# Built at import time so `uvicorn main:app` also works
app = build_app()


if __name__ == "__main__":
    print(f"[acme-bank-mcp] Starting on port {PORT}")
    print(f"[acme-bank-mcp] SSE endpoint → http://0.0.0.0:{PORT}/sse")
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
