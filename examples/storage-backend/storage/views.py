import os
from pathlib import Path
from django.conf import settings
from django.http import FileResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class StorageView(APIView):
    def post(self, request, *args, **kwargs):
        pdf = request.FILES.get('file')
        filepath = os.path.join(settings.MEDIA_ROOT, pdf.name)
        with open(filepath, 'wb') as destination:
            for chunk in pdf.chunks():
                destination.write(chunk)

        return Response(status=status.HTTP_200_OK)

    def get(self, request, filename, *args, **kwargs):
        matches = list(Path(settings.MEDIA_ROOT).glob(filename))
        if not matches:
            return Response(status=status.HTTP_404_NOT_FOUND)
        filepath = max(matches)
        response = FileResponse(open(filepath, 'rb'),
                                content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
