import os
import re
import shutil

# Define a lookup table that maps opcodes to machine code instructions

opcode_dict = {
    "DATA #5 RB": "00000010", #
    "DATA #5 500": "00000011", #
    "LOAD 10 RB": "00000100", #
    "LOAD RA+I RB": "00000101",
    "LOAD [RA] RB": "00000110",
    "LOAD RA RB": "00000111",
    "STORE RA 10": "00001000",
    "STORE RA RB+I": "00001001",
    "STORE RA [RB]": "00001010",
    "STORE RA RB": "00001011", #
    "JMP 10": "00001100",
    "JMP RB+I": "00001101",
    "JMP [RB]": "00001110",
    "JMP RB": "00001111",
    "JSR 5": "00010000",
    "JSR RB+I": "00010001",
    "JSR [RB]": "00010010",
    "JSR RB": "00010011",
    "PUSH #5": "00010100", #
    "PUSH RA": "00010101",
    "PUSH [RA]": "00010110",
    "PUSH [RA]+": "00010111",
    "POP 7": "00011000",
    "POP RB": "00011001",
    "POP [RB]": "00011010",
    "POP [RB]+": "00011011",
    "MOVE RA RB": "00011100",
    "MOVE 10 20": "00011101", 
    "EXGR RA RB": "00011110", 
    "ADD #5  RA RB": "00011111",
    "ADD RA  RB": "00100000",
    "ADD 200 RA RB": "00100001",
    "ADD [RA]+ RB": "00100010",
    "SHR #4 RA RB": "00100011",
    "SHR RA RB": "00100100",
    "SHR #4 (RB)": "00100101",
    "SHR #4 [RB]+": "00100110",
    "SHL #4 RA RB": "00100111",
    "SHL RA RB": "00101000",
    "SHL #4 (RB)": "00101001",
    "SHL #4 [RB]+": "00101010",
    "NOT 700": "00101011",
    "NOT RA RB": "00101100",
    "NOT RA (RB)": "00101101",
    "NOT RA [RB]+": "00101110",
    "AND #5 RA RB": "00101111",
    "AND RA RB": "00110000",
    "AND 200  RA RB": "00110001",
    "AND [RA]+ RB": "00110010",
    "OR #5 RA RB": "00110011",
    "OR RA RB": "00110100",
    "OR 200 RA RB": "00110101",
    "OR [RA]+ RB": "00110110",
    "XOR #5 RA RB": "00110111",
    "XOR RA RB": "00111000",
    "XOR 200  RA RB": "00111001",
    "XOR [RA]+ RB": "00111010",
    "CMP #5 RA RB": "00111011",
    "CMP RA RB": "00111100",
    "CMP 200 RA RB": "00111101",
    "CMP [RA]+ RB": "00111110",  
    "INC RA": "00111111",
    "INC 200": "01000000",
    "INC (200)": "01000001",
    "INC [RA]+ RB": "01000010",
    "DEC RA ": "01000011",
    "DEC 200": "01000100",
    "DEC (200)": "01000101",
    "DEC [RA]+ RB": "01000110",   
    "JC 5": "010001110001",
    "JA 5": "010001110010",
    "JCA 5": "010001110011",
    "JE 5": "010001110100",
    "JCE 5": "010001110101",
    "JAE 5": "010001110110",
    "JCAE 5": "010001110111",
    "JZ 5": "010001111000",
    "JCZ 5": "010001111001",
    "JEZ 5": "010001111010",
    "JNE 5": "010001111011",
    "JEZ 5": "010001111100",
    "JNC 5": "010001111101",
    "JNZ 5": "010001111110",
    "JB 5": "010001111111",
    "JC RB": "010010000001",
    "JA RB": "010010000010",
    "JCA RB": "0100100000011",
    "JE RB": "010010000100",
    "JCE RB": "010010000101",
    "JAE RB": "010010000110",
    "JCAE RB": "010010000111",
    "JZ RB": "010010001000",
    "JCZ RB": "010010001001",
    "JEZ RB": "010010001010",
    "JNE RB": "010010001011",
    "JEZ RB": "010010001100",
    "JNC RB": "010010001101",
    "JNZ RB": "010010001110",
    "JB RB": "010010001111",
    "JC [RB]": "010010010001",
    "JA [RB]": "010010010010",
    "JCA [RB]": "010010010011",
    "JE [RB]": "010010010100",
    "JCE [RB]": "010010010101",
    "JAE [RB]": "010010010110",
    "JCAE [RB]": "010010010111",
    "JZ [RB]": "010010011000",
    "JCZ [RB]": "010010011001",
    "JEZ [RB]": "010010011010",
    "JNE [RB]": "010010011011",
    "JEZ [RB]": "010010011100",
    "JNC [RB]": "010010011101",
    "JNZ [RB]": "010010011110",
    "JB [RB]": "010010011111",
    "JC [RB]+": "010010100001",
    "JA [RB]+": "010010100010",
    "JCA [RB]+": "010010100011",
    "JE [RB]+": "010010100100",
    "JCE [RB]+": "010010100101",
    "JAE [RB]+": "010010100110",
    "JCAE [RB]+": "010010100111",
    "JZ [RB]+": "010010101000",
    "JCZ [RB]+": "010010101001",
    "JEZ [RB]+": "010010101010",
    "JNE [RB]+": "010010101011",
    "JEZ [RB]+": "010010101100",
    "JNC [RB]+": "010010101101",
    "JNZ [RB]+": "010010101110",
    "JB [RB]+": "010010101111",
    "EXGM RA RB": "01001011",   
    "CLF": "0100110000000000",
    "END": "0100110100000000",
    "SUB #5 RA RB": "01001110",
    "SUB RA RB": "01001111",
    "SUB 200  RA RB": "01010000",
    "SUB [RA]+ RB": "01010001",
    "MULT #5 RA RB": "01010010",
    "MULT RA RB": "01010011",
    "MULT 200  RA RB": "01010100",
    "MULT [RA]+ RB": "01010101",
    "DIV #5 RA RB": "01010110",
    "DIV RA RB": "01010111",
    "DIV 200  RA RB": "01011000",
    "DIV [RA]+ RB": "01011001",
    "RET" : "0101101000000000",
    "CLR RB" : "01011011",
}

register_dict= {

     "R0" :  "0000",
     "R1"  : "0001",
     "R2"  : "0010",
     "R3" :  "0011",
     "R4" :  "0100",
     "R5" :  "0101",
     "FP" :  "0110",
     "IND" :  "0111",
     "SP" :  "1000",
     "FL"  : "1001",
     "TMP"  : "1010",
     "CNT"  : "1011",
     "IAR"  : "1100",
     "IR"  : "1101",
     "ACC"  : "1110",
     "MAR"  : "1111",
 }
    
