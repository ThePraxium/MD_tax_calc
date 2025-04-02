import math

# Define tax brackets and rates as constants
FEDERAL_TAX_BRACKETS = {
    1: [(11925, 0.10), (48475, 0.12), (103350, 0.22), (197300, 0.24), (250525, 0.32), (626350, 0.35), (float('inf'), 0.37)],
    2: [(23850, 0.10), (96950, 0.12), (206700, 0.22), (394600, 0.24), (501050, 0.32), (751600, 0.35), (float('inf'), 0.37)]
}

MARYLAND_TAX_BRACKETS = {
    1: [(1000, 0.02), (2000, 0.03), (3000, 0.04), (100000, 0.0475), (125000, 0.05), (150000, 0.0525), (250000, 0.055), (float('inf'), 0.0575)],
    2: [(1000, 0.02), (2000, 0.03), (3000, 0.04), (150000, 0.0475), (175000, 0.05), (225000, 0.0525), (300000, 0.055), (float('inf'), 0.0575)]
}

ANNE_ARUNDEL_TAX_BRACKETS = {
    1: [(50000, 0.027), (400000, 0.0281), (float('inf'), 0.032)],
    2: [(75000, 0.027), (480000, 0.0281), (float('inf'), 0.032)]
}

def calculate_taxes_by_bracket(income, brackets):
    taxes_owed = 0
    previous_limit = 0
    detailed_brackets = []
    for limit, rate in brackets:
        if income <= limit:
            amount_taxed = (income - previous_limit) * rate
            taxes_owed += amount_taxed
            detailed_brackets.append((previous_limit, limit, rate, amount_taxed))
            return rate, taxes_owed, detailed_brackets
        else:
            amount_taxed = (limit - previous_limit) * rate
            taxes_owed += amount_taxed
            detailed_brackets.append((previous_limit, limit, rate, amount_taxed))
            previous_limit = limit
    return rate, taxes_owed, detailed_brackets

def calculate_federal_taxes(income, filing_status):
    return calculate_taxes_by_bracket(income, FEDERAL_TAX_BRACKETS[filing_status])

def calculate_maryland_taxes(income, filing_status):
    return calculate_taxes_by_bracket(income, MARYLAND_TAX_BRACKETS[filing_status])

def calculate_anne_arundel_taxes(income, filing_status):
    return calculate_taxes_by_bracket(income, ANNE_ARUNDEL_TAX_BRACKETS[filing_status])

def calculate_taxes(income, flat_deduction, filing_status):
    # Calculate taxable income
    taxable_income = max(0, income - flat_deduction)

    # Federal taxes
    fed_rate, fed_taxes_owed, fed_brackets = calculate_federal_taxes(taxable_income, filing_status)

    # Maryland taxes
    md_rate, md_taxes_owed, md_brackets = calculate_maryland_taxes(taxable_income, filing_status)

    # Anne Arundel taxes
    aa_rate, aa_taxes_owed, aa_brackets = calculate_anne_arundel_taxes(taxable_income, filing_status)

    # Total taxes owed
    total_taxes_owed = fed_taxes_owed + md_taxes_owed + aa_taxes_owed

    # Remaining income after taxes
    post_tax_income = taxable_income - total_taxes_owed

    # Calculate spending power
    calculated_spending_power = post_tax_income + flat_deduction

    # Calculate percentages of taxable income
    fed_tax_percent = (fed_taxes_owed / taxable_income) * 100 if taxable_income > 0 else 0
    md_tax_percent = (md_taxes_owed / taxable_income) * 100 if taxable_income > 0 else 0
    aa_tax_percent = (aa_taxes_owed / taxable_income) * 100 if taxable_income > 0 else 0
    total_tax_percent = (total_taxes_owed / taxable_income) * 100 if taxable_income > 0 else 0

    # Display results with overall effective tax rate added to Total Taxes Owed
    results = {
        "Total Income": f"${income:,.2f}",
        "Flat Deduction": f"${flat_deduction:,.2f}",
        "Taxable Income": f"${taxable_income:,.2f}",
        "Federal Taxes Owed": f"${fed_taxes_owed:,.2f} :Effective Tax Rate: {fed_tax_percent:.2f}%",
        "Maryland Taxes Owed": f"${md_taxes_owed:,.2f} :Effective Tax Rate: {md_tax_percent:.2f}%",
        "Anne Arundel Taxes Owed": f"${aa_taxes_owed:,.2f} :Marginal Rate: {aa_tax_percent:.2f}%",
        "Total Taxes Owed": f"${total_taxes_owed:,.2f} :Effective Tax Rate: {total_tax_percent:.2f}%",
        "Post-Tax Income": f"${post_tax_income:,.2f}",
        "Potential Spending Power": f"${calculated_spending_power:,.2f}"
    }
         
    # Add detailed bracket information
    results["\n --- Federal Tax Brackets"] = fed_brackets
    results["\n --- Maryland Tax Brackets"] = md_brackets
    results["\n --- Anne Arundel Tax Brackets"] = aa_brackets

    return results

def compare_standard_deduction(income, filing_status):
    # Define standard deductions
    standard_deduction = 30000 if filing_status == 2 else 15000

    # Calculate taxes with standard deduction
    results = calculate_taxes(income, standard_deduction, filing_status)
    results["Standard Deduction"] = standard_deduction
    return results

# Example usage
income = float(input("Enter your total income: "))
print("Select your filing status: \n1. Single \n2. Married")
filing_status = int(input("Enter 1 for Single or 2 for Married: "))
flat_deduction = float(input("Enter your flat deduction amount: "))

# Calculate taxes with user-provided deduction
results = calculate_taxes(income, flat_deduction, filing_status)

# Calculate taxes with standard deduction
standard_results = compare_standard_deduction(income, filing_status)

print("\n--- Using User-Provided Deduction ---")
for key, value in results.items():
    if key.endswith("Brackets"):
        print(f"{key}:")
        for bracket in value:
            print(f"  Income from ${bracket[0]:,.2f} to ${bracket[1]:,.2f} taxed at {bracket[2] * 100:.2f}%: ${bracket[3]:,.2f}")
    else:
        print(f"{key}: {value}")

# Quick reference for standard deduction
print("\n--- Quick Reference for Standard Deduction ---")
# Split at colon and take the numeric portion only
std_total_taxes_str = standard_results['Total Taxes Owed'].split(":")[0]
std_total_taxes = float(std_total_taxes_str.replace('$', '').replace(',', ''))
print(f"Standard Total Taxes Owed: ${std_total_taxes:,.2f}")

std_post_tax = float(standard_results['Post-Tax Income'].replace('$', '').replace(',', ''))
print(f"Standard Post-Tax Income: ${std_post_tax:,.2f}")

standard_spending_power = std_post_tax + standard_results['Standard Deduction']
print(f"Standard Potential Spending Power: ${standard_spending_power:,.2f}")