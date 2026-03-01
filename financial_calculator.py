"""
===============================================================
  FINANCIAL MATHEMATICS CALCULATOR
  Author : Anele Ngubane
  Based on: BSc Financial Mathematics project (NWU)
  Modules : Interest Rate Conversion | Investment | Annuities
            | Loans & Amortisation | Increasing Annuities
===============================================================
"""

import math


# ──────────────────────────────────────────────────────────────
#  DISPLAY HELPERS
# ──────────────────────────────────────────────────────────────

def separator(title=""):
    width = 60
    if title:
        print(f"\n{'─' * 4}  {title}  {'─' * (width - len(title) - 6)}")
    else:
        print("─" * width)


def currency(value):
    return f"R {value:,.2f}"


def percent(value):
    return f"{value * 100:.4f}%"


# ──────────────────────────────────────────────────────────────
#  MODULE 1 — INTEREST RATE CONVERSION
#  Converts between Simple, Nominal, Effective Annual,
#  Effective Periodic, and Continuous rates.
# ──────────────────────────────────────────────────────────────

def convert_interest_rate(given_rate, given_type, given_periods,
                           requested_type, requested_periods=None, years=1):
    """
    Convert an interest rate from one form to another.

    Parameters
    ----------
    given_rate      : float  — the rate as a decimal (e.g. 0.12 for 12%)
    given_type      : str    — 'simple' | 'nominal' | 'effective_annual'
                               | 'effective_periodic' | 'continuous'
    given_periods   : int    — compounding periods per year for given rate
    requested_type  : str    — same options as given_type
    requested_periods: int   — compounding periods per year for output
    years           : float  — used for simple interest conversion
    """

    # Step 1: Convert everything → Effective Annual Rate (EAR)
    if given_type == "simple":
        ear = (1 + given_rate * years) ** (1 / years) - 1
    elif given_type == "effective_annual":
        ear = given_rate
    elif given_type == "effective_periodic":
        ear = (1 + given_rate) ** given_periods - 1
    elif given_type == "nominal":
        ear = (1 + given_rate / given_periods) ** given_periods - 1
    elif given_type == "continuous":
        ear = math.exp(given_rate) - 1
    else:
        raise ValueError(f"Unknown rate type: {given_type}")

    # Step 2: Convert EAR → requested type
    if requested_type == "simple":
        return ear                                          # approximation
    elif requested_type == "effective_annual":
        return ear
    elif requested_type == "effective_periodic":
        return (1 + ear) ** (1 / requested_periods) - 1
    elif requested_type == "nominal":
        return ((1 + ear) ** (1 / requested_periods) - 1) * requested_periods
    elif requested_type == "continuous":
        return math.log(1 + ear)
    else:
        raise ValueError(f"Unknown rate type: {requested_type}")


def run_interest_conversion():
    separator("MODULE 1 — INTEREST RATE CONVERSION")

    type_map = {
        "1": ("simple",            "Simple"),
        "2": ("nominal",           "Nominal"),
        "3": ("effective_annual",  "Effective Annual"),
        "4": ("effective_periodic","Effective Periodic"),
        "5": ("continuous",        "Continuous"),
    }

    print("\nRate types:")
    for k, (_, label) in type_map.items():
        print(f"  {k}. {label}")

    given_rate    = float(input("\nEnter given interest rate (e.g. 0.064 for 6.4%): "))
    g_choice      = input("Given rate type (1–5): ").strip()
    given_type    = type_map[g_choice][0]
    given_periods = 1
    if given_type in ("nominal", "effective_periodic"):
        given_periods = int(input("Given compounding periods per year: "))

    years = float(input("Number of years: "))

    r_choice       = input("Requested rate type (1–5): ").strip()
    requested_type = type_map[r_choice][0]
    req_periods    = 1
    if requested_type in ("nominal", "effective_periodic"):
        req_periods = int(input("Requested compounding periods per year: "))

    result = convert_interest_rate(given_rate, given_type, given_periods,
                                   requested_type, req_periods, years)

    separator()
    print(f"  Given rate   : {percent(given_rate)}  ({type_map[g_choice][1]})")
    print(f"  Requested    : {percent(result)}  ({type_map[r_choice][1]})")
    separator()


# ──────────────────────────────────────────────────────────────
#  MODULE 2 — INVESTMENT CALCULATOR
#  Solves for FV, PV, interest rate, or time given the others.
# ──────────────────────────────────────────────────────────────

