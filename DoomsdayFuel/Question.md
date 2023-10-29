# Doomsday Fuel

## Problem statement

Making fuel for the LAMBCHOP's reactor core is a tricky process because of the exotic matter involved. It starts as raw ore, then during processing, begins randomly changing between forms, eventually reaching a stable form. There may be multiple stable forms that a sample could ultimately reach, not all of which are useful as fuel.

Commander Lambda has tasked you to help the scientists increase fuel creation efficiency by predicting the end state of a given ore sample. You have carefully studied the different structures that the ore can take and which transitions it undergoes. It appears that, while random, the probability of each structure transforming is fixed. That is, each time the ore is in 1 state, it has the same probabilities of entering the next state (which might be the same state). You have recorded the observed transitions in a matrix. The others in the lab have hypothesized more exotic forms that the ore can become, but you haven't seen all of them.

Write a function answer(m) that takes an array of array of nonnegative ints representing how many times that state has gone to the next state and return an array of ints for each terminal state giving the exact probabilities of each terminal state, represented as the numerator for each state, then the denominator for all of them at the end and in simplest form. The matrix is at most 10 by 10. It is guaranteed that no matter which state the ore is in, there is a path from that state to a terminal state. That is, the processing will always eventually end in a stable state. The ore starts in state 0. The denominator will fit within a signed 32-bit integer during the calculation, as long as the fraction is simplified regularly.

For example, consider the matrix m:

```py
[
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]
```

So, we can consider different paths to terminal states, such as:

```
s0 -> s1 -> s3
s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
s0 -> s1 -> s0 -> s5
```

Tracing the probabilities of each, we find that:

```
s2 has probability 0
s3 has probability 3/14
s4 has probability 1/7
s5 has probability 9/14
```

So, putting that together, and making a common denominator, gives an answer in the form of
`[s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator]` which is:
`[0, 3, 2, 9, 14]`.

## Test cases

```py
Input:
solution.solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
Output:
[7, 6, 8, 21]

Input:
solution.solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
Output:
[0, 3, 2, 9, 14]
```

## Approach

There are 2 ways of solving this question that I have tried and both worked well:

### First Method

Using transition matrix of Markov Chains, we can find the next step of any given step as:

`Xn = AXn-1`

where `Xn` is a probability vector of step n and `Xn-1` is for step n-1, where `A` is a transition matrix. (for more info, [link to medium post](https://jadhav-pritish.medium.com/all-about-markov-chains-and-steady-state-probabilities-cdf67253cc04#:~:text=Markov%20Chain%3A&text=Given%20a%20Markov%20chain%2C%20the,distribution%20of%20the%20current%20state.))

For this question, the initial state is fixed at state 0 so we could say that `X0` or our initial step is `[1,0,0,0,0,0]`, now we just need to find the next step over and over again until the probability step stop changing, in this case, 100 times of loop will do for every test cases.

### Second Method

The second method is to calculate the terminal step probability directly using Absorbing Markov Chains. For more detail, [check the lecture from dartmouth.edu](https://math.dartmouth.edu/archive/m20x06/public_html/Lecture14.pdf)