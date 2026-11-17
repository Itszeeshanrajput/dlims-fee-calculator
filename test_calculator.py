#!/usr/bin/env python3
"""
Unit Test Suite for DLIMS Punjab Driving License Fee Calculator
Verifies 100% mathematical and regulatory correctness against the official Punjab DLIMS data.
"""

import unittest
from calculator import (
    calculate_regular_fee,
    calculate_renewal_fee,
    calculate_duplicate_fee,
    calculate_international_fee,
    calculate_learner_fee,
    FEE_DATA
)

class TestDLIMSPreciseCalculations(unittest.TestCase):

    # 1. Test Regular License
    def test_regular_license_motorcycle(self):
        # M/Cycle: Test 50, Fee 450, Courier 480 -> Total incl test = 980, excl test = 930
        res = calculate_regular_fee("M/Cycle", include_test_fee=True, include_courier=True)
        self.assertEqual(res["base_license_fee"], 450)
        self.assertEqual(res["test_fee"], 50)
        self.assertEqual(res["courier_fee"], 480)
        self.assertEqual(res["total_fee"], 980)

        # Excl test
        res_no_test = calculate_regular_fee("M/Cycle", include_test_fee=False, include_courier=True)
        self.assertEqual(res_no_test["total_fee"], 930)

        # Excl courier
        res_no_courier = calculate_regular_fee("M/Cycle", include_test_fee=True, include_courier=False)
        self.assertEqual(res_no_courier["total_fee"], 500)

    def test_regular_license_car_jeep(self):
        # Car/Jeep: Test 150, Fee 1350, Courier 480 -> Total incl test = 1980
        res = calculate_regular_fee("Car/Jeep", include_test_fee=True, include_courier=True)
        self.assertEqual(res["base_license_fee"], 1350)
        self.assertEqual(res["test_fee"], 150)
        self.assertEqual(res["courier_fee"], 480)
        self.assertEqual(res["total_fee"], 1980)

    def test_regular_license_combo(self):
        # M/Cycle+Car/Jeep: Test 200, Fee 1350, Courier 480 -> Total = 2030
        res = calculate_regular_fee("M/Cycle+Car/Jeep", include_test_fee=True, include_courier=True)
        self.assertEqual(res["base_license_fee"], 1350)
        self.assertEqual(res["test_fee"], 200)
        self.assertEqual(res["courier_fee"], 480)
        self.assertEqual(res["total_fee"], 2030)

    def test_regular_license_invalid_carriage(self):
        # Invalid carriage: Free fee, Free test, 480 courier
        res = calculate_regular_fee("Invalid Carriage", include_test_fee=True, include_courier=True)
        self.assertEqual(res["base_license_fee"], 0)
        self.assertEqual(res["test_fee"], 0)
        self.assertEqual(res["courier_fee"], 480)
        self.assertEqual(res["total_fee"], 480)

    # 2. Test Renewal & Fines
    def test_renewal_motorcycle_fines(self):
        # Base annual: 450, Courier: 480
        # No fine: 450 + 480 = 930
        r0 = calculate_renewal_fee("M/Cycle", validity_years=1, fine_status="none")
        self.assertEqual(r0["total_fee"], 930)
        self.assertEqual(r0["fine"], 0)

        # 1-3 months fine (50% = 225): 450 + 225 + 480 = 1155
        r1 = calculate_renewal_fee("M/Cycle", validity_years=1, fine_status="1_to_3m")
        self.assertEqual(r1["fine"], 225)
        self.assertEqual(r1["total_fee"], 1155)

        # 3-12 months fine (100% = 450): 450 + 450 + 480 = 1380
        r2 = calculate_renewal_fee("M/Cycle", validity_years=1, fine_status="3m_to_1y")
        self.assertEqual(r2["fine"], 450)
        self.assertEqual(r2["total_fee"], 1380)

        # >1 year fine (250% = 1125): 450 + 1125 + 480 = 2055
        r3 = calculate_renewal_fee("M/Cycle", validity_years=1, fine_status="over_1y")
        self.assertEqual(r3["fine"], 1125)
        self.assertEqual(r3["total_fee"], 2055)

        # 5 Years validity on time: 450*5 = 2250 + 480 = 2730
        r5 = calculate_renewal_fee("M/Cycle", validity_years=5, fine_status="none")
        self.assertEqual(r5["base_license_fee"], 2250)
        self.assertEqual(r5["total_fee"], 2730)

    def test_renewal_car_jeep_5_years(self):
        # Car/Jeep: 1350/yr * 5 = 6750 + 480 courier = 7230
        res = calculate_renewal_fee("Car/Jeep", validity_years=5, fine_status="none")
        self.assertEqual(res["base_license_fee"], 6750)
        self.assertEqual(res["total_fee"], 7230)

        # Expired 3m-1y (100% fine = 1350): 6750 + 1350 + 480 = 8580
        res_fine = calculate_renewal_fee("Car/Jeep", validity_years=5, fine_status="3m_to_1y")
        self.assertEqual(res_fine["fine"], 1350)
        self.assertEqual(res_fine["total_fee"], 8580)

    # 3. Test Duplicate License
    def test_duplicate_licenses(self):
        # M/Cycle duplicate: 100 + 480 = 580
        res_bike = calculate_duplicate_fee("M/Cycle")
        self.assertEqual(res_bike["base_license_fee"], 100)
        self.assertEqual(res_bike["total_fee"], 580)

        # Car/Jeep duplicate: 150 + 480 = 630
        res_car = calculate_duplicate_fee("Car/Jeep")
        self.assertEqual(res_car["base_license_fee"], 150)
        self.assertEqual(res_car["total_fee"], 630)

        # HTV duplicate: 200 + 480 = 680
        res_htv = calculate_duplicate_fee("HTV")
        self.assertEqual(res_htv["base_license_fee"], 200)
        self.assertEqual(res_htv["total_fee"], 680)

    # 4. Test International License
    def test_international_license(self):
        # Car/Jeep 1 Year: 1350 + 480 = 1830
        res_1y = calculate_international_fee("Car/Jeep", validity_years=1)
        self.assertEqual(res_1y["base_license_fee"], 1350)
        self.assertEqual(res_1y["total_fee"], 1830)

        # Car/Jeep 3 Years: 4050 + 480 = 4530
        res_3y = calculate_international_fee("Car/Jeep", validity_years=3)
        self.assertEqual(res_3y["base_license_fee"], 4050)
        self.assertEqual(res_3y["total_fee"], 4530)

        # LTV 3 Years: 5550 + 480 = 6030
        res_ltv = calculate_international_fee("LTV", validity_years=3)
        self.assertEqual(res_ltv["base_license_fee"], 5550)
        self.assertEqual(res_ltv["total_fee"], 6030)

    # 5. Test Learner Driving License
    def test_learner_license(self):
        # 1 Category: Rs. 500
        res_1 = calculate_learner_fee(["M/Cycle"])
        self.assertEqual(res_1["total_fee"], 500)

        # 2 Categories (Bike + Car): Rs. 1000
        res_2 = calculate_learner_fee(["M/Cycle", "Car/Jeep"])
        self.assertEqual(res_2["total_fee"], 1000)

        # 3 Categories (Bike + Car + LTV): Rs. 1500
        res_3 = calculate_learner_fee(["M/Cycle", "Car/Jeep", "LTV"])
        self.assertEqual(res_3["total_fee"], 1500)

if __name__ == "__main__":
    unittest.main()
