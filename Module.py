
from itertools import product
from itertools import combinations
import math
import numpy as np

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- Functions =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#=-=-=-=-=-=-=- Calculate Bound for D4 =-=-=-=-=-=-=-
def fr(r):
    """
    Calculate the bound value for D4 code analysis.

    Args:
        r (int): Input parameter representing code length

    Returns:
        int: Computed bound value

    Note:
        Follows piecewise calculation rules:
        - r=3 → n=2
        - 3<r≤7 → floor(r/2)
        - r≥8 → ceil(r/2)-1
    """
        
    n = 0
    if(r == 3):
        n = 2
    if(r>3 and r<=7):
        n = math.floor(r/2)
    elif(r>=8):
        n = math.ceil(r/2)-1
    result = 0
    for i in range(n,2*n):
        result += math.comb(r,i)
    return result

#=-=-=-=-=-=-=- var I_1&I_2 for D4 =-=-=-=-=-=-=- 
def var_d4_generate_I_odd_or_even(length,num):
    """
    Generate I-set for D4 code analysis with specified digit (1 for I_1 or 2 for I_2).

    Args:
        length (int): Desired length of index
        num (int): I_1 or I_2

    Returns:
        list: Sorted list of ternary numbers with specified digit positions

    Raises:
        ValueError: If num is not 1 or 2

    Example:
        >>> var_d4_generate_I_odd_or_even(3, 1)
        ['011', '101', '110', '111']
    """

    if num not in {1, 2}:
        raise ValueError("num should be either 1 or 2")

    n = math.ceil(length / 2) - 1
    if length > 3 and length < 8:
        n = math.floor(length / 2)
    if(length ==3):
        n = 2 
    I_list = []

    for k in range(n, 2 * n):  # k in [n, 2n-1]
        for ones_positions in combinations(range(length), k):
            ternary_number = ['0'] * length  # Start with all zeros
            for pos in ones_positions:
                ternary_number[pos] = str(num) 
            I_list.append(''.join(ternary_number))

    return sorted(I_list)

#=-=-=-=-=-=-=- Pick Indices for D3 =-=-=-=-=-=-=- 
def generate_ternary_set_half(length):
    """
    Generate a subset of ternary strings of a given length, where largest nonzero digits equals to 1.
    
    Parameters:
        length (int): The total length of each resulting ternary string.

    Returns:
        list of str: A sorted list of generated ternary strings.

    Example:
        >>> generate_ternary_set_half(3)
        ['001', '010', '011', '012', '100', '101', '102', '110', '111', '112', '120', '121', '122']
    """
        
    total_set = set()
    for i in range(0,length):
        base_ternary_set = {''.join(map(str, digits)) for digits in product(range(3), repeat=i)}
        modified_ternary_set = {"0"*(length-1-i)+'1' + num for num in base_ternary_set}
        total_set = total_set | modified_ternary_set
    
    # Return the sorted result
    return sorted(total_set)

#=-=-=-=-=-=-=- Ask Input(In whatever length) from User(But a min length)=-=-=-=-=-=-=- 
def get_ternary_input_var(min_length):
    """
    Prompt the user to input a valid ternary number (digits 0, 1, 2) with 
    a minimum required length.

    The function repeatedly asks for input until the user enters a string 
    that:
      - Contains only ternary digits ('0', '1', or '2')
      - Has a length greater than or equal to `min_length`

    Parameters:
        min_length (int): The minimum number of digits required in the input.

    Returns:
        str: A valid ternary number string entered by the user.

    Example:
        >>> get_ternary_input_var(4)
        Please enter a ternary number (digits 0, 1, 2 only, at least 4 digits long): 1020
        '1020'
    """

    while True:
        user_input = input(f"Please enter a ternary number (digits 0, 1, 2 only, at least {min_length} digits long): ")
        
        # Check if input contains only '0', '1', or '2' and has a length of at least min_length
        if len(user_input) >= min_length and all(char in '012' for char in user_input):
            return user_input
        else:
            print(f"Invalid input. Ensure you enter ternary digits (0, 1, 2) and the length is at least {min_length}.")

#=-=-=-=-=-=-=- Sort the Map with Ascending on Index =-=-=-=-=-=-=- 
def sort_ternary(list):
    """
    Sort a list of ternary numbers (as strings) in ascending order 
    based on their decimal value.

    The function converts each ternary string to its decimal equivalent,
    sorts the list, and then converts the sorted values back to uniformly
    padded ternary strings.

    Parameters:
        list (list of str): List of ternary strings (e.g., ['10', '2', '01']).

    Returns:
        list of str: Sorted list of ternary strings with consistent length.

    Example:
        >>> sort_ternary(['10', '2', '01'])
        ['01', '02', '10']
    """
    list_decimal = [int(index, 3) for index in list]
    list_decimal_sorted = sorted(list_decimal)
    max_length_list = math.ceil(math.log(max(list_decimal_sorted)+1,3)) # Notice +1 here so 100=9 will have result 3
    list_decimal_sorted_ternary = [np.base_repr(index, base=3).zfill(max_length_list) for index in list_decimal_sorted]

    return list_decimal_sorted_ternary

