# ssml

Minimal library for casting text to SSML. 

## Examples

### Code
```py
from ssml import SSML

with open("example.txt", "r") as txt_file:
    text = "".join(txt_file.readlines())
    ssml_text = SSML.cast(text)

with open("example.ssml", "w+") as ssml_file:
    ssml_file.write(ssml_text)

```

### CLI
```sh
py -m ssml.cast example.txt
```