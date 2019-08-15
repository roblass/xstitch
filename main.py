#!/usr/bin/env python

import argparse
import random
from os import listdir
from os.path import isfile, join

from PIL import Image, ImageDraw


class Picture:
    def __init__(self, step_count, height, width):
        self.step_count = step_count
        self.height = height
        self.width = width

        self.image = Image.new('RGB', (self.width, self.height), (0, 0, 0))

        # draw initial grid
        self.draw = ImageDraw.Draw(self.image)
        y_start = 0
        y_end = self.image.height
        step_size = int(self.width / self.step_count)

        for x in range(0, self.width, step_size):
            line = ((x, y_start), (x, y_end))
            self.draw.line(line, fill=(0, 0, 0))

        x_start = 0
        x_end = self.width

        for y in range(0, self.height, step_size):
            line = ((x_start, y), (x_end, y))
            self.draw.line(line, fill=(0, 0, 0))

    def show(self):
        self.image.show()

    def fill_tile(self, tile_x, tile_y, color):
        step_size = int(self.width / self.step_count)

        # draw top left to bottom right
        x_start = tile_x * step_size + 1
        x_end = (tile_x + 1) * step_size - 1

        y_start = tile_y * step_size + 1
        y_end = (tile_y + 1) * step_size - 1

        line = ((x_start, y_start), (x_end, y_end))
        self.draw.line(line, fill=color, width=3)

        # draw top right to bottom left
        x_start = (tile_x + 1) * step_size - 1
        x_end = tile_x * step_size + 1

        y_start = tile_y * step_size + 1
        y_end = (tile_y + 1) * step_size - 1

        line = ((x_start, y_start), (x_end, y_end))
        self.draw.line(line, fill=color, width=3)

    def draw_xsp(self, top_x, top_y, filename, color):
        """Assumes the letter pattern lines are fixed width."""
        data = open(filename, 'r').read()
        max_x = 0
        y_offset = 0
        for line in data.split('\n'):
            x_offset = 0
            for char in line:
                if char != ' ':
                    self.fill_tile(top_x + x_offset, top_y + y_offset, color)
                x_offset += 1
            if x_offset > max_x:
                max_x = x_offset
            y_offset += 1

        return max_x, y_offset

    def draw_letter(self, top_x, top_y, letter, color):
        return self.draw_xsp(top_x, top_y, 'patterns/{letter}.xsp'.format(letter=letter), color)

    def draw_phrase(self, top_x, top_y, phrase, color):
        x = top_x
        y = top_y
        for letter in phrase:
            if letter == ' ':
                x += 4
                continue
            x_offset, _ = self.draw_letter(x, y, letter, color)
            x += x_offset


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("width", help="width of image in pixels",
                        type=int)
    parser.add_argument("height", help="height of image in pixels",
                        type=int)
    parser.add_argument("step_count", help="how many steps across the grid",
                        type=int)
    parser.add_argument("message", help="the message to display",
                        type=str)
    parser.add_argument("--input_filename", help="input image filename to use (optional)",
                        type=str, default=None, required=False)
    parser.add_argument("-s", help="open and display the image if set",
                        action="store_true")
    args = parser.parse_args()

    _step_count = args.step_count
    _height = args.height
    _width = args.width
    _message = args.message
    _filename = args.input_filename
    _show = args.s

    if _filename is None: # pick an image at random, filter out letters and non-xsp files
        files = ['patterns/' + f for f in listdir('patterns') if isfile(join('patterns', f)) and
                 len(f) > 5]
        files = [f for f in files if f.endswith('xsp')]
        _filename = random.choice(files)


    p = Picture(_step_count, _height, _width)

    for _x in range(_width):
        for _y in range(_height):
            p.fill_tile(_x, _y, (255, 255, 255))
    p.draw_phrase(10, 10, _message, (255, 0, 0))
    p.draw_xsp(110, 20, _filename, (0, 0, 255))
    if _show:
        p.show()
    p.image.save('output.png')
