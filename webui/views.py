import logging
import yaml
import json
import os
import base64
import io
import uuid
import qrcode
import datetime
from yaml.error import YAMLError

from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse


# Set up logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)



#####################################################################
#### Home Page Views ####
#####################################################################
def show_index(request):
    return render(request, "index.html")


#####################################################################


#####################################################################
#### Tools Page Views ####
#####################################################################
def tools(request):
    return render(request, "tools.html")


from .tools import s3drop
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages


BUCKET_NAME = "aimotion-public-big-data-lecture-ws24"


# View to list existing data in the bucket and handle uploads
def s3_drop(request):
    # Initialize MinIO client
    minio_client = s3drop.get_minio_client()

    if request.method == 'POST':
        # Handle file upload
        uploaded_file = request.FILES.get('file')
        folder_path = request.POST.get('folder_path', '').strip()
        duration = int(request.POST.get('duration', 1))  # Expiry duration for presigned URL

        # Validate file input
        if not uploaded_file:
            messages.error(request, 'No file selected for upload.')
            return redirect(reverse('s3_drop'))

        # Generate object name with optional folder path
        object_name = f"{folder_path.strip('/')}/{uploaded_file.name}" if folder_path else uploaded_file.name

        try:
            # Upload file to bucket
            ## Input your code here ##

            # Generate presigned URL and QR code
            ## Input your code here ##
            ## Input your code here ##

            # Store the results in session to display after redirect
            request.session['file_url'] = file_url
            request.session['qr_code'] = qr_code

            messages.success(request, 'File uploaded successfully!')
            return redirect(reverse('s3_drop'))

        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            messages.error(request, f"Error uploading file: {e}")
            return redirect(reverse('s3_drop'))

    # Handle GET request to list objects in the bucket
    try:
        object_list = s3drop.list_bucket_objects(minio_client)
    except Exception as e:
        logger.error(f"Error listing bucket objects: {e}")
        messages.error(request, f"Error listing bucket objects: {e}")
        object_list = []

    # Retrieve URL and QR code from session if available
    file_url = request.session.pop('file_url', None)
    qr_code = request.session.pop('qr_code', None)

    return render(request, 'tools.html', {
        'object_list': object_list,
        'file_url': file_url,
        'qr_code': qr_code,
    })
    
#####################################################################
