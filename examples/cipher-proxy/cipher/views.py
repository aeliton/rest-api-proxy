import io
import sys
from rest_api_proxy.views import ProxyBase
from django.core.files.uploadedfile import InMemoryUploadedFile
from cryptography.fernet import Fernet
from django.conf import settings
from django.http import FileResponse, HttpResponse


class CipherView(ProxyBase):
    """
    Interceptor that encrypts incoming POST requests with files in it.
    """

    def cipher(self, files: dict[str: InMemoryUploadedFile]):
        """
        Encrypts all provided files.
        """
        fernet = Fernet(settings.CIPHER_KEY)
        for name, file in files.items():
            # Encrypts the file.
            file.seek(0)
            encrypted_data = fernet.encrypt(file.read())
            encypted_io = io.BytesIO()
            encypted_io.write(encrypted_data)
            encypted_io.seek(0)

            # Replace the file by it's encrypted version.
            files[name] = InMemoryUploadedFile(
                file=encypted_io,
                field_name=file.field_name,
                name=file.name,
                content_type='application/octet-stream',
                size=sys.getsizeof(encypted_io),
                charset=file.charset,
            )
        return files

    def process_files(self, request, files):
        # rest_api_proxy will hand us the files it found in `request`.
        # We need to replace the unencrypted file by the encrypted version.
        return self.cipher(files)

    def process_response(self, response):
        if not response.content:
            # we are not interested on empty content
            return HttpResponse(status=response.status_code)
        # non-empty content must mean we have an encrypted file.
        fernet = Fernet(settings.CIPHER_KEY)
        decrypted_io = io.BytesIO()
        decrypted_io.write(fernet.decrypt(response.content))
        decrypted_io.seek(0)
        return FileResponse(decrypted_io)
