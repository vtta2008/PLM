#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilities to process and convert svg images to png using palette colors.
"""

# Standard library imports
from __future__ import absolute_import, division, print_function

# Python
import os, re

# Third party imports
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

# PLM
from appData import (STYLE_IMAGE_DIR, IMAGE_BLACKLIST, STYLE_RC_DIR, TMP_DIR, STYLE_SVG_DIR, DarkPalette,
                     TEMPLATE_QRC_FILE, TEMPLATE_QRC_FOOTER, TEMPLATE_QRC_HEADER, QRC_PATH, STYLE_SCSS_PTH)
from cores.Loggers import Loggers
_logger = Loggers(__name__)


def _get_file_color_map(fname, palette):

    color_disabled      = palette.COLOR_BACKGROUND_NORMAL
    color_focus         = palette.COLOR_SELECTION_LIGHT
    color_pressed       = palette.COLOR_SELECTION_NORMAL
    color_normal        = palette.COLOR_FOREGROUND_DARK

    name, ext           = fname.split('.')

    files_map = {
        fname: {
            fname: color_normal,
            name + '_disabled.' + ext: color_disabled,
            name + '_focus.' + ext: color_focus,
            name + '_pressed.' + ext: color_pressed,
        }
    }

    for f, file_colors in files_map.items():
        if f == fname:
            break

    assert file_colors

    return file_colors


def _create_colored_svg(svg_path, temp_svg_path, color):
    with open(svg_path, 'r') as fh:
        data = fh.read()

    base_color = '#ff0000'
    new_data = data.replace(base_color, color)

    with open(temp_svg_path, 'w') as fh:
        fh.write(new_data)


def convert_svg_to_png(svg_path, png_path, height, width):
    size = QSize(height, width)
    icon = QIcon(svg_path)
    pixmap = icon.pixmap(size)
    img = pixmap.toImage()
    img.save(png_path)


def create_palette_image(base_svg_path=STYLE_SVG_DIR, path=STYLE_IMAGE_DIR, palette=DarkPalette):
    _ = QApplication([])

    base_palette_svg_path = os.path.join(base_svg_path, 'base_palette.svg')
    palette_svg_path = os.path.join(path, 'palette.svg')
    palette_png_path = os.path.join(path, 'palette.png')

    _logger.info("Creating palette image ...")
    _logger.info("Base SVG: %s" % base_palette_svg_path)
    _logger.info("To SVG: %s" % palette_svg_path)
    _logger.info("To PNG: %s" % palette_png_path)

    with open(base_palette_svg_path, 'r') as fh:
        data = fh.read()

    color_palette = palette.color_palette()

    for color_name, color_value in color_palette.items():
        data = data.replace('{{ ' + color_name + ' }}', color_value.lower())

    with open(palette_svg_path, 'w+') as fh:
        fh.write(data)

    convert_svg_to_png(palette_svg_path, palette_png_path, 4000, 4000)

    return palette_svg_path, palette_png_path


def create_images(base_svg_path=STYLE_SVG_DIR, rc_path=STYLE_RC_DIR, palette=DarkPalette):
    _ = QApplication([])

    temp_dir = TMP_DIR
    svg_fnames = [f for f in os.listdir(base_svg_path) if f.endswith('.svg')]
    base_height = 32

    heights = {32: '.png', 64: '@2x.png',}
    num_svg = len(svg_fnames)
    num_png = 0
    num_ignored = 0

    # Get rc links from scss to check matches
    rc_list = get_rc_links_from_scss()
    num_rc_list = len(rc_list)

    for height, ext in heights.items():
        width = height

        _logger.debug(" Size HxW (px): %s X %s" % (height, width))

        for svg_fname in svg_fnames:
            svg_name = svg_fname.split('.')[0]

            # Skip blacklist
            if svg_name not in IMAGE_BLACKLIST:
                svg_path = os.path.join(base_svg_path, svg_fname)
                color_files = _get_file_color_map(svg_fname, palette=palette)

                _logger.debug("  Working on: %s"
                              % os.path.basename(svg_fname))

                # Replace colors and create all file for different states
                for color_svg_name, color in color_files.items():
                    temp_svg_path = os.path.join(temp_dir, color_svg_name)
                    _create_colored_svg(svg_path, temp_svg_path, color)

                    png_fname = color_svg_name.replace('.svg', ext)
                    png_path = os.path.join(rc_path, png_fname)
                    convert_svg_to_png(temp_svg_path, png_path, height, width)
                    num_png += 1
                    _logger.debug("   Creating: %s"
                                  % os.path.basename(png_fname))

                    # Check if the rc_name is in the rc_list from scss
                    # only for the base size
                    if height == base_height:
                        rc_base = os.path.basename(rc_path)
                        png_base = os.path.basename(png_fname)
                        rc_name = '/' + os.path.join(rc_base, png_base)
                        try:
                            rc_list.remove(rc_name)
                        except ValueError:
                            pass
            else:
                num_ignored += 1
                _logger.debug("  Ignored blacklist: %s"
                              % os.path.basename(svg_fname))

    _logger.info("# SVG files: %s" % num_svg)
    _logger.info("# SVG ignored: %s" % num_ignored)
    _logger.info("# PNG files: %s" % num_png)
    _logger.info("# RC links: %s" % num_rc_list)
    _logger.info("# RC links not in RC: %s" % len(rc_list))
    _logger.info("RC links not in RC: %s" % rc_list)


def generate_qrc_file(resource_prefix='qss_icons', style_prefix='qdarkstyle'):

    files = []

    _logger.info("Generating QRC file ...")
    _logger.info("Resource prefix: %s" % resource_prefix)
    _logger.info("Style prefix: %s" % style_prefix)

    _logger.info("Searching in: %s" % STYLE_RC_DIR)

    # Search by png images
    for fname in sorted(os.listdir(STYLE_RC_DIR)):
        files.append(TEMPLATE_QRC_FILE.format(fname=fname))

    # Join parts
    qrc_content = (TEMPLATE_QRC_HEADER.format(resource_prefix=resource_prefix)
                   + '\n'.join(files)
                   + TEMPLATE_QRC_FOOTER.format(style_prefix=style_prefix))

    _logger.info("Writing in: %s" % QRC_PATH)

    # Write qrc file
    with open(QRC_PATH, 'w') as fh:
        fh.write(qrc_content)


def get_rc_links_from_scss(pattern=r"\/.*\.png"):

    with open(STYLE_SCSS_PTH, 'r') as fh:
        data = fh.read()

    lines = data.split("\n")
    compiled_exp = re.compile('(' + pattern + ')')

    rc_list = []

    for line in lines:
        match = re.search(compiled_exp, line)
        if match:
            rc_list.append(match.group(1))

    rc_list = list(set(rc_list))

    return rc_list
