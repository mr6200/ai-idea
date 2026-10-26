"""Recompute every number used in the deposit-vs-savings script (amounts in 원)."""
LUMP, MONTHLY, MONTHS = 12_000_000, 1_000_000, 12
DEPOSIT_RATE, SAVINGS_RATE = 0.03, 0.035


def deposit_interest(principal, rate, months=MONTHS):
    """Simple interest on a lump sum held for the whole term."""
    return principal * rate * months / 12


def savings_interest(monthly, rate, months=MONTHS):
    """Simple interest on an installment savings account: the k-th deposit earns (months - k + 1) months."""
    return monthly * rate * (months * (months + 1) / 2) / 12


def after_tax(interest):
    """Interest income tax 14% plus local income tax at 10% of it (1.4%), 15.4% in total."""
    income_tax = interest * 0.14
    return interest - income_tax - income_tax * 0.1


def main():
    d, s = deposit_interest(LUMP, DEPOSIT_RATE), savings_interest(MONTHLY, SAVINGS_RATE)
    print(f"예금 1,200만 원 연 3%: {d:,.0f}원, 세후 {after_tax(d):,.0f}원")
    print(f"적금 월 100만 원 연 3.5%: {s:,.0f}원, 세후 {after_tax(s):,.0f}원")
    print(f"첫 달분 {MONTHLY * SAVINGS_RATE:,.0f}원, 마지막 달분 {MONTHLY * SAVINGS_RATE / 12:,.0f}원, 평균 {78 / 12}달")
    print(f"적금 이자 / 1,200만 원 = {s / LUMP:.2%}, 예금과 차이 {d - s:,.0f}원")
    print(f"적금이 예금 3%를 따라잡는 금리 = {DEPOSIT_RATE * 12 / 6.5:.2%}")
    q = savings_interest(100_000, 0.06)
    print(f"퀴즈 월 10만 원 연 6%: {q:,.0f}원, 세후 {after_tax(q):,.0f}원")


if __name__ == "__main__":
    main()
