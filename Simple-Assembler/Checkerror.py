
# case where any other instruction can call labels handled - will give a typo
correct = ("add", "sub", "ld", "st", "mul", "div", "rs", "ls", "xor", "or", "and", "not", "cmp", "jmp", "jlt", "jgt",
           "je", "hlt", "mov", "var")

typeA = ("add","sub","mul", "xor", "or", "and")
typeB = ("rs", "ls")
typeC = ("div", "not", "cmp")
typeD = ("ld", "st")
typeE = ("jmp", "jlt", "jgt", "je")


def error_A(lin, line_no):
    if not(len(lin) == 4):
        print(f"ERROR: Incorrect syntax in line {line_no}")
        return True

    if len(lin[1]) != 2 or len(lin[2]) != 2 or len(lin[3]) != 2 or lin[1][0] != "R" or lin[2][0] != "R" or lin[3][
        0] != "R":
        print(f"ERROR: Typo in register name declaration on line {line_no}")
        return True

    for i in range(1, 4):
        if int(lin[i][1]) > 6 or int(lin[i][1]) < 0:
            print(f"ERROR: Illegal register name on line {line_no}")
            return True

    return False


def error_B(lin, line_no):
    if not(len(lin) == 3):
        print(f"ERROR: Incorrect syntax in line {line_no}")
        return True

    if lin[1][0] != "R" or lin[2][0] != "$":
        print(f"ERROR: Typo in register/immediate declaration on line {line_no}")
        return True

    if int(lin[1][1]) > 6 or int(lin[1][1]) < 0:
        print(f"ERROR: Illegal register name on line {line_no}")
        return True

    if int(lin[2][1:]) > 255 or int(lin[2][1:] < 0):
        print(f"ERROR: Illegal immediate value in line {line_no}")

    return False


def error_C(lin, line_no):
    if not(len(lin) == 3):
        print(f"ERROR: Incorrect syntax in line {line_no}")
        return True

    if len(lin[1]) != 2 or len(lin[2]) != 2 or lin[1][0] != "R" or lin[2][0] != "R":
        print(f"ERROR: Typo in register name on line {line_no}")
        return True

    for i in range(1, 3):
        if int(lin[i][1]) > 6 or int(lin[i][1]) < 0:
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

    if int(lin[1][1]) > 6 or int(lin[1][1]) < 0:
        print(f"ERROR: Illegal register name declaration on line {line_no}")
        return True

    return False


def error_E(lin, line_no):      # jmp X
    if not(len(lin) == 2):
        print(f"ERROR: Incorrect syntax in line {line_no}")
        return True

    return False


def error_mov(lin, line_no):    # mov R1 $4   /    mov R1 R2
    if not(len(lin) == 3):
        print(f"ERROR: Incorrect syntax in line {line_no}")
        return True

    if lin[1][0] != 'R' or len(lin[1]) != 2 or int(lin[1][1:]) > 6 or int(lin[1][1:]) < 0:
        print(f"ERROR: Illegal register declaration on line {line_no}")
        return True

    if lin[2][0] != '$' and lin[2][0] != 'R':
        print(f"Incorrect syntax in line {line_no}")
        return True

    if (lin[2][0] == 'R') and (len(lin[2] != 2 or int(lin[2][1:]) > 6 or int(lin[2][1:]) < 0)):
        print(f"ERROR: Illegal register declaration on line {line_no})  ")
        return True

    if lin[2][0] == '$' and (int(lin[2][1:]) < 0 or int(lin[2][1:]) > 255):
        print(f"ERROR: Illegal immediate value in line {line_no}")
        return True

    return False


def check(file):    # main function of the program
    line_no = 0
    instruct_count = 0
    defined_var = []
    defined_label = []
    temp = True

    if file[-1] != "hlt":
        print("ERROR: halt is not the last instruction.")
        return True

    for line in file[:-1]:                 # iterate over each line except last
        lin = [x for x in line.split()]
        line_no += 1

        if ':' == lin[0][-1]:
            temp = False
            instruct_count += 1
            name = lin[0][:-1]
            if name in defined_label:
                print(f"ERROR in line {line_no}: Label was already defined")
                return True

            if name not in defined_var:
                defined_label.append(name)
            else:
                print(f"ERROR in line {line_no}: Variable of same name is defined earlier ")
                return True

        elif lin[0] not in correct:          # checks first word in line
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
                defined_label.append(lin[1])
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
                print(f"ERROR in line {line_no}: Variable {v} not defined earlier ")
                return True

            elif error_D(lin, line_no):
                return True

        elif lin[0] in typeE:
            temp = False
            instruct_count += 1
            if lin[2] not in defined_label and lin[2] in defined_var:
                print(f"ERROR in line {line_no}: Misuse of variable as label ")
                return True

            elif lin[2] not in defined_label and lin[2] not in defined_var:
                v = lin[2]
                print(f"ERROR in line {line_no}: Label {v} not defined earlier ")
                return True

            elif error_E(lin, line_no):
                return True

        elif lin[0] == 'mov':   # change mov function
            temp = False
            instruct_count += 1
            if error_mov(lin, line_no):
                return True

        elif not temp:
            print(f"ERROR in line {line_no}: Variable declared after instruction")
            return True

        elif instruct_count > 256:
            print("ERROR: No of instructions exceed 256")
            return True

    return False

