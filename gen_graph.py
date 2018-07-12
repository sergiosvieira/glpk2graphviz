#!/usr/bin/python
#coding= utf-8

import sys
import pdb

def file_error():
    print("Error: please type input file name")

def is_row(line):
    return 'Rows:' in line

def is_col(line):
    return 'Columns:' in line

def extract_var_name_value(array):
    return array[1], array[3]

def is_close(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def create_dot_string(var, value):
    #pdb.set_trace()
    array = var.split('_')
    if len(array) == 1:
        #return '\t{}->{} [label="{}"]\n'.format(array[0], array[0], value)
        return ''
    elif len(array) == 2:
        if array[1] == "volGoal":
            return '\t{}->{} [label="{}"]\n'.format(array[0], array[0], value)
        elif array[1] == "s":
            return ''
        else:
            output = ""
            style = ""
            if 'j' in array[0]:
                output = '{} [shape="circle"]'.format(array[0])
            if 'd' in array[1]:
                output += ' {} [shape="diamond"]'.format(array[1])
            if is_close(float(value), 0.0): 
                style = ' color="gray"' 
            return '\t{}->{} [label="{}"{}] {}\n'.format(array[0], array[1], value, style, output)
    elif len(array) == 3:
        output = ""
        if 'r' in array[0]:
            output = '{} [shape="invtrapezium"]'.format(array[0])
        if 'd' in array[2]:
            output += ' {} [shape="diamond"]'.format(array[2])
        return '\t{}->{} [label="{}"] {}\n'.format(array[0], array[2], value, output)

def process(filename):
    with open(filename) as file:
        num_line = 1
        rows = 0
        cols = 0
        output_string = ""
        begin = 0
        end = 0
        aux_var = ""
        aux_val = 0.0
        for line in file:
            if is_row(line):
                rows = int(line.strip().split(':')[1])
                #pdb.set_trace()
                begin = 9 + rows + 4
            elif is_col(line):
                cols = int(line.strip().split(':')[1])
                #pdb.set_trace()
                end = begin + cols
            elif end > begin and num_line >= begin and num_line < end:
                array = ' '.join(line.split()).split()
                if len(array) < 4:
                    if len(aux_var) == 0:
                        aux_var = array[1]
                    else:
                        aux_val = array[1]
                        output_string += create_dot_string(aux_var, aux_val)
                        aux_var = ""
                        aux_val = 0.0
                        num_line += 1
                    continue
                var, val = extract_var_name_value(array)
                output_string += create_dot_string(var, val)
            num_line = num_line + 1
    return output_string

if __name__ == '__main__':
    if len(sys.argv) != 2:
        file_error()
    else:
        output = process(sys.argv[1]) 
        print('digraph G {rankdir="LR";\n%s}' % (output))
