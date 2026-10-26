"""Recompute every number used in the interest-tax script (amounts in 원)."""
INCOME_TAX, LOCAL_SHARE = 0.14, 0.10  # local income tax is 10% of the income tax
ISA_FREE, ISA_FREE_LOW, ISA_RATE = 2_000_000, 4_000_000, 0.099
MUTUAL_LIMIT, MUTUAL_RATE = 30_000_000, 0.014


def tax(interest):
    income = interest * INCOME_TAX
    return income + income * LOCAL_SHARE


def main():
    print(f"세율 {INCOME_TAX * (1 + LOCAL_SHARE):.1%}")
    for i in (1_000_000, 500_000):
        print(f"이자 {i:,}원 -> 세금 {tax(i):,.0f}원, 받는 돈 {i - tax(i):,.0f}원")
    print(f"ISA 비과세 {ISA_FREE:,}원 (서민형 {ISA_FREE_LOW:,}원), 초과분 {ISA_RATE:.1%}")
    print(f"상호금융 {MUTUAL_LIMIT:,}원까지 {MUTUAL_RATE:.1%}")


if __name__ == "__main__":
    main()
