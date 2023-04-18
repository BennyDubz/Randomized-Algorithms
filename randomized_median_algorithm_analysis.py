import random
import numpy as np
import math
import matplotlib.pyplot as plt
import time

# Ben Williams '25
# benjamin.r.williams.25@dartmouth.edu or roaf676@gmail.com
# Randomized Algorithms, April 10-11th 2023
# Implementation and Analysis of the randomized median algorithm

QS_comparisons = 0
RM_comparisons = 0


# Tweak test parameters here
def main():
    # graph_success_chance(100, 10000)
    # efficiency_comparison_QS(1000,1000)
    # python_sort_comparison(1000, 1000)
    test_RM(1000, 1000, True)


# Randomized implementation of finding a median in an array
# Returns either the median or the string "Failure" if the algorithm failed.
def rand_median(A):
    global RM_comparisons
    s = math.ceil(len(A) ** (2 / 3))
    t = math.floor((len(A) ** (1 / 3)) * math.log(len(A), 20))
    R = []

    # Sample s random numbers
    rand_indices = np.random.random_sample(size=s)

    # Convert random numbers to their respective indices
    for i in range(len(rand_indices)):
        R.append(int(rand_indices[i] * len(A)))

    # Bail if this happens
    # Should not happen with the rand_indices implementation
    if len(R) > 2 * s:
        return "Failure - R too large"

    list.sort(R)

    if (int(s / 2 - t) < 0 or int(s / 2 - t) >= len(R)):
        return "Failure - invalid a"
    else:
        a = R[int(s / 2 - t)]
    if (int(s / 2 + t) + 1) >= len(R):
        return "Failure - invalid b"
    else:
        b = R[int(s / 2 + t) + 1]

    (A1, A2, A3) = pivot(A, a, False)
    rank_a = len(A1)

    (B1, B2, B3) = pivot(A3, b, False)
    rank_b = rank_a + len(B1)

    # Check that a and b straddle the median
    if (rank_a > len(A) / 2) or (rank_b < len(A) / 2):
        return "Failure - straddle"

        # Check that a and b aren't too far from the median
    if (rank_a < (len(A) / 2) - (2 * len(A) * t / s)) or (rank_b > (len(A) / 2) + (2 * len(A) * t / s)):
        return "Failure - too far"

    list.sort(B1)

    final_ind = math.floor(len(A) / 2) - rank_a - 1

    # Ensure that program doesn't crash if the final index is invalid
    # Only really applicable in very small arrays
    if (0 > final_ind or final_ind >= len(B1)):
        return "Failure - invalid final index"
    else:
        return B1[final_ind]


# Randomized-pivot implementation of quicksort
# Returns the sorted array
def quicksort(A):
    global QS_comparisons
    if len(A) == 0:
        return A
    # Random pivot!
    p = A[random.randrange(len(A))]
    (X, Y, Z) = pivot(A, p, True)
    X = quicksort(X)
    Z = quicksort(Z)
    # Combine it all into one array
    X.extend(Y)
    X.extend(Z)
    return X


# Returns three arrays: X, Y, Z
# Every element in X is less than piv
# Every element in Y is equal to piv
# Every element in Z is greater than piv
def pivot(A, piv, QS=True):
    global QS_comparisons, RM_comparisons
    X = []
    Y = []
    Z = []
    for i in range(0, len(A), 1):
        if A[i] < piv:
            X.append(A[i])
            # Only one comparison here
            if QS:
                QS_comparisons += 1
            else:
                RM_comparisons += 1
        elif (A[i] == piv):
            Y.append(A[i])
            # Two comparisons including the A[i] < piv
            if QS:
                QS_comparisons += 2
            else:
                RM_comparisons += 2
        else:
            Z.append(A[i])
            # Two comparisons before, none here
            if QS:
                QS_comparisons += 2
            else:
                RM_comparisons += 2
    return (X, Y, Z)


