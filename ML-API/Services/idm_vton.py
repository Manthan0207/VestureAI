from gradio_client import Client, file
from PIL import Image
import tempfile
import os
from typing import Union
import base64

# Global client (only initialized once)
client = Client("yisol/IDM-VTON")

# Helper to save PIL image to temporary file
def save_image_to_temp(img: Image.Image) -> str:
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    img.save(tmp_file, format="PNG")
    tmp_file.close()
    return tmp_file.name

# Helper to safely remove file if it exists
def safe_remove(path: Union[str, None]):
    if path and isinstance(path, str) and os.path.exists(path):
        try:
            os.remove(path)
        except Exception as e:
            print(f"Warning: could not remove {path}: {e}")

async def handle_virtual_tryon(vton_img: str, temp_upload: str) -> str:
    """
    vton_path and garm_path must be string paths to image files
    """
    try:
        result = client.predict(
            dict={"background": file(vton_img), "layers": [], "composite": None},
            garm_img=file(temp_upload),
            garment_des="Uploaded via API",
            is_checked=True,
            is_checked_crop=False,
            # denoise_steps=30,
            denoise_steps=20,
            seed=42,
            api_name="/tryon"
        )
        # return result  # usually a URL
        processed_results = []
        for item in result:
            if item.get('image'):
                with open(item['image'], "rb") as img_file:
                    encoded = base64.b64encode(img_file.read()).decode('utf-8')
                    processed_results.append({
                        'image': f"data:image/webp;base64,{encoded}",
                        'caption': item.get('caption')
                    })

        return {"result": processed_results}
    except Exception as e:
        raise RuntimeError(f"IDM-VTON API call failed: {str(e)}")
    finally:
        safe_remove(vton_img)
        safe_remove(temp_upload)


# Use the gradio_client Python library (docs) or the @gradio/client Javascript package (docs) to query the app via API.

# 1. Install the client if you don't already have it installed.

# copy
# $ pip install gradio_client
# 2. Find the API endpoint below corresponding to your desired function in the app. Copy the code snippet, replacing the placeholder values with your own input data. If this is a private Space, you may need to pass your Hugging Face token as well (read more). Run the code, that's it!

# api_name: /tryon
# copy
# from gradio_client import Client, file

# client = Client("yisol/IDM-VTON")
# result = client.predict(
# 		dict={"background":file('https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png'),"layers":[],"composite":null},
# 		garm_img=file('https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png'),
# 		garment_des="Hello!!",
# 		is_checked=True,
# 		is_checked_crop=False,
# 		denoise_steps=30,
# 		seed=42,
# 		api_name="/tryon"
# )
# print(result)
# Accepts 7 parameters:
# dict Dict(background: filepath | None, layers: List[filepath], composite: filepath | None) Required

# The input value that is provided in the "Human. Mask with pen or use auto-masking" Imageeditor component.

# garm_img filepath Required

# The input value that is provided in the "Garment" Image component.

# garment_des str Required

# The input value that is provided in the "parameter_17" Textbox component.

# is_checked bool Default: True

# The input value that is provided in the "Yes" Checkbox component.

# is_checked_crop bool Default: False

# The input value that is provided in the "Yes" Checkbox component.

# denoise_steps float Default: 30

# The input value that is provided in the "Denoising Steps" Number component.

# seed float Default: 42

# The input value that is provided in the "Seed" Number component.

# Returns tuple of 2 elements
# [0] filepath

# The output value that appears in the "Output" Image component.

# [1] filepath

# The output value that appears in the "Masked image output" Image component.

# from gradio_client import Client, file
# from PIL import Image
# import tempfile
# import os
# from typing import Union
# import base64

# client = Client("yisol/IDM-VTON")

# def safe_remove(path: Union[str, None]):
#     if path and isinstance(path, str) and os.path.exists(path):
#         try:
#             os.remove(path)
#         except Exception as e:
#             print(f"Warning: could not remove {path}: {e}")

# async def handle_virtual_tryon(vton_img: str, temp_upload: str) -> dict:
#     """
#     vton_img and temp_upload must be string paths to image files
#     """
#     try:
#         result = client.predict(
#             dict={"background": file(vton_img), "layers": [], "composite": None},
#             garm_img=file(temp_upload),
#             garment_des="Uploaded via API",
#             is_checked=True,
#             is_checked_crop=False,
#             denoise_steps=30,
#             seed=42,
#             api_name="/tryon"
#         )

#         # result = (output_image_path, masked_image_path)
#         print(result)
#         output_base64 = []
#         for image_path in result:
#             if isinstance(image_path, str) and os.path.exists(image_path):
#                 with open(image_path, "rb") as img_file:
#                     encoded = base64.b64encode(img_file.read()).decode('utf-8')
#                     output_base64.append(f"data:image/png;base64,{encoded}")
#         print(len(output_base64))

#         return {"success": True, "result": output_base64 , "res" : result}

#     except Exception as e:
#         raise RuntimeError(f"IDM-VTON API call failed: {str(e)}")

#     finally:
#         safe_remove(vton_img)
#         safe_remove(temp_upload)
