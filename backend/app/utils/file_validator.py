import os

ALLOWED_EXTENSIONS = [
    ".pdf",
    ".txt",
    ".docx"
]

MAX_FILE_SIZE = (
    10 * 1024 * 1024
)


def validate_file(
    filename,
    size
):

    extension = os.path.splitext(
        filename
    )[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise Exception(
            "Invalid File Type"
        )

    if size > MAX_FILE_SIZE:
        raise Exception(
            "File Too Large"
        )