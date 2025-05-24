!pip install pandas
import pandas as pd
import zipfile
import os

# Define the data types for specific columns
dtype_spec = {
    'column1': 'string',
    'column2': 'string',
    'column3': 'float64',
    'column4': 'float64',
    'column5': 'float64',
    'column6': 'string',
    'column7': 'float64',
    'column8': 'float64',
    'column9': 'int64'
}

data = pd.read_csv(r'C:\Users\eliri\OneDrive\Desktop\Total.csv', dtype=dtype_spec, low_memory=False)

def display_employee_information(EmployeeName):
    return data[data['EmployeeName'] == 'ALSON LEE']
#print(display_employee_information('ALSON LEE'))

try:
    # Map employee name to salary
    salary_dict = dict(zip(data['EmployeeName'], data['TotalPayBenefits']))
    print("Salary dictionary created.")
except Exception as e:
    print(f"Error creating salary dictionary: {e}")

#Export Employee Details to CSV and Zip
def export_employee_profile(name):
        details = display_employee_information(name)
        if isinstance(details, pd.DataFrame) and not details.empty:
            csv_filename = f"{name.replace(' ', '_')}_profile.csv"
            zip_filename = "Employee Profile.zip"
            # Export to CSV
            details.to_csv(csv_filename, index=False)
            # Zip the CSV
            with zipfile.ZipFile(zip_filename, 'w') as zip_doc:
                zip_doc.write(csv_filename)
            # Remove the CSV after zipping
            os.remove(csv_filename)
            print(f"Profile for {name} exported and zipped as '{zip_filename}'.")
        else:
            print(details)


employee_name = "ALSON LEE"
print(display_employee_information(employee_name))
export_employee_profile(employee_name)

#Unzip the folder and display the data in R

unzip("Employee Profile.zip", exdir = "Employee_Profile")
csv_file <- list.files("Employee_Profile", pattern = "\\.csv$", full.names = TRUE)[1]
employee_data <- read.csv(csv_file)
print(employee_data)