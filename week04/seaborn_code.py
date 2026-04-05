# -*- coding: utf-8 -*-

# Import seaborn library for visualization
import seaborn as sns

# Load the built-in "tips" dataset
tips = sns.load_dataset('tips')

# Display first rows of dataset
print(tips.head())

# Show dataset information (columns, types, etc.)
tips.info()

# Import matplotlib for plotting
import matplotlib.pyplot as plt

# -------------------------------------
# 1. Categorical scatter plots
# -------------------------------------

# Create a figure with 2 subplots
fig = plt.figure(figsize=(15, 5))
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)

# Strip plot: shows distribution of tips by day and gender
sns.stripplot(x='day', y='tip', hue='sex', data=tips, alpha=0.7, ax=ax1)

# Swarm plot: similar to strip plot but avoids overlapping points
sns.swarmplot(x='day', y='tip', hue='sex', data=tips, palette='Set2', alpha=0.7, ax=ax2)

# Set titles for each subplot
ax1.set_title('Strip Plot of Tip by Day and Gender')
ax2.set_title('Swarm Plot of Tip by Day and Gender')

# Save the figure as image
plt.savefig('Seaborn_Figure01.jpg')

# -------------------------------------
# 2. Count plots (frequency graphs)
# -------------------------------------

fig = plt.figure(figsize=(15, 5))
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)

# Count how many meals occurred at each time (Lunch/Dinner)
sns.countplot(x='time', data=tips, ax=ax1)

# Count meals by time and day with color grouping
sns.countplot(x='time', hue='day', data=tips, palette='Set2', ax=ax2)

ax1.set_title('Frequency of Tips by Time')
ax2.set_title('Frequency of Tips by Time and Day')

plt.savefig('Seaborn_Figure02.jpg')

# -------------------------------------
# 3. Regression plots
# -------------------------------------

fig = plt.figure(figsize=(15, 5))
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)

# Scatter plot WITH regression line
sns.regplot(
    x='total_bill',
    y='tip',
    data=tips,
    color='blue',
    scatter_kws={'s': 50, 'alpha': 0.5},
    line_kws={'linestyle': '--'},
    ax=ax1
)

# Scatter plot WITHOUT regression line
sns.regplot(
    x='total_bill',
    y='tip',
    data=tips,
    color='blue',
    scatter_kws={'s': 50, 'alpha': 0.5},
    line_kws={'linestyle': '--'},
    ax=ax2,
    fit_reg=False
)

fig.suptitle('Scatter Plots with Regression Lines', fontsize=16)
ax1.set_title('fit_reg = True')
ax2.set_title('fit_reg = False')

plt.savefig('Seaborn_Figure03.jpg')

# -------------------------------------
# 4. Histogram with KDE
# -------------------------------------

# Histogram showing distribution of tip values
sns.histplot(tips['tip'], bins=30, kde=True, color='skyblue')

plt.title('Histogram with KDE for Tips')

plt.savefig('Seaborn_Figure04.jpg')

# -------------------------------------
# 5. Joint plot
# -------------------------------------

# Shows relationship between size and tip
sns.jointplot(x='size', y='tip', data=tips, kind='scatter')

plt.savefig('Seaborn_Figure05.jpg')

# -------------------------------------
# 6. Pair plot
# -------------------------------------

# Shows pairwise relationships between variables
sns.pairplot(data=tips, hue='sex', diag_kind='hist', palette='husl')

plt.suptitle('Pairplot with Histograms by Gender', y=1.05)

plt.savefig('Seaborn_Figure06.jpg')