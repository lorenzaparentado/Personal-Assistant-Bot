import random

text = open("responses.txt", "r")
lines = text.readlines()
answer = random.randint(0, len(lines) - 1)
print(lines[answer])