ascii_dict= {

    "A": "#65",
    "B": "#66",
    "C": "#67",
    "D": "#68",
    "E": "#69",
    "F": "#70",
    "G": "#71",
    "H": "#72",
    "I": "#73",
    "J": "#74",
    "K": "#75",
    "L": "#76",
    "M": "#77",
    "N": "#78",
    "O": "#79",
    "P": "#80",
    "Q": "#81",
    "R": "#82",
    "S": "#83",
    "T": "#84",
    "U": "#85",
    "V": "#86",
    "W": "#87",
    "X": "#88",
    "Y": "#89",
    "Z": "#90",
    "a": "#97",
    "b": "#98",
    "c": "#99",
    "d": "#100",
    "e": "#101",
    "f": "#102",
    "g": "#103",
    "h": "#104",
    "i": "#105",
    "j": "#106",
    "k": "#107",
    "l": "#108",
    "m": "#109",
    "n": "#110",
    "o": "#111",
    "p": "#112",
    "q": "#113",
    "r": "#114",
    "s": "#115",
    "t": "#116",
    "u": "#117",
    "v": "#118",
    "w": "#119",
    "x": "#120",
    "y": "#121",
    "z": "#122",
    "!": "#33",
    ":": "#34",
    "#": "#35",
    "$": "#36",
    "%": "#37",
    "&": "#38",
    " ": "#39",
    "(": "#40",
    ")": "#41",
    "*": "#42",
    "+": "#43",
    ",": "#44",
    "-": "#45",
    ".": "#46",
    "/": "#47",
    "0": "#48",
    "1": "#49",
    "2": "#50",
    "3": "#51",
    "4": "#52",
    "5": "#53",
    "6": "#54",
    "7": "#55",
    "8": "#56",
    "9": "#57",
    ":": "#58",
    ";": "#59",
    "<": "#60",
    "=": "#61",
    ">": "#62",
    "?": "#63",
    "@": "#64",
    "[": "#91",
    "]": "#93",
    "^": "#94",
    "_": "#95",
    "`": "#96",
    "{": "#123",
    "|": "#124",
    "}": "#125",
    "~": "#126",

 }








INSTRUCTIONS = set(opcode_dict.keys())
INSTRUCTIONS = set(register_dict.keys())


#----------------------------------------------------FIRST PASS -------------------------------------------------------------------------------------
#
#   Open the assembly langiage file. Read all the contents into a list ignoring the comments. Remove leading / trailing spaces
#   and replace commas with a space. All this is in assembly_input_dec1 (206). Open up assembly_input_dec1 one line at a time
#   and split the line iinto it's parts. First look for ORIGIN then grabs the next value after origin which can be in 3 formats
#   0b1010101, 0xCDE23 , 500 (binary , hex, decimal). If it starts with 0b or 0B it is binary so convert to decimal if 0x or 0X
#   converts from hex to decimal, else it converts string decimal to decimal.  (239) Now we have ORIGIN in a decimal format we set the
#   intitial program counter to the value of ORIGIN , unless there is no value in ORIGIN in which case we set the program counter and
#   ORIGIN to zero. 
#   Once ORIGIN has been dealt with the code then we convert
#   all the rest of the binary and hexadeciaml values to integers. If the part starts with # then we are dealing with a literal value (not a
#   memory location). So #0b101 converts to #5 , #0xC converts to #12 , we retain the # as it tells us we have a literal value. If it does not
#   begin with a # then the value is a memory location. In which case we convert 0b101 to 5, 0xC to 12. If a conversion to an integer is successful
#   Then it adds the value of ORIGIN onto it so for example JMP 5 , with origin 5 will give JMP 10.(315)
#
#------------------------------------------------------------------------------------------------------------------------------------------------------

# Get the current directory

dir_path = os.getcwd()

# Look for the first .txt file in the current directory but also ignore any file called PASS1.txt

file_path = None
for filename in os.listdir(dir_path):
    if filename.endswith(".txt") and filename != "PASS1.txt":
        file_path = os.path.join(dir_path, filename)
        break

# Exit if no .txt file is found

if file_path is None:
    print("ERROR: No .txt file found in current directory.")
    exit(1)

# Create a copy of the file with "_copy" appended to the filename as the original will be overwritten and we will copy this file
# back over at the end of the program.
file_name, file_ext = os.path.splitext(file_path)
file_copy_path = file_name + "_copy" + file_ext

# Copy the file
try:
    shutil.copyfile(file_path, file_copy_path)
    print(f"File copied: {file_copy_path}")
except shutil.Error as e:
    print(f"ERROR: Failed to copy the file: {e.filename} - {e}")
except IOError as e:
    print(f"ERROR: Failed to access the file: {e.filename} - {e.strerror}")
   

    
#------------------------------------------------------------ implement DC1: first 'hello world' and fix the CMP command--------------------------------------------------------

updated_lines = []

i = 0  # Initialize the value of i

with open(file_path, "r") as f:
    for line in f:
        line = line.strip()  # Strip leading and trailing whitespace
        line = line.replace(',', ' ')  # Remove any commas within the line
        line_parts = line.split()

        if len(line_parts) >= 3 and line_parts[0].endswith(':') and "DC" in line_parts[0] and re.match(r"'[^']{2,}'", line_parts[2]):
            characters_between_quotes = re.search(r"'([^']{2,})'", line_parts[2]).group(1)
            line_prefix = line_parts[0][:-1]
            for char in characters_between_quotes:
                i += 1  # Increment the value of i for each character
                updated_line = f"{line_prefix}_c{i}: c_{i} '{char}'"
                updated_lines.append(updated_line)
        #elif len(line_parts) >= 3 and line_parts[0] == "CMP" and (line_parts[1].startswith("#") or line_parts[1].isdigit()):
        elif len(line_parts) >= 3 and line_parts[0] == "CMP" and (line_parts[1].startswith("#") or line_parts[1].isdigit() or (line_parts[1].islower() and not line_parts[1].startswith("'") and not line_parts[1].endswith("'"))):        
            updated_line = f"{line_parts[0]} {line_parts[1]} {line_parts[2]}, {line_parts[2]}"
            updated_lines.append(updated_line)

        elif line_parts and line_parts[0] == "CMP" and any(re.match(r"'[^']{1}'", part) for part in line_parts):
            print("should be here")
            original_char = line_parts[1].strip("'")  # assuming char is in quotes at line_parts[1]
            if original_char in ascii_dict:
                updated_line = f"{line_parts[0]} {ascii_dict[original_char]} {line_parts[2]}, {line_parts[2]}"
                updated_lines.append(updated_line)

        else:
            updated_line = line.strip()
            for char in ascii_dict:
                updated_line = updated_line.replace(f"'{char}'", ascii_dict[char])
            updated_lines.append(updated_line)

# Print the updated lines
for line in updated_lines:
    print(line)

# Save the updated lines back to the original file
with open(file_path, "w") as f:
    for line in updated_lines:
        f.write(line + "\n")


#---------------------------------------------------------------------------------------------------------------------------------------------------------

# Read the contents of the file into a list, ignoring comments

