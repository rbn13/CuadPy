# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton, QMessageBox
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger, PageObject
import os
import platform
import subprocess

class Ui_CuadPy(object):
    def setupUi(self, CuadPy):
        CuadPy.setObjectName("CuadPy")
        CuadPy.resize(355, 240)
        self.label = QtWidgets.QLabel(CuadPy)
        self.label.setGeometry(QtCore.QRect(30, 30, 121, 31))
        self.label.setObjectName("label")
        self.btn1 = QtWidgets.QPushButton(CuadPy)
        self.btn1.setGeometry(QtCore.QRect(30, 190, 93, 28))
        self.btn1.setStyleSheet("QPushButton:pressed {\n"
"        dlg = QDialog(self)\n"
"        dlg.setWindowTitle(\"HELLO!\")\n"
"        dlg.exec()\n"
"}")
        self.btn1.setObjectName("btn1")
        self.btn_split = QtWidgets.QPushButton(CuadPy)
        self.btn_split.setGeometry(QtCore.QRect(130, 190, 93, 28))
        self.btn_split.setObjectName("btn_split")
        self.btn_carpeta = QtWidgets.QPushButton(CuadPy)
        self.btn_carpeta.setGeometry(QtCore.QRect(230, 190, 93, 28))
        self.btn_carpeta.setObjectName("btn_carpeta")
        self.caja = QtWidgets.QTextEdit(CuadPy)
        self.caja.setGeometry(QtCore.QRect(30, 60, 291, 121))
        self.caja.setObjectName("caja")
        self.info = QtWidgets.QToolButton(CuadPy)
        self.info.setGeometry(QtCore.QRect(310, 10, 31, 22))
        self.info.setObjectName("info")

        self.retranslateUi(CuadPy)
        QtCore.QMetaObject.connectSlotsByName(CuadPy)


# AÑADO CONEXION A LAS FUNCIONES
        self.btn1.clicked.connect(self.booklet)
        self.btn_split.clicked.connect(self.dividir)
        self.btn_carpeta.clicked.connect(self.carpeta)
        self.info.clicked.connect(self.info_autor)

    def retranslateUi(self, CuadPy):
        _translate = QtCore.QCoreApplication.translate
        CuadPy.setWindowTitle(_translate("CuadPy", "CuadPy"))
        self.caja.setText(_translate("CuadPy", "C:/Users/rromero/PycharmProjects/pdf_manager/ejemplo/pdfs/20p.pdf")) #Documento cargado
        self.label.setText(_translate("CuadPy", "Arrastra el pdf aquí"))
        self.btn1.setText(_translate("CuadPy", "Reordenar"))
        self.btn_split.setText(_translate("CuadPy", "Dividir PDF"))
        self.btn_carpeta.setText(_translate("CuadPy", "Abrir carpeta"))
        self.info.setText(_translate("CuadPy", "..."))

