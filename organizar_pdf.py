#!\usr\env\bin python
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
import os

########################################
"""CARGANDO EL PDF"""
########################################

doc = input("Arrastra el PDF a reordenar: ")
ruta_PDF = os.path.join(os.getcwd(), doc)    #ALternativa --> ruta_PDF = "ejemplo/sample.pdf"
PDF = PdfFileReader(ruta_PDF)
numPages = int(PDF.getNumPages())
#Ver numero de paginas del PDF --> print ("Tenemos %s paginas." % numPages)


########################################
"""RECUENTO DE PAGINAS y AJUSTE A MULTIPLOS DE 4"""
########################################

#PASO 1 Introducimos el numero y Transformamos el numero de paginas a un multiplo de 4 (porque sino nos dará error, porque debemos poner 4 paginas en cada hoja del folio al final)
num_hojas = numPages

#Defino la funcion que trnaforma el numero a en un multiplo de b
def multiplo(a, b):
  return int((a/b+1))*b

#Verifico si el numero de paginas del pdf es multiplo de 4
if num_hojas % 4 == 0:  # Si el residuo es 0, es múltiplo 4, por lo tanto nos quedamos el numero
  num = num_hojas

#Si no es múltiplo 4, usamos la funcion "multiplo" para transformar el numero
else:
  num=multiplo(num_hojas,4)

diferencia = num-num_hojas

#############################
"""AÑADIENDO PAGINAS BLANCAS"""
#############################

#PASO 1 Añadimos el PDF original y el PDF con paginas blancas
input_pdf = PDF
output = PdfFileWriter()
blanc_pdf = PdfFileReader("blanc.pdf")

#PASO 2 Obtenemos el numero de hojas blancas que queremos añadir
for blancas in range (diferencia):
    output.addPage(blanc_pdf.getPage(blancas))

with open(os.path.join("PDF_EDITADO", "residuo.pdf"), 'wb') as f:
    output.write(f)

#PASO 3 Juntamos le PDF con las paginas en blanco
union = PdfFileMerger()
union.append(input_pdf)
union.append("PDF_EDITADO/residuo.pdf")

with open(os.path.join("PDF_EDITADO", "residuo2.pdf"), 'wb') as f:
    union.write(f)


#######################
"""ALGORITMO DE ORDENACION"""
#######################

#PASO 1 Creamos la primera tupla con los numeros en orden de pares mayor-menor
tupla = []
for i in range(num):
  tupla.append((num-i,i+1))


#PASO 2 Hago otra tupla a partir de la generada en el paso anterior pero en orden inverso
idx = len(tupla) - 1
tupla_inversa = []
while (idx >= 0):
  tupla_inversa.append(tupla[idx])
  idx = idx - 1

#resultado paso 2 --> print(tupla_inversa)

#PASO 3 Combinamos las dos tuplas en orden normal y en orden inverso para alternar una tupla de cada
t_combinadas =[]
numI=int(num-1) #resto 1 al numero input para no tener mas tuplas de las que puede haber
for p in range (numI):
  t_combinadas.append((tupla[p],tupla_inversa[p+1]))


#PASO 4 Ahora hacemos una nueva tupla que combine una normal y una inversa

if num >=8:
  div=int(num/4) #Dividimos por 4 el numero introducido para recortar los cuadruplicados al unir 2 pares de tuplas en pasos anteriores
else:
  div=int(num/3) #Dividimos por 2 cuando los numeros son mas pequeños que 8 ()

resultados= []
for r in range (div):
  resultados.append(t_combinadas[r*2])


for item in resultados:
    print(item[0][0],',',item[0][1],'/',item[1][0],',',item[1][1])


#PASO 5 Aplanamos la tupla obtenida (que estaba comprimida) y mostramos resultados

ordenacion= [i for x in resultados for j in x for i in j]
print("El orden de las hojas será ", ordenacion)

# Imprimimos el numero de hojas añadidas, si las hay
if num_hojas % 4 == 0:
  print('OK')
else:
  print("El numero de paginas que tenia el pdf eran ", num_hojas, " Pero se han añadido ", diferencia, " hojas para que sea multiplo de 4 y cuadre con el documento final")


########################################
"""CREANDO EL PDF"""
########################################

#Cargo el pdf con las paginas blancas y creo un doc para crear
fusion= PdfFileReader("PDF_EDITADO/residuo2.pdf")
creacion=PdfFileWriter()

#Hago un bucle for que escriba siguiendo el orden de las tuplas obtenidas
for numero_pagina in ordenacion:
    temp= fusion.getPage(numero_pagina -1)
    creacion.addPage(temp)

with open(os.path.join("PDF_EDITADO", "creado.pdf"), 'wb') as f:
        creacion.write(f)


if __name__ == "__main__":

    # Abre la carpeta donde guardo el pdf editado un vez se ha finalizado el proceso
    os.system(f'start {os.path.realpath("PDF_EDITADO")}')

    quit()
