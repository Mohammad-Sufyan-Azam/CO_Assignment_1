
'''         GOALS
The assembler should be capable of:
1. Handling all supported instructions                                      |
2. Handling labels                                                          |
3. Handling variables                                                       |

4. Making sure that any illegal instruction (any instruction (or instruction usage) which is not
supported) results in a syntax error. In particular you must handle:

a. Typos in instruction name or register name                               |
b. Use of undefined variables                                               |
c. Use of undefined labels                                                  |
d. Illegal use of FLAGS register                                            |
e. Illegal Immediate values (less than 0 or more than 255)                  |
f. Misuse of labels as variables or vice-versa                              |
g. Variables not declared at the beginning. Missing hlt instruction         |
i. hlt not being used as the last instruction                               |

Wrong syntax used for instructions (For example, add instruction being used as a
type B instruction).

You need to generate distinct readable errors for all these conditions. If you find any
other illegal usage, you are required to generate a “General Syntax Error”.
'''

'''
correct = ("add", "sub", "ld", "st", "mul", "div", "rs", "ls", "xor", "or", "and", "not", "cmp", "jmp", "jlt", "jgt",
          "je", "hlt", "mov", "var")
Correct Examples:
var x
label: instruction/blank
add R0 R1 R2
ld R0 mem_addr
st R0 mem_addr
rs R0 $imm
xor R0
cmp R0 R1
jmp mem_addr
hlt
'''
# case where any other instruction can call labels not handled
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
            print(f"ERROR: Typo in register name on line {line_no}")
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

# change error_D to error_E functions
def error_D(lin, line_no):      # ld R1 X
    if not(len(lin) == 3):
        print(f"ERROR: Incorrect syntax in line {line_no}")
        return True

    if len(lin[1]) != 2 or lin[1][0] != "R": # memory address not checked
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

    # memory address not checked

    return False


def check(file):
    # main function of the program
    line_no = 0
    var_count = 0
    address_count = 0
    defined_var = []
    defined_label = []

    if file[-1] != "hlt":
        print("ERROR: halt is not the last instruction.")
        return True
    # mov instruction should be checked separately
    # labels and variables not checked
    for line in file[:-1]:
        lin = [x for x in line.split()]
        line_no += 1

        if lin[0] == 'hlt':
            print(f"ERROR in line {line_no}: halt is used multiple times ")
            return True

        elif lin[0] not in correct:          # checks first word in line
            print(f"ERROR: Typo in line {line_no}")
            # check whether it can be a label or not
            return True

        if lin[0] == 'var':
            if len(lin[0] != 2):
                print(f"ERROR: Incorrect syntax in line {line_no}")
                return True

            elif lin[1] in defined_var:
                print(f"ERROR in line {line_no}: Variable was already defined")
                return True
            # check whether the variables come before instructions only

        elif ':' == lin[0][-1]:
            name = lin[0][:-1]
            if name in defined_label:
                print(f"ERROR in line {line_no}: Label was already defined")
                return True
            defined_label.append(name)

        # check whether label is declared before calling

        elif lin[0] in typeA:
            if error_A(lin, line_no):
                return True

        elif lin[0] in typeB:
            if error_B(lin, line_no):
                return True

        elif lin[0] in typeC:
            if error_C(lin, line_no):
                return True

        elif lin[0] in typeD:
            if error_D(lin, line_no):
                return True

        elif lin[0] in typeE:
            if error_E(lin, line_no):
                return True

    return False

