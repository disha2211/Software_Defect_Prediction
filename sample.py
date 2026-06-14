def divide(a, b):
    if b == 0:
        return -1
    return a/b


"""
tested in terminal -> 

--->radon hal sample.py
output: 
sample.py:
    h1: 3
    h2: 4
    N1: 3
    N2: 5
    vocabulary: 7
    length: 8
    calculated_length: 12.75488750216347
    volume: 22.458839376460833
    difficulty: 1.875
    effort: 42.11032383086406
    time: 2.3394624350480036
    bugs: 0.007486279792153611
    
--->radon cc sample.py
output: 
sample.py
    F 1:0 divide - A
"""