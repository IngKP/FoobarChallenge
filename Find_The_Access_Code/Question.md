# Find the access code

## Problem statement

In order to destroy Commander Lambda's LAMBCHOP doomsday device, you'll need access to it. But the only door leading to the LAMBCHOP chamber is secured with a unique lock system whose number of passcodes changes daily. Commander Lambda gets a report every day that includes the locks' access codes, but only she knows how to figure out which of several lists contains the access codes. You need to find a way to determine which list contains the access codes once you're ready to go in.

Fortunately, now that you're Commander Lambda's personal assistant, she's confided to you that she made all the access codes "lucky triples" in order to help her better find them in the lists. A "lucky triple" is a `tuple (x, y, z)` where x divides y and y divides z, such as (1, 2, 4). With that information, you can figure out which list contains the number of access codes that matches the number of locks on the door when you're ready to go in (for example, if there's 5 passcodes, you'd need to find a list with 5 "lucky triple" access codes).

Write a function solution(l) that takes a list of positive integers l and counts the number of "lucky triples" of `(lst[i], lst[j], lst[k])` where `i < j < k`. The length of l is between 2 and 2000 inclusive.  The elements of l are between 1 and 999999 inclusive. The answer fits within a signed 32-bit integer. Some of the lists are purposely generated without any access codes to throw off spies, so if no triples are found, return 0.

For example, `[1, 2, 3, 4, 5, 6]` has the triples: `[1, 2, 4], [1, 2, 6], [1, 3, 6]`, making the answer 3 total.

## Test cases

```py
Input:
solution.solution([1, 2, 3, 4, 5, 6])
Output:
3

Input:
solution.solution([1, 1, 1])
Output:
1
```

## Solution

Under an assumption that l is already sorted in ascended order, for each number a, find numbers on the right that % a == 0 and store those in matrix X. For example, let `l = [1, 2, 3, 4, 5, 6]`:

```
X = [[2,3,4,5,6],   --> % 1 == 0
    [4,6],          --> % 2 == 0
    [6],            --> % 3 == 0
    [],             --> % 4 == 0
    [],             --> % 5 == 0
    []]             --> last one is always empty
```

Now we know that `l[0]` can pair with any numbers in `X[0]`, say we choose `2`, you can pair `l[0], X[0][0] and any in X[1]`. Same goes for `3`, you can pair `l[0], X[0][1] with any in X[2]`. To simplify, we only need to store index instead of actual number and count `X[index] in any matrix in X` and we could easily find an answer. For reference, you can check [James Huang's linkedin post](https://www.linkedin.com/pulse/google-foobar-challenge-lv3-james-huang/).