#! /usr/bin/python3.8 -u

# This program converts a surface source file generated in MCNP older than version 6.2
# to a surface source file that can be read by MCNP version 6.2 or newer, until
# version "SF_00001" is superseded.
# Please read the file "00_README_ConvertirFuenteMCNP.txt"


# para manejo de argumentos en linea de comandos
import sys 
# para codificar y decodificar binarios
import struct
# para manejar expresiones regulares
import re

# Checking the arguments passed
if len(sys.argv) < 3:
   print("\n\nAt least 2 arguments must be given.")
   print("1) Argument indicating the version of the surface source file to read:")
   print("      '1' if version >= 6.2")
   print("      '0' if version <=6.1")
   print("2) Name of the surface source file to read.")
   print("3) Verbosity:")
   print("      '1' prints source information on screen")
   print("      '0' silent screen (default)")
   print("4) New source generation:")
   print("      '1' generate new source file in format 'SF_00001'")
   print("      '0' do not convert the source file")
   print("5) Name of the new surface source file to be generated")
   print("6) Additional information for debugging:")
   print("      '1' print additional information")
   print("      '0' do not print (default)")
   print("      This option is useful for debugging purpuses.")
   print("      To select what information to print, follow the 'ValoresParticulas.write' instructions")
   print("      under the 'if ImprimirValores == 1:' statements.")
   print("7) Name of the file where the additional information will be written")
   print("\n\n")
   sys.exit(0)


# Corroborando el pasado de argumentos
#if len(sys.argv) < 3:
#   print("\n\nAtención, debe insertar al menos 2 argumentos")
#   print("1) '1' si versión >= 6.2, '0' si <=6.1")
#   print("2) Archivo de fuente rssa")
#   print("3) '1' para imprimir información de la fuente ('verbose'). Default=0.")
#   print("4) '1' para generar una nueva fuente en formato >=6.2. Default= no se genera.")
#   print("5) Nombre del archivo de fuente en formato >6.2 a escribir.")
#   print("6) '1' para imprimir en un archivo un parámetro seleccionado para todas las partículas. Default= no se genera.")
#   print("7) Nombre del archivo en el cual imprimir algún parámetro seleccionado de todas las partículas")
#   print("\n\n")
#   sys.exit(0)

NombreArchivoFuente=sys.argv[2]
RSSA = open(NombreArchivoFuente, mode="rb")


# Para imprimir información en pantalla
Impresion = []
if len(sys.argv)>3:
    Imprimir = int(sys.argv[3])
else:
    Imprimir = 0
    

# Para imprimir la fuente nueva
ImprimirNueva=0
if len(sys.argv)>4:
    ImprimirNueva=int(sys.argv[4])
    
ImpresionNueva = []
if len(sys.argv)>5:
    NombreFuenteNueva = sys.argv[5]


# Para imprimir ciertos valores de cada partícula
ImprimirValores=0
if len(sys.argv)>6:
    ImprimirValores=int(sys.argv[6])

if len(sys.argv)>7:
    ArchivoValoresParticulas = sys.argv[7]

# Para imprimir ciertos valores de cada partícula
if ImprimirValores ==1:
   ValoresParticulas = open(ArchivoValoresParticulas, mode="w")


    
# Para contar los bytes leidos
BytesLeidos=0

# Para contar los bytes impresos en fuente nueva
BytesImpresos=0

