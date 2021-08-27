import matplotlib.pyplot as plt
# scatter plot-
# x axis : cycle no
# y axis: address
reg_state = {'000': 0, '001': 0, '010': 0, '011': 0, '100': 0, '101': 0, '110': 0, '111': 0}
counter = []

def PC(count):
    counter.append(count)


def show(user_input):
    x = []
    y = []
    for i in range(len(counter)):
        if user_input[counter[i]][:5] == '00100':  # ld R0 x
            a = int(user_input[i][8:], 2)
            y.append(a)
            x.append(i)

        elif user_input[i][:5] == '00101':  # st R0 x
            a = int(user_input[counter[i]][8:], 2)
            y.append(a)
            x.append(i)

        x.append(i)
        y.append(counter[i])

    plt.title('Memory Address vs Cycles')
    plt.xlabel('Cycles')
    plt.ylabel('Memory Address')
    plt.scatter(x, y)
    # plt.plot(x, y)
    plt.savefig('graph.png')
    plt.show()


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

        if user_input[i][:5] == '00100':  # ld R0 x
            var_mem[user_input[i][8:]] = 0

        elif user_input[i][:5] == '00101':  # st R0 x
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

        if user_input[i][:5] == '00000':  # add R0 R1 R2
            reg_state[user_input[i][7:10]] = reg_state[user_input[i][10:13]] + reg_state[user_input[i][13:]]
            if reg_state[user_input[i][7:10]] > 65535:
                reg_state['111'] = 8
            else:
                reg_state['111'] = 0

        elif user_input[i][:5] == '00001':  # sub R0 R1 R2
            if reg_state[user_input[i][10:13]] < reg_state[user_input[i][13:]]:
                reg_state['111'] = 8
                reg_state[user_input[i][7:10]] = 0
            else:
                reg_state[user_input[i][7:10]] = reg_state[user_input[i][10:13]] - reg_state[user_input[i][13:]]
                reg_state['111'] = 0

        elif user_input[i][:5] == '00010':  # mov R0 $5
            reg_state[user_input[i][5:8]] = int(user_input[i][8:], 2)
            reg_state['111'] = 0

        elif user_input[i][:5] == '00011':  # mov R0 R1
            reg_state[user_input[i][10:13]] = reg_state[user_input[i][13:]]
            reg_state['111'] = 0

        elif user_input[i][:5] == '00100':  # ld R0 x
            reg_state[user_input[i][5:8]] = var_mem[user_input[i][8:]]
            reg_state['111'] = 0

        elif user_input[i][:5] == '00101':  # st R0 x
            var_mem[user_input[i][8:]] = reg_state[user_input[i][5:8]]
            reg_state['111'] = 0

        elif user_input[i][:5] == '00110':  # mul R0 R1 R2
            reg_state[user_input[i][7:10]] = reg_state[user_input[i][10:13]] * reg_state[user_input[i][13:]]
            if reg_state[user_input[i][7:10]] > 65535:
                reg_state['111'] = 8
            else:
                reg_state['111'] = 0

        elif user_input[i][:5] == '00111':  # div R2 R3
            if reg_state[user_input[i][13:]] == 0 or reg_state[user_input[i][10:13]] == 0:
                reg_state['000'] = 0
                reg_state['001'] = 0
            else:
                reg_state['000'] = int(reg_state[user_input[i][10:13]] / reg_state[user_input[i][13:]])
                reg_state['001'] = int(reg_state[user_input[i][10:13]] % reg_state[user_input[i][13:]])
            reg_state['111'] = 0


        elif user_input[i][:5] == '01000':  # rs R0 $5
            shift = int(user_input[i][8:], 2)
            reg = str(bin(reg_state[user_input[i][5:8]])).replace('0b', '')
            length = len(reg)
            if length > shift:
                reg = '0' * shift + reg[:length - shift]
                reg_state[user_input[i][5:8]] = int(reg, 2)
            else:
                reg_state[user_input[i][5:8]] = 0
            reg_state['111'] = 0

        elif user_input[i][:5] == '01001':  # ls R0 $5
            shift = int(user_input[i][8:], 2)
            reg = str(bin(reg_state[user_input[i][5:8]])).replace('0b', '')
            length = len(reg)
            if length > shift:
                reg = reg[shift:] + '0' * shift
                reg_state[user_input[i][5:8]] = int(reg, 2)
            else:
                reg_state[user_input[i][5:8]] = 0
            reg_state['111'] = 0

        elif user_input[i][:5] == '01010':  # xor R0 R1 R2
            a = str(bin(reg_state[user_input[i][10:13]])).replace('0b', '')
            b = str(bin(reg_state[user_input[i][13:]])).replace('0b', '')
            a = '0' * (16 - len(a)) + a
            b = '0' * (16 - len(b)) + b
            c = ''
            for j in range(len(a)):
                if a[j] != b[j]:
                    c += '1'
                else:
                    c += '0'
            reg_state[user_input[i][7:10]] = int(c, 2)
            reg_state['111'] = 0

        elif user_input[i][:5] == '01011':  # or R0 R1 R2
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

        elif user_input[i][:5] == '01100':  # and R0 R1 R2
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

        elif user_input[i][:5] == '01101':  # not R0 R1
            inv = str(bin(reg_state[user_input[i][13:]])).replace('0b', '')
            inv = '0' * (16 - len(inv)) + inv
            invert = ''
            for j in inv:
                if j == '1':
                    invert += '0'
                else:
                    invert += '1'
            reg_state[user_input[i][10:13]] = int(invert, 2)
            reg_state['111'] = 0

        elif user_input[i][:5] == '01110':  # cmp R0 R1
            if reg_state[user_input[i][10:13]] > reg_state[user_input[i][13:]]:
                reg_state['111'] = 2

            elif reg_state[user_input[i][10:13]] < reg_state[user_input[i][13:]]:
                reg_state['111'] = 4

            elif reg_state[user_input[i][10:13]] == reg_state[user_input[i][13:]]:
                reg_state['111'] = 1


        elif user_input[i][:5] == '01111':  # jmp label
            t = pc
            pc_jump = True
            pc = int(user_input[i][8:], 2)
            t = pc - t
            reg_state['111'] = 0


        elif user_input[i][:5] == '10000':  # jlt label
            if reg_state['111'] == 4:
                t = pc
                pc = int(user_input[i][8:], 2)
                t = pc - t
                pc_jump = True
            reg_state['111'] = 0


        elif user_input[i][:5] == '10001':  # jgt label
            if reg_state['111'] == 2:
                t = pc
                pc = int(user_input[i][8:], 2)
                t = pc - t
                pc_jump = True
            reg_state['111'] = 0


        elif user_input[i][:5] == '10010':  # je label
            if reg_state['111'] == 1:
                t = pc
                pc = int(user_input[i][8:], 2)
                t = pc - t
                pc_jump = True
            reg_state['111'] = 0

        if not pc_jump:
            pc += 1
            i += 1
            
    show(user_input)

main()
