import os,sys,mystring
import matplotlib.pyplot as plt

"""
* [LovelyPlots](https://github.com/killiansheriff/LovelyPlots)
* [SciencePlots](https://github.com/garrettj403/SciencePlots)
"""

styles = {
    "ipynb": "https://raw.githubusercontent.com/killiansheriff/LovelyPlots/master/lovelyplots/styles/ipynb.mplstyle",
    "ipynb_Archive": mystring.string.of("IyBmaWd1cmUgTG9vawpmaWd1cmUuZmlnc2l6ZTogNC41LCAzLjQ2CgpheGVzLmdyaWQ6IEZhbHNlCmZvbnQuc2l6ZTogMTQKCnl0aWNrLmxlZnQ6IFRydWUKeHRpY2suYm90dG9tOiBUcnVlCmltYWdlLmNtYXA6IGluZmVybm8KbGluZXMubWFya2Vyc2l6ZTogNgoKIyB0dXJuIG9uIHNjaWVudGljIG5vdGF0aW9uCmF4ZXMuZm9ybWF0dGVyLmxpbWl0czogLTEsIDEKCiMgc2V0IHRleHQgb2JqZWN0cyBlZGlkYWJsZSBpbiBBZG9iZSBJbGx1c3RyYXRvcgpwZGYuZm9udHR5cGUgOiA0Mgpwcy5mb250dHlwZTogNDIKCiMgbm8gYmFja2dyb3VuZApzYXZlZmlnLnRyYW5zcGFyZW50OiBUcnVlCgojcmVtb3ZlIHdoaXRlIHNwYWNlcwpzYXZlZmlnLmJib3g6IHRpZ2h0CgojIHJlc29sdXRpb24gCmZpZ3VyZS5kcGk6IDQ1MAoKIyBubyBsYXRleCB1c2V0aAp0ZXh0LnVzZXRleDogRmFsc2UKCiMgZGVmYXVsdCBjb2xvciBjeWNsZQpheGVzLnByb3BfY3ljbGUgOiBjeWNsZXIoJ2NvbG9yJywgWyIwMDEyMTkiLCIwMDVmNzMiLCIwYTkzOTYiLCI5NGQyYmQiLCJlOWQ4YTYiLCJlZTliMDAiLCJjYTY3MDIiLCJiYjNlMDMiLCJhZTIwMTIiLCI5YjIyMjYiXSkgKyBjeWNsZXIoJ21hcmtlcicsIFsibyIsIm8iLCJvIiwibyIsIm8iLCJvIiwibyIsIm8iLCJvIiwibyJdKQoKCiMgcmVtb3ZlIGxlZ2VuZCBmcmFtZQpsZWdlbmQuZnJhbWVvbiA6IEZhbHNlCgojIHN2ZyBmb250IHR5cGUKc3ZnLmZvbnR0eXBlOiBub25lCg=="),
    "colorsblind34": "https://raw.githubusercontent.com/killiansheriff/LovelyPlots/master/lovelyplots/styles/colors/colorsblind34.mplstyle",
    "colorsblind34_Archive":mystring.string.of("I1JhaW1ib3cgZGlzY3JldGUgaHR0cHM6Ly9vYnNlcnZhYmxlaHEuY29tL0Bqb3Rhc29sYW5vL3BhdWwtdG9sLXNjaGVtZXMKCmF4ZXMucHJvcF9jeWNsZSA6IGN5Y2xlcignY29sb3InLCBbIkU4RUNGQiIsIkQ5Q0NFMyIsIkQxQkJENyIsIkNBQUNDQiIsIkJBOERCNCIsIkFFNzZBMyIsIkFBNkY5RSIsIjk5NEY4OCIsIjg4MkU3MiIsIjE5NjVCMCIsIjQzN0RCRiIsIjUyODlDNyIsIjYxOTVDRiIsIjdCQUZERSIsIjRFQjI2NSIsIjkwQzk4NyIsIkNBRTBBQiIsIkY3RjA1NiIsIkY3Q0I0NSIsIkY2QzE0MSIsIkY0QTczNiIsIkYxOTMyRCIsIkVFODAyNiIsIkU4NjAxQyIsIkU2NTUxOCIsIkRDMDUwQyIsIkE1MTcwRSIsIjcyMTkwRSIsIjQyMTUwQSJdKQ=="),
    "science":"https://raw.githubusercontent.com/garrettj403/SciencePlots/master/scienceplots/styles/science.mplstyle",
    "science_Archive":mystring.string.of("IyBNYXRwbG90bGliIHN0eWxlIGZvciBzY2llbnRpZmljIHBsb3R0aW5nCiMgVGhpcyBpcyB0aGUgYmFzZSBzdHlsZSBmb3IgIlNjaWVuY2VQbG90cyIKIyBzZWU6IGh0dHBzOi8vZ2l0aHViLmNvbS9nYXJyZXR0ajQwMy9TY2llbmNlUGxvdHMKCiMgU2V0IGNvbG9yIGN5Y2xlOiBibHVlLCBncmVlbiwgeWVsbG93LCByZWQsIHZpb2xldCwgZ3JheQpheGVzLnByb3BfY3ljbGUgOiBjeWNsZXIoJ2NvbG9yJywgWycwQzVEQTUnLCAnMDBCOTQ1JywgJ0ZGOTUwMCcsICdGRjJDMDAnLCAnODQ1Qjk3JywgJzQ3NDc0NycsICc5ZTllOWUnXSkKCiMgU2V0IGRlZmF1bHQgZmlndXJlIHNpemUKZmlndXJlLmZpZ3NpemUgOiAzLjUsIDIuNjI1CgojIFNldCB4IGF4aXMKeHRpY2suZGlyZWN0aW9uIDogaW4KeHRpY2subWFqb3Iuc2l6ZSA6IDMKeHRpY2subWFqb3Iud2lkdGggOiAwLjUKeHRpY2subWlub3Iuc2l6ZSA6IDEuNQp4dGljay5taW5vci53aWR0aCA6IDAuNQp4dGljay5taW5vci52aXNpYmxlIDogVHJ1ZQp4dGljay50b3AgOiBUcnVlCgojIFNldCB5IGF4aXMKeXRpY2suZGlyZWN0aW9uIDogaW4KeXRpY2subWFqb3Iuc2l6ZSA6IDMKeXRpY2subWFqb3Iud2lkdGggOiAwLjUKeXRpY2subWlub3Iuc2l6ZSA6IDEuNQp5dGljay5taW5vci53aWR0aCA6IDAuNQp5dGljay5taW5vci52aXNpYmxlIDogVHJ1ZQp5dGljay5yaWdodCA6IFRydWUKCiMgU2V0IGxpbmUgd2lkdGhzCmF4ZXMubGluZXdpZHRoIDogMC41CmdyaWQubGluZXdpZHRoIDogMC41CmxpbmVzLmxpbmV3aWR0aCA6IDEuCgojIFJlbW92ZSBsZWdlbmQgZnJhbWUKbGVnZW5kLmZyYW1lb24gOiBGYWxzZQoKIyBBbHdheXMgc2F2ZSBhcyAndGlnaHQnCnNhdmVmaWcuYmJveCA6IHRpZ2h0CnNhdmVmaWcucGFkX2luY2hlcyA6IDAuMDUKCiMgVXNlIHNlcmlmIGZvbnRzCiMgZm9udC5zZXJpZiA6IFRpbWVzCmZvbnQuZmFtaWx5IDogc2VyaWYKbWF0aHRleHQuZm9udHNldCA6IGRlamF2dXNlcmlmCgojIFVzZSBMYVRlWCBmb3IgbWF0aCBmb3JtYXR0aW5nCnRleHQudXNldGV4IDogVHJ1ZQp0ZXh0LmxhdGV4LnByZWFtYmxlIDogXHVzZXBhY2thZ2V7YW1zbWF0aH0gXHVzZXBhY2thZ2V7YW1zc3ltYn0="),
    "ieee": "https://raw.githubusercontent.com/garrettj403/SciencePlots/master/scienceplots/styles/journals/ieee.mplstyle",
    "ieee_Archive":mystring.string.of("IyBNYXRwbG90bGliIHN0eWxlIGZvciBJRUVFIHBsb3RzCiMgVGhpcyBzdHlsZSBzaG91bGQgd29yayBmb3IgbW9zdCB0d28tY29sdW1uIGpvdXJuYWxzCgojIFNldCBjb2xvciBjeWNsZQojIFNldCBsaW5lIHN0eWxlIGFzIHdlbGwgZm9yIGJsYWNrIGFuZCB3aGl0ZSBncmFwaHMKYXhlcy5wcm9wX2N5Y2xlIDogKGN5Y2xlcignY29sb3InLCBbJ2snLCAncicsICdiJywgJ2cnXSkgKyBjeWNsZXIoJ2xzJywgWyctJywgJy0tJywgJzonLCAnLS4nXSkpCgojIFNldCBkZWZhdWx0IGZpZ3VyZSBzaXplCmZpZ3VyZS5maWdzaXplIDogMy4zLCAyLjUKZmlndXJlLmRwaSA6IDYwMAoKIyBGb250IHNpemVzCmZvbnQuc2l6ZSA6IDgKZm9udC5mYW1pbHkgOiBzZXJpZgpmb250LnNlcmlmIDogVGltZXM=")
}

def reset():
    import matplotlib as mpl
    mpl.rcParams.update(mpl.rcParamsDefault)
    try:
        from IPython import get_ipython
        ipython = get_ipython()
        ipython.magic("matplotlib inline")
    except:pass

def flatten(column_header):
    if isinstance(column_header, list) or isinstance(column_header, tuple):
        return ' '.join([str(ch) for ch in column_header]).strip()
    return column_header

def get_styles(folder="styles", style=None, use_archive=True):
    output = {}
    if not os.path.exists(folder):
        try:os.system("mkdir {0}".format(folder))
        except:pass

    for key,value in styles.items():
        if style is None or style == key:
            file_name = os.path.basename(value)+".mplstyle"
            file_loc = os.path.join(folder,file_name)

            if not os.path.exists(file_loc):
                if use_archive:
                    with open(file_loc, "w+") as writer:
                        writer.write(value["Archive"])
                else:
                    import urllib.request
                    urllib.request.urlretrieve(value["Link"], file_name)
                    try:os.system("mv {0} {1}".format(file_name, file_loc))
                    except:pass
    
            output[key] = os.path.abspath(file_loc)
    return output