# MCNP versión 6.2 
if sys.argv[1] == "1" :
# Leyendo archivo de fuente
   Impresion += ("\n\n*** Formato de fuente ***",)
   Bytes = RSSA.read(4)
   BytesLeidos +=4
   ImpresionNueva += (Bytes,)
   BytesImpresos += 4
   #print("Linea 0",Bytes)
   Convertido=struct.unpack_from('@i',Bytes)
   Impresion += ("Chars = {:d}".format(Convertido[0]),)
   Bytes = RSSA.read(8)
   BytesLeidos +=8
   ImpresionNueva += (Bytes,)
   BytesImpresos += 8
   #print("Linea 1",Bytes)
   Convertido=struct.unpack_from('@8s',Bytes)
   Impresion += ("Formato = {}".format(Convertido[0].decode()),)
   Bytes = RSSA.read(4)
   BytesLeidos +=4
   ImpresionNueva += (Bytes,)
   BytesImpresos += 4
   Convertido=struct.unpack_from('@i',Bytes)
   Impresion += ("Chars = {:d}".format(Convertido[0]),)
   Impresion += ("{} bytes leídos hasta aquí".format(BytesLeidos),)

   Impresion += ("\n\n*** Primer record ***",)
   # Leyendo longitud del primer record
   Bytes = RSSA.read(4)
   BytesLeidos +=4
   ImpresionNueva += (Bytes,)
   BytesImpresos += 4
   Convertido=struct.unpack_from('@i',Bytes)
   Impresion += ("Chars = {:d}".format(Convertido[0]),)
   # Leyendo el primer record
   Bytes = RSSA.read(191)
   BytesLeidos +=191
   ImpresionNueva += (Bytes,)
   BytesImpresos += 191
   Convertido=struct.unpack_from('@8s',Bytes)
   Impresion += ("Kods = {}".format(Convertido[0].decode()),)
   Convertido=struct.unpack_from('@5s',Bytes,offset=8)
   Impresion += ("vers = {}".format(Convertido[0].decode()),)
   Convertido=struct.unpack_from('@8s',Bytes,offset=13)
   Impresion += ("lods = {}".format(Convertido[0].decode()),)
   Convertido=struct.unpack_from('@19s',Bytes,offset=21)
   Impresion += ("idtms = {}".format(Convertido[0].decode()),)
   Convertido=struct.unpack_from('@19s',Bytes,offset=40)
   Impresion += ("probs = {}".format(Convertido[0].decode()),)
   Convertido=struct.unpack_from('@80s',Bytes,offset=59)
   Impresion += ("aids = {}".format(Convertido[0].decode()),)
   Convertido=struct.unpack_from('@13i',Bytes,offset=139)
   Impresion += ("knods = {}".format(Convertido[0]),)
   
   Bytes = RSSA.read(4)
   BytesLeidos +=4
   ImpresionNueva += (Bytes,)
   BytesImpresos += 4
   Convertido=struct.unpack('@i',Bytes)
   Impresion += ("Chars = {:d}".format(Convertido[0]),)
   Impresion += ("{} bytes leídos hasta aquí".format(BytesLeidos),)
   
   Impresion += ("\n\n*** Segundo record ***",)
   Bytes = RSSA.read(4)
   BytesLeidos +=4   
   ImpresionNueva += (Bytes,)
   BytesImpresos += 4
   Convertido=struct.unpack('@i',Bytes)
   Impresion += ("Chars = {:d}".format(Convertido[0]),)
   Bytes = RSSA.read(32)
   BytesLeidos +=32
   ImpresionNueva += (Bytes,)
   BytesImpresos += 32
   Convertido=struct.unpack_from('@q',Bytes)
   Impresion += ("np1 = {:.2E} (Cantidad de partículas del problema original)".format(Convertido[0]*(-1)),)
   Convertido=struct.unpack_from('@q',Bytes,offset=8)
   Impresion += ("nrss = {} (Cantidad de partículas en la fuente grabada)".format(Convertido[0]),)
   Convertido=struct.unpack_from('@i',Bytes,offset=16)
   Impresion += ("nrcd = {}".format(Convertido[0]),)
   Convertido=struct.unpack_from('@i',Bytes,offset=20)
   Impresion += ("njsw = {} (Cantidad de superficies (jasw(:)))".format(Convertido[0]),)
   Convertido=struct.unpack_from('@q',Bytes,offset=24)
   Impresion += ("niss = {} (Cantidad de historias que generan nrss)".format(Convertido[0]),)
   Bytes = RSSA.read(4)
   BytesLeidos +=4
   ImpresionNueva += (Bytes,)
   BytesImpresos += 4
   Convertido=struct.unpack('@i',Bytes)
   Impresion += ("Chars = {:d}".format(Convertido[0]),)
   Impresion += ("{} bytes leídos hasta aquí".format(BytesLeidos),)


   Impresion += ("\n\n*** Tercer record ***",)
   Bytes = RSSA.read(4)
   BytesLeidos +=4
   ImpresionNueva += (Bytes,)
   BytesImpresos += 4
   Convertido=struct.unpack('@i',Bytes)
   Impresion += ("Chars = {:d}".format(Convertido[0]),)
   Bytes = RSSA.read(80)
   BytesLeidos +=80   
   ImpresionNueva += (Bytes,)
   BytesImpresos += 80
   Convertido=struct.unpack_from('@i',Bytes)
   Impresion += ("niwr = {}".format(Convertido[0]),)
   Convertido=struct.unpack_from('@i',Bytes,offset=4)
   Impresion += ("mipts = {} ('1' para neutrones)".format(Convertido[0]),)
   Convertido=struct.unpack_from('@i',Bytes,offset=8)
   Impresion += ("kjaq = {}".format(Convertido[0]),)
   Bytes = RSSA.read(4)
   BytesLeidos +=4
   ImpresionNueva += (Bytes,)
   BytesImpresos += 4
   Convertido=struct.unpack('@i',Bytes)
   Impresion += ("Chars = {:d}".format(Convertido[0]),)
   Impresion += ("{} bytes leídos hasta aquí".format(BytesLeidos),)

   Impresion += ("\n\n*** Cuarto record ***",)
   Bytes = RSSA.read(4)
   BytesLeidos +=4
   ImpresionNueva += (Bytes,)
   BytesImpresos += 4
   Convertido=struct.unpack('@i',Bytes)
   Impresion += ("Chars = {:d}".format(Convertido[0]),)
   Bytes = RSSA.read(44)
   BytesLeidos +=44   
   ImpresionNueva += (Bytes,)
   BytesImpresos += 44
   Convertido=struct.unpack_from('@i',Bytes)
   Impresion += ("njss = {}".format(Convertido[0]),)
   Convertido=struct.unpack_from('@i',Bytes,offset=4)
   Impresion += ("jss = {}".format(Convertido[0]),)
   Convertido=struct.unpack_from('@i',Bytes,offset=8)
   Impresion += ("jx = {}".format(Convertido[0]),)
   Convertido=struct.unpack_from('@i',Bytes,offset=12)
   Impresion += ("kst = {}".format(Convertido[0]),)
   Convertido=struct.unpack_from('@i',Bytes,offset=16)
   Impresion += ("n = {}".format(Convertido[0]),)
   Convertido=struct.unpack_from('@i',Bytes,offset=20)
   Impresion += ("lsc = {}".format(Convertido[0]),)
   Convertido=struct.unpack_from('@10e',Bytes,offset=24)
   Impresion += ("scf = {}".format(Convertido),)
   Bytes = RSSA.read(4)
   BytesLeidos +=4
   ImpresionNueva += (Bytes,)
   BytesImpresos += 4
   Convertido=struct.unpack('@i',Bytes)
   Impresion += ("Chars = {:d}".format(Convertido[0]),)
   Impresion += ("{} bytes leídos hasta aquí".format(BytesLeidos),)


   Impresion += ("\n\n*** Summary record ***",)
   Bytes = RSSA.read(4)
   BytesLeidos +=4
   ImpresionNueva += (Bytes,)
   BytesImpresos += 4
   Convertido=struct.unpack('@i',Bytes)
   Impresion += ("Chars = {:d}".format(Convertido[0]),)
   Bytes = RSSA.read(608)
   BytesLeidos +=608
   ImpresionNueva += (Bytes,)
   BytesImpresos += 608
   Convertido=struct.unpack_from('@i',Bytes)
   Impresion += ("njss = {}".format(Convertido[0]),)
   Convertido=struct.unpack_from('@i',Bytes,offset=4)
   Impresion += ("nilw = {} (number of cells)".format(Convertido[0]),)
   Convertido=struct.unpack_from('@i',Bytes,offset=8)
   Impresion += ("nilw = {} (source particle type ('1' para neutrones))".format(Convertido[0]),)
   Convertido=struct.unpack_from('@2i',Bytes,offset=12)
   Impresion += ("nsl (total tracks, independent stories) = {}".format(Convertido),)
   Bytes = RSSA.read(4)
   BytesLeidos +=4
   ImpresionNueva += (Bytes,)
   BytesImpresos += 4
   Convertido=struct.unpack('@i',Bytes)
   Impresion += ("Chars = {:d}".format(Convertido[0]),)
   Impresion += ("\nBytes leídos en el encabezado: {}".format(BytesLeidos),)
   
   ParticulaAImprimir=0
   for i in range(10):
      if i == ParticulaAImprimir:
          Impresion += ("\n\n*** {}th particle record ***".format(i+1),)
      Bytes = RSSA.read(4)
      BytesLeidos +=4
      if ImprimirNueva == 1:
          ImpresionNueva += (Bytes,)
          BytesImpresos += 4
      Convertido=struct.unpack('@i',Bytes)
      if i == ParticulaAImprimir:
          Impresion += ("Chars = {:d}. Bytes {} a {}.".format(Convertido[0],BytesLeidos-3,BytesLeidos),)
      Bytes = RSSA.read(88)
      BytesLeidos +=88
      if ImprimirNueva == 1:
          ImpresionNueva += (Bytes,)
          BytesImpresos += 88
      Convertido=struct.unpack_from('@d',Bytes)
      if i == ParticulaAImprimir:
          Impresion += ("a = {}. Bytes {} a {}.".format(Convertido[0],BytesLeidos-87,BytesLeidos-80),)
      Convertido=struct.unpack_from('@d',Bytes,offset=8)
      if ImprimirValores ==1:
          ValoresParticulas.write("{}\n".format(Convertido[0]))
      if i == ParticulaAImprimir:
          Impresion += ("b = {}. Bytes {} a {}.".format(Convertido[0],BytesLeidos-79,BytesLeidos-72),)
      Convertido=struct.unpack_from('@d',Bytes,offset=16)
      if i == ParticulaAImprimir:
          Impresion += ("wgt = {}. Bytes {} a {}.".format(Convertido[0],BytesLeidos-71,BytesLeidos-64),)
      Convertido=struct.unpack_from('@d',Bytes,offset=24)
      if i == ParticulaAImprimir:
          Impresion += ("erg = {}. Bytes {} a {}.".format(Convertido[0],BytesLeidos-63,BytesLeidos-56),)
      Convertido=struct.unpack_from('@d',Bytes,offset=32)
      if i == ParticulaAImprimir:
          Impresion += ("tme = {}. Bytes {} a {}.".format(Convertido[0],BytesLeidos-55,BytesLeidos-48),)
      Convertido=struct.unpack_from('@d',Bytes,offset=40)
      if i == ParticulaAImprimir:
          Impresion += ("x = {}. Bytes {} a {}.".format(Convertido[0],BytesLeidos-47,BytesLeidos-40),)
      Convertido=struct.unpack_from('@d',Bytes,offset=48)
      if i == ParticulaAImprimir:
          Impresion += ("y = {}. Bytes {} a {}.".format(Convertido[0],BytesLeidos-39,BytesLeidos-32),)
      Convertido=struct.unpack_from('@d',Bytes,offset=56)
      if i == ParticulaAImprimir:
          Impresion += ("z = {}. Bytes {} a {}.".format(Convertido[0],BytesLeidos-31,BytesLeidos-24),)
      Convertido=struct.unpack_from('@d',Bytes,offset=64)
      if i == ParticulaAImprimir:
          Impresion += ("u = {}. Bytes {} a {}.".format(Convertido[0],BytesLeidos-23,BytesLeidos-16),)
      Convertido=struct.unpack_from('@d',Bytes,offset=72)
      if i == ParticulaAImprimir:
          Impresion += ("v = {}. Bytes {} a {}.".format(Convertido[0],BytesLeidos-15,BytesLeidos-8),)
      Convertido=struct.unpack_from('@d',Bytes,offset=80)
      if i == ParticulaAImprimir:
          Impresion += ("c = {}. Bytes {} a {}.".format(Convertido[0],BytesLeidos-7,BytesLeidos-0),)
      Bytes = RSSA.read(4)
      BytesLeidos +=4
      if ImprimirNueva == 1:
          ImpresionNueva += (Bytes,)
          BytesImpresos += 4
      Convertido=struct.unpack('@i',Bytes)
      if i == ParticulaAImprimir:
          Impresion += ("Chars = {:d}. Bytes {} a {}.".format(Convertido[0],BytesLeidos-3,BytesLeidos),)
          Impresion += ("{} bytes leídos hasta aquí".format(BytesLeidos),)
   


