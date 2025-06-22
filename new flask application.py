#%%
#pip install flask
#pip install pymongo
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

#  to Initialize Flask app
app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['user_data']
collection = db['entries']

#Home route to display form and handle submissions
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = {
             #  to Collect and format data from the form
            "age": request.form("age"),
            "gender": request.form("gender"),
            "total_income": request.form("income"),
            "expenses": {
                category: float(request.form.get(f"{category}_amount", 0))
                for category in ["utilities", "entertainment", "school_fees", "shopping", "healthcare"]
                if request.form.get(category)
            }
        }
        collection.insert_one(data)
        return redirect("/")
    return render_template("form.html")

# Run the app
if __name__ == "__main__":
    app.run(port =5000, debug=True)

import csv
from pymongo import MongoClient

# Define a User class to structure the data
class User:
    def __init__(self, age, gender, income, expenses):
        self.age = age
        self.gender = gender
        self.income = income
        self.expenses = expenses

# Function to export data from MongoDB to CSV
def export_to_csv():
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    collection = client['user_data']['entries']

    # Query all documents
    data = collection.find()

    # Create and write to CSV file
    with open("user_data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        # Write header row
        writer.writerow(["Age", "Gender", "Total Income", "Utilities", "Entertainment", "School Fees", "Shopping", "Healthcare"])

        # Loop through each MongoDB document
        for item in data:
            user = User(item["age"], item["gender"], item["total_income"], item["expenses"])
            # Prepare row with default 0 values for missing categories
            row = [
                user.age, user.gender, user.income,
                user.expenses.get("utilities", 0),
                user.expenses.get("entertainment", 0),
                user.expenses.get("school_fees", 0),
                user.expenses.get("shopping", 0),
                user.expenses.get("healthcare", 0),
            ]
            writer.writerow(row)

# Run the export function
export_to_csv()

# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv("user_data.csv")

# ----- Chart 1: Ages with the highest average income -----
plt.figure(figsize=(10, 6))
# Group by age and calculate mean income
top_income = df.groupby("Age")["Total Income"].mean().sort_values(ascending=False).head(10)
# Plot
sns.barplot(x=top_income.index, y=top_income.values)
plt.title("Top 10 Ages by Average Income")
plt.xlabel("Age")
plt.ylabel("Average Income")
plt.tight_layout()
plt.savefig("top_ages_income.png")
plt.show()

# ----- Chart 2: Gender distribution across expense categories -----
expense_cols = ["Utilities", "Entertainment", "School Fees", "Shopping", "Healthcare"]

# Reshape data to long format
melted = df.melt(id_vars=["Gender"], value_vars=expense_cols, var_name="Category", value_name="Amount")

plt.figure(figsize=(12, 6))
# Sum of expenses grouped by gender and category
sns.barplot(data=melted, x="Category", y="Amount", hue="Gender", estimator=sum)
plt.title("Gender Spending Distribution by Category")
plt.ylabel("Total Amount Spent")
plt.tight_layout()
plt.savefig("gender_spending.png")
plt.show()

