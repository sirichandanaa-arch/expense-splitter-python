from typing import List, Dict, Tuple


class Expense:
    def __init__(self, payer: str, amount: float, participants: List[str],
                 weights: List[float] = None, desc: str = ""):
        self.payer = payer.strip()
        self.amount = round(float(amount), 2)
        self.participants = [p.strip() for p in participants]
        self.desc = desc

        if weights:
            total = sum(weights)
            self.weights = [w / total for w in weights]
        else:
            self.weights = [1 / len(participants)] * len(participants)

    def shares(self) -> Dict[str, float]:
        return {
            p: round(self.amount * w, 2)
            for p, w in zip(self.participants, self.weights)
        }


def compute_net_balances(expenses: List[Expense]) -> Dict[str, float]:
    net = {}

    for e in expenses:
        for p in e.participants + [e.payer]:
            net.setdefault(p, 0.0)

        net[e.payer] += e.amount

        for p, share in e.shares().items():
            net[p] -= share

    return {p: round(a, 2) for p, a in net.items()}


def minimize_transactions(net: Dict[str, float]) -> List[Tuple[str, str, float]]:
    creditors = []
    debtors = []

    for name, bal in net.items():
        if bal > 0:
            creditors.append([name, bal])
        elif bal < 0:
            debtors.append([name, -bal])

    creditors.sort(key=lambda x: x[1], reverse=True)
    debtors.sort(key=lambda x: x[1], reverse=True)

    settlements = []
    i = j = 0

    while i < len(debtors) and j < len(creditors):
        d_name, d_amt = debtors[i]
        c_name, c_amt = creditors[j]

        pay = round(min(d_amt, c_amt), 2)
        settlements.append((d_name, c_name, pay))

        debtors[i][1] -= pay
        creditors[j][1] -= pay

        if abs(debtors[i][1]) < 0.01:
            i += 1
        if abs(creditors[j][1]) < 0.01:
            j += 1

    return settlements


if __name__ == "__main__":
    people = input("Enter participants (comma separated): ").split(',')
    n = int(input("Enter number of expenses: "))

    expenses = []

    for i in range(n):
        payer = input(f"\nExpense {i+1} - Who paid? ")
        amount = float(input("Enter amount: "))
        participants = input("Enter participants (comma separated): ").split(',')

        choice = input("Weighted split? (y/n): ").lower()
        weights = None

        if choice == 'y':
            weights = [float(x) for x in input("Enter weights (space separated): ").split()]

        expenses.append(Expense(payer, amount, participants, weights))

    net = compute_net_balances(expenses)

    print("\n===== NET BALANCES =====")
    for p, b in net.items():
        print(f"{p}: {b:+.2f}")

    print("\n===== MINIMUM TRANSACTIONS =====")
    for d, c, a in minimize_transactions(net):
        print(f"{d} pays {c}: ₹{a:.2f}")