with open(file_path, "r") as f:
    assembly_input_dec1 = []

    for line in f:
        # Ignore comments after semicolon
        line = line.split(";")[0]
        # Remove leading/trailing whitespace and replace comma with space
        line = line.strip().replace(",", " ")
        # Add to list if line is not empty     
        if line:
            assembly_input_dec1.append(line)
        

    i = 0
    while i < len(assembly_input_dec1):
        line = assembly_input_dec1[i].strip()  # Strip leading and trailing whitespaces
        
        # Check if line contains a label
        if line.endswith(':'):
            label_line = line

            # Find the next non-empty line or line with non-whitespace characters
            j = i + 1
            while j < len(assembly_input_dec1):
                next_line = assembly_input_dec1[j].strip()
                if next_line:
                    break
                j += 1

            # Add the label line and the next non-empty line to assembly_input_dec1
            if j < len(assembly_input_dec1) and not next_line.endswith(':'):
                assembly_input_dec1[i] = f"{label_line} {next_line}"
                del assembly_input_dec1[i+1:j+1]
            else:
                assembly_input_dec1[i] = label_line
                del assembly_input_dec1[i+1:j]
            
            i += 1  # Skip the blank lines
        else:
            i += 1

    # Print the modified assembly_input_dec1
    #for line in assembly_input_dec1:
        #print(line)

    for line in f:
        # Ignore comments after semicolon
        line = line.split(";")[0]
        # Remove leading/trailing whitespace and replace comma with space
        line = line.strip()
        line = line.strip().replace(",", " ")
        # Add to list if line is not empty     

        if line:
            assembly_input_dec1.append(line)
        
    #--------------------------------------------------------------------------------------------------------------------

# Copy contents of copied file back into the original and delete the copy
try:
    with open(file_copy_path, "r") as f_copy:
        copy_contents = f_copy.read()
        with open(file_path, "w") as f_original:
            f_original.write(copy_contents)
    print("Contents copied from _copy to the original file.")
except IOError as e:
    print(f"ERROR: Failed to access the files: {e.filename} - {e.strerror}")

# Delete the _copy file
try:
    os.remove(file_copy_path)
    print(f"File deleted: {file_copy_path}")
except OSError as e:
    print(f"ERROR: Failed to delete the file: {e.filename} - {e.strerror}")


#---------------------------------------------------------------------------------------------------------------------

assembly_input_dec2 = []
ORIGIN = None
Program_Counter = 0
symbol_table = {}
start_address ='0'
for line in assembly_input_dec1:
    line_parts = line.split()

    if line_parts[0] == 'STARTADDRESS':
        # Update the program counter to the value specified in the ORIGIN directive
        start_address = line_parts[1]
        print(start_address)
        Program_Counter = ORIGIN
        #continue 

    if ORIGIN is None:
        if 'ORIGIN' in line_parts:
            # Extract the number following "ORIGIN"
            ORIGIN_str = line_parts[line_parts.index('ORIGIN') + 1]
            if ORIGIN_str.startswith('0b') or ORIGIN_str.startswith('0B'):
                try:
                    ORIGIN = int(ORIGIN_str[2:], 2)
                except ValueError:
                    pass
            elif ORIGIN_str.startswith('0x') or ORIGIN_str.startswith('0X'):
                try:
                    ORIGIN = int(ORIGIN_str[2:], 16)
                    
                except ValueError:
                    pass
            else:
                try:
                    ORIGIN = int(ORIGIN_str)
                    
                except ValueError:
                    pass

            # Initialize Program_Counter with ORIGIN value
            if ORIGIN is not None:
                Program_Counter = ORIGIN
                #print(f"PC set to  {Program_Counter}")
            else:
                Program_Counter = 0
        else:
            ORIGIN = 0x8000
            Program_Counter = 0
    initial_origin = ORIGIN
     


    for i in range(len(line_parts)):
        if line_parts[i].startswith('#'):
            if line_parts[i].startswith('#0x') or line_parts[i].startswith('#0X'):
                try:
                    decimal_value = int(line_parts[i][3:], 16)
                    line_parts[i] = '#' + str(decimal_value)
                except ValueError:
                    # Skip over invalid hexadecimal literal
                    pass
            elif line_parts[i].startswith('#0b') or line_parts[i].startswith('#0B'):
                try:
                    decimal_value = int(line_parts[i][3:], 2)
                    line_parts[i] = '#' + str(decimal_value)
                except ValueError:
                    # Skip over invalid binary literal
                    pass


            else:
                # Convert decimal literal to int
                try:
                    decimal_value = int(line_parts[i])
                    line_parts[i] = str(decimal_value)
                except ValueError:
                    # Skip over non-literal value
                    pass
        else:
            # Convert decimal, hexadecimal, or binary memory location to int and add ORIGIN value
            try:
                mem_location_str = line_parts[i]
                
                if mem_location_str.startswith('0x') or mem_location_str.startswith('0X'):               
                    mem_location = int(mem_location_str, 16)
                    
                elif mem_location_str.startswith('0b') or mem_location_str.startswith('0B'):
                    mem_location = int(mem_location_str, 2)
                else:
                    mem_location = int(mem_location_str)

                if line_parts[i-1] == 'ORIGIN':
                    line_parts[i] = str(ORIGIN)
                elif line_parts[i-1] == 'STARTADDRESS':
                    line_parts[i] = str(start_address)                           
                elif not any(part.startswith('DS') for part in line_parts):
                    #line_parts[i] = str(mem_location + ORIGIN)
                    line_parts[i] = str(mem_location)
                                    
            except ValueError:
                # Skip over non-decimal, non-hexadecimal, non-binary literal value
                pass
                               
    # Update memory location with instruction and its arguments
    
    assembly_input_dec2.append(' '.join(line_parts))






#--------------------------------------------------- SECOND PASS --------------------------------------------------------------
#  
#   Now assembler_input_dec2 has been updated so that all binary and hex are now in decimal. All memory values have been
#   shifted by the value of ORIGIN. We now go through a second pass of assembler_input_dec2. In this pass we work out the
#   length of each instruciton either 1,2 or 3 full bytes (1 mean 16 bit bytes). And update the symbol table with the correct
#   program counter value and label. Also these lengths will be correct even if you repalce the numbers by labels. So for
#   example MOVE 40 ,60  , MOVE first, 60 , MOVE 40, first , MOVE first , second. We then repalce all the labels in the jump
#   instructions with the correct memory locations and remove the assembler directives and save in a file called PASS 1.(435)
#
#
#-------------------------------------------------------------------------------------------------------------------------------
    
    

# Loop over each line in assembly_input_dec2 and determine the program counter value for each new line of code (this includes possibility
# of using labels as well.
length=0
address_sum=0
instr_length=0


