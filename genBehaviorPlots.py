import json
import matplotlib.pyplot as plt

# Load data from JSON file
with open('ppo-final2048.json') as f:
    data = json.load(f)

# Plot histogram of # of steps
steps_data = data['# of steps']
plt.hist(list(map(int, steps_data.keys())), bins=20)
plt.title('Histogram of # of Steps')
plt.xlabel('# of Steps')
plt.ylabel('Frequency')
plt.savefig('steps_hist.png', dpi=300)
plt.show()

# Plot histogram of game scores
scores_data = data['Game Scores']
plt.hist(list(map(float, scores_data.keys())), bins=20)
plt.title('Histogram of Game Scores')
plt.xlabel('Game Score')
plt.ylabel('Frequency')
plt.savefig('scores_hist.png', dpi=300)
plt.show()

# Plot barchart of max scores
max_scores_data = data['Max Scores']
x_labels = [str(2**i) for i in range(12)]
y_values = [max_scores_data.get(str(float(x)), 0) for x in x_labels]
plt.bar(x_labels, y_values)
plt.title('Max Scores')
plt.xlabel('Tile Value')
plt.ylabel('Frequency')
plt.savefig('max_scores_bar.png', dpi=300)
plt.show()
