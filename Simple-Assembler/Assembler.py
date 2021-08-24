import Checkerror

opcode = {"add": "00000", "sub": "00001", "ld": "00100", "st": "00101", "mul": "00110", "div": "00111",
          "rs": "01000", "ls": "01001", "xor": "01010", "or": "01011", "and": "01100", "not": "01101",
          "cmp": "01110", "jmp": "01111", "jlt": "10000", "jgt": "10001", "je": "10010", "hlt": "10011"}

reg = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}

# mov operation handled separately
typeA = ("add", "sub", "mul", "xor", "or", "and")
typeB = ("rs", "ls")
typeC = ("div", "not", "cmp")
typeD = ("ld", "st")
typeE = ("jmp", "jlt", "jgt", "je")


def mov(arr):
    if arr[2][0] == "R" or arr[2] == 'FLAGS':
        print('00011' + '00000' + reg[arr[1]] + reg[arr[2]])

    elif arr[2][0] == "$":
        imm = str(bin(int(arr[2][1:]))).replace("0b", "")
        imm = '0' * (8 - len(imm)) + imm
        print('00010' + reg[arr[1]] + imm)


def type_A(arr):
    print(opcode[arr[0]] + '00' + reg[arr[1]] + reg[arr[2]] + reg[arr[3]])


def type_B(arr):
    imm = str(bin(int(arr[2][1:]))).replace("0b", "")
    imm = '0' * (8 - len(imm)) + imm
    print(opcode[arr[0]] + reg[arr[1]] + imm)


def type_C(arr):
    print(opcode[arr[0]] + '00000' + reg[arr[1]] + reg[arr[2]])


def type_D(arr, mem):
    mem = '0' * (8 - len(mem)) + mem
    print(opcode[arr[0]] + reg[arr[1]] + mem)


def type_E(arr, mem):
    mem = '0' * (8 - len(mem)) + mem
    print(opcode[arr[0]] + '000' + mem)


def type_F(arr):
    print(opcode[arr[0]] + '00000000000',end = "")


def main():
    user_input = []

    while True:
        try:
            line = input()
            user_input.append(line)
        except EOFError:
            break

    res = Checkerror.check(user_input)
    if not res:      # False means no error is present
        memory_add = {}
        count_var = 0
        for i in range(len(user_input)):
            empty = [x for x in user_input[i].split()]
            if len(empty) == 0:
                continue
            if user_input[i][0:3] == "var":
                count_var += 1
            elif user_input[i][0:3] != "var":
                break
        count = 0
        for i in range(len(user_input)):
            empty = [x for x in user_input[i].split()]
            if len(empty) == 0:
                continue
            if user_input[i][0:3] == "var":
                c = 4
                for x in user_input[i][4:]:
                    if x == " ":
                        c += 1
                    else:
                        break
                memory_add[user_input[i][c::]] = str(bin(len(user_input) - count_var)).replace('0b', '')
                count_var -= 1
                continue
            l = [x for x in user_input[i].split()]
            if l[0][-1] == ":":
                memory_add[l[0][:-1]] = str(bin(count)).replace('0b', '')
            count += 1

        for i in user_input:
            empty = [x for x in i.split()]
            if len(empty) == 0:
                continue
            a = [x for x in i.split()]
            if a[0][-1] == ':':
                a = a[1:]
            if a[0] in typeA:
                type_A(a)
            elif a[0] in typeB:
                type_B(a)
            elif a[0] in typeC:
                type_C(a)
            elif a[0] in typeD:
                type_D(a, memory_add[a[2]])
            elif a[0] in typeE:
                type_E(a, memory_add[a[1]])
            elif a[0] == 'hlt':
                type_F(a)
            elif a[0] == 'mov':
                mov(a)


main()
