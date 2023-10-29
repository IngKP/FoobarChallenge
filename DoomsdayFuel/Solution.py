# %%
from fractions import Fraction


# This function computes GCD 
def compute_gcd(x, y):

   while(y):
       x, y = y, x % y
   return x

# This function computes LCM
def compute_lcm(x, y):
   lcm = (x*y)//compute_gcd(x,y)
   return lcm

def matadd(X, Y):
    result = [[X[i][j] + Y[i][j]  for j in range(len(X[0]))] for i in range(len(X))]
    return result

def matmul(A, B):
    result = [[sum(a * b for a, b in zip(A_row, B_col))
                        for B_col in zip(*B)]
                                for A_row in A]
    return result

def solution(m):
    m_row = len(m)
    m_col = len(m[0])
    x_i = [[]]
    for i in range(m_col):
        x_i[0].append(0)
    x_i[0][0] = 1
    result = []
    for i in range(m_row):
        result.append(0)
    p_x = []
    special_mat = []
    for i, row in enumerate(m):
        row_sum = sum(row)
        if row_sum == 0:
            if i == 0:
                return [1, 1]
            p_x_row = row
            special_mat.append(0)
        else:
            p_x_row = [float(element) / row_sum for element in row]
            special_mat.append(1)
        p_x.append(p_x_row)
    result_2 = []
    for i in range(100):
        x_i = matmul(x_i, p_x)
        for n in range(m_row):
            result[n] += x_i[0][n]
    for i in range(m_row):
        if special_mat[i] == 0:
            result_2.append(result[i])
    denom = sum(result_2)
    ans = []
    denom_list = []
    for n in result_2:
        fr = Fraction(n/denom).limit_denominator()
        denom_list.append(fr.denominator)
        ans.append(fr.numerator)
        
    denom = max(denom_list)
    for n in denom_list:
        denom = compute_lcm(denom, n)
    for i, n in enumerate(denom_list):
        if n != denom:
            ans[i] = int(ans[i] * denom/n)
    ans.append(int(denom))

    return ans

# %%
# Using absorbing Markov Chains by creating Q, R matrices from m

# Another viable method I tried is using normal markov chains to
# predict the n state from state 0 and n could be 100 which also
# passes all the test case and have shorter code, but it is not
# as efficient as this method in term of resources

from fractions import Fraction

# computes GCD 
def compute_gcd(x, y):
   while(y):
       x, y = y, x % y
   return x

# computes LCM
def compute_lcm(x, y):
   lcm = (x*y)//compute_gcd(x,y)
   return lcm

# computes subtraction of matrices
def matsub(X, Y):
    result = [[X[i][j] - Y[i][j]  for j in range(len(X[0]))] for i in range(len(X))]
    return result

# computes multiplication of matrices
def matmul(A, B):
    result = [[sum(a * b for a, b in zip(A_row, B_col))
                        for B_col in zip(*B)]
                                for A_row in A]
    return result


# idea of finding inverse by using determinant from stack pusher
# https://stackoverflow.com/questions/32114054/matrix-inversion-without-numpy

# finding transpose of matrix
def transposeMatrix(m):
    return list(map(list,zip(*m)))

# finding n*n identity matrix
def getIdentity(n):
    I = [[0] * i + [1] + [0] * (n - i - 1) for i in range(n)]
    return I

# finding minor
def getMatrixMinor(m, i, j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

# finding determinant
def getMatrixDeternminant(m):
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c) * m[0][c] * getMatrixDeternminant(getMatrixMinor(m, 0, c))
    return determinant

# find an inverse matrix of matrix m using det and cofactors
def getMatrixInverse(m):
    determinant = getMatrixDeternminant(m)
    # special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1] / determinant, -1 * m[0][1] / determinant],
                [-1 * m[1][0] / determinant, m[0][0] / determinant]]

    # find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
        cofactors.append(cofactorRow)
    cofactors = transposeMatrix(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c] / determinant
    return cofactors

# turn matrix into probability one
def m_to_prob(m):
    for i, row in enumerate(m):
        d = sum(row)
        if d != 0:
            m[i] = [float(x) / d for x in m[i]]

# find Q, R matrices
def QR_split(m):
    """
    Return matrices Q and R where 
    
    Q: probability matrix of non-terminal to non-terminal state
    
    R: probability matrix of non-terminal to terminal state
    
    where Q[0][1] would indicate the probability of the first non-terminal state
    going to the second non- terminal state
    """
    terminal_state = []
    non_terminal_state = []
    for i, row in enumerate(m):
        if sum(row) == 0:
            terminal_state.append(i)
        else:
            non_terminal_state.append(i)
    Q = []
    for i in non_terminal_state:
        new_row = []
        for j in non_terminal_state:
            new_row.append(m[i][j])
        Q.append(new_row)
    
    R = []
    for i in non_terminal_state:
        new_row = []
        for j in terminal_state:
            new_row.append(m[i][j])
        R.append(new_row)
    return (Q, R)
    
def solution(m):
    """
    Return ans in the format of [numerator.t0, numerator.t1,..., denominator]
    as the probability of terminal state is:
    (I + Q + Q**2 + ...)R = inverse(I-Q)R = B
    Additionally, the first state is always state 0, we can find probability of
    the terminal state in the first row of B
    """
    # turn m to probability matrix
    m_to_prob(m)
    if sum(m[0]) == 0:
        return [1, 1]
    # find Q, R and B
    Q, R = QR_split(m)
    I = getIdentity(len(Q))
    N = getMatrixInverse(matsub(I, Q))
    B = matmul(N, R)
    B0 = B[0]
    
    # store all numerator and denominator
    numer = [Fraction(x).limit_denominator().numerator for x in B0]
    denom = [Fraction(x).limit_denominator().denominator for x in B0]
    # find lcm of denominator to find suitable denominator
    lcm = 1
    for x in denom:
        lcm = compute_lcm(lcm, x)
    # make sure all numerator now have the same denominator
    for i in range(len(numer)):
        numer[i] = int(numer[i] * (lcm / denom[i]))
    # store answer
    ans = numer
    ans.append(lcm)
    return ans


