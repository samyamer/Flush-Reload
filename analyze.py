import pylcs
class Access:
   def  __init__(self, access_times):
       self.sqr = access_times[0]<260
       self.mul = access_times[1]<260
       self.div = access_times[2]<260
       self.values = [access_times[0],access_times[1],access_times[2]]


def read_file(file):
    access_list =  []
    i=0
    with open(file) as f:

        for line in f:
            line_arr = line.split(',')
            if(i==36):
                print(line_arr)
            i+=1
            access_list.append([int(x) for x in line_arr])

    return [Access(i) for i in access_list]

def check_list(arr):
    spy = "".join(arr)

    return (spy in d_p) or (spy in d_q)

def _to_binary(time_slots):
    # We're building a state machine here
    START = 0
    AFTER_SQUARE = 1
    AFTER_SQUARE_MOD = 2
    AFTER_MULTIPLY = 3
    AFTER_SQUARE_MOD_EMPTY = 5

    current_state = START
    output = []
    modulo_count = 0
    zero_count = 0
    one_count = 0
    slots = []
    start = 1
    end = 1
    saw_mul = -1

    total_all_miss =0
    num_square = 0
    num_div = 0
    num_mul  = 0
    empty = False
    all_miss = 0
    for time_slot in time_slots:

        square = time_slot.sqr
        multiply = time_slot.mul
        div = time_slot.div

        empty = False
        if(not square and not multiply and not div):
            print(f"All miss at {end}")
            all_miss+=1
            total_all_miss +=1
            empty = True
        else:
            all_miss = 0

        # If 4 or more continous all misses, this is probably a gap
        if(all_miss >=10):
            output.append("?")
            current_state = START
            slots.append((start,end,"?"))
            start = end+1
            end+=1
            all_miss = 0
            continue


        if current_state == START:
            if square:
                num_square +=1
                if(num_square > 3):
                    current_state = AFTER_SQUARE
                    num_square=0
            # if multiply:
            #     current_state = AFTER_MULTIPLY
            #     saw_mul = end
                # print("Start -> After_Square")

        elif current_state == AFTER_SQUARE:
            if(div):
                num_div +=1
                if(num_div >=3):
                    num_div=0
                    current_state = AFTER_SQUARE_MOD


            if multiply:
                # current_state = AFTER_MULTIPLY
                print(f"Multiply at {end}: {time_slot.values}")
                print("Multiply after square!!")
                saw_mul = end

        elif current_state == AFTER_SQUARE_MOD:

            if multiply:
                current_state = AFTER_MULTIPLY
                print(f"Multiply at {end}: {time_slot.values}")
                saw_mul = end
                # output.append('_')

            # If we see a square, return to start and output a 0
            elif square:
                num_square +=1
                if(num_square > 3):
                    current_state = AFTER_SQUARE
                    num_square=0
                    current_state = START
                    output.append('0')
                    slots.append((start,end,0))
                    start = end+1
                    zero_count+=1


        elif current_state == AFTER_MULTIPLY:
            # If we see only a modulo, return to start and output a 1
            # Alternatively, a missed slot could be a modulo
            if div:
                num_div +=1
                if(num_div >=3):
                    num_div=0
                    current_state = START
                    output.append('1')
                    slots.append((start,end,saw_mul,1))
                    start = end+1
                    one_count +=1


        end+=1

            # If we see a square so soon, this might be invalid
            # elif square:
            #     current_state = START
            #     output.append('_')

    print(f"num 0s {zero_count}")
    print(f"num 1s {one_count}")
    print(slots)
    print(f"all miss: {total_all_miss}")
    return output


access_list = read_file("slots_out4.txt")

out = _to_binary(access_list)
print(out)
#print(_to_binary(read_file("slots_out3.txt")))


#consolidate into a list of continous string

list_out = []
element = []
prev_not_q = True
for char in out:
    if (char != "?"):
        element.append(char)
        prev_not_q = True
    elif (prev_not_q):
        list_out.append(element)
        prev_not_q = False
        element = []

lenghs = [len(e) for e in list_out]

print(list_out)
print(f"longest continous: {max(lenghs)}")
spy_out ="".join(out)

