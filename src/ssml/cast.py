from typing import Optional, TypedDict
from io import TextIOWrapper
import os

import click

from ssml import SSML


class SSMLConfigKwargs(TypedDict):
    pattern: Optional[str] = None
    indent: Optional[bool] = None
    lexicon: Optional[str] = None
    speaker: Optional[str] = None
    leading_silence: Optional[str] = None
    trailing_silence: Optional[str] = None

@click.command()
@click.argument("files", nargs=-1, type=click.File("r", encoding="utf-8"), required=True)
@click.option("--indent", type=click.BOOL, is_flag=True, default=False, help="Indent SSML tree for pretty-printing.",)
@click.option("--lexicon-uri", type=click.STRING, help="URI to a custom lexicon.")
@click.option("--speaker", type=click.STRING, default="en-US-AvaMultilingualNeural", help="Azure AI voice to use.")
def cast(
    files: tuple[TextIOWrapper],
    indent: bool = False,
    lexicon_uri: Optional[str] = None,
    speaker:Optional[str]="en-US-AvaMultilingualNeural",
    # config: Optional[SSMLConfig] = None,
):
    stdout = click.get_text_stream("stdout")
    for file in files:
        ssml = SSML.cast("".join(file.readlines()), indent=indent, lexicon_uri=lexicon_uri, speaker=speaker)
        stdout.write(ssml+os.linesep)

if __name__ == '__main__':
    cast()