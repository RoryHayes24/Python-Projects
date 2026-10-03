from project import threshold_strategy, simulate_games

def main():
    # for threshold in range(12, 21):  # Test thresholds from 12 to 21
    #     strategy = threshold_strategy(threshold)
    #     results = simulate_games(strategy, 100000)
    #     print(f"Threshold: {threshold}, Results: {results['win_rate']:.2%} wins, {results['loss_rate']:.2%} losses, {results['push_rate']:.2%} pushes, Expected Return: {results['expected_return']:.4f}")
    strategy = threshold_strategy(15)  # Example threshold
    for n in [100, 1000, 10000, 100000, 1000000]:
        for run in range(5):  # Run each simulation 5 times for averaging
            results = simulate_games(strategy, n)
            print(f"Run {run + 1}, Games: {n}, Results: {results['win_rate']:.2%} wins, {results['loss_rate']:.2%} losses, {results['push_rate']:.2%} pushes, Expected Return: {results['expected_return']:.4f}")


if __name__ == "__main__":
    main()