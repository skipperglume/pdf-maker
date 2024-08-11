from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import cm,inch


# #edbb3b == rgb(237, 187, 59)
YELLOW_COLOR = (237, 187, 59)
YELLOW_COLOR = (237, 227, 9)
# #dd2121 == rgb(221, 33, 33)
RED_COLOR = (221, 33, 33)


def lineBreaks(char:str='=')->None:
    print(char*50)


def renormalizeRGB(rgb:tuple)->tuple:
    return tuple([x/255 for x in rgb])

def drawBackground(c, unit='cm', startPoint=(1,27), size=(19,3), color=(1,1,1))->None:
    '''
    Draw a background for the label. Background is done via drawing a rectangular shape.
    '''

    c.setFillColorRGB(*color) #choose fill colour

    # `rect` method of `canvas`:
    # 'params': x, y, width, height, stroke=1, fill=0

    c.rect(startPoint[0]*cm,startPoint[1]*cm,size[0]*cm,size[1]*cm, fill=1) #draw rectangle


def displayCanvasInfo(c, onlyKeys=False)->None:
    '''
    Display the information of the canvas object.
    '''

    if not onlyKeys:
        for key in c.__dict__:
            print(key,':')
            print('\t',c.__dict__[key])
    else:
        for key in c.__dict__:
            print(key,)

def displayCanvasSize(c, unit='cm')->None:
    # Size of a canvas is in points. 1 point = 1/72 inch.
    # 2.54 cm = 1 inch
    # 1 cm = 28.3464567 point
    if unit == 'pt':
        print(f'Width: {round(c._pagesize[0],2)} pt, Height: {round(c._pagesize[1],2)} pt')
    elif unit == 'cm':
        print(f'Width: {round(c._pagesize[0]/72*2.54,2)} cm, Height: {round(c._pagesize[1]/72*2.54,2)} cm')
    elif unit == 'inch':
        print(f'Width: {round(c._pagesize[0]/72,2)} inch, Height: {round(c._pagesize[1]/72,2)} inch')



def txtToPdf(txtFilePath, pdfFilePath, fontPath, fontName):
    # Create a PDF canvas
    c = canvas.Canvas(pdfFilePath)
    
    lineBreaks()
    displayCanvasInfo(c,True)
    lineBreaks()
    displayCanvasInfo(c,False)
    lineBreaks()
    displayCanvasSize(c)

    # Register the custom font
    pdfmetrics.registerFont(TTFont(fontName, fontPath))

    # Set the font
    c.setFont(fontName, 24)



    drawBackground(c,color=renormalizeRGB(YELLOW_COLOR))

    # Read the text file
    with open(txtFilePath, 'r') as file:
        lines = file.readlines()

    c.setFillColorRGB(*renormalizeRGB(RED_COLOR)) #choose your font colour

    # Write each line to the PDF
    for i, line in enumerate(lines):
        c.drawString(72, 800 - 15 * i, line.strip())

    # Save the PDF
    c.save()

# A path of pre-written text we want to turn into pdf format.
txtFilePath = 'label.txt'
# The name of the pdf file we want to create.
pdfFilePath = 'test.pdf'

# A list of font paths
fontsPath = [
    './AberrationDemo-WyAwV.ttf',
    './AzvamethIntoDemo-ALrjp.ttf',
    './AzvamethDemo-p7dnd.ttf',
    './Faceless-K7wel.ttf',
]

# A list of font names
fontsName = [
    'Aberration',
    'Azvameth',
    'Azvameth',
    'Faceless',
]

# Dictinoary of font names and their paths
# I really Faceless, so others are commented out.
fontNamePath = {
    # 'Aberration': './AberrationDemo-WyAwV.ttf',
    # 'Azvameth': './AzvamethIntoDemo-ALrjp.ttf',
    'Faceless': './Faceless-K7wel.ttf',
}

if __name__ == '__main__':
    print(fontNamePath.items())

    for a in enumerate(list(zip(fontNamePath.items()))):
        print(a)
        # (, (name, path)) = a
        iter = a[0]
        fontName, fontPath = a[1][0]
        
        
        txtToPdf(txtFilePath, pdfFilePath, fontPath, fontName)
    