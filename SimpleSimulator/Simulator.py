reg_state = {'000': 0, '001': 0, '010': 0, '011': 0, '100': 0, '101': 0, '110': 0, '111': 0}

def PC(count):
    mem = str(bin(count)).replace('0b','')
    mem = '0'*(8 - len(mem)) + mem
    print(mem, end = " ")


def print_reg():
    mem0 = str(bin(reg_state['000'])).replace('0b','')
    mem0 = '0'*(16 - len(mem0)) + mem0

    mem1 = str(bin(reg_state['001'])).replace('0b','')
    mem1 = '0'*(16 - len(mem1)) + mem1

    mem2 = str(bin(reg_state['010'])).replace('0b','')
    mem2 = '0'*(16 - len(mem2)) + mem2

    mem3 = str(bin(reg_state['011'])).replace('0b','')
    mem3 = '0'*(16 - len(mem3)) + mem3

    mem4 = str(bin(reg_state['100'])).replace('0b','')
    mem4 = '0'*(16 - len(mem4)) + mem4

    mem5 = str(bin(reg_state['101'])).replace('0b','')
    mem5 = '0'*(16 - len(mem5)) + mem5

    mem6 = str(bin(reg_state['110'])).replace('0b','')
    mem6 = '0'*(16 - len(mem6)) + mem6

    mem7 = str(bin(reg_state['111'])).replace('0b','')
    mem7 = '0'*(16 - len(mem7)) + mem7

    if int(mem0) > 1111111111111111:
        c = len(mem0) - 16
        mem0 = mem0[c:]
        reg_state['000'] = int(mem0, 2)

    elif int(mem1) > 1111111111111111:
        c = len(mem1) - 16
        mem1 = mem1[c:]
        reg_state['001'] = int(mem1, 2)

    elif int(mem2) > 1111111111111111:
        c = len(mem2) - 16
        mem2 = mem2[c:]
        reg_state['010'] = int(mem2, 2)

    elif int(mem3) > 1111111111111111:
        c = len(mem3) - 16
        mem3 = mem3[c:]
        reg_state['011'] = int(mem3, 2)

    elif int(mem4) > 1111111111111111:
        c = len(mem4) - 16
        mem4 = mem4[c:]
        reg_state['100'] = int(mem4, 2)

    elif int(mem5) > 1111111111111111:
        c = len(mem5) - 16
        mem5 = mem5[c:]
        reg_state['101'] = int(mem5, 2)

    elif int(mem6) > 1111111111111111:
        c = len(mem6) - 16
        mem6 = mem6[c:]
        reg_state['110'] = int(mem6, 2)

    print(mem0 +' '+ mem1 +' '+ mem2 +' '+ mem3 +' '+ mem4 +' '+ mem5 +' '+ mem6 +' '+ mem7)


def print_rest(arr, var_mem):
    for mem in arr:
        print(mem)          # assembler output
    for var in sorted(var_mem.keys()):
        var = var_mem[var]
        var = str(bin(var)).replace('0b', '')
        var = '0'*(16 - len(var)) + var
        print(var)
    for _ in range(256 - len(arr)-len(var_mem)):
        print('0000000000000000')


