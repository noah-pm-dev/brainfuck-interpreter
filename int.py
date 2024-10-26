# Run with hexdump at end: python3 int.py <file> && hexdump -e'"%07.8_ad  " 8/1 "%03u " "  " 8/1 "%03u " "  |"' -e'16/1  "%_p"  "|\n"' -e'"%07.8_Ad\n"' mem.dat

import sys
import getopt
# import termios
# import tty

def peek(stack):
    if stack:
        return stack[-1]
    else:
        return None

# def getch():
#     fd = sys.stdin.fileno()
#     old_settings = termios.tcgetattr(fd)
#     try:
#         tty.setraw(sys.stdin.fileno())
#         ch = sys.stdin.read(1)
#     finally:
#         termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#     sys.stdout.write(ch)
#     sys.exit(0)
#     return ch

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
        update_mem('r', ord(sys.stdin.seek(0, 2)))
        # sys.stdin.flush()
    return None


try:
    arguments, values = getopt.getopt(sys.argv[1:], 'mf:')
except getopt.GetoptError:
    sys.stdout.write("Please specify a file name after '-f'!\n")
    sys.exit(0)

show_mem = False
file = ''
for a in arguments:
    if a[0] == '-m':
        show_mem = True
    elif a[0] == '-f':
        file = a[1]


with open(file, 'r') as bf:
    code = bf.read()


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


sys.stdout.write('\n\n')

