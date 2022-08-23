from PyPDF2 import PdfFileReader, PdfFileWriter, PageObject
import os

###################
"UNION DE PAGINAS"
"Unimos dos hojas en una sola cara"
#Ejemplos similares en https://gist.github.com/Geekfish/a4fe4efd59e158f55ca5c76479831c8d
###################

def dobles():
    pdf1 = "ejemplo/sample.pdf"
    pdf2 = "ejemplo/pdfs/6p.pdf"
    pdf3 = "ejemplo/pdfs/17p.pdf"
    pdf4 = "ejemplo/pdfs/19p.pdf"
    pdf5 = "ejemplo/pdfs/20p.pdf"
    pdf6 = "PDF_EDITADO/creado.pdf"
    pdf7 = os.path.join(os.getcwd(), pdf6)


    #Carga pdf y variables
    pdf_elegido = pdf6
    reader = PdfFileReader(open(pdf_elegido, 'rb'))#el primer pdf
    sup_reader = reader #el segundo pdf
    numPages = int(reader.getNumPages()/2)
    writer = PdfFileWriter()

    #Bucle para crear paginas

    for i in range(numPages):
        invoice_page = reader.getPage(i*2) #Hoja que ira a la izquierda del folio
        sup_page = sup_reader.getPage(int(i*2)+1)  #Hoja que ira a la derecha del folio

        # Creamos pagina en blanco con las medidas del pdf original pero multiplico ancho x2 para que quede apaisada
        largo = sup_page.mediaBox.getHeight()
        ancho = sup_page.mediaBox.getWidth()
        translated_page = PageObject.createBlankPage(None, ancho * 2, largo)

        #Localizacion de las copias en cada lado
        escala = 1  # Escala original
        desp_horizonal = int(ancho)  # pongo el ancho porque asi es justo la mitad de la hoja creada
        desp_vertical = 0
        e, x, y = [escala, desp_horizonal, desp_vertical] #Escala de la copia, colocacion en eje horizontal, colocacion eje vertical

        translated_page.mergeScaledTranslatedPage(sup_page, e, x, y)
        translated_page.mergePage(invoice_page)

        #Escribiendo el pdf
        writer.addPage(translated_page)

    with open(os.path.join("PDF_EDITADO", "IMPRIMIBLE.pdf"), 'wb') as f:
        writer.write(f)

dobles()

#Abrir carpeta en windows
os.system(f'start {os.path.realpath("PDF_EDITADO")}')
