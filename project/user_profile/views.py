# user_profile/views.py
import base64

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile
from courses.models import UserCourse
from django.http import HttpResponse
from django.template.loader import render_to_string
import fitz  # PyMuPDF
import os
from django.conf import settings


@login_required
def profile(request):
    # Check if the user has a profile, if not, create it
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    # Get user certificates from completed courses
    completed_courses = UserCourse.objects.filter(user=request.user, completed=True)
    certificates = [{'course_name': user_course.course.name, 'completion_date': user_course.date.strftime('%d %B %Y')} for user_course in completed_courses]

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'certificates': certificates
    }

    return render(request, 'user_profile/profile.html', context)


@login_required
def get_certificate(request, course_name, user_id):
    user_course = get_object_or_404(UserCourse, user__id=user_id, course__name=course_name, completed=True)
    user = user_course.user
    certificate_info = {
        'course_name': user_course.course.name,
        'completion_date': user_course.date.strftime('%d %B %Y'),  # The date format has been changed
        'username': user.username
    }

    # Generate PDF certificate
    input_path = os.path.join(settings.BASE_DIR, 'files', 'resource', 'cert_template.pdf')
    output_path = os.path.join(settings.MEDIA_ROOT, f'certificate_{user.username}_{course_name}.pdf')
    pdf_zoom_level = 46
    replacements = {
        "name": certificate_info['username'],
        "coursename": certificate_info['course_name'],
        "date": certificate_info['completion_date']
    }
    replace_text_in_pdf(input_path, output_path, replacements)
    with open(output_path, 'rb') as pdf_file:
        pdf_content = pdf_file.read()
        pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
    # Render HTML template with buttons
    context = {
        'certificate': certificate_info,
        'download_url': f'/media/certificate_{user.username}_{course_name}.pdf',
        'pdf_base64': pdf_base64
    }
    return render(request, 'user_profile/certificate.html', context)


def replace_text_in_pdf(input_path, output_path, replacements):
    # Open the PDF file
    document = fitz.open(input_path)
    print(f"Opened PDF file: {input_path}")

    # Iterate over the pages
    for page_number in range(len(document)):
        page = document.load_page(page_number)
        print(f"Processing page: {page_number + 1}")

        # Function to replace text with minimal padding for DATE to avoid covering other elements
        def replace_text(old_text, new_text, initial_fontsize, fontname, padding, y_offset, additional_width=0):
            text_instances = page.search_for(old_text)
            if not text_instances:
                print(f"Text '{old_text}' not found on page {page_number + 1}")
                return
            print(f"Found '{old_text}' on page {page_number + 1}, replacing with '{new_text}'")

            for inst in text_instances:
                # Apply custom settings for each instance
                if old_text == "NAME SURNAME":
                    specific_padding = 5
                    specific_y_offset = 0
                    specific_fontsize = 20
                    specific_additional_width = 100
                elif old_text == "Course Name.":
                    specific_padding = 0
                    specific_y_offset = 0
                    specific_fontsize = 10
                    specific_additional_width = 300
                elif old_text == "DATE":
                    specific_padding = 0
                    specific_y_offset = 3
                    specific_fontsize = 10
                    specific_additional_width = 50  # Minimal width expansion for DATE
                else:
                    # Default to general settings if no match
                    specific_padding = padding
                    specific_y_offset = y_offset
                    specific_fontsize = initial_fontsize
                    specific_additional_width = additional_width

                # Adjust bounding box with minimal padding for DATE
                half_additional_width = specific_additional_width / 2
                bbox = fitz.Rect(inst.x0 - specific_padding - half_additional_width,
                                 inst.y0 - specific_padding + specific_y_offset,
                                 inst.x1 + specific_padding + half_additional_width,
                                 inst.y1 + specific_padding + specific_y_offset)
                print(f"Adjusted bounding box for '{old_text}': {bbox}")

                # Fill only the exact area with white color
                page.draw_rect(bbox, color=(1, 1, 1), fill=(1, 1, 1))
                print(f"Filled bounding box with white color for '{old_text}'")

                # Adjust font size if text doesn’t fit in the bounding box
                fontsize = specific_fontsize
                success = False
                while fontsize > 5:
                    success = page.insert_textbox(
                        bbox,
                        new_text,
                        fontsize=fontsize,
                        fontname=fontname,
                        color=(0, 0, 0),
                        align=fitz.TEXT_ALIGN_CENTER,  # Center text horizontally
                    )
                    if success:
                        print(f"Inserted text '{new_text}' with fontsize {fontsize} in box {bbox}")
                        break
                    fontsize -= 1
                    print(f"Reduced fontsize to {fontsize} for '{new_text}'")

        replace_text("NAME SURNAME", replacements["name"], initial_fontsize=20, fontname="notos", padding=5, y_offset=0, additional_width=100)
        replace_text("Course Name.", replacements["coursename"], initial_fontsize=15, fontname="notos", padding=30, y_offset=30, additional_width=150)
        replace_text("DATE", replacements["date"], initial_fontsize=8, fontname="notos", padding=2, y_offset=-5, additional_width=10)

    document.save(output_path)
    print(f"Saved modified PDF to: {output_path}")
    document.close()
    print("Closed PDF document")
