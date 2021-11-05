list = [1,2,3,4,5]

index = 0
while True:
    print(list[index])
    index = (index + 1) % len(list)