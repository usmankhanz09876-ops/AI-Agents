import openpyxl
from datetime import date, timedelta

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Budget"
ws.append(["Date", "Type", "Category", "Amount", "Description"])

entries = [
    (date.today() - timedelta(days=20), "income",  "Salary",        3000, "Monthly salary"),
    (date.today() - timedelta(days=19), "expense", "Food",           200, "Grocery shopping"),
    (date.today() - timedelta(days=18), "expense", "Rent",           900, "Monthly rent"),
    (date.today() - timedelta(days=17), "expense", "Food",           150, "Restaurants"),
    (date.today() - timedelta(days=15), "expense", "Transport",       80, "Gas and bus"),
    (date.today() - timedelta(days=14), "income",  "Freelance",      500, "Web design project"),
    (date.today() - timedelta(days=12), "expense", "Entertainment",  120, "Netflix and games"),
    (date.today() - timedelta(days=10), "expense", "Food",           100, "Weekly groceries"),
    (date.today() - timedelta(days=8),  "expense", "Health",          60, "Gym membership"),
    (date.today() - timedelta(days=6),  "expense", "Utilities",      110, "Electricity and water"),
    (date.today() - timedelta(days=4),  "expense", "Food",            90, "Takeout orders"),
    (date.today() - timedelta(days=2),  "expense", "Shopping",       200, "Clothes and accessories"),
    (date.today() - timedelta(days=1),  "income",  "Bonus",          300, "Performance bonus"),
    (date.today(),                      "expense", "Transport",       40, "Uber rides"),
]

for e in entries:
    ws.append([str(e[0]), e[1], e[2], e[3], e[4]])

wb.save("budget.xlsx")
print("Done — budget.xlsx created with", len(entries), "entries")
