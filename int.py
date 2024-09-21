## Run with hexdump at end: python3 int.py <file> && hexdump -e'"%07.8_ad  " 8/1 "%03u " "  " 8/1 "%03u " "  |"' -e'16/1  "%_p"  "|\n"' -e'"%07.8_Ad\n"' mem.dat

from sys import argv, stdout, stdin

def update_mem(operation, num):
    global mem
    global pointer
    if operation == '+':
        try:
            mem[pointer] = mem[pointer] + num
        except ValueError:
            mem[pointer] = 0 + (num - 1) # Overflow
    else:
        try:
            mem[pointer] = mem[pointer] - num
        except ValueError:
            mem[pointer] = 255 - (num - 1) # Overflow

def iterate(loop):
    while mem[pointer] != 0:
        for i, cmd in enumerate(loop):
            check_char(cmd, i)


def check_char(cmd, i):
    # print(cmd)
    global cleaned_code
    global pointer
    global loops
    if cmd in '-+':
        update_mem(cmd, 1)
    elif cmd == '>':
        if pointer != len(mem) - 1:
            pointer += 1
    elif cmd == '<':
        if pointer != 0:
            pointer -= 1
    elif cmd == '[':
        q = 1
        loop = ''
        while cleaned_code[i + q] != ']':
            loop_indexes.append(i + q)
            loop = loop + cleaned_code[i + q]
            q += 1
        iterate(loop)
    elif cmd == '.':
        stdout.write(chr(mem[pointer]))
        # with open('mem.dat', 'wb+') as dat:
        #     dat.write(mem)
    elif cmd == ',':
        update_mem('+', ord(stdin.read(1)))


file = argv[1]

with open(file, 'r') as bf:
    code = bf.read()


cleaned_code = code[:]
for char in code:
    if char not in '-+[],.<>':
        cleaned_code = cleaned_code.replace(char, '')

cleaned_code = list(cleaned_code)

mem = bytearray(30000)
pointer = 0


for i, cmd in enumerate(cleaned_code):
    check_char(cmd, i)


stdout.write('\n\n')

