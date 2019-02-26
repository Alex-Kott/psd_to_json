import sys
import getopt

from psd_tools import PSDImage
from psd_tools.api.layers import SmartObjectLayer


def main(file_name: str):

    image = PSDImage.open(file_name)

    for layer in image:
        if layer.has_clip_layers():
            for i in layer.clip_layers:
                if isinstance(i, SmartObjectLayer):
                    print(i.__dict__)


if __name__ == "__main__":
    opts, argv = getopt.getopt(sys.argv[1:], "i:")

    for option, value in opts:
        if option == '-i':
            file_name = value

    main(file_name)