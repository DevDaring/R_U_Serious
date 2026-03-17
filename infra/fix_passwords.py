import csv
from passlib.context import CryptContext

ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
new_hash = ctx.hash("password123")
print(f"New hash: {new_hash}")

# Fix users.csv
csv_path = "/mnt/funlearn-data/csv/users.csv"
rows = []
with open(csv_path, "r") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        row["password_hash"] = new_hash
        rows.append(row)
        print(f"Updated password for user: {row['username']}")

with open(csv_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

# Also fix the backend data copy
csv_path2 = "/opt/funlearn-repo/genlearn-ai/backend/data/csv/users.csv"
rows2 = []
with open(csv_path2, "r") as f:
    reader = csv.DictReader(f)
    fieldnames2 = reader.fieldnames
    for row in reader:
        row["password_hash"] = new_hash
        rows2.append(row)

with open(csv_path2, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames2)
    writer.writeheader()
    writer.writerows(rows2)

print("Done! All users now have password: password123")
