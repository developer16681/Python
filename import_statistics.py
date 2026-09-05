import statistics
scores = [85, 90, 78, 92, 88]
a = statistics.mean(scores)
b = statistics.median(scores)
c = statistics.mode(scores)
print("Mean:", a)
print("Median:", b)
print("Mode:", c)
list_1 = [1, 2, 3, 4, 5]
list_2 = [6, 7, 8, 9, 10]
print("Low median of list_1:", statistics.median_low(list_1))
print("Low median of list_2:", statistics.median_low(list_2))
print("High median of list_1:", statistics.median_high(list_1))
print("High median of list_2:", statistics.median_high(list_2))
grades = [85, 90, 78, 92, 88]
grades_mean = statistics.mean(grades)
print("Mean of grades:", grades_mean)
grades1 = [30, 30, 30, 30, 30]
grades_mean1 = statistics.mean(grades1)
print("variance of data is:",statistics.variance(grades1,grades_mean1))
grades2 = [20, 30, 20, 30, 20]
grades_mean2 = statistics.mean(grades2)
print("variance of data is:",statistics.variance(grades2,grades_mean2))
grades3 = [10, 20, 30, 40, 50]
stdevgrades3 = statistics.stdev(grades3)
print("standard deviation of data is:", stdevgrades3)