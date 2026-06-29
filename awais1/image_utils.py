import uuid
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps

# Stored under static/ so the existing /static mount serves them.
PROFILE_PICS_DIR = Path("awais1/static/profile_pics")

# Public URL path (matches app.mount("/static", ...) in main.py)
PROFILE_PICS_URL = "/static/profile_pics"

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_IMAGE_BYTES = 5 * 1024 * 1024  # 5 MB


def process_profile_image(content: bytes) -> str:
    """Validate, normalize and store an uploaded image. Returns the filename.

    Raises PIL.UnidentifiedImageError if the bytes are not a valid image.
    """
    with Image.open(BytesIO(content)) as original:
        # Verify the image is decodable (corrupt files raise here on load).
        img = ImageOps.exif_transpose(original)

        # Crop+resize to a fixed square thumbnail.
        img = ImageOps.fit(img, (300, 300), method=Image.Resampling.LANCZOS)

        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")

        filename = f"{uuid.uuid4().hex}.jpg"
        filepath = PROFILE_PICS_DIR / filename

        PROFILE_PICS_DIR.mkdir(parents=True, exist_ok=True)

        img.save(filepath, "JPEG", quality=85, optimize=True)

    return filename


def delete_profile_image(filename: str | None) -> None:
    if not filename:
        return

    filepath = PROFILE_PICS_DIR / filename
    if filepath.exists():
        filepath.unlink()
