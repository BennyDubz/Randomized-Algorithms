import random
import matplotlib.pyplot as plt

# Ben Williams '25
# benjamin.r.williams.25@dartmouth.edu or roaf676@gmail.com
# Randomized Algorithms, April 14th 2023
# Visualization of Chernoff Bounds by sampling Bernoulli variables

e = 2.718281828459045

# Modify most of the parameters in main()
histo = True
prob_deviation_plot = False
prob = 0.5
consistent_prob = True #If False -> change probabilities manually in main()
print_x_geq_10 = False


def main():
    # Only draw histo if we want
    if histo:
        # Defining the parameters for the 50/50 Probability histogram
        fifty_fifty_plot = plt.subplot2grid((2, 4), (0, 0), rowspan=2, colspan=2)
        fifty_fifty_plot.set_title("Average Value of Bernoulli Trials \n 10000 Trials/Entry")
        fifty_fifty_plot.set_xlabel("Average value")
        fifty_fifty_plot.set_ylabel("Occurences")

        if consistent_prob:
            # Sample all the trials and plot them on the histogram
            histo_bernoulli(prob, 10000, 10, fifty_fifty_plot)
            histo_bernoulli(prob, 10000, 100, fifty_fifty_plot)
            histo_bernoulli(prob, 10000, 1000, fifty_fifty_plot)
            histo_bernoulli(prob, 10000, 10000, fifty_fifty_plot)
        else:
            # Inconsistent probability
            histo_bernoulli(0.1, 10000, 10, fifty_fifty_plot)
            histo_bernoulli(0.01, 10000, 100, fifty_fifty_plot)
            histo_bernoulli(0.001, 10000, 1000, fifty_fifty_plot)
            histo_bernoulli(0.0001, 10000, 10000, fifty_fifty_plot)

    # Only plot if we want
    if prob_deviation_plot:
        # Define epsilon
        epsilon = 0.1
        # Define parameters of the plot of deviation from expected value
        deviation_plot = plt.subplot2grid((2, 4), (0, 2), rowspan=2, colspan=2)
        if consistent_prob:
            deviation_plot.set_title(
                "Pr[Result >= (1+" + str(epsilon) + ")*Exp[Trial]], \n 1000 Trials/Entry, Exp[Trial] = " + str(prob))
        else:
            deviation_plot.set_title("Pr[Result >= (1+" + str(
                epsilon) + ")*Exp[Trial]], \n 1000 Trials/Entry, Exp[Trial] = " + "(1 / # Variables)")

        deviation_plot.set_xlabel("Number of Variables / Sample")
        deviation_plot.set_ylabel("Probability")

        plot_deviation(prob, 1000, 10000, deviation_plot, epsilon, True)

    if print_x_geq_10:
        geq_10 = [0, 0, 0, 0]
        index = 0
        for i in [10, 100, 1000, 10000]:
            results = []
            for trial in range(10000):
                results.append(sample_bernoulli(prob, i, True))
                if results[len(results) - 1] >= 10:
                    geq_10[index] += 1
            print("Pr[Sample >= 10] = " + str(geq_10[index] / 10000) + " for n = " + str(i) + " trials per sample")
            index += 1

        plt.tight_layout()
        plt.show()


# Takes a decimal probability and the number of variables
# Returns the average value of the bernoulli variable
def sample_bernoulli(probability, num_variables, return_num_ones=False):
    X = 0

    for i in range(num_variables):
        X_i = random.random()
        if X_i <= probability:
            X += 1
        # Else: add 0, so do nothing
    if return_num_ones:
        return X
    else:
        return (X / num_variables)


# Plots a histogram of value of many
def histo_bernoulli(probability, num_trials, num_variables, plot):
    results = []

    # Perform all the trials and add them to the results
    for trial in range(num_trials):
        results.append(sample_bernoulli(probability, num_variables))

    # Histogram and legend
    plot.hist(results, label=(str(num_variables) + " Variables / Trial"))
    plot.legend(loc=0)


# Plot the probabilities that a trial's average differs more than (epsilon*expected value)
#   As the number of variables / sample changes
def plot_deviation(probability, num_trials, max_variables, plot, epsilon, one_over_n=False):
    xAxis = []
    deviation_prob = []

    # Change the number of variables over time
    for num_variables in range(10, max_variables, int((max_variables - 10) / 50)):
        # Re-cast probability if necessary
        if (one_over_n):
            probability = 1 / num_variables

        results = []
        xAxis.append([num_variables])
        # Perform all the trials and add them to the results
        for trial in range(num_trials):
            results.append(sample_bernoulli(probability, num_variables))

        # Find the deviation from the expected value by positive epsilon
        count = 0
        for result in results:
            if result > probability * (1 + epsilon):
                count += 1
        deviation_prob.append(count / num_trials)

    plot.plot(xAxis, deviation_prob)


main()