for line in assembly_input_dec2:
    
    # Split the line into its parts
    line_parts = line.split()

    if line_parts[0] == 'ORIGIN':
        # Update the program counter to the value specified in the ORIGIN directive
        ORIGIN = int(line_parts[1])
        Program_Counter = ORIGIN
        continue 
    if line_parts[0] == 'STARTADDRESS':
        # Update the program counter to the value specified in the ORIGIN directive
        start_address = line_parts[1]
        Program_Counter = ORIGIN
        continue 


    # Check if line contains an assembler directive
    if line_parts[0].endswith(':') and "DS" not in line_parts[0] and "EQU" not in line_parts[0] and "DC" not in line_parts[0]:
        # Line contains an assembler directive, save symbol to symbol table
        symbol_name = line_parts[0][:-1]  # Remove the colon at the end of the symbol name
        symbol_table[symbol_name] = Program_Counter
        # Subtract 1 from the length of the instruction
        instr_length = len(line_parts) - 1
        # Remove the symbol name from the instruction
        line_parts = line_parts[1:]

    elif line_parts[0].endswith(':') and "DS" in line_parts[0] and "EQU" not in line_parts[0]:
    # Line contains an assembler directive, save symbol to symbol table

        # Check if it begins with '0b' or '0B' for binary conversion
        if start_address.startswith(('0b', '0B')):
            start_address = int(start_address, 2)
        # Check if it begins with '0x' or '0X' for hexadecimal conversion
        elif start_address.startswith(('0x', '0X')):
            start_address = int(start_address, 16)
        else:
            if start_address.startswith(('0b', '0B')):
                start_address = int(start_address, 2)
        # Check if it begins with '0x' or '0X' for hexadecimal conversion
            elif start_address.startswith(('0x', '0X')):
                start_address = int(start_address, 16)
            
            start_address = int(start_address)  # Treat as decimal

        start_address = str(int(start_address))
        symbol_name = line_parts[1]
        length_str = line_parts[2].strip()

        if length_str.startswith(('0b', '0B')):
            length = int(length_str, 2)
        elif length_str.startswith(('0x', '0X')):
            length = int(length_str, 16)
        else:
            length = int(length_str)

        symbol_table[symbol_name] = int(address_sum + int(start_address))
        address_sum += length
            


        #-------------------------------------------------------------------

    elif line_parts[0].endswith(':') and "DC" in line_parts[0] and "EQU" not in line_parts[0]and "DS" not in line_parts[0]:
    # Line contains an assembler directive, save symbol to symbol table
        
        # Check if it begins with '0b' or '0B' for binary conversion
        if start_address.startswith(('0b', '0B')):
            decimal_value = int(start_address, 2)
            line_parts[i] = str(decimal_value)   
            start_address = int(start_address, 2)
        # Check if it begins with '0x' or '0X' for hexadecimal conversion
        elif start_address.startswith(('0x', '0X')):
            decimal_value = int(start_address, 16)
            line_parts[i] = str(decimal_value)       
            start_address = int(start_address, 16)               
                
        else:
            

            if start_address.startswith(('0b', '0B')):
                start_address = int(start_address, 2)
            # Check if it begins with '0x' or '0X' for hexadecimal conversion
            elif start_address.startswith(('0x', '0X')):
                start_address = int(start_address, 16)


            start_address = int(start_address)  # Treat as decimal

        start_address = str(int(start_address))
        symbol_name = line_parts[1]
        length_str = line_parts[2].strip()

        if length_str.startswith(('0b', '0B')):
            length = int(length_str, 2)
        elif length_str.startswith(('0x', '0X')):
            length = int(length_str, 16)
        else:
            length = (length_str[1:])

        #symbol_table[symbol_name] = int(address_sum + int(start_address) + ORIGIN)
        symbol_table[symbol_name] = int(address_sum + int(start_address))
        address_sum += 1



        #-------------------------------------------------------------------
        

    elif line_parts[0].endswith(':') and "EQU" in line_parts[0]:
        # Line contains an assembler directive, save symbol to symbol table
        symbol_name = line_parts[1]
        symbol_table[symbol_name] = line_parts[2]
                    
    else:
        # Line does not contain an assembler directive, determine instruction length normally
        instr_length = len(line_parts)-0
        
    # Check instruction length
    if (instr_length ==3 and line_parts[0] == "DATA" ) and (line_parts[2].isdigit() or (line_parts[2].isalnum() and line_parts[2].islower())):
        
        # DATA instruction with immediate value
        
        Program_Counter += 3

    elif (instr_length == 3 and line_parts[0] == "MOVE") and ( ((line_parts[1].isdigit() or (line_parts[1].isalnum() and line_parts[1].islower()))) \
         and ((line_parts[2].isdigit() or (line_parts[2].isalnum() and line_parts[2].islower()))) ):
        # MOVE instruction with immediate values
        Program_Counter += 3

        #  Test lenthe 4, 3, 2, 1 length instructions

    elif instr_length == 4:
        # 4-part instruction   
        Program_Counter += 2


    elif instr_length == 3:      
        if (not line_parts[1].isdigit() and "#" not in line_parts[1] and not line_parts[2].isdigit()) and (not any(c.islower() for c in line_parts[1]) and not any(c.islower() for c in line_parts[2])):
            # 3-part instruction with symbols
            
            Program_Counter += 1
        else:
            # 3-part instruction with immediate value
            Program_Counter += 2


    elif instr_length == 2:        
        #if line_parts[1].isdigit() or (line_parts[1].isalnum() and line_parts[1].islower()): # test lower case letters for label !
            # 2-part instruction with immediate value
        if not line_parts[1].isupper():
            Program_Counter += 2
            
        elif '#' in line_parts[1]:
            # 2-part instruction with immediate value using , this covers PUSH #5 
            Program_Counter += 2           
        else:
            Program_Counter +=1   


    elif instr_length == 1:
        # 1-part instruction
        Program_Counter +=1



# JUMP instruciton labels
print(assembly_input_dec2)

# Loop over each line in assembly_input_dec2 again
for i in range(len(assembly_input_dec2)):
    line = assembly_input_dec2[i]
    
    # Split the line into its parts
    line_parts = line.split()

    # Check if line contains a jump instruction with a symbol operand

    if line_parts[0].endswith(':'):
        # Remove the symbol name from the instruction
        line_parts = line_parts[1:]
        
    if line_parts[0] in ["JMP", "JSR", "JC", "JA", "JCA", "JE", "JCE", "JAE", "JCAE", "JZ", "JCZ", "JEZ", "JNE", "JEZ", "JNC", "JNZ", "JB"] and line_parts[1] in symbol_table:
        # Replace the symbol with its memory location
        symbol_name = line_parts[1]
        memory_location = symbol_table[symbol_name]
        assembly_input_dec2[i] = f"{line_parts[0]} {memory_location}"
    # Check if line is an assembler directive or label
    if line_parts[0].endswith(':'):
        # Line is an assembler directive or label, strip it out
        assembly_input_dec2[i] = " ".join(line_parts[1:])



#   replace the labels with numbers from the symbol table

for i in range(len(assembly_input_dec2)):
    line = assembly_input_dec2[i]
    
    # Split the line into its parts
    line_parts = line.split()   

    # Split the line into its parts
    line_parts = line.split()

    for j in range(1, len(line_parts)):
        # Check if the part is a lowercase label
        if line_parts[j].islower():
            # Replace the label with its value from the symbol table
            if line_parts[j] in symbol_table:
                line_parts[j] = str(symbol_table[line_parts[j]])

    # Update the line in assembly_input_dec2
    assembly_input_dec2[i] = ' '.join(line_parts)
        

print(assembly_input_dec2)

print(symbol_table)
updated_assembly_input_dec2 = []
data_lines = []

for line in assembly_input_dec2:
    if line.startswith("DC") and ":" in line:
        line_parts = line.split()
        symbol_name = line_parts[0].strip(":")
        address = line_parts[1]
        value = line_parts[2]
        if value.startswith("'") and value.endswith("'"):
            label = line_parts[2].strip("'")
            character = line_parts[2].strip("'")[0]
            
            # Look up the ASCII value for the character in the ascii_dict dictionary
            if character in ascii_dict:
                ascii_value = ascii_dict[character]               

            value = ascii_value
        instruction_line = f"DATA {value} {address}"
        data_lines.append(instruction_line)
    else:
        updated_assembly_input_dec2.append(line)

