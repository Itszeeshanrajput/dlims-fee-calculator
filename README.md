# DLIMS Punjab Driving License Fee Calculator

An official, 100% accurate, modern, web-based fee calculator for the Punjab Driving License Information Management System (**DLIMS 2.0**), built directly from official data at:
🔗 **https://dlims.punjab.gov.pk/fee_structure**

---

## ✨ Features

- **Few-Clicks Interaction**: Calculate fees in just 1 to 2 clicks with quick presets and an intuitive visual stepper.
- **Dedicated Renewal Fee Engine**:
  - Choose between **1-Year, 3-Year, or 5-Year** validity periods.
  - **Late Renewal Fine Calculator**: Calculates exact penalties:
    - *Within 30 Days (On Time)*: No Fine (Rs. 0)
    - *Expired 1 to 3 Months*: **50% Fine** of 1-year license fee
    - *Expired 3 Months to 1 Year*: **100% Fine** of 1-year license fee
    - *Expired Over 1 Year*: **250% Fine** of 1-year license fee
  - **Smart Expiry Date Picker**: Pick your physical card's expiry date; the calculator automatically figures out the exact overdue days and applies the correct fine bracket.
  - **Multi-Year Comparison Matrix**: Live view of 1-Year vs 3-Year vs 5-Year fees side-by-side for your selected category.
- **All Service Types Supported**:
  1. 🔄 **Regular License Renewal**
  2. 🆕 **New Regular Driving License** (with test fee toggle)
  3. 📑 **Duplicate License** (Lost / Stolen / Damaged)
  4. 🌍 **International Driving Permit** (1 Year or 3 Years)
  5. 🔰 **Learner Driving Permit** (Multi-category selector, Rs. 500 per category)
  6. ➕ **Category Endorsement** (Adding a new vehicle class)
- **All Vehicle Categories (15 Categories)**:
  - Motorcycle (M/Cycle)
  - Motor Car / Jeep
  - Motorcycle + Car / Jeep Combo
  - LTV (Light Transport Vehicle)
  - Motorcycle + LTV
  - HTV (Heavy Transport Vehicle)
  - LTV + PSV (Public Service Vehicle)
  - HTV + PSV
  - Motorcycle + PSV
  - Motorcycle + LTV + Tractor Commercial
  - Rickshaw (Three-Wheeler)
  - Tractor Commercial
  - Tractor Agriculture
  - Agriculture (Other)
  - Invalid Carriage (Free for Persons with Disabilities)
- **Postal Courier Delivery**:
  - Includes standard DLIMS **Rs. 480 courier fee** (with option to toggle off for self-collection or digital e-License).
- **Highest Fee Category Rule**:
  - Properly applies the DLIMS rule where combined categories (e.g. Motorcycle + Car) are charged based on the highest category rate.
- **Bilingual English / Urdu (اردو)**: Full RTL support and translation for Pakistani citizens.
- **Printable Challan & Fee Receipt**: Ready-to-print official fee slip format with breakdown.
- **Lightweight Built-in Server & REST API**: Run locally with Python, query fees via JSON REST API.

---

## 🚀 Quick Start

### 1. Open the Web Application
You can open `index.html` directly in any web browser, or launch the built-in Python web server:

```bash
cd /root/dlims-fee-calculator
python3 server.py 8080
```

Then visit:
👉 **http://localhost:8080**

---

### 2. Command Line Interface (CLI)

Run calculation directly in your terminal:

```bash
# Calculate 5-Year Renewal for Car/Jeep (on time)
python3 calculator.py --type renewal --cat "Car/Jeep" --years 5

# Calculate 1-Year Renewal with 1-3 months late fine
python3 calculator.py --type renewal --cat "Car/Jeep" --years 1 --fine 1_to_3m

# Calculate New Motorcycle + Car Combo License
python3 calculator.py --type regular --cat "M/Cycle+Car/Jeep"

# Calculate Learner Permit for Bike and Car
python3 calculator.py --type learner --learner-cats "M/Cycle" "Car/Jeep"
```

---

### 3. REST API Endpoints

The web server includes an automated JSON API:

#### Calculate Fee
```http
GET /api/calculate?type=renewal&cat=Car/Jeep&years=5&fine=3m_to_1y&courier=true
```

Response:
```json
{
  "status": "success",
  "data": {
    "service": "Regular License Renewal",
    "category": "Car/Jeep",
    "validity_years": 5,
    "base_annual_fee": 1350,
    "base_license_fee": 6750,
    "fine_status": "Expired 3 Months to 1 Year (100% Fine)",
    "fine": 1350,
    "test_fee": 0,
    "courier_fee": 480,
    "total_fee": 8580,
    "notes": "Valid for 5 year(s). Fine applied: Rs. 1350."
  }
}
```

#### Get Raw Fee Structure Data
```http
GET /api/data
```

---

## 📊 Summary of Renewal Fees (DLIMS Punjab)

| Category | 1 Year Base | Courier Fee | Total 1Y (No Fine) | Fine 1-3 Mo (50%) | Fine 3-12 Mo (100%) | Fine &gt;1 Yr (250%) | 5 Year Total (No Fine) |
|---|---|---|---|---|---|---|---|
| **Motorcycle (M/Cycle)** | Rs. 450 | Rs. 480 | **Rs. 930** | Rs. 225 | Rs. 450 | Rs. 1,125 | **Rs. 2,730** |
| **Motor Car / Jeep** | Rs. 1,350 | Rs. 480 | **Rs. 1,830** | Rs. 675 | Rs. 1,350 | Rs. 3,375 | **Rs. 7,230** |
| **M/Cycle + Car/Jeep** | Rs. 1,350 | Rs. 480 | **Rs. 1,830** | Rs. 675 | Rs. 1,350 | Rs. 3,375 | **Rs. 7,230** |
| **LTV** | Rs. 1,850 | Rs. 480 | **Rs. 2,330** | Rs. 925 | Rs. 1,850 | Rs. 4,625 | **Rs. 9,730** |
| **HTV** | Rs. 1,850 | Rs. 480 | **Rs. 2,330** | Rs. 925 | Rs. 1,850 | Rs. 4,625 | **Rs. 9,730** |
| **Rickshaw** | Rs. 400 | Rs. 480 | **Rs. 880** | Rs. 200 | Rs. 400 | Rs. 1,000 | **Rs. 2,480** |
| **Tractor Commercial** | Rs. 1,400 | Rs. 480 | **Rs. 1,880** | Rs. 700 | Rs. 1,400 | Rs. 3,500 | **Rs. 7,480** |
| **Tractor Agriculture** | Rs. 950 | Rs. 480 | **Rs. 1,430** | Rs. 475 | Rs. 950 | Rs. 2,375 | **Rs. 5,230** |
| **Invalid Carriage** | Free (Rs. 0) | Rs. 480 | **Rs. 480** | Free (Rs. 0) | Free (Rs. 0) | Free (Rs. 0) | **Rs. 480** |

---

## 🧪 Verification & Unit Testing

Run the included automated verification test suite:

```bash
cd /root/dlims-fee-calculator
python3 test_calculator.py
```
*(All 9 unit test suites verify 100% mathematical precision against every row in DLIMS Punjab tables).*
