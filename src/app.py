from typing import Optional, TypedDict
from io import TextIOWrapper
import os

import click

from ssml import SSML

class SSMLConfigKwargs(TypedDict):
    pattern:Optional[str]=None
    indent:Optional[bool]=None
    lexicon:Optional[str]=None
    speaker:Optional[str]=None
    leading_silence:Optional[str]=None
    trailing_silence:Optional[str]=None

class SSMLConfig(click.Option):
    # TODO: somehow validate the parsed values of the conf file against a typed dict (above)
    def type_cast_value(self, ctx: click.Context, value):
        kwargs:SSMLConfigKwargs = {}
        with open(value, "r") as configfile:
            for line in configfile:
                key,_,val=line.partition("=")
                kwargs[key]=val.strip()
        return kwargs

@click.group
def app():
    pass

@app.command("help")
#TODO @click.option("--config", cls=SSMLConfig)
@click.argument("option", type=click.Choice(("pattern","indent","lexicon","config")))
def help(config:SSMLConfig, option:str):
    click.echo(config)
    match option:
        case "pattern":
            pass
        case "indent":
            pass
        case "lexicon":
            pass
        case "config":
            pass
        case _:
            click.echo("Not a valid help topic", err=True)
        


@app.command()
@click.argument("files", nargs=-1, type=click.File("r"))
@click.option("--sentence-pattern", "-p", "pattern", type=click.STRING, help="RegEx pattern to match sentences. Pattern to match as sentences must be contained within a group")
@click.option("--indent", type=click.BOOL, is_flag=True, default=False, help="Indent SSML tree for pretty-printing.")
@click.option("--lexicon-uri", "lexicon_uri", type=click.STRING, help="")
# TODO @click.option("--config", "-c", cls=SSMLConfig, help="Path to a file specifying SSML configuration. Learn about syntax for the SSML config file with `help config`")
def cast(files:list[TextIOWrapper], pattern:Optional[str]=None, indent:bool=False, lexicon_uri:Optional[str]=None, config:Optional[SSMLConfig]=None):
    stdout = click.get_text_stream("stdout")
    for file in files:
        ssml = SSML.cast("".join(file.readlines()))
        stdout.write(ssml+os.linesep)
    

if __name__ == "__main__":
    app()