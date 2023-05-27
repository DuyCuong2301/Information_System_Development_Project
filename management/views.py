from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
import face_recognition
import cv2
import numpy as np
import requests
import json
from .models import FaceRecognitionResult, Face
from django.utils import timezone

# load known face encodings and their name
known_face_encodings = np.load("/home/cuong/Project2.1/attendence/management/face_data/known_face_encodings.npy")
known_face_names = np.load("/home/cuong/Project2.1/attendence/management/face_data/known_face_names.npy")

@api_view(["POST"])
def recognize_faces(request):
    if request.method == 'POST':
        frame = request.FILES.get('image')  # Retrieve the uploaded image

        if frame is not None:
            image = face_recognition.load_image_file(frame)

            # find all the faces and face encodings in the image
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)

            face_names=[]
            for face_encoding in face_encodings:
                # See if the face is a match for the knonw face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name='Unknown'

                # Find the best match
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                face_names.append(name)

            # Prepare the response data
            response_data = {
                'face_locations': face_locations,
                'face_names': face_names
            }

            result = FaceRecognitionResult(time=timezone.now())
            result.save()

            for face_location, face_name in zip(face_locations, face_names):
                face = Face.objects.create(name=face_name)
                result.student_attend.add(face)
            
            result.save()

            # Return the response
            return JsonResponse(response_data)

        else:
            return JsonResponse({'error': 'No image provided'}, status=400)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def video_capture(request):
    return render(request, 'video_capture.html')


def attend_result(request):
    results = FaceRecognitionResult.objects.all()
    return render(request, 'attendent_result.html', {'results': results})
