import requests
import os 
API_URL = "https://api-inference.huggingface.co/models/alvdansen/phantasma-anime"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content
image_bytes = query({
	"inputs": "calm nature",
})
# You can access the image with PIL.Image for example
import io
from PIL import Image
image = Image.open(io.BytesIO(image_bytes))

