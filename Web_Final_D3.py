import Module
import math


def combine_compute_original_value(message_index_value_mapping, redundant_index_value_mapping, ternary_set):
    """
    Set the value for 00...0 to have P_all=0, and also combining two mapping together ans sorted ascending by index.

    Parameters:
        message_index_value_mapping (dict): Mapping of message indices to their values.
        redundant_index_value_mapping (dict): Mapping of redundant indices to their values.
        ternary_set (list of str): A list of ternary indices defining the desired order.

    Returns:
        dict: A dictionary mapping each index in `ternary_set` to its corresponding value,
              with the original value computed and placed at '000'.

    Example:
        >>> combine_compute_original_value({'102': 1}, {'201': 2}, ['000', '102', '201'])
        {'000': 0, '102': 1, '201': 2}
    """

    # Combine both mappings to compute the sum of all values
    total_sum = sum(message_index_value_mapping.values()) + sum(redundant_index_value_mapping.values())

    # Calculate the original value using the formula: 3 - (sum of values % 3)
    origin_value = (3 - (total_sum % 3)) % 3  # Ensuring result is in ternary range

    # Assign the original value to index '000', which means to reset P_all = 0
    combined_index_value_mapping = {**message_index_value_mapping, **redundant_index_value_mapping, '000':origin_value}

    # Reorder the combined dictionary based on ternary_set order
    ordered_combined_mapping = {idx: combined_index_value_mapping.get(idx, 0) for idx in ternary_set}

    return ordered_combined_mapping

def generate_redundant_list(length):
    """
    Generate standard basis vectors e_i as binary strings for ternary error-correcting code (d3).

    Parameters:
        length (int): Length of each binary string (also the number of strings generated).

    Returns:
        list of str: List of binary strings representing e_i vectors.

    Example:
        >>> generate_redundant_list(4)
        ['1000', '0100', '0010', '0001']
    """

    redundant_list = []
    for i in range(length):
        redundant_list.append("0"*(length-1-i)+"1"+"0"*i)

    return redundant_list

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-Main_Area=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def main_function(input_ternary):
    """
    Encode a given ternary message using a D3-style error correction code.

    Parameters:
        input_ternary (str): The input ternary message (string of digits '0', '1', '2').

    Returns:
        tuple:
            - correct_code (str): The full encoded ternary codeword.
            - code_length (int): Length of the resulting codeword.
            - efficiency (float): Ratio of input message length to codeword length.

    Example:
        >>> main_function("1021")
        Error Correction Code: 1210021
        ("1210021", 7, 0.5714285714285714)
    """

    #=-=-=-=-=-=-=- Decide Dimension =-=-=-=-=-=-=-
    length = len(input_ternary)
    dimension = 0
    while length > (math.pow(3,dimension)-1)/2-dimension:
        dimension+=1

    #=-=-=-=-=-=-=- Pick Index & Cut Suitable Length =-=-=-=-=-=-=-
    ternary_set = Module.generate_ternary_set_half(dimension)
    ternary_set = ternary_set[:length + dimension]


    #=-=-=-=-=-=-=- Pick Redundant Index =-=-=-=-=-=-=-
    redundant_list = generate_redundant_list(dimension)

    #=-=-=-=-=-=-=- Place Message Value =-=-=-=-=-=-=-
    message_indices = [index for index in ternary_set if index not in redundant_list]

    values = [int(digit) for digit in input_ternary]
    message_index_value_mapping = {}

    for idx, digit in zip(message_indices, values):
        message_index_value_mapping[idx] = digit
        if len(message_index_value_mapping) == len(values):
            break


    #=-=-=-=-=-=-=- Calculating Xor Sum(P_all) =-=-=-=-=-=-=-
    raw_xor_sum = Module.ternary_xor_sum(message_index_value_mapping)
    inverse_xor = Module.xor_multiply(2,raw_xor_sum)

    #=-=-=-=-=-=-=- Set Value for Redundant =-=-=-=-=-=-=-
    redundant_values = [int(digit) for digit in inverse_xor]
    redundant_index_value_mapping = {}

    for idx, digit in zip(redundant_list, redundant_values[::-1]):
        redundant_index_value_mapping[idx] = digit

    total_mapping = combine_compute_original_value(message_index_value_mapping, redundant_index_value_mapping,ternary_set)

    #=-=-=-=-=-=-=- Print Final Result =-=-=-=-=-=-=-
    correct_code = ''.join(str(v) for v in total_mapping.values())
    print("Error Correction Code:" + correct_code)
    code_length = len(correct_code)
    efficiency = length/code_length
    
    return correct_code, code_length, efficiency