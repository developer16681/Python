import random
print('Random Number 1=>', random.random())
print('Random Number 2=>', random.random())
print(random.randint(3, 9))
print(random.randrange(3, 9))
list = [1, 2, 3, 4, 5]
print(random.choice(list))
random.shuffle(list)
print("Printing the shuffled list", list)
numberList = [1, 2, 3, 4, 5]
print(random.choices(numberList, weights=[10, 1, 1, 1, 1], k=0))
numberList = [1, 2, 3, 4, 5]
print(random.choices(numberList, weights=[10, 1, 1, 1, 1], k=1))
numberList = [1, 2, 3, 4, 5]
print(random.choices(numberList, weights=[10, 1, 1, 1, 1], k=2))    
numberList = [1, 2, 3, 4, 5]
print(random.choices(numberList, weights=[10, 1, 1, 1, 1], k=3))
numberList = [1, 2, 3, 4, 5]
print(random.choices(numberList, weights=[10, 1, 1, 1, 1], k=4))
numberList = [1, 2, 3, 4, 5]
print(random.choices(numberList, weights=[10, 1, 1, 1, 1], k=5))   