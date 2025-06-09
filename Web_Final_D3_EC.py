import Module
import math

#=-=-=-=-=-=-=- Get the Message from Code =-=-=-=-=-=-=-
def pick_message(d3_correct_code, dimension, order_mapping):
    """
    Extract the original ternary message from a D3-encoded codeword by removing redundant trits.

    Parameters:
        d3_correct_code (str): The full D3-encoded ternary codeword.
        dimension (int): The dimension used during encoding.
        order_mapping (dict): A mapping from each ternary index to its position (1-based index).

    Returns:
        str: The original message extracted from the codeword.

    Example:
        >>> pick_message("02110200", 4, {'000':1, '001':2, '010':3, ...})
        '21102'
    """
        
    redundant_set = generate_redundant_list(dimension)
    redundant_trits_loc = {order_mapping[redundant_trit] - 1 for redundant_trit in redundant_set}
    original_message = ''.join(
        char for idx, char in enumerate(d3_correct_code) if idx not in redundant_trits_loc
    )
    return original_message

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

#=-=-=-=-=-=-=- 1st, 2nd, 3rd, 4th, ... =-=-=-=-=-=-=-
def ordinal(n):
    """Convert an integer to its ordinal suffix representation.
    
    Args:
        n (int): Input integer to convert
        
    Returns:
        str: Ordinal representation with suffix (e.g., '1st', '2nd', '3rd')
        
    Examples:
        >>> ordinal(1)
        '1st'
        >>> ordinal(12)
        '12th'
        >>> ordinal(23)
        '23rd'
        
    Notes:
        - Handles special cases for numbers ending with 11-19 (always uses 'th')
        - Supports all integers including negatives and zero (e.g., '-5th', '0th')
    """
    if 10 <= n % 100 <= 20:  # Special case for 11th to 19th
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"

#=-=-=-=-=-=-=- Get Error Location and Change =-=-=-=-=-=-=-
def check_error_half(ternary_set_half, feature_value, dimension):
    """Determine error location and modification value for ternary code analysis.
    Args:
        ternary_set_half (set): Valid set of ternary strings
        feature_value (str): Input ternary string to analyze
        dimension (int): Required length of ternary strings
        
    Returns:
        tuple: (error_location, change) pair with special codes:
            - error_location: "3"*dimension (no error), "4"*dimension (unfixable), 
              or calculated location
            - change: Modification value (1 or 2)
            
    Example:
        >>> check_error_half({"111", "222"}, "111", 3)
        ('111', 2)
        
    Note:
        - Return codes: 
            3 = No error detected
            4 = Unrecoverable error
            1/2 = Specific modification needed
        - Uses Module.xor_multiply for error location calculation
    """ 
    error_location = "3"*dimension  # Default error location
    change = 3
    if feature_value == "0"*dimension:
        return error_location, change
    if feature_value not in ternary_set_half:
        error_location = Module.xor_multiply(2,feature_value)
        if(error_location not in ternary_set_half):
            return "4"*dimension, 4
        change = 2

        #print("Error Located at: "+ error_location + ", with change + " + str(change) + "from original value")
        return error_location, change

    error_location = feature_value
    change = 1
    #print("Error Located at: "+ error_location + ", with change + " + str(change) + "from original value")
    return error_location, change

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-Error Correction Part=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def main_function(error_code):
    """Perform error detection and correction for ternary code systems.
    Args:
        error_code (str): Input ternary string containing potential errors
    
    Returns:
        tuple: Five-element tuple containing:
            - feature_value (str): Calculated parity check value (P_all)
            - error_location (str): Error position in ternary format ("3"*d = no error, "4"*d = multiple errors)
            - after_correct_code (str): Corrected ternary code
            - announcement (str): Human-readable status message
            - orignal_message (str): Recovered message or "N/A"
    
    Example:
        >>> main_function("120102")
        ('202', '101', '120100', 'The error is located at the 6th position, with a change of +2 from original value.', '010')
    
    Process Flow:
        1. Calculate code dimension from input length
        2. Generate reference ternary set
        3. Map input digits to ternary positions
        4. Calculate parity checksum (P_all)
        5. Detect/correct single errors
        6. Reconstruct original message
    
    Note:
        - Special return codes:
            "3"*dimension: No errors detected
            "4"*dimension: Multiple errors found
        - Requires helper functions from Module:
            generate_ternary_set_half(), ternary_xor_sum()
        - Uses ordinal() for position formatting
    """

    #=-=-=-=-=-=-=- Get Dimension =-=-=-=-=-=-=-
    length = len(error_code)
    dimension = math.ceil(math.log(2*length+1) / math.log(3))

    #=-=-=-=-=-=-=- Pick One Index from Each Pair =-=-=-=-=-=-=-
    ternary_set_half = Module.generate_ternary_set_half(dimension)
    ternary_set_half = ternary_set_half[:len(error_code)]

    #=-=-=-=-=-=-=- Bind Value with Index =-=-=-=-=-=-=-
    values = [int(digit) for digit in error_code]
    ternary_set_mapping = {}
    for idx, digit in zip(ternary_set_half, values):
        ternary_set_mapping[idx] = digit

    order_mapping = {}
    for idx, order in zip(ternary_set_half, range(length)):
        order_mapping[idx] = order+1

    #=-=-=-=-=-=-=- Calculate P_all =-=-=-=-=-=-=-
    feature_value = Module.ternary_xor_sum(ternary_set_mapping)

    #=-=-=-=-=-=-=- Get Error Location and Change =-=-=-=-=-=-=-
    error_location, change = check_error_half(ternary_set_half, feature_value,dimension)

    #=-=-=-=-=-=-=- If Exact One Error Exist, Trace Back Its Value =-=-=-=-=-=-=-
    if(error_location!="3"*dimension and error_location!="4"*dimension):
        ternary_set_mapping[error_location] = (ternary_set_mapping[error_location] - change)%3

    #=-=-=-=-=-=-=- Composed String for Correct Code =-=-=-=-=-=-=-
    after_correct_code = ''.join(str(v) for v in ternary_set_mapping.values())


    announcement = ""
    if(error_location=="4"*dimension):
        announcement = "There are two or more mistakes"

        return feature_value, error_location, after_correct_code, announcement, "N/A"
    else:
        if(error_location=="3"*dimension):
            announcement = "Congratulation! It is a perfect code"
        if(error_location!="3"*dimension):
            announcement = f"The error is located at the {ordinal(order_mapping[error_location])} position, with a change of +{change} from original value."
        orignal_message = pick_message(after_correct_code, dimension, order_mapping)
        
        return feature_value, error_location, after_correct_code, announcement, orignal_message