# MCNP versión 6.1 o menor
if sys.argv[1] == "0" :
# Leyendo archivo de fuente
   Impresion += ("\n\n*** Primer record ***",)
   # Leyendo longitud del primer record
   Bytes = RSSA.read(4)
   BytesLeidos +=4
   # Cambio el contenido, pongo 191 (formato >=6.2) en lugar de 143 (formato <6.2)
   ImpresionNueva += (struct.pack('@i',191),)
   BytesImpresos += 4
   Convertido=struct.unpack_from('@i',Bytes)
   Impresion += ("Chars = {:d}".format(Convertido[0]),)
   # Leyendo el primer record
   Bytes = RSSA.read(143)
   BytesLeidos +=143
   ImpresionNueva += (Bytes[0:143],)
   BytesImpresos +=143

   Convertido=struct.unpack_from('@8s',Bytes)
   Impresion += ("Kods = {}".format(Convertido[0].decode()),)
   Convertido=struct.unpack_from('@5s',Bytes,offset=8)
   Impresion += ("vers = {}".format(Convertido[0].decode()),)
   Convertido=struct.unpack_from('@8s',Bytes,offset=13)
   Impresion += ("lods = {}".format(Convertido[0].decode()),)
   Convertido=struct.unpack_from('@19s',Bytes,offset=21)
   Impresion += ("idtms = {}".format(Convertido[0].decode()),)
   Convertido=struct.unpack_from('@19s',Bytes,offset=40)
   Impresion += ("probs = {}".format(Convertido[0].decode()),)
   Convertido=struct.unpack_from('@80s',Bytes,offset=59)
   Impresion += ("aids = {}".format(Convertido[0].decode()),)
   Convertido=struct.unpack_from('@i',Bytes,offset=139)
   Impresion += ("knods = {}".format(Convertido[0]),)
   # Agrego a la fuente nueva 48 bytes nuevos (191 - 143)
   ImpresionNueva += (struct.pack('@48s', b'                                            \x16\x03\x00\x00'),)
   BytesImpresos += 48
   
   Bytes = RSSA.read(4)
   BytesLeidos +=4
   # Cambio el contenido, pongo 191 (formato >=6.2) en lugar de 143 (formato <6.2)
   ImpresionNueva += (struct.pack('@i',191),)
   BytesImpresos += 4
   Convertido=struct.unpack('@i',Bytes)
   Impresion += ("Chars = {:d}".format(Convertido[0]),)
   Impresion += ("{} bytes leídos hasta aquí".format(BytesLeidos),)
   
   Impresion += ("\n\n*** Segundo record ***",)
   Bytes = RSSA.read(4)
   BytesLeidos +=4
   ImpresionNueva += (Bytes,)
   BytesImpresos += 4
   Convertido=struct.unpack('@i',Bytes)
   Impresion += ("Chars = {:d}".format(Convertido[0]),)
   Bytes = RSSA.read(32)
   BytesLeidos +=32
   # Cambio el valor de nrcd a '-11'
   ImpresionNueva += (Bytes[0:16],)
   BytesImpresos += 16
   # Este valor, nrcd, DEBE ser negativo, según LA-UR-16-20109
   ImpresionNueva += (struct.pack('@i',-11),)
   BytesImpresos += 4
   ImpresionNueva += (Bytes[20:32],)
   BytesImpresos += 12
   Convertido=struct.unpack_from('@q',Bytes)
   Impresion += ("np1 = {:.2E} (Cantidad de partículas del problema original)".format(Convertido[0]*(-1)),)
   Convertido=struct.unpack_from('@q',Bytes,offset=8)
   Impresion += ("nrss = {} (Cantidad de partículas en la fuente grabada)".format(Convertido[0]),)
   Convertido=struct.unpack_from('@i',Bytes,offset=16)
   Impresion += ("nrcd = {}".format(Convertido[0]),)
   Convertido=struct.unpack_from('@i',Bytes,offset=20)
   Impresion += ("njsw = {} (Cantidad de superficies (jasw(:)))".format(Convertido[0]),)
   Convertido=struct.unpack_from('@q',Bytes,offset=24)
   Impresion += ("niss = {} (Cantidad de historias que generan nrss)".format(Convertido[0]),)
   Bytes = RSSA.read(4)
   BytesLeidos +=4
   ImpresionNueva += (Bytes,)
   BytesImpresos += 4
   Convertido=struct.unpack('@i',Bytes)
   Impresion += ("Chars = {:d}".format(Convertido[0]),)
   Impresion += ("{} bytes leídos hasta aquí".format(BytesLeidos),)

   Impresion += ("\n\n*** Tercer record ***",)
   Bytes = RSSA.read(4)
   BytesLeidos +=4
   ImpresionNueva += (Bytes,)
   BytesImpresos += 4
   Convertido=struct.unpack('@i',Bytes)
   Impresion += ("Chars = {:d}".format(Convertido[0]),)
   Bytes = RSSA.read(80)
   BytesLeidos +=80
   ImpresionNueva += (Bytes[0:12],)
   BytesImpresos += 12
   # Copio lo que tiene la fuente formato >6.2 en los 68 bits restantes
   # 68 Null characters
   ImpresionNueva += (struct.pack('@68s', b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),)
   BytesImpresos += 68
   Convertido=struct.unpack_from('@i',Bytes)
   Impresion += ("niwr = {}".format(Convertido[0]),)
   Convertido=struct.unpack_from('@i',Bytes,offset=4)
   Impresion += ("mipts = {} ('1' para neutrones)".format(Convertido[0]),)
   Convertido=struct.unpack_from('@i',Bytes,offset=8)
   Impresion += ("kjaq = {}".format(Convertido[0]),)
   Bytes = RSSA.read(4)
   BytesLeidos +=4
   ImpresionNueva += (Bytes,)
   BytesImpresos += 4
   Convertido=struct.unpack('@i',Bytes)
   Impresion += ("Chars = {:d}".format(Convertido[0]),)
   Impresion += ("{} bytes leídos hasta aquí".format(BytesLeidos),)

   Impresion += ("\n\n*** Cuarto record ***",)
   Bytes = RSSA.read(4)
   BytesLeidos +=4
   ImpresionNueva += (Bytes,)
   BytesImpresos += 4
   Convertido=struct.unpack('@i',Bytes)
   Impresion += ("Chars = {:d}".format(Convertido[0]),)
   Bytes = RSSA.read(44)
   BytesLeidos +=44
   ImpresionNueva += (Bytes,)
   BytesImpresos += 44
   Convertido=struct.unpack_from('@i',Bytes)
   Impresion += ("njss = {}".format(Convertido[0]),)
   Convertido=struct.unpack_from('@i',Bytes,offset=4)
   Impresion += ("jss = {}".format(Convertido[0]),)
   Convertido=struct.unpack_from('@i',Bytes,offset=8)
   Impresion += ("jx = {}".format(Convertido[0]),)
   Convertido=struct.unpack_from('@i',Bytes,offset=12)
   Impresion += ("kst = {}".format(Convertido[0]),)
   Convertido=struct.unpack_from('@i',Bytes,offset=16)
   Impresion += ("n = {}".format(Convertido[0]),)
   Convertido=struct.unpack_from('@i',Bytes,offset=20)
   Impresion += ("lsc = {}".format(Convertido[0]),)
   Convertido=struct.unpack_from('@10e',Bytes,offset=24)
   Impresion += ("scf = {}".format(Convertido),)
   Bytes = RSSA.read(4)
   BytesLeidos +=4
   ImpresionNueva += (Bytes,)
   BytesImpresos += 4
   Convertido=struct.unpack('@i',Bytes)
   Impresion += ("Chars = {:d}".format(Convertido[0]),)
   Impresion += ("{} bytes leídos hasta aquí".format(BytesLeidos),)


   Impresion += ("\n\n*** Summary record ***",)
   Bytes = RSSA.read(4)
   BytesLeidos +=4
   # Cambio el contenido, pongo 608 (formato >=6.2) en lugar de 64 (formato <6.2)
   ImpresionNueva += (struct.pack('@i',608),)
   BytesImpresos += 4
   Convertido=struct.unpack('@i',Bytes)
   Impresion += ("Chars = {:d}".format(Convertido[0]),)
   Bytes = RSSA.read(64)
   BytesLeidos +=64
   ImpresionNueva += (Bytes,)
   BytesImpresos += 64
   Convertido=struct.unpack_from('@i',Bytes)
   Impresion += ("njss = {}".format(Convertido[0]),)
   Convertido=struct.unpack_from('@i',Bytes,offset=4)
   Impresion += ("nilw = {} (number of cells)".format(Convertido[0]),)
   Convertido=struct.unpack_from('@i',Bytes,offset=8)
   Impresion += ("nilw = {} (source particle type ('1' para neutrones))".format(Convertido[0]),)
   Convertido=struct.unpack_from('@2i',Bytes,offset=12)
   Impresion += ("nsl (total tracks, independent stories) = {}".format(Convertido),)
   Bytes = RSSA.read(4)
   BytesLeidos +=4
   # Agrego a la fuente nueva 544 bytes nuevos (608 - 64)
   # 544 Null characters
   ImpresionNueva += (struct.pack('@544s', b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),)
   # Cambio el contenido, pongo 608 (formato >=6.2) en lugar de 64 (formato <6.2)
   BytesImpresos +=544
   ImpresionNueva += (struct.pack('@i',608),)
   BytesImpresos += 4
   Convertido=struct.unpack('@i',Bytes)
   Impresion += ("Chars = {:d}".format(Convertido[0]),)
   Impresion += ("\nBytes leídos en el encabezado: {}".format(BytesLeidos),)


   
   ParticulaAImprimir=17
   for i in range(18):
      if i == ParticulaAImprimir:
          Impresion += ("\n\n*** {}th particle record ***".format(i+1),)
      Bytes = RSSA.read(4)
      BytesLeidos +=4
      if ImprimirNueva == 1:
          ImpresionNueva += (Bytes,)
          BytesImpresos += 4
      Convertido=struct.unpack('@i',Bytes)
      if i == ParticulaAImprimir:
          Impresion += ("Chars = {:d}. Bytes {} a {}.".format(Convertido[0],BytesLeidos-3,BytesLeidos),)
      Bytes = RSSA.read(88)
      BytesLeidos +=88
      if ImprimirNueva == 1:
          ImpresionNueva += (Bytes[0:8],)
          BytesImpresos += 8
      # Cambio los valores de coeficientes b y c
      b=int(struct.unpack_from('@d',Bytes,offset=8)[0])
      if ImprimirNueva == 1:
         if b>0:
            ImpresionNueva += (struct.pack('@d',8.0),)
            BytesImpresos += 8
         else:
            ImpresionNueva += (struct.pack('@d',-8.0),)
            BytesImpresos += 8
         ImpresionNueva += (Bytes[16:80],)
         BytesImpresos += 64
         ImpresionNueva += (struct.pack('@d',1.0),)
         BytesImpresos += 8
      Convertido=struct.unpack_from('@d',Bytes)
      if i == ParticulaAImprimir:
          Impresion += ("a = {}. Bytes {} a {}.".format(Convertido[0],BytesLeidos-87,BytesLeidos-80),)
      Convertido=struct.unpack_from('@d',Bytes,offset=8)
      if ImprimirValores ==1:
          ValoresParticulas.write("{}\n".format(Convertido[0]))
      if i == ParticulaAImprimir:
          Impresion += ("b = {}. Bytes {} a {}.".format(Convertido[0],BytesLeidos-79,BytesLeidos-72),)
      if i == ParticulaAImprimir:
          if b>0:
             Impresion += ("b es positivo",)
          else:
             Impresion += ("b es negativo",)
          
      Convertido=struct.unpack_from('@d',Bytes,offset=16)
      if i == ParticulaAImprimir:
          Impresion += ("wgt = {}. Bytes {} a {}.".format(Convertido[0],BytesLeidos-71,BytesLeidos-64),)
      Convertido=struct.unpack_from('@d',Bytes,offset=24)
      if i == ParticulaAImprimir:
          Impresion += ("erg = {}. Bytes {} a {}.".format(Convertido[0],BytesLeidos-63,BytesLeidos-56),)
      Convertido=struct.unpack_from('@d',Bytes,offset=32)
      if i == ParticulaAImprimir:
          Impresion += ("tme = {}. Bytes {} a {}.".format(Convertido[0],BytesLeidos-55,BytesLeidos-48),)
          #print("tme = {}".format(Bytes[32:40]))
      Convertido=struct.unpack_from('@d',Bytes,offset=40)
      if i == ParticulaAImprimir:
          Impresion += ("x = {}. Bytes {} a {}.".format(Convertido[0],BytesLeidos-47,BytesLeidos-40),)
          #print("x = {}".format(Bytes[40:48]))
      Convertido=struct.unpack_from('@d',Bytes,offset=48)
      if i == ParticulaAImprimir:
          Impresion += ("y = {}. Bytes {} a {}.".format(Convertido[0],BytesLeidos-39,BytesLeidos-32),)
      Convertido=struct.unpack_from('@d',Bytes,offset=56)
      if i == ParticulaAImprimir:
          Impresion += ("z = {}. Bytes {} a {}.".format(Convertido[0],BytesLeidos-31,BytesLeidos-24),)
      Convertido=struct.unpack_from('@d',Bytes,offset=64)
      if i == ParticulaAImprimir:
          Impresion += ("u = {}. Bytes {} a {}.".format(Convertido[0],BytesLeidos-23,BytesLeidos-16),)
      Convertido=struct.unpack_from('@d',Bytes,offset=72)
      if i == ParticulaAImprimir:
          Impresion += ("v = {}. Bytes {} a {}.".format(Convertido[0],BytesLeidos-15,BytesLeidos-8),)
      Convertido=struct.unpack_from('@d',Bytes,offset=80)
      if i == ParticulaAImprimir:
          Impresion += ("c = {}. Bytes {} a {}.".format(Convertido[0],BytesLeidos-7,BytesLeidos-0),)
      Bytes = RSSA.read(4)
      BytesLeidos +=4
      if ImprimirNueva == 1:
          ImpresionNueva += (Bytes,)
          BytesImpresos += 4
      Convertido=struct.unpack('@i',Bytes)
      if i == ParticulaAImprimir:
          Impresion += ("Chars = {:d}. Bytes {} a {}.".format(Convertido[0],BytesLeidos-3,BytesLeidos),)
          Impresion += ("{} bytes leídos hasta aquí".format(BytesLeidos),)




