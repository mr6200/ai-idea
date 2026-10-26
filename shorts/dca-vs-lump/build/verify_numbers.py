"""Recompute every number used in the DCA-vs-lump-sum script (amounts in 만 원, prices in 원)."""
TOTAL, MONTHS = 1200, 12


def path(points):
    """Monthly prices for months 0..12, linear between (month, price) points."""
    out = []
    for m in range(MONTHS + 1):
        for (m0, p0), (m1, p1) in zip(points, points[1:]):
            if m0 <= m <= m1:
                out.append(p0 + (p1 - p0) * (m - m0) / (m1 - m0))
                break
    return out


SCENARIOS = {
    "up": path([(0, 10000), (12, 13000)]),
    "v": path([(0, 10000), (6, 6000), (12, 10000)]),
    "down": path([(0, 10000), (12, 7000)]),
}


def lump(prices):
    return TOTAL * prices[-1] / prices[0]


def dca(prices):
    per = TOTAL / MONTHS
    shares = sum(per / p for p in prices[:MONTHS])  # buys at months 0..11
    return shares * prices[-1]


def avg_cost(amount, prices):
    shares = [amount / p for p in prices]
    return amount * len(prices) / sum(shares), shares


def main():
    c, sh = avg_cost(30, [10000, 5000, 10000])
    print("평균 단가 예:", [round(s * 10000) for s in sh], "주, 평균 단가", round(c), "원, 평균 주가", round(sum([10000, 5000, 10000]) / 3))
    q, sh = avg_cost(20, [20000, 10000])
    print("퀴즈:", [round(s * 10000) for s in sh], "주, 평균 단가", round(q), "원")
    for k, p in SCENARIOS.items():
        print(k, "거치식", round(lump(p)), "적립식", round(dca(p)))


if __name__ == "__main__":
    main()
