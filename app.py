from pathlib import Path
import fire
import questionary

from qualifier.utils.fileio import load_csv


from qualifier.utils.calculators import (
    calculate_monthly_debt_ratio,
    calculate_loan_to_value_ratio,
)
from qualifier.utils.filters.credit_score import filter_credit_score
from qualifier.utils.filters.debit_to_income import filter_debt_to_income
from qualifier.utils.filters.loan_to_value import filter_loan_to_value
from qualifier.utils.filters.max_loan import filter_max_loan_size
from questionary.constants import YES

def load_bank_data(file_path):
    csvpath = Path(file_path)
    return load_csv(csvpath)
    

    #Questionary collects user's loan info
def get_applicant_info():
    credit_score = questionary.text("What's your credit score?").ask()
    debt = questionary.text("What's your current amount of monthly debt?").ask()
    income = questionary.text("What's your total monthly income?").ask()
    loan_amount = questionary.text("What's your desired loan amount?").ask()
    home_value = questionary.text("What's your home value?").ask()

    credit_score = int(credit_score)
    debt = float(debt)
    income = float(income)
    loan_amount = float(loan_amount)
    home_value = float(home_value)

    return credit_score, debt, income, loan_amount, home_value

    #Calculates debt & loan to value ratios and filters qualifyng loans bas on results.

def find_qualifying_loans(bank_data, credit_score, debt, income, loan, home_value):

    # Calculate the monthly debt ratio
    monthly_debt_ratio = calculate_monthly_debt_ratio(debt, income)
    print(f"The monthly debt to income ratio is {monthly_debt_ratio:.02f}")

    # Calculate loan to value ratio
    loan_to_value_ratio = calculate_loan_to_value_ratio(loan, home_value)
    print(f"The loan to value ratio is {loan_to_value_ratio:.02f}.")

    # Run qualification filters
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    bank_data_filtered = filter_credit_score(credit_score, bank_data_filtered)
    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)

    print(f"Found {len(bank_data_filtered)} qualifying loans")

    return bank_data_filtered

#     #Saves qualifing loans and asks user to confirm printing of loan lists

def save_qualifying_loans(qualifying_loans):
    
    Print_confirm = questionary.confirm("Would you like to print your qualified loans?").ask()
    
    if Print_confirm == True:
        
        with open(output_path,"w",) as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=",")
            csvwriter.writerow(header)
            for loans in qualifying_loans:
                csvwriter.writerow(loans.values()) 
            print("Please take your qualified loan list")        
        output_path = Path("your_qualified_loans.csv")    
        header = ["Lender,Max Loan Amount","Max LTV,Max DTI,Min Credit Score","Interest Rate"]
                      
    else: 
        print("Thank you.")


# # The main function for running the script.

def run():
    
    # Load Bank data
    bank_data = load_bank_data()

    # Get the applicant's information
    credit_score, debt, income, loan_amount, home_value = get_applicant_info()

    # Filter qualifying loans
    qualifying_loans = find_qualifying_loans(
        bank_data, credit_score, debt, income, loan_amount, home_value)
    #Save csv questionalry fundction
    save_qualifying_loans = qualifying_loans


if __name__ == "__main__":
    (run)
