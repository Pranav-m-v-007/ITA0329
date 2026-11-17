import math

def fspl_db(distance_km, frequency_mhz):
    if distance_km <= 0 or frequency_mhz <= 0:
        raise ValueError("Distance and frequency must be greater than zero.")
    return 32.44 + 20 * math.log10(distance_km) + 20 * math.log10(frequency_mhz)

def received_power_dbm(pt_dbm, gt_dbi, gr_dbi, distance_km, frequency_mhz):
    return pt_dbm + gt_dbi + gr_dbi - fspl_db(distance_km, frequency_mhz)

def maximum_range_km(pt_dbm, gt_dbi, gr_dbi, sensitivity_dbm, frequency_mhz):
    exponent = (pt_dbm + gt_dbi + gr_dbi - sensitivity_dbm
                - 32.44 - 20 * math.log10(frequency_mhz)) / 20
    return 10 ** exponent

def main():
    # Link-budget values; edit these to test other conditions.
    pt, gt, gr, sensitivity, frequency = 30.0, 2.0, 2.0, -90.0, 2400.0
    distances = [0.01, 0.05, 0.1, 0.5, 1, 2, 5, 10]

    print("PROGRAM 16: FREE-SPACE PATH LOSS")
    print(f"Pt={pt:.1f} dBm, Gt={gt:.1f} dBi, Gr={gr:.1f} dBi")
    print(f"Frequency={frequency:.0f} MHz, receiver sensitivity={sensitivity:.1f} dBm")
    print(f"{'Distance(km)':>14} {'FSPL(dB)':>12} {'Pr(dBm)':>12} {'Status':>8}")
    for d in distances:
        loss = fspl_db(d, frequency)
        pr = received_power_dbm(pt, gt, gr, d, frequency)
        status = "PASS" if pr >= sensitivity else "FAIL"
        print(f"{d:14.2f} {loss:12.2f} {pr:12.2f} {status:>8}")

    print("\nMaximum theoretical free-space range:")
    print(f"{maximum_range_km(pt, gt, gr, sensitivity, frequency):.3f} km")

    print("\nPath loss at 1 km for different frequencies:")
    for f in (900, 1800, 2400, 3500):
        print(f"{f:4d} MHz : {fspl_db(1, f):.2f} dB")

if __name__ == "__main__":
    main()
