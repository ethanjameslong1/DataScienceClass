#!usr/bin/python3
"""

Name: Ethan
Date: 01 8 2026
Assignment: 1
Due Date: jan 14th 2026
About this project: simple script to show that I can write python code
Assumptions: assumes you have python workined and that it's located in usr/bin/python3
All work below was performed by Ethan Long

"""

try:
    n = int(input("Please enter the number to approximate the square root of: "))
    while n < 0:
        n = int(input("Please enter a number greater than 0"))
except:
    n = int(input("Please enter a number only!"))
try:
    i = int(input("Please enter the number of iterations: "))
    while n < 0:
        n = int(input("Please enter a number greater than 0"))
except:
    n = int(input("Please enter a number only!"))

x = 1
for val in range(i):
    x = 0.5 * (x + n / x)

print(x)
