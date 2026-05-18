import asyncio
import os
import base64
import random
import time
import hashlib
from pathlib import Path

from PIL import Image

# Import project DB objects by adding src to sys.path
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from core import user_db, classes_db

# Paths
IMAGES_DIR = ROOT / "src" / "files" / "images"
CLASS_IMAGES_DIR = IMAGES_DIR / "classes"
SAMPLE_IMAGE = Path("tests") / "api" / "files" / "image.jpeg"

# Config
NUM_STUDENTS = 10
CLASS_NAMES = ["1A", "1B", "2A"]

FIRST_NAMES = ["Luca", "Marco", "Giulia", "Anna", "Francesco", "Sara", "Alessio", "Marta"]
LAST_NAMES = ["Rossi", "Bianchi", "Verdi", "Ferrari", "Russo", "Esposito"]

async def ensure_dirs():
    os.makedirs(IMAGES_DIR, exist_ok=True)
    os.makedirs(CLASS_IMAGES_DIR, exist_ok=True)

async def add_student(i, sample_image_bytes):
    # generate simple unique id and username
    user_id = int(time.time() * 1000) + i
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    full_name = f"{first} {last}"
    username = f"{first.lower()}{last.lower()}{user_id % 10000}"
    class_name = random.choice(CLASS_NAMES)

    password_hash = "changeme"  # not used for yearbook test

    created = await user_db.add(
        {
            "id": user_id,
            "username": username,
            "password": password_hash,
            "full_name": full_name,
            "class": class_name,
        },
        "username",
    )

    if not created:
        # try a fallback username
        username = f"{username}{random.randrange(1000,9999)}"
        await user_db.add(
            {
                "id": user_id,
                "username": username,
                "password": password_hash,
                "full_name": full_name,
                "class": class_name,
            },
            "username",
        )

    # save image file for profile and class
    image_name = hashlib.sha1(str(user_id).encode()).hexdigest() + ".jpeg"
    image_path = IMAGES_DIR / image_name
    with open(image_path, "wb") as f:
        f.write(sample_image_bytes)

    # update profile_image field as base64 in DB
    encoded = base64.b64encode(sample_image_bytes).decode("ascii")
    await user_db.update("id", user_id, "profile_image", encoded, "$set")

    # ensure class document
    existing_students = await classes_db.get(class_name, "students")
    if existing_students is False:
        await classes_db.add({"name": class_name, "students": [full_name]}, "name")
    else:
        await classes_db.update("name", class_name, "students", full_name, "$push")

    return {"id": user_id, "username": username, "full_name": full_name, "class": class_name}

async def ensure_class_images(sample_image_bytes):
    for c in CLASS_NAMES:
        class_img_path = CLASS_IMAGES_DIR / f"{c}.jpeg"
        if not class_img_path.exists():
            with open(class_img_path, "wb") as f:
                f.write(sample_image_bytes)

async def main():
    await ensure_dirs()

    if not SAMPLE_IMAGE.exists():
        # create a small placeholder JPEG
        img = Image.new("RGB", (200, 200), (120, 180, 200))
        buf = bytearray()
        tmp_path = IMAGES_DIR / "__placeholder__.jpeg"
        img.save(tmp_path, format="JPEG")
        with open(tmp_path, "rb") as f:
            sample_bytes = f.read()
        os.remove(tmp_path)
    else:
        with open(SAMPLE_IMAGE, "rb") as f:
            sample_bytes = f.read()

    created = []
    for i in range(NUM_STUDENTS):
        student = await add_student(i, sample_bytes)
        created.append(student)

    await ensure_class_images(sample_bytes)

    print("Created students:")
    for s in created:
        print(s)

if __name__ == "__main__":
    asyncio.run(main())
