import csv
import sys
import os

LOAD_COST = 10
READ_MEMORY = 0
WRITE_MEMORY = 8
UNAR_OPERATION = 5

def read_csv(file):
    data_dict = {}
    with open(file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            
            if len(row) >= 2:  
                key = row[0]
                value = row[1]
                data_dict[key] = value
    return data_dict

def parse_command(commands_log):
    command = commands_log["command"].strip()
    if command == "load_const":
        A = LOAD_COST
        B = int(commands_log["adress"])
        C = int(commands_log["const"])
        return A,B,C
    elif command == "read_mem":
        A=READ_MEMORY
        B=int(commands_log["adress1"])
        C=int(commands_log["adress2"])
        return A,B,C
    elif command== "write_mem":
        A=WRITE_MEMORY
        B=int(commands_log["adress1"])
        C=int(commands_log["adress2"])
        return A,B,C
    elif command =="sgn_operation":
        A=UNAR_OPERATION
        B=int(commands_log["adress1"])
        C=int(commands_log["adress2"])
        return A,B,C
def make_bytes(*args):
    A,B,C = args
    if A ==10:
        a_bits = bin(A)[2:].zfill(4)
        b_bits = bin(B)[2:].zfill(18)
        c_bits = bin(C)[2:].zfill(13)
        full_bits = '0'*5+c_bits + b_bits + a_bits
    else:
        a_bits = bin(A)[2:].zfill(4)
        b_bits = bin(B)[2:].zfill(18)
        c_bits = bin(C)[2:].zfill(18)
        full_bits = c_bits + b_bits + a_bits
    
    bytes_list = []
    for i in range(0, 40, 8):
        byte_bits = full_bits[i:i+8]
        byte_value = int(byte_bits, 2)
        bytes_list.append(byte_value)
    bytes_list.reverse()
    return [f"0x{byte:02X}" for byte in bytes_list]
def write_file(output_name,hex_bytes): #Этап 2 - функция записи в файл получившихся байтов, вывод реального размера
    bytes_list = [int(h[2:], 16) for h in hex_bytes]
    with open(output_name,"wb") as output_file:
        output_file.write(bytes(bytes_list))
        print("*байты записаны в файл")
    size = os.path.getsize(output_name)
    print(f"размер файла:{size} байт")

def load_const():
    print("load_const")

def read_mem():
    print("read_mem")

def write_mem():
    print("write_mem")

def unar_operation():
    print("unar_operation")

def main():
    if len(sys.argv)<3:
        print("не работает")
        exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    test_mode = "--test" in sys.argv
    
    print(f"Входной файл: {input_file}")
    print(f"Выходной файл: {output_file}")
    print(f"Режим тестирования: {'ВКЛ' if test_mode else 'ВЫКЛ'}")

    command_log = read_csv(input_file)
    A,B,C = parse_command(command_log)

    if test_mode:
        hex_bytes = make_bytes(A, B, C)
        print(f"Тест (A={A}, B={B}, C={C}):")
        print(", ".join(hex_bytes))
    else:
        hex_bytes =make_bytes(A, B, C)
        if A==10:
            load_const()
            write_file(output_file,hex_bytes)
        elif A==0:
            read_mem()
            write_file(output_file,hex_bytes)
        elif A==8:
            write_mem()
            write_file(output_file,hex_bytes)
        elif A==5:
            unar_operation()
            write_file(output_file,hex_bytes)

main()
