import json
import re
import sys
import getopt
from typing import Union, Optional, Dict, Tuple
from uuid import uuid4

from psd_tools import PSDImage
from psd_tools.api.layers import Layer, SmartObjectLayer
from psd_tools.api.smart_object import SmartObject
from psd_tools.constants import BlendMode
from psd_tools.psd.layer_and_mask import LayerRecord
from psd_tools.psd.tagged_blocks import TaggedBlock, PlacedLayerData


def truncate_prefix(name: str) -> str:
    return re.sub('mm_[^:]+:', '', name)


def get_transformation_dots(layer: Layer):
    if layer.has_clip_layers():
        for clip_layer in layer.clip_layers:
            coords = extract_smart_object(clip_layer)

            if coords is not None:
                if len(coords) > 0:
                    return coords


def extract_layer(layer: Layer) -> Dict[str, str]:
    item = {'id': str(uuid4()),
            'backgroundColor': '',
            'bounds': [layer.right,
                       layer.top,
                       layer.width,
                       layer.height],
            'layername': layer.name,
            'name': truncate_prefix(layer.name),
            'opacity': layer.opacity,
            'size': {
                'height': layer.height,
                'width': layer.width
            },
            'src': '',
            'type': 'normal',
            'visibility': layer.visible,
            'blendMode': layer.blend_mode.name,
            'position': {
                'x': layer.left,
                'y': layer.top
            },
            'transformation_dots': get_transformation_dots(layer)}

    if layer.has_clip_layers():
        item['child_objects'] = []
        for clip_layer in layer.clip_layers:
            item['child_objects'].append(extract_layer(clip_layer))

    return item


def unpack_placed_layer_data(item: PlacedLayerData) -> Tuple[float]:
    return item.transform


def unpack_tagged_block(block: TaggedBlock) -> Tuple[float]:
    if type(block.data) is PlacedLayerData:
        coords = unpack_placed_layer_data(block.data)

        if coords is not None:
            if len(coords) > 0:
                return coords


def extract_transformation_points(record: LayerRecord):
    for tagged_block_id, tagged_block in record.tagged_blocks.items():
        coords = unpack_tagged_block(tagged_block)

        if coords is not None:
            if len(coords) > 0:
                return coords


def extract_smart_object(layer: SmartObjectLayer):
    coords = extract_transformation_points(layer._record)

    if coords is not None:
        if len(coords) > 0:
            return coords


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
