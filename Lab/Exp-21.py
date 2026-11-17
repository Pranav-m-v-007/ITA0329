import numpy as np

def jain_fairness(values):
    values = np.asarray(values, dtype=float)
    denominator = len(values) * np.sum(values ** 2)
    return float(np.sum(values) ** 2 / denominator) if denominator > 0 else 0.0

def simulate(scheduler, users=5, resource_blocks=50, tti_count=1000, seed=21):
    """
    Simplified OFDMA downlink scheduler.
    Rates are generated per user and resource block (kbit/s per RB).
    """
    rng = np.random.default_rng(seed)
    # Different average channel qualities: edge users generally have lower rates.
    average_quality = np.linspace(0.8, 4.0, users)
    rates = rng.exponential(average_quality[:, None], size=(users, resource_blocks))
    average_throughput = np.ones(users)
    total_bits_kbit = np.zeros(users)

    for _ in range(tti_count):
        if scheduler == "RR":
            # Round robin: allocate resource blocks cyclically among users.
            owners = np.arange(resource_blocks) % users
        elif scheduler == "MAXCI":
            # Maximum C/I: choose the user with the highest instantaneous rate.
            owners = np.argmax(rates, axis=0)
        elif scheduler == "PF":
            # Proportional fair: instantaneous rate divided by past average throughput.
            metric = rates / average_throughput[:, None]
            owners = np.argmax(metric, axis=0)
        else:
            raise ValueError("Scheduler must be RR, MAXCI or PF.")

        delivered = np.zeros(users)
        for rb, user in enumerate(owners):
            delivered[user] += rates[user, rb]

        average_throughput = 0.99 * average_throughput + 0.01 * delivered
        total_bits_kbit += delivered

    # 1 TTI is treated as 1 ms; kbit per ms is numerically Mbps.
    return total_bits_kbit / tti_count

def main():
    users = 5
    print("PROGRAM 21: OFDMA DOWNLINK SCHEDULER")
    print("Simplified model; 5 users, 50 resource blocks, 1000 TTIs")
    print(f"{'Scheduler':>10}" + "".join(f"{('UE'+str(i+1)):>10}" for i in range(users))
          + f"{'Total':>10}{'Jain':>9}")
    for name in ("RR", "MAXCI", "PF"):
        throughput = simulate(name, users=users)
        print(f"{name:>10}" + "".join(f"{v:10.2f}" for v in throughput)
              + f"{throughput.sum():10.2f}{jain_fairness(throughput):9.3f}")

if __name__ == "__main__":
    main()
