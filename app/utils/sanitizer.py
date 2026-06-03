import re

def clean_text(text):

    text = re.sub(
        r"<.*?>",
        "",
        text
    )

    return text.strip()