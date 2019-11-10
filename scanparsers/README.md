### place new parsers in this folder
### add the following statement to the autoreconParser.py script in the parent directory (follow the naming convention, it makes tracking which parsers you have much easier)
```
from scanparsers.YOURNEWPARSER import YOURNEWPARSERFUNCTION
```
### then add a write statement somewhere in the body of autoreconParser.py (both regular functions and generators are present, just copy the syntax)
