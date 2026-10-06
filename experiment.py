import numpy as np
import matplotlib.pyplot as plt
import csv
from project import threshold_strategy, simulate_games

def main():
    with open("results/threshold_results.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Threshold",
            "Run",
            "Games",
            "Wins",
            "Losses",
            "Pushes",
            "Player Busts",
            "Dealer Busts",
            "Win Rate",
            "Loss Rate",
            "Push Rate",
            "Expected Return"
        ])

        for threshold in range(12, 21):  # Test thresholds from 12 to 20
            strategy = threshold_strategy(threshold)
            for _ in range(5):  # Run each simulation 5 times for averaging
                results = simulate_games(strategy, 1000000)
                writer.writerow([
                    threshold,
                    _ + 1,
                    results["games"],
                    results["wins"],
                    results["losses"],
                    results["pushes"],
                    results["player_busts"],
                    results["dealer_busts"],
                    results["win_rate"],
                    results["loss_rate"],
                    results["push_rate"],
                    results["expected_return"]
                ])

    # strategy = threshold_strategy(15)  # Example threshold
    # for n in [100, 1000, 10000, 100000, 1000000]:
    #     for run in range(5):  # Run each simulation 5 times for averaging
    #         results = simulate_games(strategy, n)
    #         print(f"Run {run + 1}, Games: {n}, Results: {results['win_rate']:.2%} wins, {results['loss_rate']:.2%} losses, {results['push_rate']:.2%} pushes, Expected Return: {results['expected_return']:.4f}")


if __name__ == "__main__":
    main()