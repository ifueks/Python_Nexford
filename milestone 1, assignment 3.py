from datetime import datetime

#Create separate classes for policyholders, products, and payments.
class policyholders:
    def __init__(self, policy_id, name, policy_type, Policy_date, date_of_birth, city) :
        #to add attributes
        self.policy_id = policy_id
        self.name = name
        self.policy_type = policy_type
        self.Policy_date = Policy_date
        self.date_of_birth = date_of_birth
        self.city = city
        self.active = True
        #to hold multiple  policies
        self.policies =[]

     #instance method
     #to add a new policy to a policyholder
    def Update_policy(self, policy_id= None, policy_type =None):
        if policy_id:
            self.policy_id = policy_id
        if policy_type :
            self.policy_type = policy_type
            print(f"{self.name}'s policy updated: Policy ID = {self.policy_id}, Type = {self.policy_type}")

    #to register a new policyholder
    def register(self,product):
        self.policies.append(product)
        print(f"{self.name} (ID: {self.policy_id}) registered successfully.")

    #to suspend policy
    def suspend(self):
        self.active = False
        print(f"{self.name} (ID: {self.policyholder_id}) has been suspended successfully.")

    #to reactivate policy
    def reactivate(self):
        self.active = True
        print(f"{self.name} (ID: {self.policyholder_id}) has been reactivated successfully.")

    #to display the policyholder details
    def display_details(self):
        status = "Active" if self.active else "Suspended"
        print(f"ID: {self.policy_id} | Name: {self.name} | Type: {self.policy_type} | Status: {status} | "
              f"Policy Date: {self.Policy_date} | DOB: {self.date_of_birth} | City: {self.city}")

    #to display policyholder account details
    def get_account_details(self):
        print(f"Account details for {self.name}:")
        self.display_details()
        print("Policies:", self.policies)
        print("Payments:", [f"{p.payment_id}: ${p.amount}" for p in self.payments])


class products:
    def __init__(self, product_id, product_name, coverage_amount, premium):
        self.product_id = product_id
        self.product_name = product_name
        self.coverage_amount = coverage_amount
        self.premium = premium
        self.status = "Active"

    #to create_product
    def create_product(self):
        print(f"Product {self.product_name} created with ID {self.product_id}, coverage {self.coverage_amount}, premium {self.premium}")

    #to update_product
    def update_product(self, new_name=None, new_coverage=None, new_premium=None):
        if new_name:
            self.product_name = new_name
        if new_coverage:
            self.coverage_amount = new_coverage
        if new_premium:
            self.premium = new_premium
        print(f"Product {self.product_name}, {self.product_id} has been updated.")

    #to suspend product
    def suspend_policy_products(self):
        self.status = "Suspended"
        print(f"Product {self.product_id} has been suspended.")

    #add a policy (product) to a policyholder.
    def add_products(self,products):
        self.products.append(products)

class Payment:
    def __init__(self, payment_id, policyholder, product, payment_amount, due_date):
        self.payment_id = payment_id
        self.policyholder = policyholder
        self.product = product
        self.amount = payment_amount
        self.due_date = datetime.strptime(due_date, "%Y-%m-%d")
        self.payment_date = datetime.now()

    #to process payment
    def process_payment(self):
        days_late = (self.payment_date - self.due_date).days
        if days_late > 0:
            self.apply_penalty(days_late)
        if not hasattr(self.policyholder, 'payments'):
            self.policyholder.payments = []
        self.policyholder.payments.append(self)
        print(f"Payment of ${self.amount:.2f} processed for {self.policyholder.name} on {self.payment_date.date()}")

    #to set payment reminders
    def payment_reminder(self):
        days_left = (self.due_date - datetime.now()).days
        if days_left < 0:
            print(f"{self.policyholder.name}, your payment of ${self.amount} is overdue by {-days_left} days!")
        else:
            print(f"{self.policyholder.name}, your payment of ${self.amount} is due in {days_left} days.")

    # to apply penalty for late payments
    def apply_penalty(self, days_late):
        if days_late > 0:
            penalty = 0.02 * self.amount * days_late
            self.amount += penalty
            print(f"late payment Penalty of ${penalty} applied. New amount: ${self.amount}")
        else:
            print("No penalty applied.")


#create policyholders
ph1 = policyholders("P1001", "Alice Johnson", "Life Insurance", "2023-06-15", "1990-03-12", "Calgary")
ph2 = policyholders("P1002", "Brian Smith", "Health Insurance", "2024-01-10", "1985-11-02", "Edmonton")
ph3 = policyholders("P1003", "Carla Mendes", "Auto Insurance", "2023-09-30", "1992-07-19", "Toronto")
ph4 = policyholders("P1004", "David Lee", "Home Insurance", "2022-12-05", "1978-04-27", "Vancouver")
ph5 = policyholders("P1005", "Emily Davis", "Travel Insurance", "2025-03-21", "1995-08-15", "Winnipeg")


#create new insurance products
product1 = products(101, "Life Insurance", 100000, 1000)
product2 = products(102, "Health Insurance", 50000, 1500)
product3 = products(103, "Car Insurance", 40000, 1200)
product4 = products(104, "House Insurance", 40000, 1200)
product5 = products(105, "Employment Insurance", 40000, 1200)
product1.create_product()
product2.create_product()
product3.create_product()
product4.create_product()
product5.create_product()

# Assign products
ph1.register("Life Insurance")
ph2.register("Health Insurance")

# Process payment
payment1 = Payment("PAY001", ph1, product1, 1000, "2025-05-01")
payment1.process_payment()

payment2 = Payment("PAY002", ph2, product2, 1500, "2025-05-10")
payment2.process_payment()

# Update and suspend product
product2.update_product(new_premium=1600)
product1.suspend_policy_products()

# Send reminders
reminder1 = Payment("PAY003", ph4, product4, 200, "2025-05-25")
reminder1.payment_reminder()

reminder2 = Payment("PAY004", ph5, product5, 230, "2025-05-25")
reminder2.payment_reminder()

# Display account details
ph1.get_account_details()
ph2.get_account_details()
