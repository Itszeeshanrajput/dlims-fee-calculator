#!/usr/bin/env python3
"""
Unit Test Suite for DLIMS Punjab Driving License Renewal Fee Calculator
Tests renewal logic, date parsing, late fines, Dastak facilitator, and courier fees.
"""

import unittest
import datetime
from calculator import calculate_renewal, calculate_all_years_quote, format_citizen_quote, get_fine_from_expiry_date, RATES

class TestRenewalCalculations(unittest.TestCase):

    def test_active_license_no_fine(self):
        # Expiry 30 days in future -> 0 fine
        future_date = (datetime.date.today() + datetime.timedelta(days=30)).strftime("%Y-%m-%d")
        res = calculate_renewal(service="regular", category="Car/Jeep", expiry_date=future_date, years=5, include_facilitator=True, include_courier=True, include_platform=True)
        # Base: 1350 * 5 = 6750, Fine: 0, Fac: 950, Courier: 480, Plat: 15 -> Total: 8195
        self.assertEqual(res["base_license_fee"], 6750)
        self.assertEqual(res["fine_amount"], 0)
        self.assertEqual(res["facilitator_fee"], 950)
        self.assertEqual(res["courier_fee"], 480)
        self.assertEqual(res["platform_fee"], 15)
        self.assertEqual(res["total_fee"], 8195)

    def test_grace_period_no_fine(self):
        # Expired 15 days ago -> within 30-day grace period -> 0 fine
        grace_date = (datetime.date.today() - datetime.timedelta(days=15)).strftime("%Y-%m-%d")
        res = calculate_renewal(service="regular", category="M/Cycle", expiry_date=grace_date, years=1, include_facilitator=False, include_courier=True, include_platform=True)
        # Base: 450 * 1 = 450, Fine: 0, Courier: 480, Plat: 15 -> Total: 945
        self.assertEqual(res["base_license_fee"], 450)
        self.assertEqual(res["fine_amount"], 0)
        self.assertEqual(res["total_fee"], 945)

    def test_fine_1_to_3_months(self):
        # Expired 45 days ago -> 50% fine
        expired_date = (datetime.date.today() - datetime.timedelta(days=45)).strftime("%Y-%m-%d")
        res = calculate_renewal(service="regular", category="Car/Jeep", expiry_date=expired_date, years=1, include_facilitator=False, include_courier=False, include_platform=False)
        # Base: 1350, Fine: 675 -> Total: 2025
        self.assertEqual(res["base_license_fee"], 1350)
        self.assertEqual(res["fine_amount"], 675)
        self.assertEqual(res["total_fee"], 2025)

    def test_fine_3_to_12_months(self):
        # Expired 180 days ago -> 100% fine
        expired_date = (datetime.date.today() - datetime.timedelta(days=180)).strftime("%Y-%m-%d")
        res = calculate_renewal(service="regular", category="LTV", expiry_date=expired_date, years=3, include_facilitator=False, include_courier=False, include_platform=False)
        # LTV Base: 1850 * 3 = 5550, Fine: 1850 -> Total: 7400
        self.assertEqual(res["base_license_fee"], 5550)
        self.assertEqual(res["fine_amount"], 1850)
        self.assertEqual(res["total_fee"], 7400)

    def test_fine_over_1_year(self):
        # Expired 400 days ago -> 250% fine
        expired_date = (datetime.date.today() - datetime.timedelta(days=400)).strftime("%Y-%m-%d")
        res = calculate_renewal(service="regular", category="M/Cycle", expiry_date=expired_date, years=1, include_facilitator=False, include_courier=False, include_platform=False)
        # Motorcycle: 450, Fine: 1125 -> Total: 1575
        self.assertEqual(res["base_license_fee"], 450)
        self.assertEqual(res["fine_amount"], 1125)
        self.assertEqual(res["total_fee"], 1575)

    def test_international_max_3_years(self):
        # Asking for 5 years for international should clamp to 3 years
        future_date = (datetime.date.today() + datetime.timedelta(days=10)).strftime("%Y-%m-%d")
        res = calculate_renewal(service="international", category="Car/Jeep", expiry_date=future_date, years=5, include_facilitator=False, include_courier=False, include_platform=False)
        self.assertEqual(res["years"], 3)
        self.assertEqual(res["base_license_fee"], 1350 * 3)

    def test_invalid_carriage_free(self):
        # Invalid carriage is free base and free fine
        res = calculate_renewal(service="regular", category="Invalid Carriage", expiry_date="2020-01-01", years=5, include_facilitator=False, include_courier=False, include_platform=False)
        self.assertEqual(res["base_license_fee"], 0)
        self.assertEqual(res["fine_amount"], 0)
        self.assertEqual(res["total_fee"], 0)

    def test_all_years_quote_breakdown(self):
        # 1-5 years quote for Car/Jeep with valid license
        future_date = (datetime.date.today() + datetime.timedelta(days=30)).strftime("%Y-%m-%d")
        quote = calculate_all_years_quote(service="regular", category="Car/Jeep", expiry_date=future_date, include_facilitator=True, include_courier=True, include_platform=True)
        self.assertEqual(len(quote["years_breakdown"]), 5)
        # Year 1: 1350 + 950 + 480 + 15 = 2795
        self.assertEqual(quote["years_breakdown"][0]["total_fee"], 2795)
        # Year 5: 6750 + 950 + 480 + 15 = 8195
        self.assertEqual(quote["years_breakdown"][4]["total_fee"], 8195)
        # Citizen quote string
        txt = format_citizen_quote(quote, is_urdu=False)
        self.assertIn("• 1 Year:  Rs. 2,795", txt)
        self.assertIn("• 5 Years:  Rs. 8,195", txt)

        # Urdu citizen quote string
        txt_ur = format_citizen_quote(quote, is_urdu=True)
        self.assertIn("1 سال: Rs. 2,795", txt_ur)
        self.assertIn("5 سال: Rs. 8,195", txt_ur)

if __name__ == "__main__":
    unittest.main()
