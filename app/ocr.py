import easyocr
from PIL import Image
import tempfile

reader = easyocr.Reader(
    ["en"]
)

def extract_code_from_image(
    image_bytes
):

    with tempfile.NamedTemporaryFile(
        suffix=".png"
    ) as tmp:

        tmp.write(image_bytes)
        tmp.flush()

        lines = reader.readtext(
            tmp.name,
            detail=0
        )

    return "\n".join(lines)