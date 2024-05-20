# AuxiliaryCodes
Auxiliary codes for calculations


###############################################################
# This section of the README file is associated to the program "ConvertirFuenteMCNP.py".


WHAT IS:
This program converts a surface source file generated in MCNP 5 1.60 (or older) to the new "SF_00001" format.
Up to version 6.1 of MCNP the format of the surface source file was not publicly documented. In 2016 the technical report LA-UR-16-20109 was released, documenting for the first time the surface  source file format, introducing some changes to previous format versions. The format was given the code "SF_00001" and is used in MCNP version 6.2 and higher, although it might be further modified in the future.


DISCLAIMER:
This little piece of software was developed by Héctor Lestani (hectorlestani@cnea.gob.ar) while working as a researcher for CNEA, the Atomic Energy Commission of Argentina (https://www.argentina.gob.ar/cnea). It is not intended to replace any resource provided by the team at Los Alamos National Lab (https://www.lanl.gov/) responsible for MCNP development (https://mcnp.lanl.gov/). It is shared under GNU General Public License v3.0.

This program was succesfully tested to convert dozens of surface source files generated in MCNP 5 (1.60), containing only neutrons, to the new "SF_00001" format. The results were compared against results obtained with surface source files generated directly in MCNP 6.2, and the tallies obtained were 100 % accurate (exact same numbers using the same random number seed). Nevertheless more testing is needed in order to assure accuracy in other cases (containing other particles than neutron).

USE:
The program can be executed with no arguments and the following self-explanatory text is printed:
""""
At least 2 arguments must be given.
1) Argument indicating the version of the surface source file to read:
      '1' if version >= 6.2
      '0' if version <=6.1
2) Name of the surface source file to read.
3) Verbosity:
      '1' prints source information on screen
      '0' silent screen (default)
4) New source generation:
      '1' generate new source file in format 'SF_00001'
      '0' do not convert the source file
5) Name of the new surface source file to be generated
6) Additional information for debugging:
      '1' print additional information
      '0' do not print (default)
      This option is useful for debugging purpuses.
      To select what information to print, follow the 'ValoresParticulas.write' instructions
      under the 'if ImprimirValores == 1:' statements.
7) Name of the file where the additional information will be written
""""

REQUIREMENTS:
For the program to run "Python 3.8" must be installed. Other versions of Python should be easily used, but no tests have been made so far.
The Python modules "sys", "struct" and "re" must be installed.
# End of the section of the README file associated to the program "ConvertirFuenteMCNP.py".
###############################################################


