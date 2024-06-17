from pymol import cmd
from pymol.Qt import *
import csv
import os

@cmd.extend
def atom_distance(file_path=None):
    """
    DESCRIPTION:
    
    Compute the distance between specific atoms of two molecules.

    Args:
    file_path: path to a csv file with columns: 
        pdbfile path, chain of mol A, residue name of mol A, residue number of mol A, atom identifier of mol A,
        chain of mol B, residue name of mol B, residue number of mol B, atom identifier of mol B 

    
    """

    if file_path is None:
        fname, _ = QtWidgets.QFileDialog.getOpenFileName()
        if not fname:
            raise Exception("No input file selected")
        print(f"input file: {fname} was provided")
        return
    
    cols = ["pdb_file", "a_chain", "a_resn",  "a_resi", "a_atom" , "b_chain", "b_resn", "b_resi", "b_atom"]
    with open(file_path) as fh:
        reader = csv.DictReader(fh, fieldnames=cols)
        for c, line in enumerate(reader):
            name = line["pdb_file"].split("/")[-1]
            name = name.replace(".pdb", "")
            if not os.path.exists(line["pdb_file"]):
                raise Exception(f"File: {line['pdb_file']} | Line: {c} - first field is not an existent file ")
            
            if not line["pdb_file"].endswith(".pdb"):
                raise Exception(f"File: {line['pdb_file']} | Line: {c} - first field is not a pdb file, please change file to end with `.pdb`")
            cmd.load(line["pdb_file"])


            a_mol = "/" +  name +  "//" + line["a_chain"] + "/" + line["a_resn"] + "`" + line["a_resi"] + "/" 
            b_mol = "/" +  name +  "//" + line["b_chain"] + "/" + line["b_resn"] + "`" + line["b_resi"] + "/"
            print(a_mol)
            print(b_mol)
            cmd.show("stick", a_mol)
            cmd.show("stick", b_mol)
            a_mol += line["a_atom"].strip()
            b_mol += line["b_atom"].strip()
            dist = cmd.distance("tmp",a_mol, b_mol)
            cmd.set("cartoon_transparency", 0.5)
            print(a_mol + "\t" + b_mol + "\t" + str(dist))

    