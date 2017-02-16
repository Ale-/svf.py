#!/usr/bin/python
# svf is a python script that generates svg filters for image processing in web design

# Copyright (c) 2016 Ale
# This software is free; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License version 2.1 as published by the Free Software Foundation.
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General
# Public License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330,
# Boston, MA 02111-1307 USA

import sys
import xml.etree.ElementTree as etree

try:
  import tkFileDialog as fd
except ImportError:
  print "You need 'tkFileDialog' module to run this script. Install 'python-tk' package to solve this dependency. \n Try 'sudo apt install python-tk'"
  sys.exit(1)

##
# Formats a string representing a floating point number with a precision of three digits
# @param float_string The string representing the number to format. For instance: "9.89457687999"
# @return A string with three-digit precision. For instance: "9.894"
#

def f(float_string):
    return '%.3f' % float_string

##
# Given a RGB color in hexadecimal representation returns an array with its components as floating point number values
# @param hex_color An hexadecimal representacion of a RGB color. For instance: "#FFFF00"
# return An array with the color components formatted as normalized value strings. For instance: ["1.000", "1.000", "0.000" ]
#

def getColorComponents(hex_color):
    colors = []
    col = int(hex_color, 16)
    colors.append( f(((col >> 16) & 255) / 255.) )
    colors.append( f(((col >>  8) & 255) / 255.) )
    colors.append( f(((col      ) & 255) / 255.) )
    return colors

##
# Main
#

svg = etree.Element("svg")
svg.set("xmlns", "http://www.w3.org/2000/svg")
svg.set("version", "1.1")

def prompt():
    option = raw_input("Add tint filter, duotone filter, save file or exit without saving? [t/d/s/e]: ")
    # (t)int. Creates a svg filter to tint an image using a given spot color and adds it to the resulting svg file.
    if option == 't':
        color = raw_input("Specify a hex color: ")
        svg_filter = etree.Element("filter")
        if(color[0] == '#'): color = color[1::]
        fid = raw_input("Specify an id tag for the filter ('tint_" + color + "'): ")
        if not fid:
            fid = color
        svg_filter.set("id", fid)
        svg.append(svg_filter)
        filter_matrix = etree.Element("feColorMatrix")
        filter_matrix.set("type", "matrix")
        filter_matrix.set("color-interpolation-filters", "sRGB")
        c = getColorComponents( color )
        filter_matrix.set("values", c[0] + " 0 0 0 0 0 " + c[1] + " 0 0 0 0 0 " + c[2] + " 0 0 0 0 0 1 0")
        svg_filter.append(filter_matrix)
        prompt()
    # (d)uotone. Creates a svg filter to create a duotone images using two given spot colors and adds it to the resulting svg file.
    elif option =='d':
        color_first = raw_input("Specify a hex value for dark tones: ")
        if(color_first[0] == '#'): color_first = color_first[1::]
        color_second = raw_input("Specify a hex value for light tones: ")
        if(color_second[0] == '#'): color_second = color_second[1::]
        svg_filter = etree.Element("filter")
        fid = raw_input("Specify an id tag for the filter ('duotone_" + color_first + '_' + color_second + "'): ")
        if not fid:
            fid = 'duotone_' + color_first + '_' + color_second
        svg_filter.set("id", fid)
        svg.append(svg_filter)
        filter_matrix = etree.Element("feColorMatrix")
        filter_matrix.set("type", "matrix")
        filter_matrix.set("values", "1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 0 0 0 1 0")
        c1 = getColorComponents( color_first  )
        c2 = getColorComponents( color_second )
        svg_filter.append(filter_matrix)
        filter_transfer = etree.Element("feComponentTransfer")
        filter_transfer.set("color-interpolation-filters", "sRGB")
        for fe in [('R', c1[0], c2[0]), ('G', c1[1], c2[1]), ('B', c1[2], c2[2]), ('A', "0", "1")]:
            fe_func = etree.Element("feFunc" + fe[0])
            fe_func.set("type", "table")
            fe_func.set("tableValues", fe[1] + " " + fe[2])
            filter_transfer.append(fe_func)
        svg_filter.append(filter_transfer)
        prompt()
    #(s)ave. Saves the resulting SVG file with all previously defined filters.
    elif option =='s':
        svg_tree = etree.ElementTree(svg)
        filename = fd.asksaveasfilename(defaultextension=".svg", title="Save filter file")
        svg_tree.write(filename, encoding="utf-8", xml_declaration=False)
    #(e)xit. Close the script without saving any previously defined filter.
    elif option =='e':
        print "Bye, dear."
        sys.exit(1)
    else:
        print("Please select a valid option.")
        prompt()

prompt()
