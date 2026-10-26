"""Recompute every number used in the card-installments script (amounts in 원)."""
PRICE, MONTHS = 1_200_000, 3
QUIZ_PRICE, QUIZ_MONTHS = 3_000_000, 6
# 7 card companies' installment fee income (CEO Score Daily, 2026-08), in 원
FEE_2024, FEE_2025 = 3_458_000_000_000, 3_602_400_000_000


def main():
    print(f"{PRICE:,}원 {MONTHS}개월 무이자 -> 매달 {PRICE // MONTHS:,}원, 이자 0원")
    print(f"퀴즈: {QUIZ_PRICE:,}원 {QUIZ_MONTHS}개월 -> 매달 {QUIZ_PRICE // QUIZ_MONTHS:,}원")
    print(f"할부 수수료 수익 2025년 {FEE_2025 / 1e12:.2f}조 (전년 {FEE_2024 / 1e12:.2f}조, {FEE_2025 / FEE_2024 - 1:+.1%})")


if __name__ == "__main__":
    main()
