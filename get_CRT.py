d = 
p =
q = 
d_binary_str = ''.join(format(ord(i), '08b') for i in d)
p_binary_str = ''.join(format(ord(i), '08b') for i in d)
q_binary_str = ''.join(format(ord(i), '08b') for i in d)

d_decimal = int(d_binary_str,2)
p_decimal = int(p_binary_str,2)
q_decimal = int(p_binary_str,2)

dp_decimal = d_decimal % (p_decimal - 1)
dq_decimal = d_decimal % (q_decimal - 1)

print("--------------dp----------------")
print(bin(dp_decimal))

print("--------------dq----------------")
print(bin(dp_decimal))