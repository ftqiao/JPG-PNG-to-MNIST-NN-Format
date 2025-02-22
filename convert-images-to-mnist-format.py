import os
from PIL import Image
from array import *
from random import shuffle

# Load from and save to
Names = [['./training-images', 'train'], ['./test-images', 'test']]

for name in Names:

    data_image = array('H')
    data_label = array('H')

    FileList = []
    for dirname in os.listdir(name[0]):  # [1:] Excludes .DS_Store from Mac OS
        path = os.path.join(name[0], dirname)
        for filename in os.listdir(path):
            if filename.endswith(".png"):
                FileList.append(os.path.join(name[0], dirname, filename))

    shuffle(FileList)  # Usefull for further segmenting the validation set

    for filename in FileList:

        # label = int(filename.split('/')[2])
        label = int(filename.split('\\')[1])

        Im = Image.open(filename).convert('L')

        pixel = Im.load()

        width, height = Im.size

        for x in range(0, width - 1):
            for y in range(0, height - 1):
                data_image.append(pixel[x, y])

        data_label.append(label)  # labels start (one unsigned byte each)

    hexval = "{0:#0{1}x}".format(len(FileList), 10)  # number of files in HEX

    # header for label array

    header = array('H')
    # header.extend([0, 0, 8, 1, 0, 0])
    # header.append(int('0x' + hexval[2:][:2], 16))
    # header.append(int('0x' + hexval[2:][2:], 16))

    header.extend([0, 0, 8, 1])
    header.append(int('0x' + hexval[2:][:2], 16))
    header.append(int('0x' + hexval[4:][:2], 16))
    header.append(int('0x' + hexval[6:][:2], 16))
    header.append(int('0x' + hexval[8:][:2], 16))

    data_label = header + data_label

    # additional header for images array

    # if max([width, height]) <= 256:
    #     header.extend([0, 0, 0, width, 0, 0, 0, height])
    # else:
    #     raise ValueError('Image exceeds maximum size: 256x256 pixels')

    hexval = "{0:#0{1}x}".format(width, 10)  # width in HEX
    header.append(int('0x' + hexval[2:][:2], 16))
    header.append(int('0x' + hexval[4:][:2], 16))
    header.append(int('0x' + hexval[6:][:2], 16))
    header.append(int('0x' + hexval[8:][:2], 16))
    hexval = "{0:#0{1}x}".format(height, 10)  # height in HEX
    header.append(int('0x' + hexval[2:][:2], 16))
    header.append(int('0x' + hexval[4:][:2], 16))
    header.append(int('0x' + hexval[6:][:2], 16))
    header.append(int('0x' + hexval[8:][:2], 16))

    header[3] = 3  # Changing MSB for image data (0x00000803)

    data_image = header + data_image

    output_file = open(name[1] + '-images-idx3-ubyte', 'wb')
    data_image.tofile(output_file)
    output_file.close()

    output_file = open(name[1] + '-labels-idx1-ubyte', 'wb')
    data_label.tofile(output_file)
    output_file.close()

# gzip resulting files

for name in Names:
    os.system('gzip ' + name[1] + '-images-idx3-ubyte')
    os.system('gzip ' + name[1] + '-labels-idx1-ubyte')
