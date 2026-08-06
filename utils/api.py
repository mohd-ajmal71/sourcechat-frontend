import requests
from utils.config import BACKEND_URL


def upload_pdf(files):
    url = f"{BACKEND_URL}/upload"

    data = []

    for file in files:
        data.append(
            (
                "files",
                (file.name, file.getvalue(), "application/pdf")
            )
        )

    response = requests.post(url, files=data)

    return response.json()