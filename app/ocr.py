import easyocr
import tempfile
import os

# =====================================
# OCR Reader
# =====================================

reader = easyocr.Reader(
    ["en"],
    gpu=False
)

# =====================================
# Common OCR Noise
# =====================================

NOISE_WORDS = {

    "users",
    "desktop",
    "onedrive",
    "downloads",
    "documents",
    "pictures",
    "videos",

    "visual studio code",
    "explorer",
    "search",
    "run",
    "terminal",
    "output",
    "debug",
    "extensions",

    "python",
    "powershell",

    "file",
    "edit",
    "selection",
    "view",
    "go",
    "help"
}


# =====================================
# OCR Text Cleaner
# =====================================

def clean_ocr_text(text: str) -> str:

    cleaned_lines = []

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        # Remove obvious noise
        if any(
            noise in line.lower()
            for noise in NOISE_WORDS
        ):
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


# =====================================
# OCR Extraction
# =====================================

def extract_code_from_image(
    image_bytes: bytes
) -> str:

    with tempfile.NamedTemporaryFile(
        suffix=".png",
        delete=False
    ) as tmp:

        tmp.write(image_bytes)

        temp_path = tmp.name

    try:

        results = reader.readtext(
            temp_path,
            detail=1
        )

        extracted_lines = []

        for _, text, confidence in results:

            # Skip weak detections
            if confidence < 0.70:
                continue

            extracted_lines.append(text)

        raw_text = "\n".join(
            extracted_lines
        )

        cleaned_text = clean_ocr_text(
            raw_text
        )

        return cleaned_text

    finally:

        if os.path.exists(
            temp_path
        ):
            os.remove(
                temp_path
            )