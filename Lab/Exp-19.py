import numpy as np

D = 1000.0       # distance between base stations (m)
P0 = -30.0       # received power at 1 m (dBm)
PATH_LOSS = 3.5
SHADOW_SIGMA = 4.0
SPEED = 10.0

def run(hysteresis_db, rng, speed=SPEED, shadow_sigma=SHADOW_SIGMA, sample_step=0.5):
    """Simulate one mobile crossing; return handoffs, ping-pongs, first handoff position."""
    serving = 0
    handoffs = ping_pongs = 0
    last_handoff_time = -99.0
    last_from_cell = None
    first_position = None

    for t in np.arange(0.0, D / speed, sample_step):
        x = speed * t
        distances = [max(abs(x), 1.0), max(abs(x - D), 1.0)]
        rss = [P0 - 10 * PATH_LOSS * np.log10(d) + rng.normal(0, shadow_sigma)
               for d in distances]
        candidate = 1 - serving

        if rss[candidate] > rss[serving] + hysteresis_db:
            if last_from_cell == candidate and (t - last_handoff_time) < 10.0:
                ping_pongs += 1
            handoffs += 1
            last_from_cell = serving
            last_handoff_time = t
            serving = candidate
            if first_position is None:
                first_position = x

    return handoffs, ping_pongs, first_position

def main():
    rng = np.random.default_rng(1)
    repetitions = 300
    print("PROGRAM 19: HANDOFF SIMULATION WITH HYSTERESIS")
    print(f"Runs per hysteresis value: {repetitions}; speed={SPEED} m/s; shadow sigma={SHADOW_SIGMA} dB")
    print(f"{'H(dB)':>7} {'Mean handoffs':>16} {'Mean ping-pong':>17} {'First handoff(m)':>19}")

    for h in (0, 2, 4, 6, 8, 10):
        results = [run(h, rng) for _ in range(repetitions)]
        mean_handoffs = np.mean([r[0] for r in results])
        mean_pingpong = np.mean([r[1] for r in results])
        positions = [r[2] for r in results if r[2] is not None]
        mean_position = float(np.mean(positions)) if positions else float("nan")
        print(f"{h:7.1f} {mean_handoffs:16.2f} {mean_pingpong:17.2f} {mean_position:19.1f}")

if __name__ == "__main__":
    main()