def investment_calculator(pv=None, fv=None, rate=None, years=None, periods=1):
    """
    Solve for the missing investment variable.
    Rate is effective periodic rate.
    n = years * periods  (total number of periods)
    """
    n = None
    if years is not None:
        n = years * periods

    if fv is None:
        fv = pv * (1 + rate) ** n
        return "Future Value", fv

    if pv is None:
        pv = fv / (1 + rate) ** n
        return "Present Value", pv

    if rate is None:
        rate = (fv / pv) ** (1 / n) - 1
        return "Interest Rate (effective periodic)", rate

    if years is None:
        years = math.log(fv / pv) / (periods * math.log(1 + rate))
        return "Years", years

    raise ValueError("All variables are already known — nothing to solve.")


def run_investment():
    separator("MODULE 2 — INVESTMENT CALCULATOR")
    print("\nLeave the unknown variable blank (press Enter).")

    pv_in      = input("Present Value (PV)            : ").strip()
    fv_in      = input("Future Value  (FV)            : ").strip()
    rate_in    = input("Effective periodic rate        : ").strip()
    years_in   = input("Years                          : ").strip()
    periods_in = input("Periods per year (default 1)   : ").strip()

    pv      = float(pv_in)      if pv_in      else None
    fv      = float(fv_in)      if fv_in      else None
    rate    = float(rate_in)    if rate_in    else None
    years   = float(years_in)   if years_in   else None
    periods = int(periods_in)   if periods_in else 1

    label, result = investment_calculator(pv, fv, rate, years, periods)

    separator()
    if "Rate" in label:
        print(f"  {label}: {percent(result)}")
    else:
        print(f"  {label}: {currency(result) if 'Value' in label else f'{result:.4f}'}")
    separator()


# ──────────────────────────────────────────────────────────────
#  MODULE 3 — ANNUITIES CALCULATOR
#  Supports: ordinary annuity (arrears) and annuity-due (advance)
#  Solves for: FV, PV, payment (R), interest rate, or periods
# ──────────────────────────────────────────────────────────────

def annuity_fv(pmt, rate, n, advance=False):
    """Future value of an annuity."""
    fv = pmt * ((1 + rate) ** n - 1) / rate
    if advance:
        fv *= (1 + rate)
    return fv


def annuity_pv(pmt, rate, n, advance=False):
    """Present value of an annuity."""
    pv = pmt * (1 - (1 + rate) ** (-n)) / rate
    if advance:
        pv *= (1 + rate)
    return pv


def annuity_payment_from_fv(fv, rate, n, advance=False):
    pmt = fv * rate / ((1 + rate) ** n - 1)
    if advance:
        pmt /= (1 + rate)
    return pmt


def annuity_payment_from_pv(pv, rate, n, advance=False):
    pmt = pv * rate / (1 - (1 + rate) ** (-n))
    if advance:
        pmt /= (1 + rate)
    return pmt


def annuity_periods_from_fv(fv, pmt, rate, advance=False):
    if advance:
        pmt *= (1 + rate)
    return math.log(1 + fv * rate / pmt) / math.log(1 + rate)


def annuity_periods_from_pv(pv, pmt, rate, advance=False):
    if advance:
        pmt *= (1 + rate)
    return -math.log(1 - pv * rate / pmt) / math.log(1 + rate)


def run_annuities():
    separator("MODULE 3 — ANNUITIES CALCULATOR")

    print("\nAnnuity type:")
    print("  1. Ordinary annuity (Arrears — payments at END of period)")
    print("  2. Annuity-due      (Advance — payments at START of period)")
    a_type   = input("Choice (1/2): ").strip()
    advance  = a_type == "2"

    print("\nSolve for:")
    print("  1. Future Value (FV)")
    print("  2. Present Value (PV)")
    print("  3. Payment amount (R)")
    print("  4. Number of periods (n)")
    solve_for = input("Choice (1–4): ").strip()

    rate_in = float(input("Effective periodic interest rate (e.g. 0.01 for 1%): "))
    n_in    = None
    pmt_in  = None
    pv_in   = None
    fv_in   = None

    if solve_for != "4":
        n_in = float(input("Total number of periods (n): "))
    if solve_for not in ("3",):
        pmt_in = float(input("Payment amount (R): ")) if solve_for != "1" or True else None

    # Gather what's needed per solve target
    if solve_for == "1":          # FV
        pmt_in = float(input("Payment amount (R): "))
        n_in   = float(input("Number of periods (n): "))
        result = annuity_fv(pmt_in, rate_in, n_in, advance)
        label  = "Future Value"

    elif solve_for == "2":        # PV
        pmt_in = float(input("Payment amount (R): "))
        n_in   = float(input("Number of periods (n): "))
        result = annuity_pv(pmt_in, rate_in, n_in, advance)
        label  = "Present Value"

    elif solve_for == "3":        # Payment
        print("Solve from:")
        print("  1. Known FV")
        print("  2. Known PV")
        sub = input("Choice (1/2): ").strip()
        n_in = float(input("Number of periods (n): "))
        if sub == "1":
            fv_in  = float(input("Future Value (FV): "))
            result = annuity_payment_from_fv(fv_in, rate_in, n_in, advance)
        else:
            pv_in  = float(input("Present Value (PV): "))
            result = annuity_payment_from_pv(pv_in, rate_in, n_in, advance)
        label = "Payment amount"

    elif solve_for == "4":        # n
        print("Solve from:")
        print("  1. Known FV")
        print("  2. Known PV")
        sub    = input("Choice (1/2): ").strip()
        pmt_in = float(input("Payment amount (R): "))
        if sub == "1":
            fv_in  = float(input("Future Value (FV): "))
            result = annuity_periods_from_fv(fv_in, pmt_in, rate_in, advance)
        else:
            pv_in  = float(input("Present Value (PV): "))
            result = annuity_periods_from_pv(pv_in, pmt_in, rate_in, advance)
        label = "Number of periods"

    separator()
    annuity_label = "Annuity-due (Advance)" if advance else "Ordinary Annuity (Arrears)"
    print(f"  Type    : {annuity_label}")
    print(f"  Rate    : {percent(rate_in)}")
    if label in ("Future Value", "Present Value", "Payment amount"):
        print(f"  {label}: {currency(result)}")
    else:
        print(f"  {label}: {result:.4f} periods")
    separator()


