"""
Multi-Paradigm Tax Calculator
Author: Ion Cervatiuc

This program demonstrates four programming paradigms in one Python file:
1. Procedural Programming
2. Object-Oriented Programming
3. Functional Programming
4. Event-Driven Programming (Tkinter GUI)

Tax rules used:
- Up to £20,000: 0%
- £20,001 to £100,000: 20% on income above £20,000
- Above £100,000: 45% on income above £100,000,
  plus 20% on the amount between £20,000 and £100,000
"""

import tkinter as tk
from tkinter import messagebox


# =========================================================
# SHARED TAX LOGIC
# =========================================================
PERSONAL_ALLOWANCE_LIMIT = 20000
BASIC_RATE_LIMIT = 100000
BASIC_RATE = 0.20
ADDITIONAL_RATE = 0.45


def calculate_tax_by_rules(income: float) -> tuple[float, str, float]:
    """
    Calculate tax, tax band, and net pay based on the assignment tax rules.
    Returns: (tax, band, net_pay)
    """
    if income <= PERSONAL_ALLOWANCE_LIMIT:
        tax = 0.0
        band = "Personal Allowance (0%)"
    elif income <= BASIC_RATE_LIMIT:
        tax = (income - PERSONAL_ALLOWANCE_LIMIT) * BASIC_RATE
        band = "Basic Rate (20%)"
    else:
        basic_tax = (BASIC_RATE_LIMIT - PERSONAL_ALLOWANCE_LIMIT) * BASIC_RATE
        additional_tax = (income - BASIC_RATE_LIMIT) * ADDITIONAL_RATE
        tax = basic_tax + additional_tax
        band = "Additional Rate (45%)"

    net_pay = income - tax
    return tax, band, net_pay


def get_valid_income() -> float | None:
    """
    Read and validate income from keyboard input.
    Returns None if input is invalid.
    """
    try:
        income = float(input("Enter annual income (£): "))
        if income < 0:
            print("Error: Income cannot be negative.")
            return None
        return income
    except ValueError:
        print("Error: Please enter a valid numeric income.")
        return None


def print_payslip(name: str, organisation: str, income: float, band: str, tax: float, net_pay: float) -> None:
    """
    Print a formatted payslip.
    """
    print("\n--- Payslip ---")
    print(f"Employee Name   : {name}")
    print(f"Organisation    : {organisation}")
    print(f"Annual Income   : £{income:,.2f}")
    print(f"Tax Band        : {band}")
    print(f"Tax Amount      : £{tax:,.2f}")
    print(f"Net Pay         : £{net_pay:,.2f}")


# =========================================================
# 1. PROCEDURAL PROGRAMMING
# =========================================================
def procedural_tax_calculator() -> None:
    """
    Procedural version of the tax calculator.
    """
    print("\n=== Procedural Tax Calculator ===")
    name = input("Enter employee name: ").strip()
    organisation = input("Enter organisation name: ").strip()

    income = get_valid_income()
    if income is None:
        return

    tax, band, net_pay = calculate_tax_by_rules(income)
    print_payslip(name, organisation, income, band, tax, net_pay)


# =========================================================
# 2. OBJECT-ORIENTED PROGRAMMING
# =========================================================
class Employee:
    """
    Represents an employee and their tax calculation details.
    """

    def __init__(self, name: str, organisation: str, income: float) -> None:
        self.name = name
        self.organisation = organisation
        self.income = income
        self.tax = 0.0
        self.band = ""
        self.net_pay = 0.0
        self.calculate_tax()

    def calculate_tax(self) -> None:
        """
        Calculate tax using shared tax rules.
        """
        self.tax, self.band, self.net_pay = calculate_tax_by_rules(self.income)

    def display_payslip(self) -> None:
        """
        Display employee payslip.
        """
        print_payslip(
            self.name,
            self.organisation,
            self.income,
            self.band,
            self.tax,
            self.net_pay,
        )


def oop_tax_calculator() -> None:
    """
    Object-oriented version of the tax calculator.
    """
    print("\n=== Object-Oriented Tax Calculator ===")
    name = input("Enter employee name: ").strip()
    organisation = input("Enter organisation name: ").strip()

    income = get_valid_income()
    if income is None:
        return

    employee = Employee(name, organisation, income)
    employee.display_payslip()


