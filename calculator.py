#!/usr/bin/env python3
"""
DLIMS & Dastak Punjab Driving License Renewal Fee Calculator
Accurate renewal and international renewal fee calculation based on Issue/Expiry dates,
duration (1 to 5 years), Rs. 950 Dastak Doorstep Facilitator, and Rs. 480 Courier delivery.
"""

import datetime
import json
import os
import sys

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dlims_fee_data.json")

# Category Renewal Base Rates per Annum
RATES = {
    "m/cycle": {"name": "Motorcycle (M/Cycle)", "rate_1yr": 450, "fine_50": 225, "fine_100": 450, "fine_250": 1125},
    "car/jeep": {"name": "Motor Car / Jeep", "rate_1yr": 1350, "fine_50": 675, "fine_100": 1350, "fine_250": 3375},
    "m/cycle+car/jeep": {"name": "Motorcycle + Car/Jeep", "rate_1yr": 1350, "fine_50": 675, "fine_100": 1350, "fine_250": 3375},
    "m/cycle+m/car": {"name": "Motorcycle + Motor Car", "rate_1yr": 1350, "fine_50": 675, "fine_100": 1350, "fine_250": 3375},
    "ltv": {"name": "LTV (Light Transport)", "rate_1yr": 1850, "fine_50": 925, "fine_100": 1850, "fine_250": 4625},
    "m/cycle+ltv": {"name": "Motorcycle + LTV", "rate_1yr": 1850, "fine_50": 925, "fine_100": 1850, "fine_250": 4625},
    "htv": {"name": "HTV (Heavy Transport)", "rate_1yr": 1850, "fine_50": 925, "fine_100": 1850, "fine_250": 4625},
    "ltv + psv": {"name": "LTV + PSV (Commercial)", "rate_1yr": 1850, "fine_50": 925, "fine_100": 1850, "fine_250": 4625},
    "htv + psv": {"name": "HTV + PSV (Commercial)", "rate_1yr": 1850, "fine_50": 925, "fine_100": 1850, "fine_250": 4625},
    "m/cycle+psv": {"name": "Motorcycle + PSV", "rate_1yr": 1850, "fine_50": 925, "fine_100": 1850, "fine_250": 4625},
    "m/cycle+ltv+trac com": {"name": "Motorcycle + LTV + Tractor Com", "rate_1yr": 1850, "fine_50": 925, "fine_100": 1850, "fine_250": 4625},
    "rickshaw": {"name": "Rickshaw", "rate_1yr": 400, "fine_50": 200, "fine_100": 400, "fine_250": 1000},
    "tractor commercial": {"name": "Tractor Commercial", "rate_1yr": 1400, "fine_50": 700, "fine_100": 1400, "fine_250": 3500},
    "tractor agri": {"name": "Tractor Agriculture", "rate_1yr": 950, "fine_50": 475, "fine_100": 950, "fine_250": 2375},
    "agriculture": {"name": "Agriculture (Other)", "rate_1yr": 1350, "fine_50": 675, "fine_100": 1350, "fine_250": 3375},
    "invalid carriage": {"name": "Invalid Carriage", "rate_1yr": 0, "fine_50": 0, "fine_100": 0, "fine_250": 0}
}

COURIER_FEE = 480
FACILITATOR_FEE = 950
PLATFORM_FEE = 15

def get_fine_from_expiry_date(expiry_date_str, category_info):
    if not expiry_date_str:
        return 0, "No Expiry Date Specified (0% Fine)"
    
    try:
        expiry = datetime.datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
    except ValueError:
        return 0, "Invalid Date Format"

    today = datetime.date.today()
    diff_days = (today - expiry).days

    if diff_days <= 0:
        return 0, f"Valid / Active ({abs(diff_days)} days remaining)"
    elif diff_days <= 30:
        return 0, f"Within 30-Day Grace Period (Expired {diff_days} days ago)"
    elif diff_days <= 90:
        return category_info["fine_50"], f"1 to 3 Months Overdue (50% Fine: Rs. {category_info['fine_50']})"
    elif diff_days <= 365:
        return category_info["fine_100"], f"3 Months to 1 Year Overdue (100% Fine: Rs. {category_info['fine_100']})"
    else:
        return category_info["fine_250"], f"Over 1 Year Overdue (250% Fine: Rs. {category_info['fine_250']})"

