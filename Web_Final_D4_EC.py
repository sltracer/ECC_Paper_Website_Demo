
import Module

#=-=-=-=-=-=-=- Pick Message from Correct Code =-=-=-=-=-=-=-
def pick_message(correct_error_correction,redundant_set, order_mapping):
    """
    Extract the original ternary message from a D4-encoded codeword by removing redundant trits.

    Parameters:
        correct_error_correction (str): Corrected perfect D4 code
        redundant_set (list of str): Indices of redundant trits
        order_mapping (dict): A mapping from each ternary index to its position (1-based index).

    Returns:
        str: The original message extracted from the codeword.

    Example:
        >>> pick_message("02110200", 4, {'000':1, '001':2, '010':3, ...})
        '21102'
        (Just to display the format)
    """
    regular_text = correct_error_correction[:-2]
    redundant_trits_loc = {order_mapping[redundant_trit] - 1 for redundant_trit in redundant_set}
    original_message = ''.join(
        char for idx, char in enumerate(regular_text) if idx not in redundant_trits_loc
    )
    return original_message

#=-=-=-=-=-=-=- 1st, 2nd, 3rd, 4th, ... =-=-=-=-=-=-=-
def ordinal(n):
    """Convert an integer to its ordinal suffix representation.
    Args:
        n (int): Input integer to convert
        
    Returns:
        str: Ordinal representation with suffix (e.g., '1st', '2nd', '3rd'), except for O and E to keep the same.
        
    Examples:
        >>> ordinal(O)
        'O'
        >>> ordinal(1)
        '1st'
        >>> ordinal(0)
        '0th'
        
    Notes:
        - Handles special cases for numbers ending with 11-19 (always uses 'th')
        - Supports all integers including negatives and zero (e.g., '-5th', '0th')
        - Ignore O and E.
    """
    if n == "O" or n == "E":
        return n
    if 10 <= n % 100 <= 20:  # Special case for 11th to 19th
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


#=-=-=-=-=-=-=- Error Correction, According to P_all, P_1, P_2 =-=-=-=-=-=-=-
def error_correction(dimension, error_syndrome, odd_sum, even_sum, I_1, I_2):
    """Perform D4 error localization and validation using parity checks.
    Args:
        dimension (int): Lenth of Index
        error_syndrome (str): Calculated parity value (P_all)
        odd_sum (int): O parity check result, P_1
        even_sum (int): E parity check result, P_2
        I_1 (list): Primary valid indices set
        I_2 (list): Secondary valid indices set
        
    Returns:
        str: Error location code with special conventions:
            - "3"*d: Multiple errors detected
            - "4"*d: No errors found
            - "O"/"E": Parity bit error
            - Valid index: Single error location
            
    Example:
        >>> error_correction(3, "000", 0, 0, ["011"], ["122"])
        '444'  # No errors
        (Just for format, not precise)

    Error Detection Logic:
        1. Multi-error: Both parity checks fail
        2. Single-error: Validate against I₁/I₂ sets
        3. Parity-bit error: Only O/E check fails
        4. No-error: All checks pass
        
    Note:
        - Requires Module.xor_multiply for error validation
        - Special codes use base-3 digit conventions
        - I₁/I₂ define valid error positions
    """
        
    all_regular_digits = I_1 + I_2
    error_loc = "3"*dimension

    # Case 0: Double mistakes on same region
    if odd_sum == 0 and even_sum == 0 and error_syndrome != "0"* dimension:
        print("There are 2 or more mistakes!!!")
        return error_loc
    
    # Case 1: No mistakes
    if error_syndrome == "0" * dimension and odd_sum == 0 and even_sum == 0:
        print("There are no mistakes!")
        return "4" * dimension

    # Case 1b: Unique mistake on O or E
    if error_syndrome == "0" * dimension and odd_sum != 0 and even_sum == 0:
        print("Error on O")
        return "O"

    if error_syndrome == "0" * dimension and even_sum != 0 and odd_sum ==0:
        print("Error on E")
        return "E"

    # Case 2: Two or more errors detected
    if odd_sum != 0 and even_sum != 0:
        print("There are two or more errors.")
        return error_loc

    # Case 3: Either odd_sum or even_sum is non-zero
    if odd_sum != 0 or even_sum != 0:
        if error_syndrome not in all_regular_digits and Module.xor_multiply(2,error_syndrome) not in all_regular_digits:
        # So, Fix a mistake here when variable length that value no longer in all digits!!!!!!
            print("There are two or more errors.")
            return error_loc

        error_count = 0
        # Sub-case: odd_sum is non-zero
        if odd_sum != 0:
            error_count = Module.xor_multiply(odd_sum,error_syndrome) # Since k*a=b iff a=k*b in xor
            #print("error_count: "+ error_count)
            if error_count in I_1:
                return error_count
            else:
                print("There are two or more errors.")
                return error_loc

        # Sub-case: even_sum is non-zero
        if even_sum != 0:
            error_count = Module.xor_multiply(even_sum,error_syndrome)
            if error_count in I_2:
                return error_count
            else:
                print("There are two or more errors.")
                return error_loc

    return error_loc



