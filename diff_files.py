# /usr/bin/python
# -*- coding: utf_8 -*-
#
# diff_files.py
#
# Compares files and generate output files.
#
# D.C.-G. 2014
#
import sys
import os

helpText = """Runs on Linux only.
Must have two commandline parameters at least.

Usage:

[python] diff_files[.py] [--extensions(-e)=<list_of_extensions>] [--recursive(-r)] [--output(-o)=<folder>] file_or_folder_1 file_or_folder_2

--extensions(-e)=<list_of_extensions>   Comma separated list of file extensions to compare when comparing folders content.
                                        If the short version is used, do not separate extensions with comma.
--recursive(-r)                         Make the comparison recursive when comparing folders content
--output(-o)=<folder>                   Write the output files in this folder. If not specified, the output is written on stdout.
"""

if not sys.platform == "linux2":
    print helpText
    sys.exit()

def parseCmdLine(args):
    """Gets the commanline options and parameters."""
    exts = []
    recursive = False
    outputFolder = None
    src1 = None
    src2 = None
    param = None
    for i in range(len(args)):
        arg = args.pop(0)
#        print arg
        if arg == "-e":
            param = exts
        elif arg in ("-r", "--recursive"):
            recursive = True
            param = None
        elif arg == "-o":
            param = outputFolder
        elif param == outputFolder:
            outputFolder = arg
        elif arg.startswith("--extensions="):
            exts += list(arg.split("=")[1].split(","))
        elif param == exts:
            exts.append(arg)
            param = exts
        elif arg.startswith("--output="):
            outputFolder = arg.split("=")[1]
            param = None
        elif not param:
            if not src1:
                src1 = arg
            elif not src2:
                src2 = arg
    return exts, recursive, outputFolder, src1, src2

exts, recursive, outputFolder, src1, src2 = parseCmdLine(sys.argv[1:])

print "exts         ", exts
print "recursive    ", recursive
print "outputFolder ", outputFolder
print "src1         ", src1
print "src2         ", src2

#sysCommand = "diff -y %s %s >%s"

def compareFiles(file1, file2, output=None):
    """Compares two files. If output specified, writes the resutl to the file."""
    print "*** Comparing (F)", file1
    print "              and", file2
    if output:
#        os.system("diff -y -LTYPE-line-format=\"%%F %%L %%N %%<%%>\" %s %s > %s"%(file1, file2, output))
        os.system("diff -y -LTYPE-line-format=\"%F | %L | %N | %<%>\" " + "%s %s > %s"%(file1, file2, output))
    else:
        os.system("diff -y -n %s %s"%(file1, file2))

def compareFolders(folder1, folder2, exts=exts, output=None):
    """Compares two folders non recursively. If output specified, uses this folder to write results.
    Returns the list of folders found in folred1."""
    print "*** Comparing (D)", folder1
    print "              and", folder2
    folders = []
    for fName in os.listdir(folder1):
        if fName in os.listdir(folder2):
            if os.path.isfile(os.path.join(folder1, fName)):
                outName = None
                if output:
                    outName = os.path.join(output, os.path.basename(fName) + ".diff")
                if not exts or os.path.splitext(fName)[1][1:] in exts:
                    compareFiles(os.path.join(folder1, fName), os.path.join(folder2, fName), output=outName)
            else:
                folders.append(os.path.join(folder1, fName))
    return folders

def compare(in1, in2, exts=exts, recursive=recursive, output=None):
    """Compares files or folders."""
    if os.path.isfile(in1) and os.path.isfile(in2):
        compareFiles(in1, in2, output=output)
    elif os.path.isdir(in1) and os.path.isdir(in2):
        folders = compareFolders(in1, in2, exts=exts, output=output)
        if recursive:
            while folders:
                folder = folders.pop(0).replace(in1 +"/", "")
                if output:
                    os.mkdir(os.path.join(output, folder))
#                folders += compareFolders(os.path.join(in1, folder), os.path.join(in2, folder), exts=exts, output=output)
                folders += compareFolders(os.path.join(in1, folder), os.path.join(in2, folder), exts=exts, output=os.path.join(output, folder))
    else:
        print "Can not compare %s and %s."%(in1, in2)

compare(src1, src2, exts, recursive, outputFolder)


