import random
import numpy as np
import matplotlib.pyplot as plt

# Ben Williams '25
# benjamin.r.williams.25@dartmouth.edu or roaf676@gmail.com
# Randomized Algorithms, April 9th 2023
# Experimental analysis of quicksort

comparisons = 0


# Tweak test parameters here
def main():
    comparisons_hist()
    # Takes a little while to run
    experiment_and_plot(100, 10000, 100)  # Max size is inclusive


# Randomized-pivot implementation of quicksort
# Returns the sorted array
def quicksort(A):
    global comparisons
    if len(A) == 0:
        return A
    # Random pivot!
    p = A[random.randrange(len(A))];
    (X, Y, Z) = pivot(A, p)
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
def pivot(A, piv):
    global comparisons
    X = []
    Y = []
    Z = []
    for i in range(0, len(A), 1):
        if A[i] < piv:
            X.append(A[i])
            # Only one comparison here
            comparisons += 1
        elif A[i] == piv:
            Y.append(A[i])
            # Two comparisons including the A[i] < piv
            comparisons += 2
        else:
            Z.append(A[i])
            # Two comparisons before, none here
            comparisons += 2
    return (X, Y, Z)


# Creates a histogram of the number of comparisons for arrays of size 100 and 1000
def comparisons_hist():
    global comparisons
    plot1 = plt.subplot2grid((2, 1), (0, 0))
    plot2 = plt.subplot2grid((2, 1), (1, 0))

    # Array of size 100
    A = np.random.permutation(100);
    result_100 = []
    for i in range(0, 100):
        quicksort(A)
        result_100.append(comparisons)
        comparisons = 0
    plot1.hist(result_100)
    plot1.set_title("Comparisons for n = 100")
    plot1.set_xlabel("# Comparisons")
    plot1.set_ylabel("# Occurrences")

    # Array of size 1000
    B = np.random.permutation(1000)
    result_1000 = []
    for i in range(0, 100):
        quicksort(B)
        result_1000.append(comparisons)
        comparisons = 0
    plot2.hist(result_1000)
    plot2.set_title("Comparisons for n = 1000")
    plot2.set_xlabel("# Comparisons")
    plot2.set_ylabel("# Occurences")

    plt.tight_layout()
    plt.show()


# Input: The range of sizes that will be experimented on
# Plots the array
def experiment_and_plot(start, finish, step):
    global comparisons

    # List of the differences from avg comparisons to expected
    deltaList = []
    expected = []
    actual_average = []
    xAxis = []

    # For all sizes in the range (inclusive)
    for size in range(start, finish + step, step):
        # Progress check for sanity (takes a while to run)
        # print(size)
        xAxis.append(size)
        A = np.random.permutation(size)

        # Sort the array 100 times, while the comparisons keep increasing
        for i in range(100):
            quicksort(A)
        avgComp = comparisons / 100

        actual_average.append(avgComp)
        harmonic = 0

        # Calculate the harmonic value (Approx ln(n), but using actual value here to be accurate)
        for j in range(1, size):
            harmonic += (1 / j)

        expected.append(2 * size * harmonic)

        # Deviation from the expected number of comparisons
        delta = avgComp / (2 * size * harmonic)
        deltaList.append(delta)

        # Reset comparisons after
        comparisons = 0

    # Make 3 plots
    plot1 = plt.subplot2grid((4, 4), (0, 0), rowspan=2, colspan=2)
    plot2 = plt.subplot2grid((4, 4), (2, 0), rowspan=2, colspan=2)

    plot1.plot(xAxis, expected)
    plot1.set_title("Expected Comparisons (orange) vs Actual Comparisons (green)")
    plot1.plot(xAxis, expected)
    plot1.plot(xAxis, actual_average)
    plot1.set_xlabel("Size of array")
    plot1.set_ylabel("# Comparisons")

    plot2.plot(xAxis, deltaList)
    plot2.set_title("Ratio of actual / expected comparisons")
    plot2.set_xlabel("Size of array")
    plot2.set_ylabel("Actual / Expected")

    plt.tight_layout()
    plt.show()


main()