def calculate_renewal(
    service="regular", # 'regular' or 'international'
    category="Car/Jeep",
    issue_date=None,
    expiry_date=None,
    years=5,
    include_facilitator=True,
    include_courier=True,
    include_platform=True
):
    clean_cat = category.lower().replace(" ", "")
    matched = None
    for k, v in RATES.items():
        if k.replace(" ", "") == clean_cat:
            matched = v
            break
    if not matched:
        matched = RATES["car/jeep"]

    # Validate years: 1 to 5 for regular, 1 to 3 for international
    if service == "international" and years > 3:
        years = 3
    if years < 1:
        years = 1
    if years > 5:
        years = 5

    base_fee = matched["rate_1yr"] * years
    fine_amount, fine_desc = get_fine_from_expiry_date(expiry_date, matched)
    fac_fee = FACILITATOR_FEE if include_facilitator else 0
    cour_fee = COURIER_FEE if include_courier else 0
    plat_fee = PLATFORM_FEE if include_platform else 0

    total = base_fee + fine_amount + fac_fee + cour_fee + plat_fee

    return {
        "service": "Regular License Renewal" if service == "regular" else "International License Renewal",
        "category": matched["name"],
        "rate_per_annum": matched["rate_1yr"],
        "years": years,
        "base_license_fee": base_fee,
        "issue_date": issue_date,
        "expiry_date": expiry_date,
        "fine_amount": fine_amount,
        "fine_status": fine_desc,
        "facilitator_fee": fac_fee,
        "courier_fee": cour_fee,
        "platform_fee": plat_fee,
        "total_fee": total
    }

def calculate_all_years_quote(
    service="regular",
    category="Car/Jeep",
    issue_date=None,
    expiry_date=None,
    include_facilitator=True,
    include_courier=True,
    include_platform=True
):
    max_years = 3 if service == "international" else 5
    breakdown = []
    first_res = None
    for y in range(1, max_years + 1):
        res = calculate_renewal(
            service=service,
            category=category,
            issue_date=issue_date,
            expiry_date=expiry_date,
            years=y,
            include_facilitator=include_facilitator,
            include_courier=include_courier,
            include_platform=include_platform
        )
        if first_res is None:
            first_res = res
        breakdown.append({
            "years": y,
            "base_license_fee": res["base_license_fee"],
            "total_fee": res["total_fee"]
        })

    return {
        "service": first_res["service"],
        "category": first_res["category"],
        "rate_per_annum": first_res["rate_per_annum"],
        "issue_date": issue_date,
        "expiry_date": expiry_date,
        "fine_amount": first_res["fine_amount"],
        "fine_status": first_res["fine_status"],
        "facilitator_fee": first_res["facilitator_fee"],
        "courier_fee": first_res["courier_fee"],
        "platform_fee": first_res["platform_fee"],
        "years_breakdown": breakdown
    }