if Imprimir == 1:
    for i in range(len(Impresion)):
        print(Impresion[i])
        


if ImprimirNueva == 1:
    print("Generando fuente nueva en '{}'".format(NombreFuenteNueva))
    FuenteNueva = open(NombreFuenteNueva, mode="wb", buffering=0)
    # Si venía leyendo fuente formato <6.2, agrego encabezado de formato
    if sys.argv[1] == "1":
        print("No se imprime encabezado")
    else:
        print("\n\nAgregando encabezado:")
        FuenteNueva.write(b'\x08\x00\x00\x00')
        BytesImpresos += 4
        print("{}".format(b'SF_00001'))
        FuenteNueva.write(b'SF_00001')
        BytesImpresos += 8
        FuenteNueva.write(b'\x08\x00\x00\x00')
        BytesImpresos += 4
    
    print("\n\nImprimiendo fuente.")
    for i in range(len(ImpresionNueva)):
        FuenteNueva.write(ImpresionNueva[i])
    
# Agrego a la fuente nueva copia exacta de todas las restantes partículas
if ImprimirNueva == 1 or ImprimirValores ==1:
   Bytes=RSSA.read(96)
   while len(Bytes) > 0 :
       if ImprimirNueva == 1:
           FuenteNueva.write(Bytes[0:12])
           BytesImpresos += 12
           # Cambio los valores de coeficientes b y c
           b=int(struct.unpack_from('@d',Bytes,offset=12)[0])
           if b>0:
               FuenteNueva.write(struct.pack('@d',8.0),)
           else:
               FuenteNueva.write(struct.pack('@d',-8.0),)
           BytesImpresos += 8
           FuenteNueva.write(Bytes[20:84])
           BytesImpresos += 64
           FuenteNueva.write(struct.pack('@d',1.0),)
           BytesImpresos += 8
           FuenteNueva.write(Bytes[92:96])
           BytesImpresos += 4
       if ImprimirValores ==1:
           ValoresParticulas.write("{}\n".format((struct.unpack_from('@d',Bytes,offset=12))[0]))
       Bytes=RSSA.read(96)
    
        
        
if ImprimirNueva == 1:
    FuenteNueva.close()
RSSA.close()

if ImprimirValores ==1:
    ValoresParticulas.close()

sys.exit(0)




"""
Borrado   
"""
