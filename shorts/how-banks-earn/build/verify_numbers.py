"""Recompute every number used in the how-banks-earn script (amounts in 원)."""
DEPOSIT, DEP_RATE, LOAN_RATE = 100_000_000, 0.03, 0.05

# 2025 domestic bank results (FSS, provisional, released 2026-03-19), in 조 원
NET_INTEREST, NON_INTEREST = 60.4, 7.6


def main():
    paid, earned = DEPOSIT * DEP_RATE, DEPOSIT * LOAN_RATE
    print(f"예금 이자 {paid:,.0f}원, 대출 이자 {earned:,.0f}원, 은행 몫 {earned - paid:,.0f}원")
    share = NET_INTEREST / (NET_INTEREST + NON_INTEREST)
    print(f"이자이익 비중 {share:.1%} -> 10원 중 약 {share * 10:.1f}원")
    print(f"퀴즈: 1억 원, 예금 3%, 대출 6% -> {DEPOSIT * (0.06 - 0.03):,.0f}원")


if __name__ == "__main__":
    main()
