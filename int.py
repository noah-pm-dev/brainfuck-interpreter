# Run with hexdump at end: python3 int.py <file> && hexdump -e'"%07.8_ad  " 8/1 "%03u " "  " 8/1 "%03u " "  |"' -e'16/1  "%_p"  "|\n"' -e'"%07.8_Ad\n"' mem.dat

import sys
import getopt
import subprocess

def peek(stack):
    if stack:
        return stack[-1]
    else:
        return None

def flushI():
    while sys.stdin.read(1) != '\n':
        pass


def update_mem(operation, num):
    global mem
    global pointer
    if operation == '+':
        try:
            mem[pointer] = mem[pointer] + num
        except ValueError:
            mem[pointer] = 0 + (num - 1) # Overflow
    elif operation == 'r':
        mem[pointer] = num
    elif operation == '-':
        try:
            mem[pointer] = mem[pointer] - num
        except ValueError:
            mem[pointer] = 255 - (num - 1) # Overflow


def check_char(cmd):
    global cleaned_code
    global pointer
    global loop
    if cmd in '-+':
        update_mem(cmd, 1)
    elif cmd == '>':
        if pointer != len(mem) - 1:
            pointer += 1
    elif cmd == '<':
        if pointer != 0:
            pointer -= 1
    elif cmd == '.':
        sys.stdout.write(chr(mem[pointer]))
        sys.stdout.flush()
    elif cmd == ',':
        update_mem('r', ord(sys.stdin.read(1)))
        flushI()
    return None


try:
    arguments, values = getopt.getopt(sys.argv[1:], 'mvf:', ["help"])
except getopt.GetoptError as e:
    sys.stdout.write("\nInvalid argument:\n%s\n\n" % e)
    sys.exit(0)

show_mem = False
verbose = False
filename = ''
for a in arguments:
    if a[0] == "--help":
        sys.stdout.write("\nOptions:\n\n\033[1m-f\033[0m\n\tSpecify a file.\n\t\tIncorrect: `int.py -mfv hello_world.bf`\n\t\tCorrect: `int.py -mvf hello_world.bf`\n\033[1m-m\033[0m\n\tShow last state of memory on program termination.\n\033[1m-v\033[0m\n\tProvides more memory information. (Does nothing if `-m` is not present)\n\n")
        exit(0)
    elif a[0] == '-m':
        show_mem = True
    elif a[0] == '-v':
        verbose = True
    elif a[0] == '-f':
        filename = a[1]

try:
    with open(filename, 'r') as bf:
        code = bf.read()
except FileNotFoundError:
    sys.stdout.write("\nInvalid filename. Please enter a valid brainfuck file directly after the -f option!\nIncorrect: `int.py -mfv hello_world.bf`\nCorrect: `int.py -mvf hello_world.bf`\n\n")
    sys.exit(0)


cleaned_code = code[:]
for char in code:
    if char not in '-+[],.<>':
        cleaned_code = cleaned_code.replace(char, '')

cleaned_code = list(cleaned_code)

mem = bytearray(30000)
pointer = 0

stack = []
index = 0

while index != len(cleaned_code):
    char = cleaned_code[index]
    if char == '[':
        if mem[pointer] == 0:
            bstack = 1
            i = index + 1
            while bstack != 0:
                if cleaned_code[i] == '[':
                    bstack += 1
                elif cleaned_code[i] == ']':
                    bstack -= 1
                i += 1
            index = i
        else:
            if peek(stack) != index:
                stack.append(index)
            index += 1


    elif char == ']':
        if mem[pointer] == 0:
            stack.pop()
            index += 1
        else:
            index = peek(stack)
        

    else:
        check_char(char)
        index += 1





with open('mem.dat', 'wb+') as dat:
    dat.write(mem)

if show_mem == True:
    if verbose:
        mem_output = subprocess.check_output([
            "hexdump",
            "-e", '"%07.8_ad  " 8/1 "%03u " "  " 8/1 "%03u " "  |"',
            "-e", '16/1  "%_p"  "|\n"',
            "-e", '"%07.8_Ad\n"',
            "mem.dat"
        ])
    else:
        mem_output = subprocess.check_output([
            "hexdump",
            "-e", '16/1 "%03u " "\n"',
            "mem.dat"
        ])
    sys.stdout.write("\n%s\n" % mem_output.decode())

sys.stdout.write('\n\n')

