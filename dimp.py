from monsterapi import client
import base64 
import requests
import random
api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImY5Y2YxMTgyNjJlMDkyM2EzY2UyYjFjYjhiZmI2MGFmIiwiY3JlYXRlZF9hdCI6IjIwMjQtMDctMDRUMTE6NDM6MDIuMjM4OTkxIn0.pO5nxO6lX6P94GuH8jHJjhYS9ar1vtn3MEHxz8nCpQk'  
monster_client = client(api_key)

model = 'txt2img'  
random_seed = random.randint(1, 10000)  

input_data = {
'prompt': 'anime character (single color background) ',
'negprompt': 'deformed, bad anatomy, disfigured, poorly drawn face',
'samples': 1,
'steps': 50,
'aspect_ratio': 'square',
'guidance_scale': 7.5,
'seed': random_seed,
            }
result = monster_client.generate(model, input_data)

image_filename = "generated_image.png"
image_data = result['output'][0]

if image_data.startswith("http"):
    # Handle the case where it's a URL
    image_filename = "generated_image.png"
    response = requests.get(image_data)
    with open(image_filename, "wb") as f:
        f.write(response.content)
    print(f"Image saved as {image_filename}")
else:
    # Assuming it's base64, handle padding issues
    missing_padding = len(image_data) % 4
    if missing_padding:
        image_data += '=' * (4 - missing_padding)

    # Decode and save the base64 image
    image_filename = "generated_image.png"
    with open(image_filename, "wb") as f:
        f.write(base64.b64decode(image_data))
    print(f"Image saved as {image_filename}")