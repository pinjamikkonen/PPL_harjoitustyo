# COMP.CS.400 Principles of Programming Languages Course Project

## Project overview

This is the final project of the Principles of Programming Languages -course, made by Pinja Mikkonen. 
In this project we created a code compiler for fictional 'sheetscript'-programming language. The code compiler includes full lexical 
and syntax analysis, building a syntax tree, and the end result can perform some semantic checks and run simple programs.

This project is written in Python and uses PLY.

The project was created in four separate phases, but the final version of the project that also includes phases 1-3 
can be found in folder 04_semantics_and_running. Folder 04_semantics_and_running also has a subfolder 'Input', where test
files written in 'sheetscript' can be found. The code compiler can run these files and detect errors in them.

Some files in phase 4 folder (semantics_common and tree_print) were provided by teacher as tools for students.

## Implemented features

Lexical analyser, syntax analyser and syntax tree (Phases 1-3) have full functionality.

The semantic analyser performs the following checks:
- Variable names need to be initialized before being called
- Two variables cannot share a name
- Sheet rows must be the same length
- Ranges must refer to either a vertical or a horizontal range, ie. either the row or colum indicators must match
- Subroutines and functions can be initialized and called
- Subroutines cannot be called as functions and vice versa
- Subroutine and function calls must contain the correct number of arguments

Running the program includes the following functionalities:
- Simple arithmetics
- Changing variable values
- Print-statements
- If- and while-loops

## Running the program

Install Python and PLY in order to run the program. Program phase 4 can be run with command Python main.py -f [FILENAME].
Possible input files can be found in 'Input' -folder.

PLY: https://www.dabeaz.com/ply/