def format_citizen_quote(quote_data, is_urdu=False):
    if is_urdu:
        lines = [
            "*پنجاب ڈرائیونگ لائسنس تجدید - سرکاری فیس کوٹیشن*",
            f"🚗 کیٹیگری: {quote_data['category']}",
            f"📅 صورتحال: {quote_data['fine_status']}",
            f"✅ شامل اخراجات: دستک ({quote_data['facilitator_fee']} روپے) | کوریئر ({quote_data['courier_fee']} روپے) | آئی ٹی ({quote_data['platform_fee']} روپے)",
            "",
            "*کل واجب الادا رقم سال کے حساب سے:*"
        ]
        for item in quote_data["years_breakdown"]:
            best = " (⭐ تجویز کردہ)" if item["years"] == len(quote_data["years_breakdown"]) else ""
            lines.append(f"• {item['years']} سال: Rs. {item['total_fee']:,} روپے{best}")
        lines.extend([
            "",
            "💳 ادائیگی: جاز کیش، ایزی پیسہ یا موبائل بینکنگ میں 17 ہندسوں کے PSID سے کریں۔",
            "حکومت پنجاب • DLIMS اور مریم کی دستک پلیٹ فارم"
        ])
    else:
        lines = [
            "*PUNJAB DRIVING LICENSE RENEWAL - OFFICIAL QUOTE*",
            f"🚗 Category: {quote_data['category']}",
            f"📅 Status: {quote_data['fine_status']}",
            f"✅ Included: Dastak (Rs. {quote_data['facilitator_fee']}) | Courier (Rs. {quote_data['courier_fee']}) | IT (Rs. {quote_data['platform_fee']})",
            "",
            "*TOTAL PAYABLE BY DURATION:*"
        ]
        for item in quote_data["years_breakdown"]:
            best = " (⭐ Recommended - Best Value)" if item["years"] == len(quote_data["years_breakdown"]) else ""
            lines.append(f"• {item['years']} Year{'s' if item['years'] > 1 else ''}:  Rs. {item['total_fee']:,}{best}")
        lines.extend([
            "",
            "💳 Pay via 17-digit PSID on JazzCash, EasyPaisa, or 1Bill Mobile Banking.",
            "Official DLIMS Punjab & Maryam Ki Dastak Platform"
        ])
    return "\n".join(lines)

def print_renewal_slip(result):
    print("=" * 60)
    print("      GOVERNMENT OF PUNJAB - DLIMS & DASTAK 2.0     ")
    print("           DRIVING LICENSE RENEWAL SLIP             ")
    print("=" * 60)
    print(f" Service:            {result['service']}")
    print(f" Vehicle Category:   {result['category']}")
    print(f" Renewal Duration:   {result['years']} Year(s)")
    if result.get("issue_date"):
        print(f" License Issue Date: {result['issue_date']}")
    if result.get("expiry_date"):
        print(f" License Expiry Date:{result['expiry_date']}")
        print(f" Expiry Status:      {result['fine_status']}")
    print("-" * 60)
    print(f" Base Government Fee ({result['rate_per_annum']} × {result['years']}y): Rs. {result['base_license_fee']:,}")
    if result['fine_amount'] > 0:
        print(f" Late Renewal Penalty:                 Rs. {result['fine_amount']:,}")
    print(f" Dastak Doorstep Facilitator Fee:       Rs. {result['facilitator_fee']:,}")
    print(f" Smart Card Courier Delivery Fee:       Rs. {result['courier_fee']:,}")
    print(f" Platform / IT Service Fee:             Rs. {result['platform_fee']:,}")
    print("-" * 60)
    print(f" TOTAL AMOUNT PAYABLE:                  Rs. {result['total_fee']:,} PKR")
    print("=" * 60)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Punjab License Renewal Calculator")
    parser.add_argument("--service", choices=["regular", "international"], default="regular", help="regular or international renewal")
    parser.add_argument("--cat", default="Car/Jeep", help="Vehicle category")
    parser.add_argument("--issue", default="2021-11-17", help="Issue date YYYY-MM-DD")
    parser.add_argument("--expiry", default="2026-11-17", help="Expiry date YYYY-MM-DD")
    parser.add_argument("--years", type=int, default=5, choices=[1, 2, 3, 4, 5], help="Renewal duration in years")
    parser.add_argument("--no-facilitator", action="store_true", help="Exclude Rs. 950 facilitator")
    parser.add_argument("--no-courier", action="store_true", help="Exclude Rs. 480 courier")

    parser.add_argument("--all-years", action="store_true", help="Generate 1-5 years quote for citizens")

    args = parser.parse_args()
    if args.all_years:
        quote = calculate_all_years_quote(
            service=args.service,
            category=args.cat,
            issue_date=args.issue,
            expiry_date=args.expiry,
            include_facilitator=not args.no_facilitator,
            include_courier=not args.no_courier
        )
        print(format_citizen_quote(quote))
    else:
        res = calculate_renewal(
            service=args.service,
            category=args.cat,
            issue_date=args.issue,
            expiry_date=args.expiry,
            years=args.years,
            include_facilitator=not args.no_facilitator,
            include_courier=not args.no_courier
        )
        print_renewal_slip(res)
