def erlang_b(offered_traffic, channels):
    """Erlang B blocking probability using a stable recursive calculation."""
    if offered_traffic < 0 or channels < 0:
        raise ValueError("Traffic and channel count cannot be negative.")
    blocking = 1.0
    for m in range(1, channels + 1):
        blocking = offered_traffic * blocking / (m + offered_traffic * blocking)
    return blocking

def channels_needed(offered_traffic, target_gos):
    if not 0 < target_gos < 1:
        raise ValueError("GOS must be between 0 and 1.")
    channels = 0
    while erlang_b(offered_traffic, channels) > target_gos:
        channels += 1
    return channels

def max_load(channels, target_gos, upper=500.0):
    low, high = 0.0, upper
    for _ in range(80):
        mid = (low + high) / 2
        if erlang_b(mid, channels) <= target_gos:
            low = mid
        else:
            high = mid
    return low

def main():
    print("PROGRAM 18: ERLANG B CALL BLOCKING")
    print("Blocking probability B(E,C)\n")
    traffic_values = (2, 5, 10, 20)
    print(f"{'C':>4}" + "".join(f"{('E='+str(e)):>12}" for e in traffic_values))
    for c in (5, 10, 20, 30):
        print(f"{c:4d}" + "".join(f"{erlang_b(e,c):12.4f}" for e in traffic_values))

    users, calls_per_hour, holding_seconds = 2000, 1.5, 120
    offered = users * calls_per_hour * holding_seconds / 3600
    print(f"\nOffered traffic = {offered:.1f} Erlang")
    for gos in (0.05, 0.02, 0.01):
        print(f"GOS {gos:.0%}: channels needed = {channels_needed(offered, gos)}")
    print(f"Maximum load for 20 channels at 2% blocking = {max_load(20, 0.02):.2f} Erlang")

    # Trunking comparison: one 30-channel group vs three independent 10-channel groups.
    total_load = 20.0
    one_group = erlang_b(total_load, 30)
    three_groups = erlang_b(total_load / 3, 10)  # same load divided equally
    print("\nTrunking comparison at 20 Erlang total:")
    print(f"One group (30 channels): blocking = {one_group:.4%}")
    print(f"Three groups (10 channels each): blocking per group = {three_groups:.4%}")

if __name__ == "__main__":
    main()
