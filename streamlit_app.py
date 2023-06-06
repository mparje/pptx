import streamlit as st
import os
from pptx import Presentation
from pptx.util import Inches
import openai


# Configura la API de OpenAI
openai.api_key = 'TU_API_KEY'


# Genera el resumen utilizando GPT-3
def generate_summary(pdf_path):
    # Leer el contenido del PDF (puedes utilizar una biblioteca como PyPDF2 o pdfminer.six)
    # y almacenarlo en una variable llamada 'content'

    # Llamar a la API de GPT-3 para generar el resumen
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=content,
        max_tokens=150,
        temperature=0.5,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    summary = response.choices[0].text.strip()
    return summary


# Genera el archivo PPTX utilizando el resumen y las imágenes
def generate_pptx(summary, images, pptx_path):
    presentation = Presentation()

    # Agrega el resumen como el contenido de la primera diapositiva
    slide = presentation.slides.add_slide(presentation.slide_layouts[1])
    slide.shapes.title.text = 'Resumen del PDF'
    slide.placeholders[1].text = summary

    # Agrega las imágenes a las diapositivas
    for image_path in images:
        slide = presentation.slides.add_slide(presentation.slide_layouts[1])
        slide.shapes.add_picture(image_path, Inches(1), Inches(1), width=Inches(8), height=Inches(6))

    # Guarda la presentación como un archivo PPTX
    presentation.save(pptx_path)


# Aplicación de Streamlit
def main():
    st.title("Generador de Presentaciones PPTX desde PDF")
    pdf_file = st.file_uploader("Cargar archivo PDF", type=["pdf"])

    if pdf_file is not None:
        # Guarda el archivo PDF en el sistema de archivos
        with open('temp.pdf', 'wb') as f:
            f.write(pdf_file.getvalue())

        # Genera el resumen del PDF
        summary = generate_summary('temp.pdf')

        # Convierte las páginas del PDF a imágenes (puedes utilizar la biblioteca pdf2image)
        images = convert_pdf_to_images('temp.pdf')

        # Genera la presentación PPTX utilizando el resumen y las imágenes
        generate_pptx(summary, images, 'output.pptx')

        # Descarga el archivo PPTX
        with open('output.pptx', 'rb') as f:
            st.download_button('Descargar PPTX', f.read(), file_name='output.pptx')

        # Elimina los archivos temporales
        os.remove('temp.pdf')
        os.remove('output.pptx')


if __name__ == '__main__':
    main()
