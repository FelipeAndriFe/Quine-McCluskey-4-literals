# QUINE MCCLUSKEY 4 LITERALS

## Author: Felipe Andriotti Ferreira

To use the program, put the equations you want to minimize in the "equations.txt" file, then execute it.

The "equations.txt" file already has 3 examples, to which the minimized output is:
!A!B!C + !ABC + !A!CD / 9 literais
ABD + !BC!D + A!C + !AB!D / 11 literais
!AD + A!C / 4 literais

The order of the final terms is random because the program stores them in a set.

The program uses the Petrick Method to solve the remaining coverage table after the essencial prime implicants are removed.

