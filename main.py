import json
import sys
import getopt
from typing import Union
from uuid import uuid4

from psd_tools import PSDImage
from psd_tools.api.layers import Layer
from psd_tools.api.smart_object import SmartObject
from psd_tools.constants import BlendMode


def extract_layer(layer: Layer):
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


def main(file_name: str):
    image = PSDImage.open(file_name)

    data = {}
    data['layers'] = []
    for layer in image:

        # print(layer.blend_mode.name)
        # if isinstance(layer, SmartObject):
        #     print(layer.__dict__)

        item = extract_layer(layer)

        # if layer.has_clip_layers():
        #     for i in layer.clip_layers:
        #         if isinstance(i, SmartObjectLayer):
        #             print(i.__dict__)
        data['layers'].append(item)

    print(json.dumps(data, indent=4, sort_keys=True))


if __name__ == "__main__":
    opts, argv = getopt.getopt(sys.argv[1:], "i:")

    for option, value in opts:
        if option == '-i':
            file_name = value

    main(file_name)
