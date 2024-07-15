from io import TextIOWrapper
import re
from typing import Optional
import xml.etree.ElementTree as ET

SENTENCE_PATTERN = re.compile(r"([^\.]+[\.\!\?])")
SSML_NAMESPACES = {"":"http://www.w3.org/2001/10/synthesis", "mstts":"https://www.w3.org/2001/mstts"}

class SSML:
    def __init__(self, input_bytes: Optional[TextIOWrapper] = None) -> None:
        self.input = input_bytes
        self.value = self.cast(input_bytes) if input_bytes else None
        self.pattern = SENTENCE_PATTERN

    @staticmethod
    def cast(
        input: TextIOWrapper,
        sentence_pattern: re.Pattern = SENTENCE_PATTERN,
        indent:bool=False,
        speaker: str = "en-US-AvaMultilingualNeural",
        leading_silence: Optional[str] = "1s",
        trailing_silence: Optional[str] = "1s",
    )->str:
        """Cast text input into an SSML hierarchy.

        :param input: TextIOWrapper text to cast to SSML
        :param sentence_pattern: re.Pattern Regex pattern used to split text to sentences.
        :param speaker: str Azure Speech Services voice to use for generation. Default = "en-US-AvaMultilingualNeural"
        :param leading_silence: str (optional) Length of leading silence. Default = "1s"
        :param trailing_silence: str (optional) Length of trailing silence. Default = "1s"
        :returns: SSML hierarchy as string
        """

        # Set up speak element with required attributes
        speak = ET.Element(
            "speak",
            attrib={
                "version": "1.0",
                "xmlns": "http://www.w3.org/2001/10/synthesis",
                "xmlns:mstts": "https://www.w3.org/2001/mstts",
                "xml:lang": "en-US",
            },
        )

        # Specify voice element with required Azure Speech services voice 
        voice = ET.SubElement(speak, "voice", attrib={"name": speaker})

        # Add optional leading silence
        if leading_silence:
            ET.SubElement(
                voice,
                "mstts:silence",
                attrib={"type": "Leading", "value": leading_silence},
            )

        # Add optional trailing silence
        if trailing_silence:
            ET.SubElement(
                voice,
                "mstts:silence",
                attrib={"type": "Trailing", "value": trailing_silence},
            )

        # Paragraph element
        p = ET.SubElement(voice, "p")

        # Join TextIOWrapper to string
        text = "".join(input).strip()

        # Find all sentences
        sentences = sentence_pattern.findall(text)
        
        # Join each sentence as <s> element to root paragraph
        for sentence in sentences:
            s = ET.SubElement(p, "s")
            s.text = sentence.strip()

        # Optionally indent XML for pretty printing
        if indent:
            ET.indent(speak)

        # deserialize ElementTree to string
        return ET.tostring(speak, encoding="unicode")
    
    @staticmethod
    def modify(input:TextIOWrapper , 
        speaker: str = "en-US-AvaMultilingualNeural",
        lexicon_uri:Optional[str]=None)->str:
        """Modify the speaker or lexicon of an existing SSML file
        :param input TextIOWrapper:         File containing the SSML hierarchy to modify
        :param speaker str:                 MS Azure Voice to replace the original voice with.
        :param lexicon_uri str:             [Optional] lexicon URI to add or substitute.    
        """
                # Register SSML namespaces
        for namespace in SSML_NAMESPACES.items():
            ET.register_namespace(*namespace)


        tree = ET.parse(input)
        
        # Find elements of interest
        voice = tree.find(".//voice", SSML_NAMESPACES)
        lexicon = voice.find(".//lexicon", SSML_NAMESPACES)

        if speaker:
            if voice.attrib["name"] == speaker:
                # Do nothing if the voices are equivalent
                pass
            else: 
                voice.attrib["name"] = speaker

        if lexicon_uri:
            # Remove the original lexicon if it already exists
            if lexicon:
                voice.remove(lexicon)
            ET.SubElement(voice ,"lexicon", attrib={"uri":lexicon_uri})

        return ET.tostring(tree.getroot(), encoding="unicode")
