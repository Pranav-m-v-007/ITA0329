import numpy as np

def walsh(order):
    """Generate a Walsh-Hadamard matrix; order must be a power of two."""
    if order < 1 or order & (order - 1):
        raise ValueError("Walsh matrix order must be a positive power of 2.")
    matrix = np.array([[1]], dtype=int)
    while matrix.shape[0] < order:
        matrix = np.block([[matrix, matrix], [matrix, -matrix]])
    return matrix

def main():
    rng = np.random.default_rng(11)
    chips_per_bit, users, bits_per_user = 8, 3, 6
    codes = walsh(chips_per_bit)[:users]

    print("PROGRAM 20: CDMA SPREADING AND DESPREADING")
    print("Walsh codes:")
    print(codes)
    print("\nNormalized code correlation matrix:")
    print((codes @ codes.T) / chips_per_bit)

    bits = rng.integers(0, 2, (users, bits_per_user)) * 2 - 1
    spread_signals = np.array([np.kron(bits[u], codes[u]) for u in range(users)])
    combined_channel = spread_signals.sum(axis=0)

    last_estimates = None
    for sigma in (0.0, 1.0, 2.0):
        received = combined_channel + rng.normal(0, sigma, combined_channel.shape)
        chip_blocks = received.reshape(bits_per_user, chips_per_bit)
        estimates = np.sign(chip_blocks @ codes.T / chips_per_bit).T
        errors = int(np.count_nonzero(estimates != bits))
        print(f"Noise sigma={sigma:.1f}: bit errors = {errors} of {users * bits_per_user}")
        last_estimates = estimates

    print("\nSent user 1:     ", bits[0])
    print("Received user 1:", last_estimates[0].astype(int))

    # Demonstrate decoding with an unused orthogonal code.
    wrong_code = walsh(chips_per_bit)[7]
    user1_blocks = combined_channel.reshape(bits_per_user, chips_per_bit)
    wrong_decoding = np.sign(user1_blocks @ wrong_code / chips_per_bit).astype(int)
    print("Wrong-code output:", wrong_decoding)

if __name__ == "__main__":
    main()
