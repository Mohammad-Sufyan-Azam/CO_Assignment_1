from sys import stdin
# import Checkerror

opcode = { "add": "00000", "sub": "00001", "ld": "00100", "st": "00101", "mul": "00110", "div": "00111",
           "rs": "01000", "ls": "01001", "xor": "01010", "or": "01011", "and": "01100", "not": "01101",
           "cmp": "01110", "jmp": "01111", "jlt": "10000", "jgt": "10001", "je": "10010", "hlt": "10011" }

reg = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}
# mov operation handled separately
# FLAGS not given in any case
# case where any other instruction can call labels not handled
# registers not initialised to zero
typeA = ("add","sub","mul", "xor", "or", "and")
typeB = ("rs", "ls")
typeC = ("div", "not", "cmp")
typeD = ("ld", "st")
typeE = ("jmp", "jlt", "jgt", "je")

def mov(arr):
    if arr[2][0] == "R":
        print( opcode[arr[0]] + '00000' + reg[arr[1]] + reg[arr[2]] )

    elif arr[2][0] == "$":
        imm = bin(arr[2][1:]).replace("0b", "")
        imm += '0'*(8 - len(b))
        print( opcode[arr[0]] + reg[arr[1]] + imm )

def type_A(arr):
    print(arr[0] + '00' + arr[1] + arr[2] + arr[3])

def type_B(arr):
    imm = bin(arr[2][1:]).replace("0b", "")
    imm += '0' * (8 - len(b))
    print(opcode[arr[0]] + reg[arr[1]] + imm)

def type_C(arr):
    print(opcode[arr[0]] + '00000' + reg[arr[1]] + reg[arr[2]])

def type_D(arr):
    # insert memory address also
    print(opcode[arr[0]] + reg[arr[1]] )

def type_E(arr):
    # insert memory address also
    print(opcode[arr[0]] + '000' )

def type_F(arr):
    print(opcode[arr[0]] + '00000000000')

def main():
    user_input = []
    for line in stdin:
        if line == '':  # If empty string is read then stop the loop
            break
        user_input.append(line)

    # res = Checkerrror.check(user_input)
    # if res == False:      # False means no error is present
    for i in user_input:
        a = [ x for x in i.split() ]
        if a[0] == 'label:':
            a = a[1:]

        if a[0] in typeA:
            type_A(a)
        elif a[0] in typeB:
            type_B(a)
        elif a[0] in typeC:
            type_C(a)
        elif a[0] in typeD:
            type_D(a)
        elif a[0] in typeE:
            type_E(a)
        elif a[0] == 'hlt':
            type_F(a)
        elif a[0] == 'mov':
            mov(a)


main()


