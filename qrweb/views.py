from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from io import BytesIO
import base64
import qrcode
from .models import shelter  # Assuming your model is named Shelter

from django.shortcuts import get_object_or_404
from django.http import JsonResponse

import pandas as pd
from PIL import Image,ImageDraw
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from  qrcode.image.styles.colormasks import SolidFillColorMask

def style_inner_eyes(img):
  img_size = img.size[0]
  eye_size = 70 #default
  quiet_zone = 40 #default
  mask = Image.new('L', img.size, 0)
  draw = ImageDraw.Draw(mask)
  draw.rectangle((60, 60, 90, 90), fill=255) #top left eye
  draw.rectangle((img_size-90, 60, img_size-60, 90), fill=255) #top right eye
  draw.rectangle((60, img_size-90, 90, img_size-60), fill=255) #bottom left eye
  return mask


def style_outer_eyes(img):
  img_size = img.size[0]
  eye_size = 70 #default
  quiet_zone = 40 #default
  mask = Image.new('L', img.size, 0)
  draw = ImageDraw.Draw(mask)
  draw.rectangle((40, 40, 110, 110), fill=255) #top left eye
  draw.rectangle((img_size-110, 40, img_size-40, 110), fill=255) #top right eye
  draw.rectangle((40, img_size-110, 110, img_size-40), fill=255) #bottom left eye
  draw.rectangle((60, 60, 90, 90), fill=0) #top left eye
  draw.rectangle((img_size-90, 60, img_size-60, 90), fill=0) #top right eye
  draw.rectangle((60, img_size-90, 90, img_size-60), fill=0) #bottom left eye  
  return mask 

def index(request):
    context = {}
    no_data = False
    
    if request.method == "POST":
        qr_text = request.POST.get('qr_text', '').strip()
        if not qr_text:
            no_data = True
        else:
            qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
            qr.add_data(qr_text)
            qr_inner_eyes_img = qr.make_image(image_factory=StyledPilImage,
                                              eye_drawer=RoundedModuleDrawer(1),
                                              color_mask=SolidFillColorMask(front_color=(128, 0, 128)))

            qr_outer_eyes_img = qr.make_image(image_factory=StyledPilImage,
                                              eye_drawer=RoundedModuleDrawer(1),
                                              color_mask=SolidFillColorMask(front_color=(128, 0, 128)))                            

            qr_img = qr.make_image(image_factory=StyledPilImage,
                                   module_drawer=RoundedModuleDrawer(),
                                   color_mask=SolidFillColorMask(front_color=(0, 0, 255)),
                                   embeded_image_path="signpost_edited.png")

            inner_eye_mask = style_inner_eyes(qr_img)
            outer_eye_mask = style_outer_eyes(qr_img)
            intermediate_img = Image.composite(qr_inner_eyes_img, qr_img, inner_eye_mask)
            final_image = Image.composite(qr_outer_eyes_img, intermediate_img, outer_eye_mask)

            
            stream = BytesIO()
            final_image.save(stream, format='PNG')
            qr_image_data = stream.getvalue()
            qr_image_base64 = base64.b64encode(qr_image_data).decode('utf-8')
            context['qr_image_base64_1'] = qr_image_base64
            context['variable_1'] = qr_text  # Set the variable to display in the template

    context['no_data_1'] = no_data  # Add 'no_data' to the context


    return render(request, 'qrweb/home.html', context=context)

# def index(request):
#     context = {}
#     no_data = False
#     logo_path = "logo.png"
#     if request.method == "POST":
#         qr_text = request.POST.get('qr_text', '').strip()
#         if not qr_text:
#             no_data = True
#         else:
#             qr = qrcode.QRCode(
#                 version=4,
#                 error_correction=qrcode.constants.ERROR_CORRECT_H,
#                 box_size=5,
#                 border=2,
#             )
#             qr.add_data(qr_text)
#             qr.make(fit=True)

#             qr_image = qr.make_image(fill_color="purple", back_color="white")

#             if logo_path:
#                 logo = Image.open(logo_path)
#                 logo = logo.convert("RGBA")
#                 qr_image = qr_image.convert("RGBA")

#                 # Resize logo to fit in the center of the QR code
#                 qr_size = qr_image.size[0]
#                 logo = logo.resize((qr_size // 5, qr_size // 5))

#                 # Calculate position to place the logo in the center
#                 position = (
#                     (qr_image.size[0] - logo.size[0]) // 2,
#                     (qr_image.size[1] - logo.size[1]) // 2,
#                 )

#                 qr_image.paste(logo, position, logo)
#             qr_image = qr_image.resize((qr_image.size[0] // 2, qr_image.size[1] // 2))
#             stream = BytesIO()
#             qr_image.save(stream, format='PNG')
#             qr_image_data = stream.getvalue()
#             qr_image_base64 = base64.b64encode(qr_image_data).decode('utf-8')
#             context['qr_image_base64_1'] = qr_image_base64
#             context['variable_1'] = qr_text  # Set the variable to display in the template

#     context['no_data_1'] = no_data  # Add 'no_data' to the context


#     return render(request, 'home.html', context=context)

# def upload_data(request):
#     if request.method == "POST":
#         # Retrieve data from POST request
#         id_value = request.POST.get("id")
#         name = request.POST.get("name")
#         shelter_type = request.POST.get("type")
#         location = request.POST.get("location")
#         contact = request.POST.get("contact")
#         size = request.POST.get("size")

