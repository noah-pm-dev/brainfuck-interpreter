## Run with hexdump at end: python3 int.py <file> && hexdump -e'"%07.8_ad  " 8/1 "%03d " "  " 8/1 "%03d " "  |"' -e'16/1  "%_p"  "|\n"' -e'"%07.8_Ad\n"' mem.dat

from sys import argv

def update_mem(operation, num):
    global mem
    global pointer
    if operation == '+':
        try:
            mem[pointer] = mem[pointer] + num
        except ValueError as e:
            mem[pointer] = 0 + (num - 1) # Overflow
    else:
        try:
            mem[pointer] = mem[pointer] - num
        except ValueError as e:
            mem[pointer] = 255 - (num - 1) # Overflow


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
    if cmd in '-+':
        cleaned_code[i] = '/'
        q = 1
        try:
            while cleaned_code[i + q] == cmd:
                cleaned_code[i + q] = '/'
                q += 1
        except IndexError as e:
            pass
        
        update_mem(cmd, q)
    elif cmd == '>':
        pointer += 1
    elif cmd == '<':
        pointer -= 1

with open('mem.dat', 'wb+') as dat:
    dat.write(mem)

