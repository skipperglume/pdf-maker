from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import cm, inch

import os
from PIL import Image

# import numpy as np

# #edbb3b == rgb(237, 187, 59)
YELLOW_COLOR = (237, 187, 59)
YELLOW_COLOR = (237, 227, 9)
# #dd2121 == rgb(221, 33, 33)
RED_COLOR = (221, 33, 33)
BLACK_COLOR = (0, 0, 0)


def lineBreaks(char: str = "=") -> None:
    print(char * 50)


def renormalizeRGB(rgb: tuple) -> tuple:
    return tuple([x / 255 for x in rgb])


def drawBackground(
    c, unit="cm", startPoint=(1, 27), size=(19, 3), color=(1, 1, 1)
) -> None:
    """
    Draw a background for the label. Background is done via drawing a rectangular shape.
    """

    c.setFillColorRGB(*color)  # choose fill colour

    # `rect` method of `canvas`:
    # 'params': x, y, width, height, stroke=1, fill=0

    c.rect(
        startPoint[0] * cm, startPoint[1] * cm, size[0] * cm, size[1] * cm, fill=1
    )  # draw rectangle


def displayCanvasInfo(c, onlyKeys=False) -> None:
    """
    Display the information of the canvas object.
    """

    if not onlyKeys:
        for key in c.__dict__:
            print(key, ":")
            print("\t", c.__dict__[key])
    else:
        for key in c.__dict__:
            print(
                key,
            )


def displayCanvasSize(c, unitOut="cm", unitIn="pt") -> None:
    # Size of a canvas is in points. 1 point = 1/72 inch.
    # 2.54 cm = 1 inch
    # 1 cm = 28.3464567 point

    # `unitIn`` is not used yet.

    if unitOut == "pt":
        print(
            f"Width: {round(c._pagesize[0],2)} pt, Height: {round(c._pagesize[1],2)} pt"
        )
    elif unitOut == "cm":
        print(
            f"Width: {round(c._pagesize[0]/72*2.54,2)} cm, Height: {round(c._pagesize[1]/72*2.54,2)} cm"
        )
    elif unitOut == "inch":
        print(
            f"Width: {round(c._pagesize[0]/72,2)} inch, Height: {round(c._pagesize[1]/72,2)} inch"
        )

    # float('%.2f' % (f))


def txtToPdf(txtFilePath, pdfFilePath, fontPath, fontName):
    # Create a PDF canvas
    c = canvas.Canvas(pdfFilePath)

    lineBreaks()
    displayCanvasInfo(c, True)
    lineBreaks()
    displayCanvasInfo(c, False)
    lineBreaks()
    displayCanvasSize(c)

    # Register the custom font
    pdfmetrics.registerFont(TTFont(fontName, fontPath))

    # Set the font
    c.setFont(fontName, 24)

    drawBackground(c, color=renormalizeRGB(YELLOW_COLOR))

    # Read the text file
    with open(txtFilePath, "r") as file:
        lines = file.readlines()

    # c.setFillColorRGB(*renormalizeRGB(RED_COLOR))  # choose your font colour
    c.setFillColorRGB(*renormalizeRGB(BLACK_COLOR))  # choose your font colour

    # Write each line to the PDF
    for i, line in enumerate(lines):
        c.drawString(72, 800 - 15 * i, line.strip())

    # Save the PDF
    c.save()

    print(f"Created PDF: [{pdfFilePath}] using font: [{fontName}]")


# A path of pre-written text we want to turn into pdf format.
txtFilePath = "label.txt"
# The name of the pdf file we want to create.
pdfFilePath = "test.pdf"

# A list of font paths
fontsPath = [
    "./AberrationDemo-WyAwV.ttf",
    "./AzvamethIntoDemo-ALrjp.ttf",
    "./AzvamethDemo-p7dnd.ttf",
    "./Faceless-K7wel.ttf",
]

# A list of font names
fontsName = [
    "Aberration",
    "Azvameth",
    "Azvameth",
    "Faceless",
]

# Dictinoary of font names and their paths
# I really Faceless, so others are commented out.
fontNamePath = {
    "Aberration": "./fonts/AberrationDemo-WyAwV.ttf",
    "Azvameth": "./fonts/AzvamethIntoDemo-ALrjp.ttf",
    "Faceless": "./fonts/Faceless-K7wel.ttf",
    "Monas": "./fonts/Monas-BLBW8.ttf",
    "DansDisney_1": "./fonts/DansDisney-3nJ8.ttf",
    "DansDisney_2": "./fonts/DansDisneyUi-x5Aq.ttf",
}


def text_over_image(
    text_file_path,
    pdf_file_path,
    font_path,
    font_name,
    background_image_path,
):
    """
    Method generates a PDF file with text over a background image.
    """
    # Create a PDF canvas
    c = canvas.Canvas(pdf_file_path)

    if background_image_path is not None:
        # Ensure the background image file exists
        if not os.path.isfile(background_image_path):
            raise FileNotFoundError(
                f"Background image not found: [{background_image_path}]"
            )
        # Get the size of the image:

        with Image.open(background_image_path) as img:
            img_width, img_height = img.size

        print(f"Image size: {img_width}, {img_height}")
        # Draw the background image
        # Scale it up proportionally to fill the width

        print(f"PDF Size: {c._pagesize[0]:.2f} {c._pagesize[1]:.2f}")

        # Rescale hieght:
        new_img_width = c._pagesize[0]
        new_img_height = new_img_width / img_width * img_height

        print(f"Rescaled Image size: {new_img_width}, {new_img_height}")

        # Print image RGB values
        print(img.getbands())
        # Print R
        # print(img.getchannel("R"))

        c.drawImage(
            background_image_path,
            0,
            0,
            width=new_img_width,
            height=new_img_height,
        )

    # Read the text file
    with open(text_file_path, "r") as file:
        lines = file.readlines()

    # Register the custom font
    pdfmetrics.registerFont(TTFont(font_name, font_path))

    # Set the font
    c.setFont(font_name, 50)

    # c.setFillColorRGB(*renormalizeRGB(RED_COLOR))  # choose your font colour
    c.setFillColorRGB(*renormalizeRGB(BLACK_COLOR))  # choose your font colour

    # Write each line to the PDF
    for i, line in enumerate(lines):
        c.drawString(100, 800 - 50 * i, line.strip())

    # Save the PDF
    c.save()

    print(f"Created PDF: [{pdf_file_path}] using font: [{font_name}]")


if __name__ == "__main__":
    print(fontNamePath.items())

    background = None
    font_name = "DansDisney_1"
    font_path = fontNamePath[font_name]
    text_file_path = "names.txt"
    pdfFilePath = "output/names_with_background.pdf"
    # background = "band_logos/Larcenia_Roe.png"
    # background = "band_logos/A_Wake_in_Providence_symbol.webp"
    # background = "band_logos/sunscourge.jpg"
    # background = "band_logos/Proliferation.jpg"
    # txtToPdf(text_file_path, pdfFilePath, font_path, font_name)

    text_over_image(
        text_file_path,
        pdfFilePath,
        font_path,
        font_name,
        background,
    )
