import sys
import getopt

from psd_tools import PSDImage
from psd_tools.api.layers import SmartObjectLayer


def main(file_name: str):
    image = PSDImage.open(file_name)

    data = {}
    data['layers'] = []
    for layer in image:
        item = {}

        item['backgroundColor'] = ''  # ?
        item['bounds'] = [layer.right,
                          layer.top,
                          layer.width,
                          layer.height]

        item['layername'] = layer.name
        item['name'] = layer.name
        item['opacity'] = layer.opacity
        item['size'] = {
            'height': layer.height,
            'width': layer.width
        }

        item['']


        # if layer.has_clip_layers():
        #     for i in layer.clip_layers:
        #         if isinstance(i, SmartObjectLayer):
        #             print(i.__dict__)
        data['layers'].append(item)


if __name__ == "__main__":
    opts, argv = getopt.getopt(sys.argv[1:], "i:")

    for option, value in opts:
        if option == '-i':
            file_name = value

    main(file_name)