# =========================================================
# 3. FUNCTIONAL PROGRAMMING
# =========================================================
def functional_calculate_tax(income: float) -> tuple[float, str, float]:
    """
    Functional-style tax calculation.
    """
    return (
        (0.0, "Personal Allowance (0%)", income)
        if income <= PERSONAL_ALLOWANCE_LIMIT
        else (
            (income - PERSONAL_ALLOWANCE_LIMIT) * BASIC_RATE,
            "Basic Rate (20%)",
            income - ((income - PERSONAL_ALLOWANCE_LIMIT) * BASIC_RATE),
        )
        if income <= BASIC_RATE_LIMIT
        else (
            ((BASIC_RATE_LIMIT - PERSONAL_ALLOWANCE_LIMIT) * BASIC_RATE)
            + ((income - BASIC_RATE_LIMIT) * ADDITIONAL_RATE),
            "Additional Rate (45%)",
            income
            - (
                ((BASIC_RATE_LIMIT - PERSONAL_ALLOWANCE_LIMIT) * BASIC_RATE)
                + ((income - BASIC_RATE_LIMIT) * ADDITIONAL_RATE)
            ),
        )
    )


def create_payslip(name: str, organisation: str, income: float) -> dict:
    """
    Create a payslip dictionary in a functional style.
    """
    tax, band, net_pay = functional_calculate_tax(income)
    return {
        "name": name,
        "organisation": organisation,
        "income": income,
        "band": band,
        "tax": tax,
        "net_pay": net_pay,
    }


def display_functional_payslip(payslip: dict) -> None:
    """
    Display payslip created in functional style.
    """
    print_payslip(
        payslip["name"],
        payslip["organisation"],
        payslip["income"],
        payslip["band"],
        payslip["tax"],
        payslip["net_pay"],
    )


def functional_tax_calculator() -> None:
    """
    Functional version of the tax calculator.
    """
    print("\n=== Functional Tax Calculator ===")
    name = input("Enter employee name: ").strip()
    organisation = input("Enter organisation name: ").strip()

    income = get_valid_income()
    if income is None:
        return

    payslip = create_payslip(name, organisation, income)
    display_functional_payslip(payslip)


# =========================================================
# 4. EVENT-DRIVEN PROGRAMMING
# =========================================================
def event_driven_tax_calculator() -> None:
    """
    Event-driven version of the tax calculator using Tkinter.
    """

    def on_calculate() -> None:
        name = entry_name.get().strip()
        organisation = entry_organisation.get().strip()
        income_text = entry_income.get().strip()

        if not name or not organisation or not income_text:
            messagebox.showerror("Input Error", "Please complete all fields.")
            return

        try:
            income = float(income_text)
            if income < 0:
                messagebox.showerror("Input Error", "Income cannot be negative.")
                return
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid numeric income.")
            return

        tax, band, net_pay = calculate_tax_by_rules(income)

        result = (
            f"Employee Name   : {name}\n"
            f"Organisation    : {organisation}\n"
            f"Annual Income   : £{income:,.2f}\n"
            f"Tax Band        : {band}\n"
            f"Tax Amount      : £{tax:,.2f}\n"
            f"Net Pay         : £{net_pay:,.2f}"
        )
        label_result.config(text=result)

    window = tk.Tk()
    window.title("Event-Driven Tax Calculator")
    window.geometry("520x430")
    window.resizable(False, False)

    title_label = tk.Label(window, text="Tax Calculator", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    label_name = tk.Label(window, text="Employee Name:")
    label_name.pack()
    entry_name = tk.Entry(window, width=40)
    entry_name.pack(pady=5)

    label_organisation = tk.Label(window, text="Organisation Name:")
    label_organisation.pack()
    entry_organisation = tk.Entry(window, width=40)
    entry_organisation.pack(pady=5)

    label_income = tk.Label(window, text="Annual Income (£):")
    label_income.pack()
    entry_income = tk.Entry(window, width=40)
    entry_income.pack(pady=5)

    calculate_button = tk.Button(window, text="Calculate Tax", command=on_calculate)
    calculate_button.pack(pady=15)

    label_result = tk.Label(window, text="", justify="left", font=("Arial", 11))
    label_result.pack(pady=10)

    window.mainloop()


# =========================================================
# MAIN MENU
# =========================================================
def display_menu() -> None:
    """
    Display the main menu.
    """
    print("\n====================================")
    print(" MULTI-PARADIGM TAX CALCULATOR ")
    print("====================================")
    print("1. Procedural Programming")
    print("2. Object-Oriented Programming")
    print("3. Functional Programming")
    print("4. Event-Driven Programming")
    print("5. Exit")


def main() -> None:
    """
    Main program loop.
    """
    while True:
        display_menu()
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            procedural_tax_calculator()
        elif choice == "2":
            oop_tax_calculator()
        elif choice == "3":
            functional_tax_calculator()
        elif choice == "4":
            event_driven_tax_calculator()
        elif choice == "5":
            print("Program closed.")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, 4, or 5.")


if __name__ == "__main__":
    main()