from fastapi import APIRouter, UploadFile, File, HTTPException
# from Services.virtual_tryon_service import handle_virtual_tryon
from Services.idm_vton import handle_virtual_tryon
from Services.detection import detect_faces_and_bodies
from Services.cloth_seg_service import preprocess_image, predict_mask, mask_to_rgb

from PIL import Image
from io import BytesIO
import tempfile
import os
import numpy as np

router = APIRouter()

def save_pil_to_temp(img: Image.Image, suffix=".png") -> str:
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    img.save(tmp_file, format="PNG")
    tmp_file.close()
    return tmp_file.name

def save_upload_file_tmp(upload_file: UploadFile) -> str:
    suffix = os.path.splitext(upload_file.filename)[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(upload_file.file.read())
        return tmp_file.name

def extract_upper_body(original_img: Image.Image, color_mask_img: Image.Image) -> Image.Image:
    color_mask_img = color_mask_img.resize(original_img.size, Image.NEAREST)
    original_np = np.array(original_img)
    mask_np = np.array(color_mask_img)

    red = (255, 0, 0)
    binary_mask = np.all(mask_np == red, axis=-1).astype(np.uint8)
    mask_3ch = np.stack([binary_mask] * 3, axis=-1)

    result_np = original_np * mask_3ch
    return Image.fromarray(result_np)

@router.post("/virtual-tryon")
async def virtual_tryon(
    vton_img: UploadFile = File(...),
    garm_img: UploadFile = File(...)
):
    print("hi_vton")
    temp_path = None
    try:
        garm_img.file.seek(0)
        detection_result = detect_faces_and_bodies(garm_img)
        garm_img.file.seek(0)

        if detection_result["faceDetected"] or detection_result["bodyDetected"]:
            # Step 1: Segment and extract upper body
            tensor, _ = preprocess_image(garm_img)
            mask = predict_mask(tensor)
            color_mask = mask_to_rgb(mask)

            garm_img.file.seek(0)
            original = Image.open(garm_img.file).convert("RGB")
            extracted_upper = extract_upper_body(original, color_mask)

            temp_path = save_pil_to_temp(extracted_upper)
        else:
            temp_path = save_upload_file_tmp(garm_img)

        # Run virtual try-on
        with open(temp_path, "rb") as f:
            temp_upload = UploadFile(filename=os.path.basename(temp_path), file=f)
            result = await handle_virtual_tryon(vton_img, temp_upload)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Virtual try-on failed: {str(e)}")

    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception as cleanup_error:
                print(f"Warning: Could not delete temp file {temp_path}: {cleanup_error}")


# @router.post("/virtual-tryon")
# async def virtual_tryon(
#     vton_img: UploadFile = File(...),
#     garm_img: UploadFile = File(...)
# ):
#     print("hi_vton")
#     temp_path = None
#     vton_temp_path = None  # ✅ new
#     try:
#         garm_img.file.seek(0)
#         detection_result = detect_faces_and_bodies(garm_img)
#         garm_img.file.seek(0)

#         if detection_result["faceDetected"] or detection_result["bodyDetected"]:
#             tensor, _ = preprocess_image(garm_img)
#             mask = predict_mask(tensor)
#             color_mask = mask_to_rgb(mask)

#             garm_img.file.seek(0)
#             original = Image.open(garm_img.file).convert("RGB")
#             extracted_upper = extract_upper_body(original, color_mask)

#             temp_path = save_pil_to_temp(extracted_upper)
#         else:
#             temp_path = save_upload_file_tmp(garm_img)

#         # ✅ Save vton_img to file too
#         vton_temp_path = save_upload_file_tmp(vton_img)

#         # ✅ Pass file paths (strings), not UploadFile objects
#         result = await handle_virtual_tryon(vton_temp_path, temp_path)

#         return result

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Virtual try-on failed: {str(e)}")

#     finally:
#         for p in [temp_path, vton_temp_path]:
#             if p and os.path.exists(p):
#                 try:
#                     os.remove(p)
#                 except Exception as cleanup_error:
#                     print(f"Warning: Could not delete temp file {p}: {cleanup_error}")

