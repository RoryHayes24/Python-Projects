import numpy as np
import matplotlib.pyplot as plt
from project import threshold_strategy, simulate_games

def main():
    thresholds = []
    expected_returns = []
    standard_errors = []
    for threshold in range(12, 21):  # Test thresholds from 12 to 20
        strategy = threshold_strategy(threshold)
        results_array = []
        for _ in range(5):  # Run each simulation 5 times for averaging
            results = simulate_games(strategy, 10000)
            # print(f"Threshold: {threshold}, Results: {results['win_rate']:.2%} wins, {results['loss_rate']:.2%} losses, {results['push_rate']:.2%} pushes, Expected Return: {results['expected_return']:.4f}")
            results_array.append(results['expected_return'])
        avg_expected_return = np.mean(results_array)
        std_expected_return = np.std(results_array, ddof=1)  # Sample standard deviation
        standard_error = std_expected_return / np.sqrt(len(results_array))
        thresholds.append(threshold)
        expected_returns.append(avg_expected_return)
        standard_errors.append(standard_error)
    print(thresholds)
    print(expected_returns)
    plt.errorbar(thresholds, expected_returns, yerr=standard_errors)
    plt.xlabel('Threshold')
    plt.ylabel('Expected Return')
    plt.title('Expected Return vs Blackjack Hit Thresholds')
    plt.grid(True)
    plt.show()
    # strategy = threshold_strategy(15)  # Example threshold
    # for n in [100, 1000, 10000, 100000, 1000000]:
    #     for run in range(5):  # Run each simulation 5 times for averaging
    #         results = simulate_games(strategy, n)
    #         print(f"Run {run + 1}, Games: {n}, Results: {results['win_rate']:.2%} wins, {results['loss_rate']:.2%} losses, {results['push_rate']:.2%} pushes, Expected Return: {results['expected_return']:.4f}")


if __name__ == "__main__":
    main()