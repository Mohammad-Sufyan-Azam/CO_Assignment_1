# case where any other instruction can call labels handled - will give a typo

correct = ("add", "sub", "ld", "st", "mul", "div", "rs", "ls", "xor", "or", "and", "not", "cmp", "jmp", "jlt", "jgt",
           "je", "hlt", "mov", "var")

typeA = ("add", "sub", "mul", "xor", "or", "and")
typeB = ("rs", "ls")
typeC = ("div", "not", "cmp")
typeD = ("ld", "st")
typeE = ("jmp", "jlt", "jgt", "je")


def error_A(lin, line_no):      # ADD R0 R1 R2
    if not(len(lin) == 4):
        print(f"ERROR: Incorrect syntax in line {line_no}")
        return True

    if len(lin[1]) != 2 or len(lin[2]) != 2 or len(lin[3]) != 2 or lin[1][0] != "R" or lin[2][0] != "R" or lin[3][
        0] != "R":
        print(f"ERROR: Typo in register name declaration on line {line_no}")
        return True

    for i in range(1, 4):
        if lin[i][1].isalpha() or int(lin[i][1]) > 6 or int(lin[i][1]) < 0:
            print(f"ERROR: Illegal register name on line {line_no}")
            return True

    return False


def error_B(lin, line_no):      # rs R1 $5
    if not(len(lin) == 3):
        print(f"ERROR: Incorrect syntax in line {line_no}")
        return True

    if lin[1][0] != "R" or lin[2][0] != "$":
        print(f"ERROR: Typo in register/immediate declaration on line {line_no}")
        return True

    if lin[1][1].isalpha() or int(lin[1][1]) > 6 or int(lin[1][1]) < 0:
        print(f"ERROR: Illegal register name on line {line_no}")
        return True

    if int(lin[2][1:]) > 255 or int(lin[2][1:]) < 0:
        print(f"ERROR: Illegal immediate value in line {line_no}")

    return False


def error_C(lin, line_no):      # div R2 R3
    if not(len(lin) == 3):
        print(f"ERROR: Incorrect syntax in line {line_no}")
        return True

    if len(lin[1]) != 2 or len(lin[2]) != 2 or lin[1][0] != "R" or lin[2][0] != "R":
        print(f"ERROR: Typo in register name on line {line_no}")
        return True

    for i in range(1, 3):
        if lin[i][1].isalpha() or int(lin[i][1]) > 6 or int(lin[i][1]) < 0:
            print(f"ERROR: Illegal register name declaration on line {line_no}")
            return True

    return False


def error_D(lin, line_no):      # ld R1 X
    if not(len(lin) == 3):
        print(f"ERROR: Incorrect syntax in line {line_no}")
        return True

    if len(lin[1]) != 2 or lin[1][0] != "R":
        print(f"ERROR: Typo in register name on line {line_no}")
        return True

    if lin[1][1].isalpha() or int(lin[1][1]) > 6 or int(lin[1][1]) < 0:
        print(f"ERROR: Illegal register name declaration on line {line_no}")
        return True

    return False


def error_E(lin, line_no):      # jmp X
    if not(len(lin) == 2):
        print(f"ERROR: Incorrect syntax in line {line_no}")
        return True

    return False


def error_mov(lin, line_no):    # mov R1 $4   /    mov R1 R2    /      mov R1 FLAGS
    if not(len(lin) == 3):
        print(f"ERROR: Incorrect syntax in line {line_no}")
        return True

    if lin[1][0] != 'R' or len(lin[1]) != 2 or lin[1][1].isalpha() or int(lin[1][1:]) > 6 or int(lin[1][1:]) < 0:
        print(f"ERROR: Illegal register declaration on line {line_no}")
        return True

    if lin[2][0] != '$' and lin[2][0] != 'R' and lin[2] != 'FLAGS':
        print(f"Incorrect syntax in line {line_no}")
        return True

    if (lin[2][0] == 'R') and (len(lin[2]) != 2 or lin[2][1].isalpha() or int(lin[2][1:]) > 6 or int(lin[2][1:]) < 0):
        print(f"ERROR: Illegal register declaration on line {line_no})")
        return True

    if (lin[2][0] == '$') and (int(lin[2][1:]) < 0 or int(lin[2][1:]) > 255):
        print(f"ERROR: Illegal immediate value in line {line_no}")
        return True

    return False


