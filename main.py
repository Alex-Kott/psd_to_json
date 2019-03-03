import json
import sys
import getopt
from typing import Union, Optional, Dict
from uuid import uuid4

from psd_tools import PSDImage
from psd_tools.api.layers import Layer
from psd_tools.api.smart_object import SmartObject
from psd_tools.constants import BlendMode


def extract_layer(layer: Layer) -> Dict[str, str]:
    item = {'id': str(uuid4()),
            'backgroundColor': '',
            'bounds': [layer.right,
                       layer.top,
                       layer.width,
                       layer.height],
            'layername': layer.name,
            'name': layer.name,
            'opacity': layer.opacity,
            'size': {
                'height': layer.height,
                'width': layer.width
            },
            'src': '',
            'type': 'normal',
            'visibility': layer.visible,
            'blendMode': layer.blend_mode.name,
            'position': [layer.left, layer.top]}

    if layer.has_clip_layers():
        item['child_objects'] = []
        for clip_layer in layer.clip_layers:
            item['child_objects'].append(extract_layer(clip_layer))

    return item


def main(input_file: str, output_file: Optional[str] = None):
    image = PSDImage.open(input_file)

    data = {}
    data['layers'] = []
    for layer in image:
        item = extract_layer(layer)
        data['layers'].append(item)

    if output_file:
        with open(output_file, 'w') as file:
            json.dump(data, file)
    else:
        print(json.dumps(data, indent=4, sort_keys=True))


if __name__ == "__main__":
    opts, argv = getopt.getopt(sys.argv[1:], "i:o:")

    input_file_name = None
    output_file_name = None

    for option, value in opts:
        if option == '-i':
            input_file_name = value
        if option == '-o':
            output_file_name = value

    if not input_file_name:
        print('Type input file: -i example.psd')
    else:
        main(input_file_name, output_file_name)