# ──────────────────────────────────────────────────────────────
#  MODULE 4 — LOAN / AMORTISATION CALCULATOR
#  Generates a full amortisation schedule.
#  Supports arrears and advance loan types.
# ──────────────────────────────────────────────────────────────

def build_amortisation_schedule(loan, rate, n, advance=False):
    """
    Build a full amortisation schedule.

    Returns
    -------
    payment  : float
    schedule : list of dicts with keys:
               period, opening_balance, interest, capital, payment, closing_balance
    """
    if advance:
        payment = (loan * (1 + rate) * rate) / (1 - (1 + rate) ** (-n))
    else:
        payment = (loan * rate) / (1 - (1 + rate) ** (-n))

    schedule = []
    balance  = loan

    for k in range(1, int(round(n)) + 1):
        if advance:
            # Payment at start of period
            capital_component = payment - balance * rate / (1 + rate)
            interest          = balance * rate / (1 + rate)
        else:
            interest          = balance * rate
            capital_component = payment - interest

        closing = balance - capital_component
        schedule.append({
            "period"          : k,
            "opening_balance" : balance,
            "interest"        : interest,
            "capital"         : capital_component,
            "payment"         : payment,
            "closing_balance" : max(closing, 0),
        })
        balance = max(closing, 0)

    return payment, schedule


def run_loans():
    separator("MODULE 4 — LOAN / AMORTISATION CALCULATOR")

    loan    = float(input("\nLoan amount (PV)                         : R "))
    rate    = float(input("Effective periodic interest rate          : "))
    years   = float(input("Loan term in years                        : "))
    periods = int(input(  "Payments per year                         : "))
    a_type  = input(      "Loan type — Arrears (A) or Advance (D)    : ").strip().upper()
    advance = a_type == "D"
    n       = years * periods

    payment, schedule = build_amortisation_schedule(loan, rate, n, advance)

    separator()
    loan_type = "Advance (Annuity-due)" if advance else "Arrears (Ordinary)"
    print(f"\n  Loan Amount   : {currency(loan)}")
    print(f"  Rate          : {percent(rate)} per period")
    print(f"  Term          : {years} years  ({int(n)} periods)")
    print(f"  Type          : {loan_type}")
    print(f"  Payment (R)   : {currency(payment)}")
    print(f"  Total Paid    : {currency(payment * n)}")
    print(f"  Total Interest: {currency(payment * n - loan)}")

    show = input("\nPrint full amortisation table? (y/n): ").strip().lower()
    if show == "y":
        separator("AMORTISATION SCHEDULE")
        header = f"{'Period':>7}  {'Opening Bal':>14}  {'Interest':>12}  {'Capital':>12}  {'Payment':>12}  {'Closing Bal':>14}"
        print(header)
        print("─" * len(header))
        for row in schedule:
            print(
                f"{row['period']:>7}  "
                f"{row['opening_balance']:>14,.2f}  "
                f"{row['interest']:>12,.2f}  "
                f"{row['capital']:>12,.2f}  "
                f"{row['payment']:>12,.2f}  "
                f"{row['closing_balance']:>14,.2f}"
            )

    # Query specific period
    k_in = input("\nView interest/capital for a specific period? Enter period number (or Enter to skip): ").strip()
    if k_in:
        k   = int(k_in)
        row = schedule[k - 1]
        separator(f"Period {k} Breakdown")
        print(f"  Opening Balance  : {currency(row['opening_balance'])}")
        print(f"  Interest         : {currency(row['interest'])}")
        print(f"  Capital          : {currency(row['capital'])}")
        print(f"  Payment          : {currency(row['payment'])}")
        print(f"  Closing Balance  : {currency(row['closing_balance'])}")

    # Range sum
    rng = input("\nSum interest/capital over a range? Enter 'start,end' (or Enter to skip): ").strip()
    if rng:
        x1, x2 = [int(v) for v in rng.split(",")]
        sub     = schedule[x1 - 1: x2]
        t_int   = sum(r["interest"] for r in sub)
        t_cap   = sum(r["capital"]  for r in sub)
        separator(f"Periods {x1} to {x2} Summary")
        print(f"  Total Interest   : {currency(t_int)}")
        print(f"  Total Capital    : {currency(t_cap)}")
        print(f"  Total Paid       : {currency(t_int + t_cap)}")

    separator()