# Add the data lines at the top of updated_assembly_input_dec2
updated_assembly_input_dec2 = data_lines + updated_assembly_input_dec2

#for line in updated_assembly_input_dec2:
 #   print(line)



filtered_lines = []

for line in updated_assembly_input_dec2:
    line_parts = line.split()
    if line_parts[0].startswith(('DS', 'DC', 'EQU', 'ORIGIN', 'STARTADDRESS')):
        continue  # Skip lines starting with 'DS:', 'EQU:', 'EQU:', 'ORIGIN', or 'STARTADDRESS'
    elif line_parts[0].endswith(':'):
        line_parts[0] = line_parts[0].split(':')[1]  # Remove content before ':'
    filtered_lines.append(' '.join(line_parts))

updated_assembly_input_dec2 = filtered_lines
      
#print(assembly_input_dec2)

with open('PASS1.txt', 'w') as f:
    for line in updated_assembly_input_dec2:
        f.write(line + '\n')


#  print outputs
##print("Program_Counter:", Program_Counter)
##print(assembly_input_dec2)
print(symbol_table)




#-------------------------------------------------------------------------------------------------------------------------------------------------






#-----------------------------------------------------------------THIRD PASS-----------------------------------------------------------------------
  # Open up PASS1. Read out each line and savr it to the list assembly_input[].

#Get the current directory

dir_path = os.getcwd()

# Look for the first .txt file in the current directory

file_path = None
for filename in os.listdir(dir_path):
    if filename == "PASS1.txt":
        file_path = os.path.join(dir_path, filename)
        break

# Exit if no .txt file is found

if file_path is None:
    print("ERROR: No .txt file found in current directory.")
    exit(1)

# Read the contents of the file into a list, ignoring comments

machine_code = []

with open(file_path, "r") as f:
    assembly_input = []
    for line in f:
        assembly_input.append(line.strip())
        

    # -------------------------------------------------------------------------------------------------------

# Group of 4