#         # Create a Shelter model instance and save data
#         shelter_instance = shelter(
#             id=id_value,
#             name=name,
#             type=shelter_type,
#             location=location,
#             contact=contact,
#             size=size,
#         )
#         shelter_instance.save()

#         messages.success(request, "Data uploaded successfully")

#         return redirect(
#             "http://127.0.0.1:8000/home/upload/"
#         )  # You can return any response you need

#     else:
#         return render(request, "upload.html")
def upload_data(request):
    if request.method == "POST":
        if 'file' in request.FILES:  # Check if a file is uploaded
            file = request.FILES['file']
            if file.name.endswith('.xlsx') or file.name.endswith('.csv'):
                df = pd.read_excel(file) if file.name.endswith('.xlsx') else pd.read_csv(file)
                expected_columns = ['id', 'name', 'type', 'location', 'contact', 'size']  # Your database columns
                print(f"expected column names : {expected_columns}")
                if all(col.lower().strip() in map(str.lower, df.columns.str.strip()) for col in expected_columns):
                    for index, row in df.iterrows():
                        shelter_instance = shelter(
                            id=row['id'],
                            name=row['name'],
                            type=row['type'],
                            location=row['location'],
                            contact=row['contact'],
                            size=row['size']
                        )
                        shelter_instance.save()

                    messages.success(request, "Data uploaded successfully from the file.")
                    return redirect("https://web-production-0ef6.up.railway.app/home/upload/")
                else:
                    messages.error(request, "Column names in the file do not match the expected columns.")
                    return redirect("https://web-production-0ef6.up.railway.app/home/upload/")
            else:
                messages.error(request, "Please upload a valid .xlsx or .csv file.")
                return redirect("https://web-production-0ef6.up.railway.app/home/upload/")
        else:
            # Handle normal text input as before
            id_value = request.POST.get("id")
            name = request.POST.get("name")
            shelter_type = request.POST.get("type")
            location = request.POST.get("location")
            contact = request.POST.get("contact")
            size = request.POST.get("size")

            shelter_instance = shelter(
                id=id_value,
                name=name,
                type=shelter_type,
                location=location,
                contact=contact,
                size=size,
            )
            shelter_instance.save()

            messages.success(request, "Data uploaded successfully from the form.")
            return redirect("https://web-production-0ef6.up.railway.app/home/upload/")
    else:
        return render(request, "qrweb/upload.html")

def generate_qr(request):
    context = {}
    shelter_id = request.GET.get('shelter_id')
    if not shelter_id:
        context['no_id'] = True
        return render(request, 'qrweb/index.html', context=context)

    try:
        shelter_instance = shelter.objects.get(id=shelter_id)
    except shelter.DoesNotExist:
        context['no_data_found'] = True
        return render(request, 'qrweb/index.html', context=context)

    shelter_url = f"https://web-production-0ef6.up.railway.app/home/upload/qr/{shelter_instance.id}"  # Replace with your URL pattern

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)

    qr.add_data(shelter_url)
    qr_inner_eyes_img = qr.make_image(image_factory=StyledPilImage,
                                        eye_drawer=RoundedModuleDrawer(1),
                                        color_mask=SolidFillColorMask(front_color=(128, 0, 128)))

    qr_outer_eyes_img = qr.make_image(image_factory=StyledPilImage,
                                        eye_drawer=RoundedModuleDrawer(1),
                                        color_mask=SolidFillColorMask(front_color=(128, 0, 128)))                            

    qr_img = qr.make_image(image_factory=StyledPilImage,
                            module_drawer=RoundedModuleDrawer(),
                            color_mask=SolidFillColorMask(front_color=(0, 0, 255)),
                            embeded_image_path="signpost_edited.png")

    inner_eye_mask = style_inner_eyes(qr_img)
    outer_eye_mask = style_outer_eyes(qr_img)
    intermediate_img = Image.composite(qr_inner_eyes_img, qr_img, inner_eye_mask)
    final_image = Image.composite(qr_outer_eyes_img, intermediate_img, outer_eye_mask)
    stream = BytesIO()
    final_image.save(stream, format='PNG')
    qr_image_data = stream.getvalue()
    qr_image_base64 = base64.b64encode(qr_image_data).decode('utf-8')
    context['qr_image_base64'] = qr_image_base64
    context['variable'] = shelter_url
            
    # If shelter_id is not present or shelter_instance is None
    return render(request, 'qrweb/index.html', context=context)  # Renders the index.html with an empty context
# Adjust this to a suitable error page or response



# def generate_text_file(request, shelter_id):
#     # Retrieve data from the database based on the shelter_id
#     data = get_object_or_404(shelter, id=shelter_id)

#     # Generate text content based on the retrieved data
#     text_content = f"Hoarding ID: {data.id}\nOwner Name: {data.name}\nSite no: {data.type}\nLocation: {data.location}\nContact number: {data.contact}\nSize: {data.size}"

#     # Create a text file and serve it as a response
#     response = HttpResponse(content_type='text/plain')
#     response['Content-Disposition'] = f'attachment; filename="{shelter_id}.txt"'
#     response.write(text_content)
#     return response

def show_shelter_details(request, shelter_id):
    # Retrieve data from the database based on the shelter_id
    shelter_obj = get_object_or_404(shelter, id=shelter_id)

    # Pass shelter data to the HTML template
    context = {
        'shelter': shelter_obj
    }
    return render(request, 'qrweb/details.html', context)

