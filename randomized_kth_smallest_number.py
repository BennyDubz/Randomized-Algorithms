import random
import numpy as np
import math

# Ben Williams '25
# benjamin.r.williams.25@dartmouth.edu or roaf676@gmail.com
# Randomized Algorithms, April 17th 2023
# Implementation of the randomized kth-smallest number algorithm
# Modified version of the randomized median algorithm


# Tweak test parameters here
def main():
    test_RK(1000, 1000, True)

RK_comparisons = 0

# Randomized implementation of finding a median in an array
# Returns either the median or the string "Failure" if the algorithm failed.
def rand_k_smallest(A, k):
    global RK_comparisons
    s = math.ceil(len(A) ** (2 / 3))
    t = math.floor((len(A) ** (1 / 3)) * math.log(len(A), 20))  # Note 1/4
    R = []
    n = len(A)

    # Sample s random numbers
    rand_indices = np.random.random_sample(size=s)

    # Convert random numbers to their respective indices
    for i in range(len(rand_indices)):
        R.append(int(rand_indices[i] * len(A)))

    list.sort(R)

    if int((k * s / n) - t) >= len(R):
        return "Failure - invalid a"
    elif (int((k * s / n) - t)) < 0:
        a = R[0]
    else:
        a = R[int((k * s / n) - t)]
    if (int((k * s / n) + t) + 1) >= len(R):
        b = R[len(R) - 1]
    else:
        b = R[int((k * s / n) + t) + 1]

    (A1, A2, A3) = pivot(A, a, False)
    rank_a = len(A1)

    (B1, B2, B3) = pivot(A3, b, False)
    rank_b = rank_a + len(B1)

    # Check that a and b straddle the median
    if (rank_a > k) or (rank_b < k):
        return "Failure - straddle"

        # Check that a and b aren't too far from the median
    if rank_a < (k - (2 * n * t / s)) or rank_b > k + (2 * n * t / s):
        return "Failure - too far"

    list.sort(B1)

    # Index of the kth smallest number in B1
    final_ind = math.floor(k) - rank_a - 2

    # Ensure that program doesn't crash if the final index is invalid
    # Only really applicable in very small arrays
    # print(B1)
    # print(final_ind)
    if (0 > final_ind or final_ind >= len(B1)):
        return "Failure - invalid final index"
    else:
        return B1[final_ind]


# Returns three arrays: X, Y, Z
# Every element in X is less than piv
# Every element in Y is equal to piv
# Every element in Z is greater than piv
def pivot(A, piv, QS=True):
    global QS_comparisons, RK_comparisons
    X = []
    Y = []
    Z = []
    for i in range(0, len(A), 1):
        if A[i] < piv:
            X.append(A[i])
            # Only one comparison here
            RK_comparisons += 1
        elif (A[i] == piv):
            Y.append(A[i])
            # Two comparisons including the A[i] < piv
            RK_comparisons += 2
        else:
            Z.append(A[i])
            # Two comparisons before, none here
            RK_comparisons += 2
    return (X, Y, Z)


# Tests and returns the success rate of the rand_median algorithm
# Has the option to print out specifically where it failed
def test_RK(array_size, num_attempts, print_fail=False):
    A = np.random.permutation(array_size);

    # Variables to keep track of specific types of algo failure
    success = 0
    fail_r = 0
    fail_straddle = 0
    fail_too_far = 0
    fail_invalid_b = 0
    fail_invalid_a = 0
    fail_invalid_final = 0
    fail_wrong = 0

    # Run through all attempts
    for i in range(num_attempts):
        k = random.randint(1, array_size)
        result = rand_k_smallest(A, k)
        if (result == "Failure - R too large"):
            fail_r += 1
        elif (result == "Failure - straddle"):
            fail_straddle += 1
        elif (result == "Failure - too far"):
            fail_too_far += 1
        elif (result == "Failure - invalid b"):
            fail_invalid_b += 1
        elif (result == "Failure - invalid a"):
            fail_invalid_a += 1
        elif (result == "Failure - invalid final index"):
            fail_invalid_final += 1
        elif (result != k - 1):
            fail_wrong += 1
        else:
            success += 1

    # Only print the fails if wanted
    if (print_fail):
        print("Success: " + str(success) + " Percent Success: " + str(success / num_attempts * 100) + "%")
        print("R too large Fail: " + str(fail_r))
        print("Straddle Fail: " + str(fail_straddle))
        print("Too far Fail: " + str(fail_too_far))
        print("Invalid b fail: " + str(fail_invalid_b))
        print("Invalid a fail: " + str(fail_invalid_a))
        print("Invalid final index fail: " + str(fail_invalid_final))
        print("Wrong value: " + str(fail_wrong))

    return success


main()