
# Return the Hamming distance between string1 and string2.
# string1 and string2 should be the same length.



def hamming_distance(string1, string2):
    # Start with a distance of zero, and count up
    distance = 0
    position = '' # start form 1
    # Loop over the indices of the string
    L = len(string1)
    for i in range(L):
        # Add 1 to the distance if these two characters are not equal
        if string1[i] != string2[i]:
            distance += 1
            position += ' '+str(i+1)
    # Return the final count of differences
    return distance, position


# def match_check(vector, string2, mismatch_tolerance):
#     # Start with a distance of zero, and count up
#     distance = 0
#     position = '' # start form 1
#     # Loop over the indices of the string
#     L = len(string1)
#     for i in range(L):
#         # Add 1 to the distance if these two characters are not equal
#         if string1[i] != string2[i]:
#             distance += 1
#             if distance
#     # Return the final count of differences
#     return distance

# vector = 'atcgttgactggttaac'
# primer = 'ttcact'
# mismatch_tolerance = 1

def match_primer(vector, primer, mismatch_tolerance=0):
    L = len(vector)
    Lp = len(primer)
    status = False
    p_anneal = -1
    p_mismatch = ''
    for i in range(L-Lp):
        vector_segment = vector[i:i+Lp]
        distance, position = hamming_distance(vector_segment, primer)
        if distance <= mismatch_tolerance:
            # print(f'anneal at position {i} and mismatch at{position}th nt')
            p_anneal = i
            p_mismatch = position
            status = True
            break
        else:
            pass
    return status, p_anneal, p_mismatch
