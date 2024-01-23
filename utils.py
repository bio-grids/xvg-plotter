import re
import shlex
import sys
import typing

import numpy as np
import numpy.typing as npt


class Labels(typing.TypedDict):
    xaxis: str
    yaxis: str
    series: list[str]


class Metadata(typing.TypedDict):
    title: str
    labels: Labels


def parse_xvg(data: str, columns: list[int] | None = None) -> tuple[Metadata, npt.NDArray]:
    _ignored = {'legend', 'view'}
    _re_series = re.compile('s[0-9]+$')
    _re_axis = re.compile('[xy]axis$')

    metadata: Metadata = {}
    num_data = []

    metadata['labels'] = {
        "xaxis": "",
        "yaxis": "",
        "series": [],
    }

    for line in data.split("\n"):
        line = line.strip()

        if line.startswith("@"):
            tokens = shlex.split(line[1:])

            if tokens[0] in _ignored:
                continue
            elif tokens[0] == "TYPE":
                if tokens[1] != 'xy':
                    print("Unsupported")
            elif _re_series.match(tokens[0]):
                metadata['labels']['series'].append(clean_label(tokens[-1]))
            elif _re_axis.match(tokens[0]):
                if "label" in tokens:
                    if tokens[0] == "xaxis":
                        metadata['labels']["xaxis"] = clean_label(tokens[-1])
                    else:
                        metadata['labels']["yaxis"] = clean_label(tokens[-1])
            elif len(tokens) == 2:
                if tokens[0] == "title":
                    metadata["title"] = tokens[1]
            else:
                print('Unsupported entry: {0} - ignoring'.format(tokens[0]), file=sys.stderr)

        elif len(line) and line[0].isdigit():
            num_data.append(list(map(float, line.split())))

    data: npt.NDArray = np.array(num_data)

    if len(metadata['labels']['series']) < 1:
        for index, series in enumerate(list(range(data.shape[1] - 1))):
            metadata['labels']['series'].append(f"Series {index + 1}")

    if columns:
        sel_columns = [0] + list(map(lambda x: int(x + 1), columns))
        data = data[..., sel_columns]

        metadata['labels']['series'] = [metadata['labels']['series'][col - 1] for col in sel_columns[1:]]

    return metadata, data


legend_locations = [
    "best", "upper right", "upper left", "lower left", "lower right", "right", "center left", "center right",
    "lower center", "upper center", "center"
]


def clean_label(string):
    """Parses Grace label syntax into LaTeX"""

    substring = string
    chunks = []

    while substring:
        for key in _all_codes:
            if substring.startswith(key):
                chunks.append(key)
                substring = substring[len(key):]
                break

        else:
            chunks.append(substring[0])
            substring = substring[1:]

    chunks = [c for c in chunks if c not in _ignorable_codes]

    string = ''

    # sub/superscripts
    for chunk in chunks:
        if chunk == "\\s":
            string += r'}_{\text{'
        elif chunk == "\\S":
            string += r'}^{\text{'
        elif chunk == "\\N" or chunk == "\\v{}\\z{}":
            string += r'}}\text{'
        else:
            string += chunk

    string = r'$\text{' + string + '}$'

    return string


_font_codes = {
    "\\f{x}": 'switch to font named "x"',
    "\\f{n}": 'switch to font number n',
    "\\f{}": 'return to original font',
    "\\x": 'switch to Symbol font (same as \\f{Symbol})',
}

_color_codes = {
    "\\R{x}": 'switch to color named "x"',
    "\\R{n}": 'switch to color number n',
    "\\R{}": 'return to original color',
}

_style_codes = {
    "\\u": 'begin underline',
    "\\U": 'stop underline',
    "\\o": 'begin overline',
    "\\O": 'stop overline',
    "\\q": 'make font oblique (same as \\l{0.25})',
    "\\Q": 'undo oblique (same as \\l{-0.25})',
}

_script_codes = {
    "\\s": 'begin subscripting (same as \\v{-0.4}\\z{0.71})',
    "\\S": 'begin superscripting (same as \\v{0.6}\\z{0.71})',
    "\\N": 'return to normal style (same as \\v{}\\t{})',
    "\\v{}\\z{}": 'return to normal style',
}

_other_codes = {
    "\\#{x}": 'treat "x" (must be of even length) as list of hexadecimal char codes',
    "\\t{xx xy yx yy}": 'apply transformation matrix',
    "\\t{}": 'reset transformation matrix',
    "\\z{x}": 'zoom x times',
    "\\z{}": 'return to original zoom',
    "\\r{x}": 'rotate by x degrees',
    "\\l{x}": 'slant by factor x',
    "\\v{x}": 'shift vertically by x',
    "\\v{}": 'return to unshifted baseline',
    "\\V{x}": 'shift baseline by x',
    "\\V{}": 'reset baseline',
    "\\h{x}": 'horizontal shift by x',
    "\\n": 'new line',
    "\\Fk": 'enable kerning',
    "\\FK": 'disable kerning',
    "\\Fl": 'enable ligatures',
    "\\FL": 'disable ligatures',
    "\\m{n}": 'mark current position as n',
    "\\M{n}": 'return to saved position n',
    "\\dl": 'LtoR substring direction',
    "\\dr": 'RtoL substring direction',
    "\\dL": 'LtoR text advancing',
    "\\dR": 'RtoL text advancing',
    "\\+": 'increase size (same as \\z{1.19} ; 1.19 = sqrt(sqrt(2)))',
    "\\-": 'decrease size (same as \\z{0.84} ; 0.84 = 1/sqrt(sqrt(2)))',
    "\\T{xx xy yx yy}": 'same as \\t{}\\t{xx xy yx yy}',
    "\\Z{x}": 'absolute zoom x times (same as \\z{}\\z{x})',
    "\\\\": 'print \\',
    "\\c": 'begin using upper 128 characters of set (deprecated)',
    "\\C": 'stop using upper 128 characters of set (deprecated)',
}

_ignorable_codes = _font_codes | _color_codes | _style_codes | _other_codes
_all_codes = _script_codes | _font_codes | _style_codes | _color_codes | _other_codes