# FUNCIONES DE LOS BOTONES

    #Funcion que invoca la funcion de reorganizar pdf, poner dos hojas en una cara y borrar los pdfs que surgen del proceso
    def booklet(self):
        self.reorganiza()
        self.dobles()
        self.borrar_residuos()

    #Organizar las paginas del pdf segun el orden surgido del algoritmo en una tupla
    def reorganiza(self):

        #Cargar pdf
        doc = self.caja.toPlainText()
        ruta_PDF = os.path.join(os.getcwd(), doc)  # ALternativa --> ruta_PDF = "ejemplo/sample.pdf"
        PDF = PdfFileReader(ruta_PDF)
        numPages = int(PDF.getNumPages())

        ########################################
        """RECUENTO DE PAGINAS y AJUSTE A MULTIPLOS DE 4"""
        ########################################

        # PASO 1 Introducimos el numero y Transformamos el numero de paginas a un multiplo de 4 (porque sino nos dará error, porque debemos poner 4 paginas en cada hoja del folio al final)
        num_hojas = numPages

        # Defino la funcion que trnaforma el numero a en un multiplo de b
        def multiplo(a, b):
            return int((a / b + 1)) * b

        # Verifico si el numero de paginas del pdf es multiplo de 4
        if num_hojas % 4 == 0:  # Si el residuo es 0, es múltiplo 4, por lo tanto nos quedamos el numero
            num = num_hojas

        # Si no es múltiplo 4, usamos la funcion "multiplo" para transformar el numero
        else:
            num = multiplo(num_hojas, 4)

        diferencia = num - num_hojas

        #############################
        """AÑADIENDO PAGINAS BLANCAS"""
        #############################

        # PASO 1 Añadimos el PDF original y creamos las paginas blancas a añadir
        input_pdf = PDF
        output = PdfFileWriter()
        medida_hoja = input_pdf.getPage(0)  # Tomo la primera hoja del pdf para crear paginas blancas de la misma medida

        # PASO 2 Obtenemos el numero de hojas blancas que queremos añadir y creamos hojas blancas segun se necesitan
        for blancas in range(diferencia):
            largo = medida_hoja.mediaBox.getHeight()
            ancho = medida_hoja.mediaBox.getWidth()
            blanc_pdf = PageObject.createBlankPage(None, ancho, largo)  # Creamos pagina en blanco con las medidas del pdf original
            output.addPage(blanc_pdf)

        with open(os.path.join("PDF_EDITADO", "residuo.pdf"), 'wb') as f:
            output.write(f)

        # PASO 3 Juntamos le PDF con las paginas en blanco
        union = PdfFileMerger()
        union.append(input_pdf)
        union.append("PDF_EDITADO/residuo.pdf")

        with open(os.path.join("PDF_EDITADO", "residuo2.pdf"), 'wb') as f:
            union.write(f)

        #######################
        """ALGORITMO DE ORDENACION"""
        #######################

        # PASO 1 Creamos la primera tupla con los numeros en orden de pares mayor-menor
        tupla = []
        for i in range(num):
            tupla.append((num - i, i + 1))

        # PASO 2 Hago otra tupla a partir de la generada en el paso anterior pero en orden inverso
        idx = len(tupla) - 1
        tupla_inversa = []
        while (idx >= 0):
            tupla_inversa.append(tupla[idx])
            idx = idx - 1

        # resultado paso 2 --> print(tupla_inversa)

        # PASO 3 Combinamos las dos tuplas en orden normal y en orden inverso para alternar una tupla de cada
        t_combinadas = []
        numI = int(num - 1)  # resto 1 al numero input para no tener mas tuplas de las que puede haber
        for p in range(numI):
            t_combinadas.append((tupla[p], tupla_inversa[p + 1]))

        # PASO 4 Ahora hacemos una nueva tupla que combine una normal y una inversa

        if num >= 8:
            div = int(
                num / 4)  # Dividimos por 4 el numero introducido para recortar los cuadruplicados al unir 2 pares de tuplas en pasos anteriores
        else:
            div = int(num / 3)  # Dividimos por 2 cuando los numeros son mas pequeños que 8 ()

        resultados = []
        for r in range(div):
            resultados.append(t_combinadas[r * 2])

        for item in resultados:
            print(item[0][0], ',', item[0][1], '/', item[1][0], ',', item[1][1])

        # PASO 5 Aplanamos la tupla obtenida (que estaba comprimida) y mostramos resultados

        ordenacion = [i for x in resultados for j in x for i in j]
        print("El orden de las hojas será ", ordenacion)

        # Imprimimos el numero de hojas añadidas, si las hay
        if num_hojas % 4 == 0:
            self.caja.setText("OK")
        else:
            self.caja.setText("El numero de paginas que tenia el pdf eran "+ str(num_hojas)+ " Pero se han añadido "+ str(diferencia)+" hojas para que sea multiplo de 4 y cuadre con el documento final")

        ########################################
        """CREANDO EL PDF"""
        ########################################

        # Cargo el pdf con las paginas blancas y creo un doc para crear
        fusion = PdfFileReader("PDF_EDITADO/residuo2.pdf")
        creacion = PdfFileWriter()

        # Hago un bucle for que escriba siguiendo el orden de las tuplas obtenidas
        for numero_pagina in ordenacion:
            temp = fusion.getPage(numero_pagina - 1)
            creacion.addPage(temp)

        with open(os.path.join("PDF_EDITADO", "creado.pdf"), 'wb') as f:
            creacion.write(f)


    def dobles(self): #CREAR UN BOOKLET CON LAS PAGINAS YA ORDENADAS

        # Carga pdf y variables
        doc= "PDF_EDITADO/creado.pdf"
        pdf_elegido = os.path.join(os.getcwd(), doc)
        reader = PdfFileReader(pdf_elegido)#(open(pdf_elegido, 'rb'))  # el primer pdf
        sup_reader = reader  # el segundo pdf
        numPags = int(reader.getNumPages()/2)
        writer = PdfFileWriter()

        # Bucle para crear paginas
        for i in range(numPags):
            invoice_page = reader.getPage(i * 2)  # Hoja que ira a la izquierda del folio
            sup_page = sup_reader.getPage(int(i * 2) + 1)  # Hoja que ira a la derecha del folio

            # Creamos pagina en blanco con las medidas del pdf original pero multiplico ancho x2 para que quede apaisada
            largo = sup_page.mediaBox.getHeight()
            ancho = sup_page.mediaBox.getWidth()
            translated_page = PageObject.createBlankPage(None, ancho * 2, largo)

            # Localizacion de las copias en cada lado
            escala = 1  # Escala original
            desp_horizonal = int(ancho)  # pongo el ancho porque asi es justo la mitad de la hoja creada
            desp_vertical = 0
            e, x, y = [escala, desp_horizonal,
                       desp_vertical]  # Escala de la copia, colocacion en eje horizontal, colocacion eje vertical

            translated_page.mergeScaledTranslatedPage(sup_page, e, x, y)
            translated_page.mergePage(invoice_page)

            # Escribiendo el pdf
            writer.addPage(translated_page)

        with open(os.path.join("PDF_EDITADO", "IMPRIMIBLE.pdf"), 'wb') as f:
            writer.write(f)

    def carpeta(self):
        # Abrir carpeta en funcion al sistema operatico que estemos usando
        def open_file(path):
            if platform.system() == "Windows":
                os.startfile(path)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])

        open_file("PDF_EDITADO")

    def dividir(self):
        self.caja.setText("Dividido en pares e impares para imprimir por caras")

        # Cargo el pdf con las paginas blancas y creo un doc para crear
        xdividir = PdfFileReader("PDF_EDITADO/IMPRIMIBLE.pdf")
        hojas_pares = PdfFileWriter()
        hojas_impares = PdfFileWriter()
        numPages = int(xdividir.getNumPages()/2)

        #Creo un pdf con paginas pares
        for i in range(numPages):
            pares = xdividir.getPage(int(i*2)+1)
            hojas_pares.addPage(pares)
        with open(os.path.join("PDF_EDITADO", "1_Pares_carasB.pdf"), 'wb') as f:
            hojas_pares.write(f)

        # Creo un pdf con paginas impares
        for i in range(numPages):
            impares = xdividir.getPage(i*2)
            hojas_impares.addPage(impares)
        with open(os.path.join("PDF_EDITADO", "2_Impares_carasA.pdf"), 'wb') as f:
            hojas_impares.write(f)

    def borrar_residuos(self):
        from os import remove
        remove("PDF_EDITADO/residuo2.pdf")
        remove("PDF_EDITADO/creado.pdf")

    def info_autor(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Creado por R.Romero")
        msgBox.setWindowTitle("Info")
        msgBox.setStandardButtons(QMessageBox.Ok)

        #msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        #msgBox.buttonClicked.connect(msgButtonClick)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            print('OK clicked')

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CuadPy = QtWidgets.QDialog()
    ui = Ui_CuadPy()
    ui.setupUi(CuadPy)
    CuadPy.show()
    sys.exit(app.exec_())