# Tests and returns the success rate of the rand_median algorithm
# Has the option to print out specifically where it failed
def test_RM(array_size, num_attempts, print_fail=False):
    A = np.random.permutation(array_size)

    # Variables to keep track of specific types of algo failure
    success = 0
    fail_r = 0
    fail_straddle = 0
    fail_too_far = 0
    fail_invalid_b = 0
    fail_invalid_a = 0
    fail_invalid_final = 0

    # Run through all attempts
    for i in range(num_attempts):
        result = rand_median(A)
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

    return success

# Graphs the chance of rand_median success as the array size changes
def graph_success_chance(max_array_size, num_attempts):
    xAxis = []
    success_percent = []

    for size in range(10, max_array_size, int(max_array_size / 50)):
        xAxis.append(size)
        success_percent.append(test_RM(size, num_attempts) / num_attempts)

    plot1 = plt.subplot2grid((2, 2), (0, 0), rowspan=2, colspan=2)

    plot1.plot(xAxis, success_percent)
    plot1.set_title("rand_median Probability of Success")
    plot1.set_xlabel("Size of array")
    plot1.set_ylabel("Success Chance")

    plt.tight_layout()
    plt.show()


# graph_success_chance(250, 1000)

def efficiency_comparison_QS(max_array_size, num_attempts):
    global QS_comparisons, RM_comparisons
    xAxis = []
    QS_results = []
    RM_results = []
    for size in range(50, max_array_size, int(max_array_size / 50)):
        xAxis.append(size)

        # Test quicksort
        for i in range(num_attempts):
            A = np.random.permutation(size);
            quicksort(A)
            # Median is just middle of returned list, so only 1 more check and we don't count it

        avgCompQS = QS_comparisons / num_attempts
        QS_results.append(avgCompQS)
        QS_comparisons = 0

        # Test RM
        test_RM(size, num_attempts)
        avgCompRM = RM_comparisons / num_attempts
        RM_results.append(avgCompRM)
        RM_comparisons = 0

    plot = plt.subplot2grid((2, 2), (0, 0), rowspan=2, colspan=2)

    plot.plot(xAxis, QS_results)
    plot.set_title("QS Comparisons (Blue) versus RM comparisons (Orange)")
    plot.plot(xAxis, RM_results)
    plot.set_xlabel("Size of array")
    plot.set_ylabel("# Comparisons")

# Compares the time elapsed of Python's sorting of an array (since the median is trivial then)
#   to the rand_median algorithm
# Plots out the results
def python_sort_comparison(max_array_size, num_attempts):
    xAxis = []
    PY_S_results = []
    RM_results = []

    # Run tests for every size in the array range (50 different values)
    for size in range(50, max_array_size, int(max_array_size / 50)):
        xAxis.append(size)

        # Test quicksort
        PY_S_Time_start = time.time()
        for i in range(num_attempts):
            A = list(np.random.permutation(size));
            list.sort(A)
            # Median is just middle of returned list, so only 1 more check and we don't count it
        PY_S_Time_end = time.time()

        # Calculate the average time/run and add to results
        avgPYSTime = (PY_S_Time_end - PY_S_Time_start) / num_attempts
        PY_S_results.append(avgPYSTime)

        # Test rand_median
        RM_Time_Start = time.time()
        for i in range(num_attempts):
            A = list(np.random.permutation(size));
            rand_median(A)
        RM_Time_End = time.time()

        # Calculate the average time/run and add to results
        avgRMTime = (RM_Time_End - RM_Time_Start) / num_attempts
        RM_results.append(avgRMTime)

    plot1 = plt.subplot2grid((4, 4), (0, 2), rowspan=2, colspan=2)

    plot1.plot(xAxis, PY_S_results)
    plot1.set_title("Python Sort Time (Blue) versus RM Time (Orange)")
    plot1.plot(xAxis, RM_results)
    plot1.set_xlabel("Size of array")
    plot1.set_ylabel("Amount of Time")


main()
