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

    metadata['labels'] = {}
    metadata['labels']['series'] = []

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
                metadata['labels']['series'].append(tokens[-1])
            elif _re_axis.match(tokens[0]):
                if "label" in tokens:
                    if tokens[0] == "xaxis":
                        metadata['labels']["xaxis"] = tokens[-1]
                    else:
                        metadata['labels']["yaxis"] = tokens[-1]
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
