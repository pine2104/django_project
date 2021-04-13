import numpy as np
import math
from pydna.dseq import Dseq

# Return the Hamming distance between string1 and string2.
# string1 and string2 should be the same length.

def get_prop_primers(primers, vector):
    vector_name = vector.name
    seq = str.lower(vector.sequence)
    seq = Dseq(seq.replace(' ', ''))
    L = len(str(seq))
    rseq = seq.reverse_complement()
    for primer in primers:
        primer_nor = primer.sequence.replace(' ', '')

        p_seq = Dseq(primer_nor)
        p_seq_s = str.lower(str(p_seq)) # all lower case
        nt='atcgn'
        idt_codes_subtract1 = ['icy5', 'icy3', '5biosg', '(am)']
        idt_codes_subtract2 = ['dspacer']
        idt_codes_subtract3 = ['dbcoteg']
        idt_codes_subtract4 = ['biotinteg']
        idt_codes_plus1 = ['ds', 'idsp']

        Lp_subtract = 0
        for s1 in idt_codes_subtract1:
            if p_seq_s.find(s1) >= 0:
                Lp_subtract += 1
        for s2 in idt_codes_subtract2:
            if p_seq_s.find(s2) >= 0:
                Lp_subtract += 2
        for s3 in idt_codes_subtract3:
            if p_seq_s.find(s3) >= 0:
                Lp_subtract += 3
        for s4 in idt_codes_subtract4:
            if p_seq_s.find(s4) >= 0:
                Lp_subtract += 4
        for p1 in idt_codes_plus1:
            if p_seq_s.find(p1) >= 0:
                Lp_subtract -= 1

        Lp = 0
        for i in nt:
            Lp += p_seq_s.count(i)
        Lp = Lp - Lp_subtract
        if seq.find(p_seq_s) != -1: # match it
            position = seq.find(p_seq_s) + 1
            dir = 'forward'
            in_vector = True
        elif rseq.find(p_seq_s) != -1:
            position = rseq.find(p_seq_s) - L - 1
            dir = 'reverse'
            in_vector = True
        else:
            position = -1
            dir = 'none'
            in_vector = False
        primer.position = position
        primer.dir = dir
        primer.in_vector = in_vector
        primer.length = Lp
        primer.save()
    return vector_name, seq, L, position, dir, in_vector


def setL_pcr(L_vector, pos1, pos2):
    if pos1<0 and pos2>0:
        pr = pos1
        pf = pos2
    elif pos1>0 and pos2<0:
        pr = pos2
        pf = pos1
    else:
        return 0
    if abs(pr) >= abs(pf):
        L_pcr = -pr-pf
    else:
        L_pcr = L_vector-pr-pf
    return int(L_pcr)





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

def generate_indicator(template):
    n = math.ceil(len(template)/100)
    n_small_seq = 10
    pos = 0
    result = []
    for i in range(n):
        num_string = ''
        initial = '.'*(n_small_seq-1)
        for j in range(10):
            pos += n_small_seq
            pos_s = str(pos)
            L_pos = len(pos_s)
            num_string += initial + '^' + f'{pos}'
            initial = '.'*(n_small_seq-1-L_pos)
        result += [num_string]
    return result

def plotpcr(template, p1, p2): #p1 is forward, p2 is reverse
    template = str.lower(template.replace(' ', ''))
    p1 = str.lower(p1.replace(' ', ''))
    p2 = str.lower(p2.replace(' ', ''))[::-1]
    r_template = str(Dseq(template).reverse_complement())[::-1]
    L = len(template)
    n_seg = 100
    n_sep = 120
    i_end = np.append(np.arange(n_seg, L, n_seg), L)
    indicator_pos = generate_indicator(template)
    seq_show = ''
    pf = template.find(p1) + 1
    pr = r_template.find(p2) + 1
    # primer_f_seq_show = ''
    # primer_r_seq_show = ''
    for i, n_end in enumerate(i_end):
        if (pf >= i*n_seg) and (pf < n_end): # in that range
            if (len(p1) <= n_end-pf): #not exceed a row
                primer_f_seq_show = '.'*(pf-1-3-i*n_seg) +"5'-"+ p1 + "-3'-->>dir" + '\n'
                template_seq = primer_f_seq_show + template[i*n_seg:n_end] + '\n'
                seq_show += template_seq + indicator_pos[i] + '\n'
                # seq_show += '-' * n_seg + '\n'
        else: #not in range
            template_seq = template[i * n_seg:n_end] + '\n'
            seq_show += template_seq + indicator_pos[i] + '\n'
            # seq_show += '-' * n_seg + '\n'

        if (pr >= i*n_seg) and (pr < n_end):
            if (len(p2) <= n_end - pr):
                primer_r_seq_show = '.'*(pr-i*n_seg-10) +"dir<<-3'-"+ p2 + "-5'" + '\n'
                r_template_seq = r_template[i*n_seg:n_end] + '\n'
                seq_show += r_template_seq + '\n' + primer_r_seq_show
                seq_show += '-' * n_sep + '\n'
        else:
            seq_show += r_template[i * n_seg:n_end] + '\n' + '-' * n_sep + '\n'


    return seq_show