'''	OUTPUT
    # V L G E
    # ! ! ! !
    # 8 4 2 1
'''
def main():
    user_input = []

    while True:
        try:
            line = input()
            user_input.append(line)
        except EOFError:
            break

    i = 0
    var_mem = {}
    while i != len(user_input):
    
        if user_input[i][:5] == '00100': # ld R0 x
            var_mem[user_input[i][8:]] = 0

        elif user_input[i][:5] == '00101': # st R0 x
            var_mem[user_input[i][8:]] = 0
            
        i += 1

    pc = 0
    i = 0
    t = 0
    
    while i != len(user_input):

        i += t
        t = 0
        pc_jump = False
        
        PC(pc)
        
        if user_input[i][:5] == '00000': # add R0 R1 R2
            reg_state[user_input[i][7:10]] = reg_state[user_input[i][10:13]] + reg_state[user_input[i][13:]]
            if reg_state[user_input[i][7:10]] > 65535:
                reg_state['111'] = 8
            else:
                reg_state['111'] = 0

        elif user_input[i][:5] == '00001': # sub R0 R1 R2
            if reg_state[user_input[i][10:13]] < reg_state[user_input[i][13:]]:
                reg_state['111'] = 8
                reg_state[user_input[i][7:10]] = 0
            else:
                reg_state[user_input[i][7:10]] = reg_state[user_input[i][10:13]] - reg_state[user_input[i][13:]]
                reg_state['111'] = 0

        elif user_input[i][:5] == '00010': # mov R0 $5
            reg_state[user_input[i][5:8]] = int(user_input[i][8:], 2)
            reg_state['111'] = 0

        elif user_input[i][:5] == '00011': # mov R0 R1
            reg_state[user_input[i][10:13]] = reg_state[user_input[i][13:]]
            reg_state['111'] = 0

        elif user_input[i][:5] == '00100': # ld R0 x
            reg_state[user_input[i][5:8]] = var_mem[user_input[i][8:]]
            reg_state['111'] = 0

        elif user_input[i][:5] == '00101': # st R0 x
            var_mem[user_input[i][8:]] = reg_state[user_input[i][5:8]]
            reg_state['111'] = 0

        elif user_input[i][:5] == '00110': # mul R0 R1 R2
            reg_state[user_input[i][7:10]] = reg_state[user_input[i][10:13]] * reg_state[user_input[i][13:]]
            if reg_state[user_input[i][7:10]] > 65535:
                reg_state['111'] = 8
            else:
                reg_state['111'] = 0

        elif user_input[i][:5] == '00111': # div R2 R3
            if reg_state[user_input[i][13:]] == 0 or reg_state[user_input[i][10:13]] == 0:
                reg_state['000'] = 0
                reg_state['001'] = 0
            else:
                reg_state['000'] = int(reg_state[user_input[i][10:13]] / reg_state[user_input[i][13:]])
                reg_state['001'] = int(reg_state[user_input[i][10:13]] % reg_state[user_input[i][13:]])
            reg_state['111'] = 0


        elif user_input[i][:5] == '01000': # rs R0 $5
            shift = int(user_input[i][8:], 2)
            reg = str(bin(reg_state[user_input[i][5:8]])).replace('0b', '')
            length = len(reg)
            if length > shift:
                reg = '0'*shift + reg[:length-shift]
                reg_state[user_input[i][5:8]] = int(reg, 2)
            else:
                reg_state[user_input[i][5:8]] = 0
            reg_state['111'] = 0

        elif user_input[i][:5] == '01001': # ls R0 $5
            shift = int(user_input[i][8:], 2)
            reg = str(bin(reg_state[user_input[i][5:8]])).replace('0b', '')
            length = len(reg)
            if length > shift:
                reg = reg[shift:] + '0'*shift
                reg_state[user_input[i][5:8]] = int(reg, 2)
            else:
                reg_state[user_input[i][5:8]] = 0
            reg_state['111'] = 0

        elif user_input[i][:5] == '01010': # xor R0 R1 R2
            a = str(bin(reg_state[user_input[i][10:13]])).replace('0b', '')
            b = str(bin(reg_state[user_input[i][13:]])).replace('0b', '')
            a = '0'*(16 - len(a)) + a
            b = '0' * (16 - len(b)) + b
            c = ''
            for j in range(len(a)):
                if a[j] != b[j]:
                    c += '1'
                else:
                    c += '0'
            reg_state[user_input[i][7:10]] = int(c, 2)
            reg_state['111'] = 0

        elif user_input[i][:5] == '01011': # or R0 R1 R2
            a = str(bin(reg_state[user_input[i][10:13]])).replace('0b', '')
            b = str(bin(reg_state[user_input[i][13:]])).replace('0b', '')
            a = '0' * (16 - len(a)) + a
            b = '0' * (16 - len(b)) + b
            c = ''
            for j in range(len(a)):
                if a[j] == '1' or b[j] == '1':
                    c += '1'
                else:
                    c += '0'
            reg_state[user_input[i][7:10]] = int(c, 2)
            reg_state['111'] = 0

        elif user_input[i][:5] == '01100': # and R0 R1 R2
            a = str(bin(reg_state[user_input[i][10:13]])).replace('0b', '')
            b = str(bin(reg_state[user_input[i][13:]])).replace('0b', '')
            a = '0' * (16 - len(a)) + a
            b = '0' * (16 - len(b)) + b
            c = ''
            for j in range(len(a)):
                if a[j] == b[j]:
                    c += a[j]
                else:
                    c += '0'
            reg_state[user_input[i][7:10]] = int(c, 2)
            reg_state['111'] = 0

        elif user_input[i][:5] == '01101': # not R0 R1
            inv = str(bin(reg_state[user_input[i][13:]])).replace('0b', '')
            inv = '0'*(16 - len(inv)) + inv
            invert = ''
            for j in inv:
                if j == '1':
                    invert += '0'
                else:
                    invert += '1'
            reg_state[user_input[i][10:13]] = int(invert, 2)
            reg_state['111'] = 0

        elif user_input[i][:5] == '01110': # cmp R0 R1
            if reg_state[user_input[i][10:13]] > reg_state[user_input[i][13:]]:
                reg_state['111'] = 2

            elif reg_state[user_input[i][10:13]] < reg_state[user_input[i][13:]]:
                reg_state['111'] = 4

            elif reg_state[user_input[i][10:13]] == reg_state[user_input[i][13:]]:
                reg_state['111'] = 1


        elif user_input[i][:5] == '01111': # jmp label  01111 000 00000000
            t = pc
            pc_jump = True
            pc = int(user_input[i][8:], 2)
            t = pc - t
            reg_state['111'] = 0


        elif user_input[i][:5] == '10000': # jlt label
            if reg_state['111'] == 4:
                t = pc
                pc = int(user_input[i][8:], 2)
                t = pc - t
                pc_jump = True
            reg_state['111'] = 0


        elif user_input[i][:5] == '10001': # jgt label
            if reg_state['111'] == 2:
                t = pc
                pc = int(user_input[i][8:], 2)
                t = pc - t
                pc_jump = True
            reg_state['111'] = 0


        elif user_input[i][:5] == '10010': # je label
            if reg_state['111'] == 1:
                t = pc
                pc = int(user_input[i][8:], 2)
                t = pc - t
                pc_jump = True
            reg_state['111'] = 0

        print_reg()
        
        if not pc_jump:
            pc += 1
            i += 1
    print_rest(user_input, var_mem)

    

main()