d_p = "101110001111001001111101000101101101110111101110001000011010010010110101011101001101011010010001001110010000101010010001011011000110100011000011000011011001000111110011101000100100100101000100010001101100011001010110110111011111111101010101101101111010111011001001011011010011100100100011101110011101101011101110010001010101011000011000100000101010010110000101011100110000001011111100000000111001100111011111111111111111001001111101010101001101010110111000010000100111100011111011101100011001111100100000110110111011100010110111100110110111010111000010110110101110111001000100000001010000100010111001011100111111100010001001111110100010000011110110000111101100001110010001010110011100110111010111100010101010001000100100011100110110110010010011101011001101000000110001100101000000111110000111011000101001111000001010111111100100100011000101100000111000111101001100110001101100110000110111010011000011111010111010101101011001111110101010101000011010010011000110000001101110010101010110000011001111011101110001001111011100100011011010010000001100100100111100001000011010100111001101110100111011101011111101010000010010001100110001110000001000001000010111000101001111101010100010011010101101010100100000001011101001100101100011101000011110011010110110010101011011011111111111101001111101100100111110111001111101001110011011001011011001001010010000010101010011100000011010010011111111010101011101111110011000101101110111011100000000010111001110001100001101011100011100011100011100001110011011000101110001010001001001011000100110010100101101111101011011010010111110011110111110001101110110100010010101111001010000101101100100110111011101101100001001001010111100111110110001100011111110001101011011000011001011101111111101001100010001011100010101101110001110000000011111111001111001010111011101101101110011011010000001111110001110110110111111000100001010010011111110010000001101111111011001010011111011101110010101110010111111000010010101001001110001001110111010110110010001000100001010111010111001110110101000010101100000111100011111000100111011101001"

d_q = "100000011000110000000011110011101011010011101110100001101111000001001000000011111001011101011110001110010011111001101001100111000000000011111001000001001000010111111001110101001101010111001010011110000111101011111000011100111010101010000001010001111111011111000101011110101110010000000110111001001001111010100101101110001001100011111101101000101101100011011100100010100100001010000110000111100010111001110000000110101100100110000011100001011000000001010111110001100111001101011011110011100111000001000111001111111101010011111110110001001101111000111101010010110101000111101101010000100110101001011111101101101000011011010011111001011111111010101110010100110011110101011010011101111010101101001000111001110110010010101110001101110110000111110000110100101100011100001001010110001111010010110001011000110101001011011000010111010100011001101111111011110001110111110011111001001111011000000000010011011100011000011101001001100010000000001001000011001111001100110101111110111111011110010101101110101110011010000001100111100010111111000001000110111101000011011111000100000110010011010010011111111000111110011000110001110010110110111111110011000010111110100001111001000010011011101001111101101100000100000001011110100011000110000111101001110001101010111101100011000111100000001101101110101111100010001100010100111000111101011011011011111110101110011010011001100110010111110111111010110000011110100100110010111110011101101000111111110011010010110001011001111010100001100011110010100010101010110101100000111100111110000010000111011110010001100001111011101010000001100100000000110011010110110001011101111110101110000110100101010100011000001001111110111001011000001000011101100011101010001001111001100111001001100100011100110110001001001100001110010001001111101100010000111110001101011100111110110110101101010101100101110010011000001011101010111010001010100000100111101000111110110110000010010000000100010000000011100001101100000110110001001001000000100010010100001001000110111110001101101000110101001100001001100001010010100001001000101101011001001110111101"


def check_list(arr):
    spy = "".join(arr)

    return (spy in d_p) or (spy in d_q)

exist = [check_list(e) for e in list_out]

print(exist)
print(lenghs)


d_p_lcs = pylcs.lcs_string_length(spy_out, d_p)
d_q_lcs = pylcs.lcs_string_length(spy_out, d_q)


# d_p_lcs = 30
# d_q_lcs = 30
print(f"D_p len:{len(d_p)}")
print(f"D_q len:{len(d_q)}")


print(f"Spy Out len is {len(spy_out)}")

print("-----Common subs in d_p and d_q-----")
# print(common_subs_length(d_p,d_q))

# Calculate F with p_q
num_trials = len(spy_out) - d_p_lcs +1
prob_success = 2**(-1*d_p_lcs)
prob_fail = 1 -prob_success
F = 1 - (prob_fail**(num_trials))

print("----------LCS with DP------------------")
print(f"LCS: {d_p_lcs}")
print(f"F: {F}")

print("-----Common subs in spy and d_p-----")
#count,subs = common_subs_length(spy_out,d_p)
#print(count)
#print(subs)

num_trials = len(spy_out) - d_q_lcs +1
prob_success = 2**(-1*d_q_lcs)
prob_fail = 1 -prob_success
F = 1 - (prob_fail**(num_trials))


print("----------LCS with DQ------------------")
print(f"LCS: {d_q_lcs}")
print(f"F: {F}")


print("-----Common subs in spy and d_p-----")
#count,subs = common_subs_length(spy_out,d_q)
#print(count)
#print(subs)