# ──────────────────────────────────────────────────────────────
#  MODULE 5 — INCREASING ANNUITIES
#  Geometric (rate-linked) increasing cashflows.
#  Supports FV and PV for arrears and advance.
# ──────────────────────────────────────────────────────────────

def increasing_annuity_fv(pmt, interest_rate, growth_rate, n, advance=False):
    """
    Future value of a geometrically increasing annuity.
    Formula: R * [(1+i)^n - (1+g)^n] / (i - g)
    """
    if abs(interest_rate - growth_rate) < 1e-12:
        fv = pmt * n * (1 + interest_rate) ** (n - 1)
    else:
        fv = pmt * ((1 + interest_rate) ** n - (1 + growth_rate) ** n) / (interest_rate - growth_rate)
    if advance:
        fv *= (1 + interest_rate)
    return fv


def increasing_annuity_pv(pmt, interest_rate, growth_rate, n, advance=False):
    """
    Present value of a geometrically increasing annuity.
    """
    fv = increasing_annuity_fv(pmt, interest_rate, growth_rate, n, advance)
    return fv / (1 + interest_rate) ** n


def run_increasing_annuities():
    separator("MODULE 5 — INCREASING ANNUITIES")

    print("\nSolve for:")
    print("  1. Future Value (FV)")
    print("  2. Present Value (PV)")
    solve_for = input("Choice (1/2): ").strip()

    print("\nAnnuity type:")
    print("  1. Arrears (payments at END of period)")
    print("  2. Advance (payments at START of period)")
    a_type  = input("Choice (1/2): ").strip()
    advance = a_type == "2"

    pmt           = float(input("Initial cashflow (first payment) R        : "))
    interest_rate = float(input("Effective periodic interest rate          : "))
    growth_rate   = float(input("Growth rate per period                    : "))
    n             = float(input("Number of periods (n)                     : "))

    if solve_for == "1":
        result = increasing_annuity_fv(pmt, interest_rate, growth_rate, n, advance)
        label  = "Future Value"
    else:
        result = increasing_annuity_pv(pmt, interest_rate, growth_rate, n, advance)
        label  = "Present Value"

    separator()
    print(f"  Initial payment : {currency(pmt)}")
    print(f"  Interest rate   : {percent(interest_rate)}")
    print(f"  Growth rate     : {percent(growth_rate)}")
    print(f"  Periods         : {n}")
    print(f"  {label}         : {currency(result)}")
    separator()


# ──────────────────────────────────────────────────────────────
#  MAIN MENU
# ──────────────────────────────────────────────────────────────

MENU = {
    "1": ("Interest Rate Conversion",  run_interest_conversion),
    "2": ("Investment Calculator",     run_investment),
    "3": ("Annuities Calculator",      run_annuities),
    "4": ("Loan / Amortisation",       run_loans),
    "5": ("Increasing Annuities",      run_increasing_annuities),
    "0": ("Exit",                      None),
}


def main():
    print("\n" + "═" * 60)
    print("   FINANCIAL MATHEMATICS CALCULATOR")
    print("   Anele Ngubane  |  BSc Financial Mathematics (NWU)")
    print("═" * 60)

    while True:
        print("\nMain Menu:")
        for key, (label, _) in MENU.items():
            print(f"  {key}. {label}")

        choice = input("\nSelect module: ").strip()

        if choice == "0":
            print("\n  Goodbye!\n")
            break
        elif choice in MENU:
            try:
                MENU[choice][1]()
            except ValueError as e:
                print(f"\n  ⚠  Input error: {e}")
            except ZeroDivisionError:
                print("\n  ⚠  Division by zero — check your inputs (rate cannot be 0 for this calculation).")
            except Exception as e:
                print(f"\n  ⚠  Unexpected error: {e}")
        else:
            print("  Invalid choice. Please enter 0–5.")


if __name__ == "__main__":
    main()