#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-Main_Area=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def main_function(input_ternary):
    """D4 Error Correction, and Report
    Args:
        input_ternary (str): Input code with parity bits (length not restrict here, but in website)
        
    Returns:
        tuple: 
            [0] Corrected code (str)
            [1] Decoded message (str) or "-1" for uncorrectable
            [2] Error location code (str)
            [3] Human-readable status (str)
            [4] P_all, checksum (str)
            [5] P_1, parity value (int)
            [6] P_2, parity value (int)
            [7] P_all, case code (0: clean, 1: single error, 2: multi-error)
            [8] I, Sorted regular digits list (list)
    
    Example:
        >>> main_function("12010212")
        ('12010212', "-1", '333', 'Sorry, notice that there are two or more mistakes.', '200', 0, 0, 2, ['011', '022', '101', '110', '111', '202'])

    Process Flow:
        1. Dimension Calculation: Auto-adjust based on input length
        2. Index Generation: Create redundancy sets (R, I₁, I₂)
        3. Parity Calculation:
           - P_all (XOR checksum)
           - P_1 (Odd sum)
           - P_2 (Even sum)
        4. Error Correction: Localize and fix single errors
        5. Message Recovery: Extract original payload

    Error Codes:
        - "3"*d: Multiple errors detected
        - "4"*d: Perfect code (no errors)
        - "O"/"E": Parity bit errors

    Dependencies:
        - Module functions: fr(), d4_build_redundant_list(), var_d4_generate_I_odd_or_even()
        - Helper functions: error_correction(), pick_message(), ordinal()
    """
    original_input = input_ternary

    #=-=-=-=-=-=-=- Calculate Dimension(Number of Regular Redundant) =-=-=-=-=-=-=-
    length =  len(input_ternary)
    dimension = 3 # Initial Value
    max_length_curr_dimension = 2*Module.fr(dimension)+2
    while length > max_length_curr_dimension:
        dimension+=1
        max_length_curr_dimension = 2*Module.fr(dimension)+2


    #=-=-=-=-=-=-=- Build R,I_1,I_2 =-=-=-=-=-=-=-
    R = Module.d4_build_redundant_list(dimension)
    I_1 = Module.var_d4_generate_I_odd_or_even(dimension,1)
    I_2 = Module.var_d4_generate_I_odd_or_even(dimension,2)
    first_cut = length-2
    if(len(I_1)>first_cut):
        I_1 = I_1[:first_cut]
    second_cut_amount = (length-2)-(len(I_1))   #Module.fr(dimension)) # amount left after 1st set
    I_2 = I_2[:second_cut_amount]
    if(second_cut_amount<=0):
        I_2 = []

    #=-=-=-=-=-=-=- Mapping Picked Index with Value from Code =-=-=-=-=-=-=-
    all_regular_digits = I_1+I_2
    all_regular_digits_sorted_ternary = Module.sort_ternary(all_regular_digits)
    order_mapping = {
        key: index 
        for index, key in zip(
            range(1, len(all_regular_digits_sorted_ternary) + 1),
            all_regular_digits_sorted_ternary
        )
    }
    regular_mapping = {key: int(value) for key, value in zip(all_regular_digits_sorted_ternary, input_ternary[:length-2])}
    #print(regular_mapping)
    #=-=-=-=-=-=-=- Calculating P_all =-=-=-=-=-=-=-
    error_feature = Module.ternary_xor_sum(regular_mapping)
    print("P_all error_feature: " + error_feature)
    P_all_case = -1
    if(error_feature in all_regular_digits_sorted_ternary or Module.xor_multiply(2,error_feature) in all_regular_digits_sorted_ternary):
        P_all_case = 1
    else:
        P_all_case = 2
    if(error_feature == "0"*dimension):
        P_all_case = 0
    
    #=-=-=-=-=-=-=- Calculating P_2 =-=-=-=-=-=-=-
    even_sum = 0
    for index in I_2:
        even_sum+=regular_mapping[index]
    even_sum += int(input_ternary[-1])
    even_sum = even_sum %3
    print("P_2 even_sum: " + str(even_sum))

    #=-=-=-=-=-=-=- Calculating P_1 =-=-=-=-=-=-=-
    odd_sum = 0
    for index in I_1:
        odd_sum+=regular_mapping[index]
    odd_sum += int(input_ternary[-2])
    odd_sum = odd_sum % 3
    print("P_1 odd_sum: " + str(odd_sum))

    #=-=-=-=-=-=-=- Error Correction =-=-=-=-=-=-=-
    error_loc = error_correction(dimension, error_feature, odd_sum, even_sum, I_1, I_2)
    change = 0
    # "3" When there are two or more error 
    # "4" When it is perfect 

    announcement = ""
    if(error_loc!='3'*dimension and error_loc!='4'*dimension):
        if(error_loc != "O" and error_loc != "E"):
            change = odd_sum+even_sum
            regular_mapping[error_loc]-= (odd_sum+even_sum)
            regular_mapping[error_loc] %= 3
            error_num = all_regular_digits_sorted_ternary.index(error_loc)
            input_ternary = input_ternary[:error_num]+ str(regular_mapping[error_loc]) + input_ternary[error_num+1:]

        if(error_loc == "O"):
            original_odd = (int(input_ternary[-2]) - odd_sum)%3
            change = int(input_ternary[-2])-original_odd
            input_ternary = input_ternary[:-2]+ str(original_odd) + input_ternary[-1]

        if(error_loc == "E"):
            original_even = (int(input_ternary[-1]) - even_sum)%3
            change = int(input_ternary[-1])-original_even
            input_ternary = input_ternary[:-1]+ str(original_even)

        #print("raw_text:" + original_input)#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if(error_loc!="O" and error_loc!="E"):
            announcement = f"The error is located at the {ordinal(order_mapping[error_loc])} position, with a change of +{change}  from original value."
        else:
            announcement = f"The error is located at the {error_loc} position, with a change of +{change}  from original value.(O as second last digit, E as last digit)"
        pure_message = pick_message(input_ternary,R, order_mapping)
        return input_ternary, pure_message, error_loc, announcement, error_feature, odd_sum, even_sum , P_all_case, all_regular_digits_sorted_ternary
    elif(error_loc == '3'*dimension):
        announcement = "Sorry, notice that there are two or more mistakes."
        return input_ternary, "-1", error_loc, announcement, error_feature, odd_sum, even_sum , P_all_case, all_regular_digits_sorted_ternary
    elif(error_loc == '4'*dimension):
        announcement = "Congratulation! It is a perfect code with 0 error."
        pure_message = pick_message(input_ternary,R, order_mapping)
        return input_ternary, pure_message, error_loc, announcement, error_feature, odd_sum, even_sum , P_all_case, all_regular_digits_sorted_ternary