for line in assembly_input:
    parts4 = line.split()
    
    # Test for 4 parts
    if len(parts4) == 4:
           
        

        # parse input line
        assembly4_name = parts4[0]                                      # "ADD"
        assembly4_imm = parts4[1]                                       # ["#7"]
        assembly4_RA = parts4[2]                                        # ["R0"]
        assembly4_RB = parts4[3]                                        # ["R1"]

        # Check if assembly4_imm starts with #
        if assembly4_imm.startswith("#"):
            assembly4_imm_parts = [assembly4_imm[0], assembly4_imm[1:]]
        else:
            assembly4_imm_parts = [assembly4_imm]
            
        assembly4_imm_parts_0 = assembly4_imm[0]                        # ['#']
        assembly4_imm_parts_1 = assembly4_imm_parts[1] if len(assembly4_imm_parts) > 1 else None   # ['5'] or None
            
        for opcode_line, opcode in opcode_dict.items():
        # parse the opcode line
            
            opcode4_parts = opcode_line.split()
                
            if len(opcode4_parts) == 4:
                
                #  we can get access to all the parts of the assembly language and the opcode dictionary for comparison

                opcode4_name = opcode4_parts[0]                                 # "ADD"
                opcode4_imm = opcode4_parts[1]                                  # ["#7"]
                opcode4_RA = opcode4_parts[2]                                   # ["R0"]
                opcode4_RB = opcode4_parts[3]                                   # ["R1"]
                opcode4_imm_parts = [opcode4_imm[0], opcode4_imm[1:]]           # ['#', '7']
                opcode4_imm_parts_0 = opcode4_imm[0]                            # ['#']
                opcode4_imm_parts_1 = opcode4_imm_parts[1] if len(opcode4_imm_parts) > 1 else None  # ['5'] or None
               
                # The comparison parts go here

                # This covers ADD #5 RA RB , AND #5 RA RB , OR #5 RA RB , XOR #5 RA RB , SHL #5 RA RB , SHR #5 RA RB  - 7 cases

                if assembly4_name == opcode4_name and assembly4_imm_parts_0 == opcode4_imm_parts_0 == "#":      

                    # split assembly2_RA into # and 5 to get access to the decimal value 5

                    assembly4_imm_REG = [0, 0]
                    assembly4_imm_REG[1] = assembly4_imm.split('#')[1]
            
                    # map RA and RB registers to 4-bit values using register_dict
                    ra_value = register_dict[assembly4_RA]
                    rb_value = register_dict[assembly4_RB]

                    # convert decimal immediate value to binary string and pad with zeros to 8 bits
                    assembly4_imm_binary = bin(int(assembly4_imm_REG[1]))[2:].zfill(16)
                      
                    #concatenate
                    machine_code.append(opcode + ra_value + rb_value + " " + assembly4_imm_binary )  
                
                    break
        


                # This covers ADD 200 RA RB --- AND 200 RA RB --- OR 200 RA RB --- XOR 20 RA RB --- CMP 200 RA RA  - 5 Cases

                if assembly4_name == opcode4_name and opcode4_imm_parts_0.isdigit():

                     
                    # map RA and RB registers to 4-bit values using register_dict
                    ra_value = register_dict[assembly4_RA]
                    rb_value = register_dict[assembly4_RB]

                    # convert decimal immediate value to binary string and pad with zeros to 8 bits
                    assembly4_imm_binary = bin(int(assembly4_imm))[2:].zfill(16)
            
                    #concatenate
                    machine_code.append(opcode + ra_value + rb_value + " " + assembly4_imm_binary )  
         
                    break          

                    # 14 IN GROUP 4 - TESTED AND WORKING PICKS UP ALL 14 INSTRUCTIONS IN A BLOCK OF 4
            
            # --------------------------------------------------------------------------------------------------------------------------------

            #  Group of 3

                #parts3 = line.split()
    elif len(parts4) == 3:       
           # parse input line
            parts3=parts4
            assembly3_name = parts3[0]                                      # "LOAD"
            assembly3_RA = parts3[1]                                        # ["RA"]
            assembly3_RB = parts3[2]                                        # ["RB"]
            for opcode_line, opcode in opcode_dict.items():
                # parse the opcode line
                
                opcode3_parts = opcode_line.split()
                
                if len(opcode3_parts) != 3:
                   
                    continue  # skip to next iteration of the loop         

                #  we can get access to all the parts of the assembly language and the opcode dictionary for comparison

                opcode3_name = opcode3_parts[0]                             # "ADD"
                opcode3_RA = opcode3_parts[1]                               # ["R0"]
                opcode3_RB = opcode3_parts[2]                               # ["R1"]
         
                #  This covers DATA #5, 500 - 1 case
                
                if assembly3_name == "DATA" and opcode3_name == "DATA" and opcode3_RB.isdigit() and assembly3_RB.isdigit():   

                     
                # split assembly2_RA into # and 5 to get access to the decimal value 5

                     assembly3_RA_REG = [0, 0]
                     assembly3_RA_REG[1] = assembly3_RA.split('#')[1]

                # map RA and RB registers to 4-bit values using register_dict
                     ra_value = register_dict['R0']
                     rb_value = register_dict['R0']

                # convert decimal immediate value to binary string and pad with zeros to 16 bits
                     assembly3_RA_binary = bin(int(assembly3_RA_REG[1]))[2:].zfill(16)

                # convert decimal immediate value to binary string and pad with zeros to 16 bits
                     assembly3_RB_binary = bin(int(assembly3_RB))[2:].zfill(16)
                
                #concatenate
                     machine_code.append(opcode + ra_value + rb_value + " " + assembly3_RA_binary + " " + assembly3_RB_binary )  
                     break  
                      
                 #  This covers STORE RA ,10  - 1 cases

                elif assembly3_name == "STORE" and opcode3_name == "STORE" and opcode3_RB.isdigit() and assembly3_RB.isdigit(): 
                     
                    # map RA and RB registers to 4-bit values using register_dict
                     ra_value = register_dict[assembly3_RA]
                     rb_value = register_dict['R0']

                # convert decimal immediate value to binary string and pad with zeros to 16 bits
                     assembly3_RB_binary = bin(int(assembly3_RB))[2:].zfill(16)
                     machine_code.append(opcode + ra_value +rb_value + " " + assembly3_RB_binary)
                     break


                # this covers MOVE 20, 40 - 1 case

                elif assembly3_name == "MOVE" and opcode3_name == "MOVE" and opcode3_RB.isdigit() and assembly3_RB.isdigit(): 

                    # map RA and RB registers to 4-bit values using register_dict
                     ra_value = register_dict['R0']
                     rb_value = register_dict['R0']

                    # convert decimal immediate value to binary string and pad with zeros to 16 bits
                     assembly3_RA_binary = bin(int(assembly3_RA))[2:].zfill(16)

                    # convert decimal immediate value to binary string and pad with zeros to 16 bits
                     assembly3_RB_binary = bin(int(assembly3_RB))[2:].zfill(16)
                
                    #concatenate
                     machine_code.append(opcode + ra_value + rb_value + " " + assembly3_RA_binary + " " + assembly3_RB_binary )  
                     break  
          
                # This covers DATA #5, RB    - 1 cases

                elif assembly3_name == "DATA" and opcode3_name == "DATA"  and  not opcode3_RB.isdigit() and  not assembly3_RB.isdigit():                                                                    

                    # split assembly2_RA into # and 5 to get access to the decimal value 5

                     assembly3_RA_REG = [0, 0]
                     assembly3_RA_REG[1] = assembly3_RA.split('#')[1]

                    # map RA and RB registers to 4-bit values using register_dict
                     ra_value = register_dict['R0']
                     rb_value = register_dict[assembly3_RB]

                    # convert decimal immediate value to binary string and pad with zeros to 16 bits
                     assembly3_RA_binary = bin(int(assembly3_RA_REG[1]))[2:].zfill(16)
                     machine_code.append(opcode + ra_value + rb_value + " " + assembly3_RA_binary)
                     break

                #  This covers LOAD 10, RB - 1 cases
         
                elif assembly3_name == opcode3_name and opcode3_RA.isdigit() and assembly3_RA.isdigit():                     
                    # map RA and RB registers to 4-bit values using register_dict
                     ra_value = register_dict['R0']
                     rb_value = register_dict[assembly3_RB]

                    # convert decimal immediate value to binary string and pad with zeros to 16 bits
                     assembly3_RA_binary = bin(int(assembly3_RA))[2:].zfill(16)
                     machine_code.append(opcode + ra_value + rb_value + " " + assembly3_RA_binary)
                     break  

                #  This covers LOAD [RA] RB - 1 cases

                elif assembly3_name == opcode3_name and "[" in opcode3_RA and "[" in assembly3_RA and "+" not in opcode3_RA and "+" not in assembly3_RA:

                    # Give us the value [RA] from RA
                     assembly3_RA_REG = [0, 0]
                     assembly3_RA_REG[1] = assembly3_RA[1:-1]   

                    # map RA and RB registers to 4-bit values using register_dict
                     ra_value = register_dict[assembly3_RA_REG[1]]
                     rb_value = register_dict[assembly3_RB]           
                    #concatenate
                     machine_code.append(opcode + ra_value + rb_value )  
                     break       

                #  This covers STORE RA [RB] - 1 cases

                elif assembly3_name == opcode3_name and "[" in opcode3_RB and "[" in assembly3_RB and "+" not in opcode3_RB and "+" not in assembly3_RB:

                    # Give us the value RA from [RA]
                     assembly3_RB_REG = [0, 0]
                     assembly3_RB_REG[1] = assembly3_RB[1:-1]   

                    # map RA and RB registers to 4-bit values using register_dict
                     ra_value = register_dict[assembly3_RA]
                     rb_value = register_dict[assembly3_RB_REG[1]]
                                 
                    #concatenate
                     machine_code.append(opcode + ra_value + rb_value )  
                     break
                    
                #  This covers   ADD [RA]+ , RB --- AND [RA]+ , RB --- OR [RA]+ , RB , XOR [RA]+ , RB , CMP [RA]+ , RB , INC [RA]+ , RB , DEC [RA]+, RB  - 7 cases

                if assembly3_name == opcode3_name and "[" in opcode3_RA and "[" in assembly3_RA and "+"  in opcode3_RA and "+"  in assembly3_RA:

                    #get access to RA from [RA]+
                     assembly3_RA_REG = [0, 0]
                     assembly3_RA_REG[1] = assembly3_RA[1:-2]
                        
                    # map RA and RB registers to 4-bit values using register_dict
                     ra_value = register_dict[assembly3_RA_REG[1]]
                     rb_value = register_dict[assembly3_RB]
                                 
                    #concatenate
                     machine_code.append(opcode + ra_value + rb_value )
                     break          

                #  This covers  SHR #4, [RB]+ --- SHL #4, [RB]+ --- NOT RA, [RB]+  - 3 cases

                elif assembly3_name == opcode3_name and "[" in opcode3_RB and "[" in assembly3_RB and "+"  in opcode3_RB and "+"  in assembly3_RB:

                     # need to split this into 2 sepetate statements , one for JUMPIF and the other for the rest
                      if  assembly3_name in ["SHL" ,"SHR"]:

                        # split assembly3_RA into # and 5 to get access to the decimal value 5
                        assembly3_RA_REG = [0, 0]
                        assembly3_RA_REG[1] = assembly3_RA.split('#')[1]

                        # Split [RB]+ into RB
                        assembly3_RB_REG = [0, 0]
                        assembly3_RB_REG[1] = assembly3_RB[1:-2]

                        # map RA and RB registers to 4-bit values using register_dict
                        ra_value = register_dict['R0']
                        rb_value = register_dict[assembly3_RB_REG[1]]

                        # convert decimal immediate value to binary string and pad with zeros to 16 bits
                        assembly3_RA_binary = bin(int(assembly3_RA_REG[1]))[2:].zfill(16)
                
                        #concatenate
                        machine_code.append(opcode + ra_value + rb_value + " " + assembly3_RA_binary )                     

                      else:

                        # Split [RB]+ into RB
                        assembly3_RB_REG = [0, 0]
                        assembly3_RB_REG[1] = assembly3_RB[1:-2]

                        # map RA and RB registers to 4-bit values using register_dict
                        ra_value = register_dict[assembly3_RA]
                        rb_value = register_dict[assembly3_RB_REG[1]]
                        
                        #machine_code.append(opcode + rb_value + " " + assembly2_RA_binary )
                                
                        machine_code.append(opcode + ra_value +rb_value)
                     
                      break          

                #  This covers LOAD RA+5 , RB  - 1 cases

                elif assembly3_name == opcode3_name and "[" not in opcode3_RA and "[" not in assembly3_RA and "+"  in opcode3_RA and "+"  in assembly3_RA:

                     #get access to RA from RA+5
                     assembly3_RA_REG = [0, 0]
                     assembly3_RA_REG[1] = assembly3_RA.split('+')[0]
                        
                    # map RA and RB registers to 4-bit values using register_dict
                     ra_value = register_dict[assembly3_RA_REG[1]]
                     rb_value = register_dict[assembly3_RB]
                                 
                    #concatenate
                     machine_code.append(opcode + ra_value + rb_value )
                     break          
                       
                #  This covers STORE RA , RB+5  - 1 cases

                elif assembly3_name == opcode3_name and "[" not in opcode3_RB and "[" not in assembly3_RB and "+"  in opcode3_RB and "+"  in assembly3_RB:

                    #get access to RA from RA+5
                     assembly3_RB_REG = [0, 0]
                     assembly3_RB_REG[1] = assembly3_RB.split('+')[0]
                        
                    # map RA and RB registers to 4-bit values using register_dict
                     ra_value = register_dict[assembly3_RA]
                     rb_value = register_dict[assembly3_RB_REG[1]]
                                 
                    #concatenate
                     machine_code.append(opcode + ra_value + rb_value )
                     break          

                #  This covers SHR #4 , (RB) --- SHL #4 , (RB) --- NOT RA, (RB)  - 3 cases

                elif assembly3_name == opcode3_name and "("  in opcode3_RB and "("  in assembly3_RB:
                      
                     # need to split this into 2 sepetate statements , one for JUMPIF and the other for the rest
                      if  assembly3_name in ["SHL" ,"SHR"]:

                        # split assembly3_RA into # and 5 to get access to the decimal value 5
                        assembly3_RA_REG = [0, 0]
                        assembly3_RA_REG[1] = assembly3_RA.split('#')[1]

                        # Split (RB) into RB
                        assembly3_RB_REG = [0, 0]
                        assembly3_RB_REG[1] = assembly3_RB[1:-1]

                        # map RA and RB registers to 4-bit values using register_dict
                        ra_value = register_dict['R0']
                        rb_value = register_dict[assembly3_RB_REG[1]]

                        # convert decimal immediate value to binary string and pad with zeros to 16 bits
                        assembly3_RA_binary = bin(int(assembly3_RA_REG[1]))[2:].zfill(16)
                
                        #concatenate
                        machine_code.append(opcode + ra_value + rb_value + " " + assembly3_RA_binary )                     

                      else:

                        # Split (RB) into RB
                        assembly3_RB_REG = [0, 0]
                        assembly3_RB_REG[1] = assembly3_RB[1:-1]

                        # map RA and RB registers to 4-bit values using register_dict
                        ra_value = register_dict[assembly3_RA]
                        rb_value = register_dict[assembly3_RB_REG[1]]
                        
                        #machine_code.append(opcode + rb_value + " " + assembly2_RA_binary )
                                
                        machine_code.append(opcode + ra_value +rb_value)
                     
                      break         
               
                     #  This covers MOVE RA, RB --- EXGR RA, RB --- ADD RA, RB --- SHR RA,RB --- SHL RA,RB --- NOT RA,RB --- AND RA,RB  - 15 cases
                     #  OR RA,RB --- XOR RA,RB --- CMP RA,RB --- INC RA, RB --- DEC RA, RB --- EXGM RA,RB --- LOAD RA,RB --- STORE RA,RB 

                elif assembly3_name == opcode3_name and assembly3_RA.isalnum() and not assembly3_RA.isdigit() and opcode3_RA.isalnum() and not opcode3_RA.isdigit()\
                        and assembly3_RB.isalnum() and not assembly3_RB.isdigit() and opcode3_RB.isalnum() and not opcode3_RB.isdigit():  

                        # map RA and RB registers to 4-bit values using register_dict
                        ra_value = register_dict[assembly3_RA]
                        rb_value = register_dict[assembly3_RB]           
                        #concatenate
                        machine_code.append(opcode + ra_value + rb_value )  
                        break       
                          
                                          # 37 CASES IN GROUP 3  ALL TESTED AND WORKING
            
                    #--------------------------------------------------------------------------------------------------------------------------------
                    #
                    #                                                               Group of 2
                    #
                    #---------------------------------------------------------------------------------------------------------------------------------

                    # parts2 = line.split()  
    elif len(parts4) == 2:
            parts2=parts4        
           # parse input line
            
            assembly2_name = parts2[0]
            assembly2_RA = parts2[1]                                             
                                         
            for opcode_line, opcode in opcode_dict.items():
                # parse the opcode line

                opcode2_parts = opcode_line.split()
                    
                if len(opcode2_parts) != 2:
                            
                    continue  # skip to next iteration of the looP    
                    
                #  we can get access to all the parts of the assembly language and the opcode dictionary for comparison
                #print(opcode2_parts)
                opcode2_name = opcode2_parts[0]                                     # "ADD"
                opcode2_RA = opcode2_parts[1]                                       # ["#7"]
                
                # This covers 15 JUMPIF instructions (JC 5 --- JA 5 ....) --- JMP 10 --- JSR 5 --- POP 10 --- NOT 700 --- INC 200 --- DEC 200 - 21 Cases

                if assembly2_name == opcode2_name and opcode2_RA.isdigit() and assembly2_RA.isdigit():
                    
                    
                # if assembly2_name == opcode2_name and opcode2_RA.isdigit() and assembly2_RA.isdigit():                  
          
                # need to split this into 2 sepetate statements , one for JUMPIF and the other for the rest
                      if  assembly2_name in ["JMP" ,"JSR", "POP", "NOT", "INC","DEC"]:
                        
                        # map RA and RB registers to 4-bit values using register_dict
                        ra_value = register_dict['R0']
                        rb_value = register_dict['R0']

                        # convert decimal immediate value to binary string and pad with zeros to 8 bits
                        assembly2_RA_binary = bin(int(assembly2_RA))[2:].zfill(16)
                
                        #concatenate
                        machine_code.append(opcode + ra_value + rb_value + " " + assembly2_RA_binary )  

                      else:
                        #concatenate  
                        rb_value = register_dict['R0']
                        assembly2_RA_binary = bin(int(assembly2_RA))[2:].zfill(16)
                        machine_code.append(opcode + rb_value + " " + assembly2_RA_binary )
                       
                      break

                #  This covers JMP RB+5 --- JSR RB+5  - 2 cases

                elif assembly2_name == opcode2_name and "[" not in opcode2_RA and "[" not in assembly2_RA and "+"  in opcode2_RA and "+"  in assembly2_RA:

                    # split assembly2_RA into R0 and ignore the +5 to get access to the register

                    assembly2_RA_REG = [0, 0]
                    assembly2_RA_REG[1] = assembly2_RA.split('+')[0]

                    # map RA and RB registers to 4-bit values using register_dict
                    ra_value = register_dict['R0']
                    rb_value = register_dict[assembly2_RA_REG[1]]

                    machine_code.append(opcode + ra_value +rb_value) 
                    break

                #  This covers Push #5 - 1 cases

                elif assembly2_name == opcode2_name and "#" in opcode2_RA and "#" in assembly2_RA:

                    # split assembly2_RA into # and 5 to get access to the decimal value 5

                    assembly2_RA_REG = [0, 0]
                    assembly2_RA_REG[1] = assembly2_RA.split('#')[1]
                
                    # map RA and RB registers to 4-bit values using register_dict
                    ra_value = register_dict['R0']
                    rb_value = register_dict['R0']

                    # convert decimal immediate value to binary string and pad with zeros to 8 bits
                    assembly2_RA_binary = bin(int(assembly2_RA_REG[1]))[2:].zfill(16)
                
                    #concatenate
                    machine_code.append(opcode + ra_value + rb_value + " " + assembly2_RA_binary )  
             
                    break



                        #  This covers INC (200) and DEC (200) -  2 cases

                elif assembly2_name == opcode2_name and "(" in opcode2_RA and "(" in assembly2_RA:                                                           

                    # map RA and RB registers to 4-bit values using register_dict
                    ra_value = register_dict['R0']
                    rb_value = register_dict['R0']
                                 
                    #concatenate
                    machine_code.append(opcode + ra_value + rb_value )                    
                   
                    break       

                #  This covers 15 JUMPIF instructions (JC [R0] --- JA [R0]...) -- JMP [R0] --- JSR [R0] --- PUSH [R0] --- POP [R0] - 19 cases

                elif assembly2_name == opcode2_name and "[" in opcode2_RA and "[" in assembly2_RA and "+" not in opcode2_RA and "+" not in assembly2_RA:
                     
                       # need to split this into 2 sepetate statements , one for JUMPIF and the other for the rest
                      if  assembly2_name in ["JMP" ,"JSR", "PUSH", "POP"]:

                        assembly2_RA_REG = [0, 0]
                        assembly2_RA_REG[1] = assembly2_RA[1:-1]   

                        # map RA and RB registers to 4-bit values using register_dict
                        ra_value = register_dict['R0']
                        rb_value = register_dict[assembly2_RA_REG[1]]
                                 
                        #concatenate
                        machine_code.append(opcode + ra_value + rb_value )  

                      else:
                        #concatenate
                        assembly2_RA_REG = [0, 0]
                        assembly2_RA_REG[1] = assembly2_RA[1:-1]
                        rb_value = register_dict[assembly2_RA_REG[1]]
                        machine_code.append(opcode + rb_value)
                      break          

                        #  This covers 15 JUMPIF instructions (JC [R0]+ --- JA [R0]+...) --- PUSH [R0]+ --- POP [R0]+ - 17 cases

                elif assembly2_name == opcode2_name and "[" in opcode2_RA and "[" in assembly2_RA and "+"  in opcode2_RA and "+"  in assembly2_RA:                  
        
                       # need to split this into 2 sepetate statements , one for JUMPIF and the other for the rest
                      if  assembly2_name in ["JMP" ,"JSR", "PUSH", "POP"]:

                        assembly2_RA_REG = [0, 0]
                        assembly2_RA_REG[1] = assembly2_RA[1:-2]
                        

                        # map RA and RB registers to 4-bit values using register_dict
                        ra_value = register_dict['R0']
                        rb_value = register_dict[assembly2_RA_REG[1]]
                                 
                        #concatenate
                        machine_code.append(opcode + ra_value + rb_value )  

                      else:
                        #concatenate
                        assembly2_RA_REG = [0, 0]
                        assembly2_RA_REG[1] = assembly2_RA[1:-2]
                        rb_value = register_dict[assembly2_RA_REG[1]]
                        machine_code.append(opcode + rb_value)
                        break          

                #  This covers --- 15 JUMPIF instructions JC R0 , JA R0...) --- PUSH R0 , POP R0 . INC R0 , DEC R0 , CLR R0 --- JMP R0 --- JSR R0 - 20 cases
            
                elif assembly2_name == opcode2_name and opcode2_RA.isalnum() and  assembly2_RA.isalnum() and not opcode2_RA.isdigit() and not assembly2_RA.isdigit() :

                         # need to split this into 2 sepetate statements , one for JUMPIF and the other for the rest
                      if  assembly2_name in ["JMP" ,"JSR", "PUSH", "POP","INC" , "DEC" , "CLR"]:
                        # map RA and RB registers to 4-bit values using register_dict
                        ra_value = register_dict['R0']
                        rb_value = register_dict[assembly2_RA]
                                 
                        #concatenate
                        machine_code.append(opcode + ra_value + rb_value )  

                      else:
                        #concatenate
                        rb_value = register_dict[assembly2_RA]
                        machine_code.append(opcode + rb_value)
                      break   



       
                # THIS COVERS 79 CASES ALL TESTED AND WORKING

                 #               --------------------------------------------------------------------------------------------------------------------------------

                 # Group of 1


                   # parts1 = line.split() 
    if len(parts4) == 1:
        parts1=parts4          
        assembly1_name = parts1[0]                                  # "LOAD"
           
        for opcode_line, opcode in opcode_dict.items():
            # parse the opcode line

            opcode1_parts = opcode_line.split()
              
            if len(opcode1_parts) != 1:
                
                continue  # skip to next iteration of the loop

            #  we can get access to all the parts of the assembly language and the opcode dictionary for comparison

            opcode1_name = opcode1_parts[0]                         # "ADD"
                
            # This covers CLF --- END --- RET , 3 cases

            if assembly1_name == opcode1_name:
                machine_code.append(opcode)
                break


