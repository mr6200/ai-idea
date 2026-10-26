"""Recompute every number used in the 4%-rule script (amounts in 만 원)."""

# returns used in the sequence-of-returns example (S12); the good order is the reverse
SEQ = [-0.25, -0.15, 0.05, 0.10, 0.12, 0.08, 0.15, 0.10, 0.07, 0.12] * 3
START, FIRST_DRAW, INFLATION = 90000, 3600, 0.025


def balances(returns):
    b, out = START, [START]
    for year, r in enumerate(returns):
        b = max(0.0, (b - FIRST_DRAW * (1 + INFLATION) ** year) * (1 + r)) if b > 0 else 0.0
        out.append(b)
    return out


def main():
    print("1/4% =", 1 / 0.04)
    for monthly in (200, 250, 300, 400):
        print(f"월 {monthly}만 -> 연 {monthly * 12}만 -> x25 = {monthly * 12 * 25}만")
    print("연금 100만 차감:", (300 - 100) * 12 * 25)
    print("1/3% =", round(1 / 0.03, 1), " 1/3.5% =", round(1 / 0.035, 1))
    print("월 300만 @3% =", round(3600 / 0.03), " @3.5% =", round(3600 / 0.035))
    geo = 1.0
    for r in SEQ:
        geo *= 1 + r
    print("S12 연평균 수익률", round(geo ** (1 / len(SEQ)) - 1, 4))
    good, bad = balances(SEQ[::-1]), balances(SEQ)
    print("좋은 순서 30년 뒤", round(good[-1]), "만")
    print("나쁜 순서 바닥난 해", next(i for i, b in enumerate(bad) if b == 0))


if __name__ == "__main__":
    main()