def check(file):    # main function of the program
    line_no = 0
    instruct_count = 0
    defined_var = []
    defined_label = []
    temp = True        # empty lines not checked

    last = [x for x in file[-1].split()]
    i = -1
    pos = len(file)
    while True:
        if len(last) == 0:             # an empty line
            if len(file) > -i:         # all empty lines present handled
                i -= 1
                last = [x for x in file[i].split()]
            else:
                print(f"ERROR in line {pos}: halt is not the last instruction.")
                return True

        if len(last) != 0 and file[i] != "hlt" and (':' not in file[i]):
            print(f"ERROR in line {pos}: halt is not the last instruction.")
            return True

        if len(last) != 0 and ':' in file[i]:
            hlt_label_check = last
            if len(hlt_label_check) != 2:
                print(f"ERROR in line {pos}: halt is not the last instruction.")
                return True
            if hlt_label_check[0][-1] == ':' and hlt_label_check[1] != 'hlt':
                print(f"ERROR in line {pos}: halt is not the last instruction.")
                return True

        if len(last) != 0 and (('hlt' == last[0]) or (':' == last[0][-1] and 'hlt' == last[1])):
            break

        pos -= 1

    position = 0
    for label in file:           # Updating labels in list
        position += 1
        lin = [x for x in label.split()]
        if len(lin) == 0:     # an empty line
            continue

        elif ':' not in lin[0]:  # not a label
            continue

        elif ':' in lin[0]:
            if ':' != lin[0][-1]:
                print(f"ERROR: Syntax error in line {position}")
                return True

            elif ':' == lin[0][-1]:
                name = lin[0][:-1]
                if name in defined_label:
                    print(f"ERROR in line {position}: Label was already defined")
                    return True
                defined_label.append(name)

    for line in file[:i]:     # iterate over each line except last
        lin = [x for x in line.split()]
        line_no += 1

        if len(lin) == 0:       # empty lines skipped
            continue

        if ':' == lin[0][-1]:
            temp = False
            instruct_count += 1
            name = lin[0][:-1]
            if name in defined_var:
                print(f"ERROR in line {line_no}: A variable of the same name is defined earlier")
                return True
            lin = lin[1:]

        if len(lin) == 0:       # empty labels skipped
            continue

        if lin[0] not in correct:          # checks first word in line
            print(f"ERROR: Typo in line {line_no}")
            return True

        if lin[0] == 'hlt':
            print(f"ERROR in line {line_no}: halt is used multiple times ")
            return True

        elif lin[0] == 'var' and temp:
            instruct_count += 1
            if len(lin) != 2:
                print(f"ERROR: Incorrect syntax in line {line_no}")
                return True

            elif lin[1] in defined_var:
                print(f"ERROR in line {line_no}: Variable was already defined")
                return True

            if lin[1] not in defined_label:
                defined_var.append(lin[1])
            else:
                print(f"ERROR in line {line_no}: Label of same name was defined earlier ")
                return True

        elif lin[0] in typeA:
            temp = False
            instruct_count += 1
            if error_A(lin, line_no):
                return True

        elif lin[0] in typeB:
            temp = False
            instruct_count += 1
            if error_B(lin, line_no):
                return True

        elif lin[0] in typeC:
            temp = False
            instruct_count += 1
            if error_C(lin, line_no):
                return True

        elif lin[0] in typeD:
            temp = False
            instruct_count += 1
            if lin[2] not in defined_var and lin[2] in defined_label:
                print(f"ERROR in line {line_no}: Misuse of label as variable ")
                return True

            elif lin[2] not in defined_label and lin[2] not in defined_var:
                v = lin[2]
                print(f"ERROR in line {line_no}: Variable ({v}) not defined in the program ")
                return True

            elif error_D(lin, line_no):
                return True

        elif lin[0] in typeE:
            temp = False
            instruct_count += 1
            if lin[1] not in defined_label and lin[1] in defined_var:
                print(f"ERROR in line {line_no}: Misuse of variable as label ")
                return True

            elif lin[1] not in defined_label and lin[1] not in defined_var:
                v = lin[1]
                print(f"ERROR in line {line_no}: Label ({v}) not defined in the program ")
                return True

            elif error_E(lin, line_no):
                return True

        elif lin[0] == 'mov':
            temp = False
            instruct_count += 1
            if error_mov(lin, line_no):
                return True

        elif lin[0] == 'var' and not temp:
            print(f"ERROR in line {line_no}: Variable declared after instruction")
            return True

        elif instruct_count > 256:
            print("ERROR: No of instructions exceed 256")
            return True

    return False
