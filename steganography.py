"""A program that encodes and decodes hidden messages in images through LSB steganography"""
from PIL import Image, ImageFont, ImageDraw
import textwrap


def decode_image(file_location="/home/sam/Documents/softDes/ToolBoxes/Toolbox-ImageSteganography/images/encoded_sample.png"):
    """Decodes the hidden message in an image file_location: the location of the image file to decode. By default is the provided encoded image in the images folder
    """
    encoded_image = Image.open(file_location)
    red_channel = encoded_image.split()[0]
    im = red_channel.load()
    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]
    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()
    """if (pixb[-1] == '0'):
        print("bit yo")
    else:
        return("lol no")
    """
    for i in range(x_size):
        for j in range(y_size):
            pix = im[i, j]
            pixb = bin(pix) # makes it biniary
            if (pixb[-1] == '0'): # checks if the last bit is a 0
                pixels[i, j] = (0, 0, 0) # makes pxel black
            else:
                pixels[i, j] = (255, 255, 255) # checks it white
    decoded_image.save("/home/sam/Documents/softDes/ToolBoxes/Toolbox-ImageSteganography/images/decoded_image.png")


decode_image()


def write_text(text_to_write, image_size):
    """Writes text to an RGB image. Automatically line wraps

    text_to_write: the text to write to the image
    image_size: size of the resulting text image. Is a tuple (x_size, y_size)
    """
    image_text = Image.new("RGB", image_size)
    print(image_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)

    # Text wrapping. Change parameters for different text formatting
    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin, offset), line, font=font)
        offset += 10
    return image_text


def encode_image(text_to_encode, template_image="images/111.png"):
    """Encodes a text message into an image

    text_to_encode: the text to encode into the template image
    template_image: the image to use for encoding. An image is provided by default.
    """
    temp_image = Image.open(template_image)
    preencode = write_text(text_to_encode, (temp_image.size[0], temp_image.size[1]))
    red_channel = preencode.split()[0]
    encode = Image.new("RGB", preencode.size)
    encodepix = encode.load()
    im = red_channel.load()
    x_size = temp_image.size[0]
    y_size = temp_image.size[1]
    pixelTemp = temp_image.load()
    for i in range(x_size):
        for j in range(y_size):
            pix = im[i, j]
            if (pix == 0): # checks to see if the text image pixel  is black
                encodepix[i, j] = (pixelTemp[i, j][0] & ~1, pixelTemp[i, j][1], pixelTemp[i, j][2]) # changes the LSB of red channel
            elif(pix == 255): # checks to see if the text image pixel is white
                encodepix[i, j] = (pixelTemp[i, j][0] | 1, pixelTemp[i, j][1],  pixelTemp[i, j][2]) # changes LSB of red channel

    encode.save("/home/sam/Documents/softDes/ToolBoxes/Toolbox-ImageSteganography/images/111.png")


if __name__ == '__main__':
    print("Decoding the image...")
    decode_image()
    encode_image("Louis, I think this is the beginning of a beautiful friendship.")
    decode_image("images/111.png")
    # decode_image("images/111.png")
