import io
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
from PIL import UnidentifiedImageError

def optimize_pdf(input_path, output_path):
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        # Remove JavaScript and forms
        page.compress_content_streams()
        if '/Annots' in page:
            del page['/Annots']
        if '/JS' in page:
            del page['/JS']

        # Optimize images
        if '/Resources' in page and '/XObject' in page['/Resources']:
            xObject = page['/Resources']['/XObject'].get_object()
            for obj in xObject:
                if xObject[obj]['/Subtype'] == '/Image':
                    try:
                        if '/SMask' in xObject[obj]:
                            del xObject[obj]['/SMask']  # Remove image masks
                        if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                            # Convert to grayscale
                            img_data = xObject[obj]._data
                            img = Image.open(io.BytesIO(img_data))
                            img_gray = img.convert('L')
                            img_byte_arr = io.BytesIO()
                            img_gray.save(img_byte_arr, format='JPEG', optimize=True, quality=85)
                            xObject[obj] = {
                                '/ColorSpace': '/DeviceGray',
                                '/Filter': '/DCTDecode',
                                '/Width': img.width,
                                '/Height': img.height,
                                '/BitsPerComponent': 8,
                                '/Subtype': '/Image'
                            }
                            xObject[obj]._data = img_byte_arr.getvalue()
                    except UnidentifiedImageError:
                        print(f"Skipping unidentified image in {input_path}")
                    except Exception as e:
                        print(f"Error processing image in {input_path}: {str(e)}")

        writer.add_page(page)

    # Optimize for web
    writer.add_metadata({
        '/Creator': 'Web Crawler PDF Generator',
        '/Producer': 'PyPDF2'
    })

    try:
        with open(output_path, 'wb') as f:
            writer.write(f)
        print(f"Optimized PDF saved as {output_path}")
    except Exception as e:
        print(f"Error saving optimized PDF {output_path}: {str(e)}")

