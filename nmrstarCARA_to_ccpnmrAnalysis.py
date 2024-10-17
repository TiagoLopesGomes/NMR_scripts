# Converts bmrb nmrstar file from cara lua script to be read by ccpnmr analysis
#Adds _Atom_chem_shift.Atom_isotope_number string and a header that works. also adds the corresponding isotope number after atom_type column
#Before residue name only two columns. The atom number and sequence number. Delete extra columns.

#execute as python nmrstarCARA_to_ccpnmrAnalysis.py input.str output.str

#Tiago Lopes Gomes May/2023

import sys

header='''data_50758

save_assigned_chemical_shifts_1
    _Assigned_chem_shift_list.Sf_category                  assigned_chemical_shifts 
    _Assigned_chem_shift_list.Sf_framecode                 assigned_chemical_shifts_1 
    _Assigned_chem_shift_list.Entry_ID                     50758 


    loop_
        _Atom_chem_shift.ID
        _Atom_chem_shift.Seq_ID
        _Atom_chem_shift.Comp_ID
        _Atom_chem_shift.Atom_ID
        _Atom_chem_shift.Atom_type
        _Atom_chem_shift.Atom_isotope_number
        _Atom_chem_shift.Val
        _Atom_chem_shift.Val_err
        _Atom_chem_shift.Assigned_chem_shift_list_ID
'''
try:
    with open(sys.argv[1], "r") as file:
        lines = file.readlines()

    while lines and '_Chem_shift_ambiguity_code' not in lines[0]:
        lines.pop(0)

    if lines and '_Chem_shift_ambiguity_code' in lines[0]:
        lines.pop(0)



    # Function to add column
    def add_column(line):
        parts = line.split()
        #print(parts)
        if len(parts) >= 7:
            if parts[4] in ["C"]:
                parts.insert(5, "13")
            elif parts[4] == "H":
                parts.insert(5, "1")
            elif parts[4] == "N":
                parts.insert(5, "15")
            return "          " + " ".join(parts) + "\n"
        else:
            return line

    # Apply function to lines
    new_lines = [add_column(line) for line in lines]
    #removes stop_ because it stays...add it at the end agian
    new_lines = new_lines[:-1] 

    # Write new brmb file
    with open(sys.argv[2], "w") as file:
        file.write(header+"\n")
        for line in new_lines:
            file.write(line)
        file.write("    stop_"+"\n"+"\n")
        file.write("save_")
        print("-------")
        print("Apparently no errors found. Check your file : "+ sys.argv[2])
        print("-------")

except Exception as e:
    print("An error occurred: ", e)