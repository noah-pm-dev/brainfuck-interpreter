## Run with hexdump at end: python3 int_copy.py <file> && hexdump -e'"%07.8_ad  " 8/1 "%03u " "  " 8/1 "%03u " "  |"' -e'16/1  "%_p"  "|\n"' -e'"%07.8_Ad\n"' mem.dat

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


def check_char(cmd):
    # print(cmd)
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
        stdout.write(chr(mem[pointer]))
    # elif cmd == ',':
    #     update_mem('+', ord(stdin.read(1)))

def iterate(index):
    num = 0
    while ((num == len(loops[index]) - 1) and ((mem[pointer] == 0) or index == 0)) == False:
        for num, char in enumerate(loops[index]):
            # print(char)
            if char.isnumeric() == False and char != 'v':
                check_char(char)
            elif char == 'v':
                loop = ''
                i = num + 1
                while loops[index][i].isnumeric() == True:
                    loop = loop + loops[index][i]
                    i += 1
                    try:
                        loops[index][i]
                    except IndexError:
                        break
                iterate(int(loop))
            
    #         print('index: ', index, '; num: ', num)
    #         print('mem: ', mem[pointer], '; pointer: ', pointer)
    #         print(((num == len(loops[index]) - 1) and (mem[pointer] == 0)))
    #         print()
    # print('rsdukoghosdi')
            
                



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

loops = ['']
level = 0

for i, cmd in enumerate(cleaned_code):
    if cmd not in '[]':
        try:
            loops[level] = loops[level] + cmd
        except IndexError:
            loops.append('')
            loops[level] = loops[level] + cmd
    elif cmd == '[':
        loops.append('%d' % level)
        loops[level] = loops[level] + 'v' + str(len(loops) - 1)
        level = len(loops) - 1
    elif cmd == ']':
        parent = ''
        i = 0
        while loops[level][i].isnumeric():
            parent = parent + loops[level][i]
            i += 1
        level = int(parent)
print(loops)

iterate(0)

        



with open('mem.dat', 'wb+') as dat:
    dat.write(mem)


stdout.write('\n\n')

