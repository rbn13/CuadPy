# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton, QMessageBox

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
        self.btn1.clicked.connect(self.reorganiza)
        self.btn_split.clicked.connect(self.mensaje)
        self.btn_carpeta.clicked.connect(self.carpeta)
        self.info.clicked.connect(self.info_autor)

    def retranslateUi(self, CuadPy):
        _translate = QtCore.QCoreApplication.translate
        CuadPy.setWindowTitle(_translate("CuadPy", "CuadPy"))
        self.caja.setText(_translate("CuadPy", "PDF Aqui")) #Documento cargado
        self.label.setText(_translate("CuadPy", "Arrastra el pdf aquí"))
        self.btn1.setText(_translate("CuadPy", "Reordenar"))
        self.btn_split.setText(_translate("CuadPy", "Dividir PDF"))
        self.btn_carpeta.setText(_translate("CuadPy", "Abrir carpeta"))
        self.info.setText(_translate("CuadPy", "..."))

#Funciones del boton
    def reorganiza(self):
        from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
        import os

        ########################################
        """CARGANDO EL PDF"""
        ########################################

        doc = self.caja.toPlainText()
        ruta_PDF = os.path.join(os.getcwd(), doc)  # ALternativa --> ruta_PDF = "ejemplo/sample.pdf"
        PDF = PdfFileReader(ruta_PDF)
        numPages = int(PDF.getNumPages())
        # Ver numero de paginas del PDF --> print ("Tenemos %s paginas." % numPages)

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

        # PASO 1 Añadimos el PDF original y el PDF con paginas blancas
        input_pdf = PDF
        output = PdfFileWriter()
        blanc_pdf = PdfFileReader("blanc.pdf")

        # PASO 2 Obtenemos el numero de hojas blancas que queremos añadir
        for blancas in range(diferencia):
            output.addPage(blanc_pdf.getPage(blancas))

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

    def carpeta(self):
        import os
        import platform
        import subprocess
        
#Abrir carpeta en en windows        
        os.system(f'start {os.path.realpath("PDF_EDITADO")}')
        
#Abrir carpeta en funcion al sistema operatico que estemos usando
        def open_file(path):
            if platform.system() == "Windows":
                os.startfile(path)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])

        open_file("PDF_EDITADO")


    def mensaje(self):
        self.caja.setText("FIN")

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
