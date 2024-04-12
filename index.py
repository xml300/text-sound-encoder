import scipy.io.wavfile as wav
import numpy as np

def lzw_compress(string):
    res = []
    table = {chr(i): i - 2**15 for i in range(0, 256)}
    prev = string[0]
    
    for i in range(1, len(string)):
        print(f'\rCompressing: {(100 * (i+1)) / len(string):.2f}%', end = '')
        cur = string[i]
        if(table.get(prev + cur) != None):
            prev = prev + cur
        else:
            res.append(table[prev])
            table[prev + cur] = len(table) - 2**15
            prev = cur
    res.append(table[prev])
    print()
    return table, res


def lzw_decompress(table, code_arr):
    table = {v: k for k,v in table.items()}
    res = []
    old = code_arr[0]
    res.append(table[old])
    ch_c = table[old][0]
    
    for i in range(1, len(code_arr)):
        print(f'\rDecompressing: {(100 * i) / len(code_arr):.2f}%', end = '')
        new = code_arr[i]
        if(table.get(new) == None):
            ch = table[old]
            ch = ch + ch_c
        else:
            ch = table[new]
        res.append(ch)
        ch_c = ch[0]
        table[len(table) - 2**15] = table[old] + ch_c
        old = new
    print()
    return res


def encode(string):
    filename = 'test.wav'
    t, data = lzw_compress(string)
    if(len(t) <= 63000):
        wav.write(filename, 44100, np.asarray(data, np.int16))
    else:
        wav.write(filename, 44100, np.asarray(data, np.int32))
    return filename

def decode(filename):
    table = {chr(i):i - 2**15 for i in range(0, 256)}
    _,data = wav.read(filename)
    
    str_arr = lzw_decompress(table, data)
    return ''.join(str_arr)

def valid_input(message, constraints: dict):
    type = constraints.get('type')
    contains = constraints.get('contains')
    min = constraints.get('min')
    max = constraints.get('max')
    value = None
    valid = False

    while not valid:
        if type == 'int':
            try:
                value = int(input(message))
                if (min and value < min) or (max and value > max):
                    raise NameError
                valid = True
            except:
                print("invalid input")
        elif type == 'str':
            try:
                value = input(message)
                if contains and value.find(contains) == -1:
                    raise NameError
                valid = True
            except:
                print("Invalid Input")
    return value

print("Welcome to Text-Sound Encoder")
print("Select an option: \n\
      1. Encode text \n\
      2. Decode sound")
opt = valid_input("Option: ", {'type':'int','min': 1,'max': 2})

if opt == 1:
    print("Select an option: \n\
          1. Encode from text file \n\
          2. Encode from user input")
    encode_opt = valid_input("Option: ", {'type':'int', 'min': 1, 'max': 2})
    str_data = None

    if encode_opt == 1:
        filename = valid_input("Enter filename: ", {'type':'str', 'contains': '.txt'})
        str_data = open(filename, 'r').read()
    elif encode_opt == 2:
        str_data = input('Enter text to be encoded: ')

    filename_output = encode(str_data)
    print(f"File successfully saved as {filename_output}")
        
elif opt == 2:
    filename = valid_input("Enter filename: ", {'type':'str', 'contains': '.wav'})
    out_filename = valid_input("Enter output filename: ", {'type':'str', 'contains':'.txt'})
    decode_str = decode(filename)
    open(out_filename,'w').write(decode_str)
    print(f"File successfully saved as {out_filename}")
