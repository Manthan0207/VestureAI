import os
import shutil
import tempfile
import traceback
import base64

from fastapi import UploadFile, HTTPException
from gradio_client import Client, handle_file

def get_viton_client():
    from gradio_client import Client
    try:
        return Client("BoyuanJiang/FitDiT")
    except Exception as e:
        print(f"Error : {e}")
        return None
client = get_viton_client()


def save_upload_file_tmp(upload_file: UploadFile) -> str:
    suffix = os.path.splitext(upload_file.filename)[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        shutil.copyfileobj(upload_file.file, tmp_file)
        return tmp_file.name

def generate_mask_sync(vton_img_path: str, category: str, offsets: dict):
    return client.predict(
        vton_img=handle_file(vton_img_path),
        category=category,
        offset_top=offsets.get("top", 0),
        offset_bottom=offsets.get("bottom", 0),
        offset_left=offsets.get("left", 0),
        offset_right=offsets.get("right", 0),
        api_name="/generate_mask"
    )

def wrap_pre_mask(pre_mask: dict) -> dict:
    return {
        "background": handle_file(pre_mask.get("background")) if pre_mask.get("background") else None,
        "layers": [handle_file(layer) for layer in pre_mask.get("layers", [])],
        "composite": handle_file(pre_mask.get("composite")) if pre_mask.get("composite") else None,
        "id": pre_mask.get("id")
    }

def process_tryon_sync(vton_img_path: str, garm_img_path: str, pre_mask: dict, pose_image: str, params: dict):
    return client.predict(
        vton_img=handle_file(vton_img_path),
        garm_img=handle_file(garm_img_path),
        pre_mask=wrap_pre_mask(pre_mask),
        pose_image=handle_file(pose_image),
        n_steps=params.get("n_steps", 20),
        image_scale=params.get("image_scale", 2),
        seed=params.get("seed", 0),
        num_images_per_prompt=params.get("num_images_per_prompt", 1),
        resolution=params.get("resolution", "768x1024"),
        api_name="/process"
    )

async def handle_virtual_tryon(vton_img: UploadFile, garm_img: UploadFile):
    vton_img_path = None
    garm_img_path = None

    try:
        vton_img_path = save_upload_file_tmp(vton_img)
        garm_img_path = save_upload_file_tmp(garm_img)

        if not os.path.exists(vton_img_path) or os.path.getsize(vton_img_path) == 0:
            raise ValueError("vton_img file is empty.")
        if not os.path.exists(garm_img_path) or os.path.getsize(garm_img_path) == 0:
            raise ValueError("garm_img file is empty.")

        pre_mask, pose_image = generate_mask_sync(vton_img_path, "Upper-body", {
            "top": 0, "bottom": 0, "left": 0, "right": 0
        })

        if pre_mask is None or pose_image is None:
            raise ValueError("Mask or pose image not generated.")

        result = process_tryon_sync(
            vton_img_path, garm_img_path, pre_mask, pose_image,
            {
                "n_steps": 20,
                "image_scale": 2,
                "seed": 0,
                "num_images_per_prompt": 1,
                "resolution": "768x1024"
            }
        )

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
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    finally:
        for path in [vton_img_path, garm_img_path]:
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except Exception as e:
                    print(f"[WARNING] Could not delete {path}: {e}")


