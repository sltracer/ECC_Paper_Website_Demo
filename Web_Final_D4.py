
import Module
import math


def set_redundant(target_value, redundant_list):
    """ Given indices of redundant_list, set values for them that their Xor sum equals to the given target_value.
    Args:
        target_value (str): Target Xor product sum of all redundant trits.
        redundant_list (list): Indices of all redundant trits
        
    Returns:
        dict: Redundant trits with their values that P_all = 0.
        
    Example:
        >>> set_redundant("120", ["011", "010", "110"])
        {'011': 0, '010': 1, '110': 1}

    Special Cases:
        - 3D case: Uses specific linear combinations of first 3 digits
        - Even dimensions <7: Implements symmetric difference equations
        - General case: Follows center-out pattern calculations
        
    Note:
        - All values computed modulo 3
        - Calculation rules vary by dimension parity and size
    """
    dimension = len(redundant_list)
    value = "0"*dimension
    Redundant_Mapping = {key: int(value) for key, value in zip(redundant_list, value)}

    if(dimension==3):
        Redundant_Mapping = {key: int(value) for key, value in zip(redundant_list, value)}
        Redundant_Mapping[redundant_list[0]] = (2*int(target_value[0])+ int(target_value[1]))%3
        Redundant_Mapping[redundant_list[1]] = (int(target_value[0])+ 2*int(target_value[1])+ int(target_value[2]))%3
        Redundant_Mapping[redundant_list[2]] = (int(target_value[1])+ 2*int(target_value[2]))%3
        return Redundant_Mapping
    
    if(dimension<7 and dimension%2==0):
        Redundant_Mapping[redundant_list[0]]+=int(target_value[dimension//2])
        for i in range(0,(dimension-1)//2):
            Redundant_Mapping[redundant_list[2*i+1]]+=(int(target_value[dimension-1-i])-int(target_value[dimension//2]))
            Redundant_Mapping[redundant_list[2*i+2]]-=(int(target_value[dimension-1-i])-int(target_value[dimension//2]))

        for j in range(0, dimension//2):
            Redundant_Mapping[redundant_list[2*j]]-=int(target_value[dimension//2-1-j])
            Redundant_Mapping[redundant_list[2*j+1]]+=int(target_value[dimension//2-1-j])
        
        Redundant_Mapping = {key: value % 3 for key, value in Redundant_Mapping.items()}
    else:
        Redundant_Mapping[redundant_list[0]]+=int(target_value[math.ceil(dimension/2)-1])

        for i in range(0,(dimension)//2):
            Redundant_Mapping[redundant_list[2*i]]+=(int(target_value[dimension-1-i])-int(target_value[math.ceil(dimension/2)-1]))
            Redundant_Mapping[redundant_list[2*i+1]]-=(int(target_value[dimension-1-i])-int(target_value[math.ceil(dimension/2)-1]))

        for j in range(0, (dimension-1)//2):
            Redundant_Mapping[redundant_list[2*j+1]]-=int(target_value[math.ceil(dimension/2)-1-(j+1)])
            Redundant_Mapping[redundant_list[2*j+2]]+=int(target_value[math.ceil(dimension/2)-1-(j+1)])
        Redundant_Mapping = {key: value % 3 for key, value in Redundant_Mapping.items()}

    return Redundant_Mapping

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-Main_Area=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def main_function(input_ternary):
    """D4 Error-Correcting Code Generator
    Encodes an input ternary string into a D4 error-correcting code.
    
    Args:
        input_ternary (str): Input ternary message
        
    Returns:
        tuple: 
            - final_code (str): Encoded ternary string with parity bits
            - code_length (int): Total length of encoded message
            - efficiency (float): Ratio of original length to encoded length
    
    Example:
        >>> main_function("120102")
        ('211120102110', 12, 0.5)
        
    Process Flow:
        1. Dimension Calculation: Determine optimal code dimension
        2. Index Generation: Create I_1 and I_2 
        3. Redundancy Selection: Identify redundancy positions
        4. Mapping: Assign input digits to message positions
        5. Parity Calculation:
           - P_all: Main parity checksum (forced to 0)
           - O: Odd parity check
           - E: Even parity check
        6. Code Assembly: Combine message + parity bits
    
    Special Features:
        - Adaptive dimension selection based on input length
        - Dual parity system (O and E bits)
        - Optimized redundancy placement via d4_build_redundant_list
        
    Note:
        - Requires helper functions from Module.py:
            var_d4_generate_I_odd_or_even(), d4_build_redundant_list(), 
            sort_ternary(), ternary_xor_sum()
    """
        
    #=-=-=-=-=-=-=- Determine the Dimension =-=-=-=-=-=-=-
    length = len(input_ternary)
    dimension = 3 # Here we start with 3 need to announce it

    max_length_curr_dimension = 2*Module.fr(dimension)-dimension
    while length > max_length_curr_dimension:
        dimension+=1
        max_length_curr_dimension = 2*Module.fr(dimension)-dimension

    #=-=-=-=-=-=-=- Generate I_1&I_2 =-=-=-=-=-=-=-
    I_1 = Module.var_d4_generate_I_odd_or_even(dimension,1)
    I_2 = Module.var_d4_generate_I_odd_or_even(dimension,2)
    second_cut_amount = length-(Module.fr(dimension)-dimension) # amount left after 1st set


    I_2 = I_2[:second_cut_amount] # Still need to double check this length


    #=-=-=-=-=-=-=- Pick Redundant Index from I_1=-=-=-=-=-=-=-
    S = Module.d4_build_redundant_list(dimension) # Which is the redundant Cell for now.

    #=-=-=-=-=-=-=- Let Rest be Message Index =-=-=-=-=-=-=-
    Message_digits = [x for x in I_1 if x not in S] + I_2
    Message_digits_sorted_ternary = Module.sort_ternary(Message_digits)


    #=-=-=-=-=-=-=- Mapping Value with Index =-=-=-=-=-=-=-
    ternary_mapping = {key: int(value) for key, value in zip(Message_digits_sorted_ternary, input_ternary)}

    #=-=-=-=-=-=-=- Calculate P_all =-=-=-=-=-=-=-
    raw_xor_sum = Module.ternary_xor_sum(ternary_mapping)

    #=-=-=-=-=-=-=- Set P_all = 0 =-=-=-=-=-=-=-
    redundant_xor_target = Module.xor_multiply(2,raw_xor_sum)
    redundant_mapping = set_redundant(redundant_xor_target,S)
    total_mapping = redundant_mapping | ternary_mapping

    #=-=-=-=-=-=-=- Set P_1, P_2 = 0 =-=-=-=-=-=-=-
    even_sum = 0
    for index in I_2:
        even_sum+=total_mapping[index]
    E = (3-even_sum)%3
    total_mapping["E"] = E
    O = (3-sum(total_mapping.values()))%3
    total_mapping["O"] = O

    #=-=-=-=-=-=-=- Print Final Result =-=-=-=-=-=-=-
    all_regular_digits = I_1 + I_2
    all_regular_digits_sorted_ternary = Module.sort_ternary(all_regular_digits)

    final_code = ""
    for index in all_regular_digits_sorted_ternary:
        final_code += str(total_mapping[index])
    final_code +=str(O)
    final_code +=str(E)
    code_length = len(final_code)
    efficiency = length/code_length

    return final_code, code_length, efficiency