#=-=-=-=-=-=-=- Special Redundant_List for D4 =-=-=-=-=-=-=- 
def d4_build_redundant_list(dimension):
    """
    Construct a list of redundant ternary strings used in the D4 encoding scheme,
    based on a given dimension.

    The function generates a list `R` of length `dimension`, where each entry is a
    specially patterned ternary string (consisting of 0s and 1s) used for parity
    or redundancy checks in coding theory (e.g., error correction).

    Parameters:
        dimension (int): The size of the D4 code (number of bits or symbols).

    Returns:
        list of str: A list of `dimension` ternary strings representing the
                     redundant structure for the D4 code.

    Example:
        >>> d4_build_redundant_list(3)
        ['011', '111', '110']
    """

    n = math.ceil(dimension / 2) - 1
    if dimension == 3:
        n = 2
    if dimension > 3 and dimension < 8:
        n = math.floor(dimension / 2)-1

    R = [None]*dimension

    if(dimension==3):
        R[0] = "011"
        R[1] = "111"
        R[2] = "110"
        return R
    for k in range(0, dimension):
        if(dimension%2 == 1 or dimension > 7):
            R[k] = "0"*(dimension-(n+1)-(k+2)//2) +"1"*(n+1 + (k+1)%2) + "0"* ((k+1)//2)
        else:
            R[k] = "0"*(dimension-(n+1)-(k+1)//2) +"1"*(n+1 + (k)%2) + "0"* ((k)//2)
    
    return R

#=-=-=-=-=-=-=- Calculating Xor Sum(P_all) =-=-=-=-=-=-=- 
def ternary_xor_sum(index_value_mapping):
    """
    Compute the cumulative ternary XOR sum (P_all) for a mapping of ternary indices 
    and their corresponding scalar coefficients.

    Parameters:
        index_value_mapping (dict): Dictionary where keys are ternary strings (indices),
                                    and values are integer coefficients (0, 1, or 2).

    Returns:
        str: The resulting ternary number as a string after calculating the XOR sum.

    Example:
        >>> ternary_xor_sum({'102': 1, '210': 2})
        '021'
    """

    first_index = next(iter(index_value_mapping))
    current_xor_sum = '0' * len(first_index)

    for index, value in index_value_mapping.items():
        current_product = xor_multiply(value,index)
        current_xor_sum = ternary_xor(current_xor_sum,current_product)

    return current_xor_sum

#=-=-=-=-=-=-=- Operation: Multiply(Basic on Xor) =-=-=-=-=-=-=-
def xor_multiply(coefficient, index):
    """
    Perform a specialized ternary multiplication based on XOR operation.

    Multiplies a ternary number ('index') by a scalar coefficient (0, 1, or 2)
    using ternary XOR arithmetic.

    Parameters:
        coefficient (int): The scalar multiplier (allowed values: 0, 1, or 2).
        index (str): The ternary number to be multiplied.

    Returns:
        str: The resulting ternary number after multiplication.

    Example:
        >>> xor_multiply(0, '102')
        '000'

        >>> xor_multiply(1, '102')
        '102'

        >>> xor_multiply(2, '102')
        '201'
    """

    mult_result = '0' * len(index)  # Default result as zero string of same length as index

    if coefficient == 0:
        return mult_result  # If coefficient is 0, result is all zeros
    if coefficient == 1:
        return index  # If coefficient is 1, return the index itself
    if coefficient == 2:
        return ternary_xor(index, index)  # If coefficient is 2, perform ternary XOR of index with itself
    
    print("Coefficient:"+ coefficient+" Type:"+ type(coefficient))
    print("Value of coefficient is illegal")
    return mult_result

#=-=-=-=-=-=-=- Operation: Xor(for Ternary) =-=-=-=-=-=-=-
def ternary_xor(a, b):
    """
    Perform a ternary XOR operation between two ternary numbers.

    The ternary XOR is defined digit-wise as (a_i + b_i) mod 3, 
    for corresponding digits a_i and b_i.

    Parameters:
        a (str): First ternary number as a string.
        b (str): Second ternary number as a string.

    Returns:
        str: Resulting ternary number as a string.

    Example:
        >>> ternary_xor('102', '221')
        '020'
        
        >>> ternary_xor('12', '1020')
        '1102'
    """

    max_length = max(len(a), len(b))
    a = a.zfill(max_length)
    b = b.zfill(max_length)
    
    result = []
    for i in range(max_length):
        xor_value = (int(a[i]) + int(b[i])) % 3
        result.append(str(xor_value))
    
    return ''.join(result)

#=-=-=-=-=-=-=- All Ternary Number with in Such Length =-=-=-=-=-=-=-
def generate_ternary_set(length):
    """
    Generate a sorted list of all possible ternary numbers (numbers using digits 0, 1, 2)
    of a specified length.

    Parameters:
        length (int): The length of the ternary numbers to be generated.

    Returns:
        list of str: Sorted list containing all possible ternary numbers as strings.

    Example:
        >>> generate_ternary_set(2)
        ['00', '01', '10', '11']
        
        >>> generate_ternary_set(3)
        ['000', '001', '002', ..., '221', '222']
    """

    ternary_set = {''.join(map(str, digits)) for digits in product(range(length), repeat=length)}
    return sorted(ternary_set)

