from io import TextIOWrapper
import re
from typing import Optional
import xml.etree.ElementTree as ET

SENTENCE_PATTERN = re.compile(r"([^\.]+[\.\!\?])")

class SSML:
    def __init__(self, input_bytes: Optional[TextIOWrapper]=None) -> None:
        self.input = input_bytes
        self.value = self.cast(input_bytes) if input_bytes else None
        self.pattern = SENTENCE_PATTERN

    @staticmethod
    def cast(input:TextIOWrapper, speaker:str="en-US-AvaMultilingualNeural", leading_silence:Optional[str]="1s", trailing_silence:Optional[str]="1s", sentence_pattern:re.Pattern=SENTENCE_PATTERN):

        speak = ET.Element(
            "speak",
            attrib={
                "version": "1.0",
                "xmlns": "http://www.w3.org/2001/10/synthesis",
                "xmlns:mstts": "https://www.w3.org/2001/mstts",
                "xml:lang": "en-US",
            },
        )
        voice = ET.SubElement(speak, "voice", attrib={"name": speaker})
        if leading_silence:
            ET.SubElement(
                voice, "mstts:silence", attrib={"type": "Leading", "value": leading_silence}
            )

        if trailing_silence:
            ET.SubElement(
                voice, "mstts:silence", attrib={"type": "Trailing", "value": trailing_silence}
            )

        p = ET.SubElement(voice, "p")

        text = "".join(input).strip()

        sentences = sentence_pattern.findall(text)
        for sentence in sentences:
            s = ET.SubElement(p, "s")
            s.text = sentence.strip()

        # self.value = ET.tostring(speak)
        return ET.tostring(speak)