#---------------------------------------------------------------------------------------------------------------------------------------

# 4 PARTS - 14 CSES
# 3 PARTS - 37 CASES
# 2 PARTS - 79 CASES
# 1 PART  - 2 CASES

# TOTAL CASES = 132 CASES TESTED AND WORKING


#---------------------------------------------------------------------------------------------------------------------------------------

#Output file format

HEX_out = []

for binary_string in machine_code:
    binary_list = binary_string.split() # Split the string into individual 16-bit binary strings
    hex_list = []
    for binary in binary_list:
        hex_list.append(hex(int(binary, 2))[2:].zfill(4)) # Convert each binary string to hex and append to the hex_list
    HEX_out.append(" ".join(hex_list))


HEX_output=[]
for line in HEX_out:
    # Split each line at the space character
    hex_numbers = line.split(' ')
    # Append the hex numbers to the output list
    HEX_output.extend(hex_numbers)
print(HEX_output)


# Create the subfolder "Machine_Code" if it doesn't already exist
subfolder = "Machine_Code"
if not os.path.exists(subfolder):
    os.mkdir(subfolder)

# Write the HEX_output list to a file called "MC_H.txt" in the subfolder
filepath = os.path.join(subfolder, "MC_H.txt")
with open(filepath, "w") as f:
    for hex_num in HEX_output:
        f.write(hex_num + "\n")












