import xml.etree.ElementTree as ElementTree
import os, re
from xml.etree.ElementTree import Element, SubElement, Comment
from xml.dom import minidom
from tkinter import filedialog
from tkinter import Tk

# Return a pretty-printed XML string for the Element.
def prettify(elem):
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

#######################################################
# Open FPL file and get root
currentDir = os.getcwd()
fplFileName = filedialog.askopenfilename(initialdir = currentDir, title='Select FPL file', filetypes = (("fpl files","*.fpl"),("all files","*.*")))

fplTree = ElementTree.parse(fplFileName)
fplRoot = fplTree.getroot()
waypointTable = fplRoot[3]
#######################################################

#######################################################
# Store lats and lons in lists, then create string with them combined
lats = []
lons = []
latLonString = ''

for child in waypointTable:
    lats.append(child[2].text)
    lons.append(child[3].text)

for x in range(len(lats)):
    latLonString = latLonString + lons[x] + ','
    latLonString = latLonString + lats[x] + ','
    latLonString = latLonString + '0 '
#######################################################

#######################################################
# Start kml file                       
root = Element('kml')
root.set('xmlns', 'http://www.opengis.net/kml/2.2')
root.set('xmlns:gx', 'http://www.google.com/kml/ext/2.2')
root.set('xmlns:kml', 'http://www.opengis.net/kml/2.2')
root.set('xmlns:atom', 'http://www.w3.org/2005/Atom')

document = SubElement(root, 'Document')
#
name = SubElement(document, 'name')
name.text = input('Enter a name for the KML file: ')
#
style1 = SubElement(document, 'Style')
style1.set('id', 's_ylw-pushpin_h1')
##
lineStyle1 = SubElement(style1, 'LineStyle')
###
width1 = SubElement(lineStyle1, 'width')
width1.text = '5'
#
styleMap = SubElement(document, 'StyleMap')
styleMap.set('id', 'm_ylw-pushpin')
##
pair1 = SubElement(styleMap, 'Pair')
###
key1 = SubElement(pair1, 'key')
key1.text = 'normal'
###
styleUrl1 = SubElement(pair1, 'styleUrl')
styleUrl1.text = '#s_ylw-pushpin'
##
pair2 = SubElement(styleMap, 'Pair')
###
key2 = SubElement(pair2, 'key')
key2.text = 'highlight'
###
styleUrl2 = SubElement(pair2, 'styleUrl')
styleUrl2.text = '@s_ylw-pushpin_h1'
#
style2 = SubElement(document, 'Style')
style2.set('id', 's_ylw-pushpin')
##
lineStyle2 = SubElement(style2, 'LineStyle')
###
width2 = SubElement(lineStyle2, 'width')
width2.text = '5'
#
placemark = SubElement(document, 'Placemark')
##
placemarkName = SubElement(placemark, 'name')
placemarkName.text = name.text
##
placemarkStyleUrl = SubElement(placemark, 'styleUrl')
placemarkStyleUrl.text = '#m_ylw-pushpin'
##
lineString = SubElement(placemark, 'LineString')
###
tessellate = SubElement(lineString, 'tessellate')
tessellate.text = '1'
###
coordinates = SubElement(lineString, 'coordinates')
coordinates.text = latLonString
#######################################################

#######################################################
# Write to KML file
fileName = name.text + '.kml'
with open(fileName, 'w') as file:
    file.write(prettify(root))
#######################################################