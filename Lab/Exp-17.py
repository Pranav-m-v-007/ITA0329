import math

def valid_cluster_sizes(limit=20):
    values = {i*i + i*j + j*j for i in range(8) for j in range(8)}
    return sorted(n for n in values if n > 0)[:limit]

def reuse_metrics(cluster_size, total_channels=336, total_cells=21, path_loss_exponent=4.0):
    if cluster_size <= 0 or total_channels <= 0 or total_cells <= 0:
        raise ValueError("Cluster size, channels and cells must be positive.")
    channels_per_cell = total_channels // cluster_size
    reuse_ratio = math.sqrt(3 * cluster_size)  # D/R
    si_linear = reuse_ratio ** path_loss_exponent / 6.0
    si_db = 10 * math.log10(si_linear)
    capacity = total_cells * channels_per_cell
    return channels_per_cell, capacity, reuse_ratio, si_db

def main():
    total_channels, total_cells, n, required_si = 336, 21, 4.0, 18.0
    candidates = [1, 3, 4, 7, 9, 12, 13, 16, 19, 21]

    print("PROGRAM 17: FREQUENCY REUSE")
    print(f"Total channels={total_channels}, cells={total_cells}, path-loss exponent={n}")
    print(f"Required S/I = {required_si:.1f} dB\n")
    print(f"{'N':>3} {'D/R':>7} {'Ch/cell':>9} {'Capacity':>10} {'S/I(dB)':>10} {'Meets?':>8}")
    best = None
    for N in candidates:
        k, capacity, q, si = reuse_metrics(N, total_channels, total_cells, n)
        meets = si >= required_si
        if meets and best is None:
            best = N
        print(f"{N:3d} {q:7.2f} {k:9d} {capacity:10d} {si:10.2f} {('YES' if meets else 'NO'):>8}")
    print("\nSmallest cluster size meeting requirement:", best)

if __name__ == "__main__":
    main()
