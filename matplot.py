import matplotlib.pyplot as plt  # type: ignore[import-not-found]

# 1. Define the data
months = ['Jan', 'Feb', 'Mar', 'Apr']
sales = [10, 15, 7, 22]  # Note the drop in March (an anomaly!)

# 2. Create the plot
plt.plot(months, sales, marker='o', color='purple')

# 3. Add context (labels and title)
plt.title('2026 Q1 Sales Report')
plt.xlabel('Months')
plt.ylabel('Revenue (in thousands)')

# 4. Display the chart
plt.show()
