#!/usr/bin/env python
# coding: utf-8

# ## Data File
# Finish Function provided by Udacity

# In[2]:


#!/usr/bin/env python
# -*- coding: utf-8 -*-


# 
# """
# After auditing is complete the next step is to prepare the data to be inserted into a SQL database.
# To do so you will parse the elements in the OSM XML file, transforming them from document format to
# tabular format, thus making it possible to write to .csv files.  These csv files can then easily be
# imported to a SQL database as tables.
# 
# The process for this transformation is as follows:
# - Use iterparse to iteratively step through each top level element in the XML
# - Shape each element into several data structures using a custom function
# - Utilize a schema and validation library to ensure the transformed data is in the correct format
# - Write each data structure to the appropriate .csv files
# 
# We've already provided the code needed to load the data, perform iterative parsing and write the
# output to csv files. Your task is to complete the shape_element function that will transform each
# element into the correct format. To make this process easier we've already defined a schema (see
# the schema.py file in the last code tab) for the .csv files and the eventual tables. Using the 
# cerberus library we can validate the output against this schema to ensure it is correct.
# 
# ## Shape Element Function
# The function should take as input an iterparse Element object and return a dictionary.
# 
# ### If the element top level tag is "node":
# The dictionary returned should have the format {"node": .., "node_tags": ...}
# 
# The "node" field should hold a dictionary of the following top level node attributes:
# - id
# - user
# - uid
# - version
# - lat
# - lon
# - timestamp
# - changeset
# All other attributes can be ignored
# 
# The "node_tags" field should hold a list of dictionaries, one per secondary tag. Secondary tags are
# child tags of node which have the tag name/type: "tag". Each dictionary should have the following
# fields from the secondary tag attributes:
# - id: the top level node id attribute value
# - key: the full tag "k" attribute value if no colon is present or the characters after the colon if one is.
# - value: the tag "v" attribute value
# - type: either the characters before the colon in the tag "k" value or "regular" if a colon
#         is not present.
# 
# Additionally,
# 
# - if the tag "k" value contains problematic characters, the tag should be ignored
# - if the tag "k" value contains a ":" the characters before the ":" should be set as the tag type
#   and characters after the ":" should be set as the tag key
# - if there are additional ":" in the "k" value they and they should be ignored and kept as part of
#   the tag key. For example:
# 
#   <tag k="addr:street:name" v="Lincoln"/>
#   should be turned into
#   {'id': 12345, 'key': 'street:name', 'value': 'Lincoln', 'type': 'addr'}
# 
# - If a node has no secondary tags then the "node_tags" field should just contain an empty list.
# 
# The final return value for a "node" element should look something like:
# 
# {'node': {'id': 757860928,
#           'user': 'uboot',
#           'uid': 26299,
#        'version': '2',
#           'lat': 41.9747374,
#           'lon': -87.6920102,
#           'timestamp': '2010-07-22T16:16:51Z',
#       'changeset': 5288876},
#  'node_tags': [{'id': 757860928,
#                 'key': 'amenity',
#                 'value': 'fast_food',
#                 'type': 'regular'},
#                {'id': 757860928,
#                 'key': 'cuisine',
#                 'value': 'sausage',
#                 'type': 'regular'},
#                {'id': 757860928,
#                 'key': 'name',
#                 'value': "Shelly's Tasty Freeze",
#                 'type': 'regular'}]}
# 
# ### If the element top level tag is "way":
# The dictionary should have the format {"way": ..., "way_tags": ..., "way_nodes": ...}
# 
# The "way" field should hold a dictionary of the following top level way attributes:
# - id
# -  user
# - uid
# - version
# - timestamp
# - changeset
# 
# All other attributes can be ignored
# 
# The "way_tags" field should again hold a list of dictionaries, following the exact same rules as
# for "node_tags".
# 
# Additionally, the dictionary should have a field "way_nodes". "way_nodes" should hold a list of
# dictionaries, one for each nd child tag.  Each dictionary should have the fields:
# - id: the top level element (way) id
# - node_id: the ref attribute value of the nd tag
# - position: the index starting at 0 of the nd tag i.e. what order the nd tag appears within
#             the way element
# 
# The final return value for a "way" element should look something like:
# 
# {'way': {'id': 209809850,
#          'user': 'chicago-buildings',
#          'uid': 674454,
#          'version': '1',
#          'timestamp': '2013-03-13T15:58:04Z',
#          'changeset': 15353317},
#  'way_nodes': [{'id': 209809850, 'node_id': 2199822281, 'position': 0},
#                {'id': 209809850, 'node_id': 2199822390, 'position': 1},
#                {'id': 209809850, 'node_id': 2199822392, 'position': 2},
#                {'id': 209809850, 'node_id': 2199822369, 'position': 3},
#                {'id': 209809850, 'node_id': 2199822370, 'position': 4},
#                {'id': 209809850, 'node_id': 2199822284, 'position': 5},
#                {'id': 209809850, 'node_id': 2199822281, 'position': 6}],
#  'way_tags': [{'id': 209809850,
#                'key': 'housenumber',
#                'type': 'addr',
#                'value': '1412'},
#               {'id': 209809850,
#                'key': 'street',
#                'type': 'addr',
#                'value': 'West Lexington St.'},
#               {'id': 209809850,
#                'key': 'street:name',
#                'type': 'addr',
#                'value': 'Lexington'},
#               {'id': '209809850',
#                'key': 'street:prefix',
#                'type': 'addr',
#                'value': 'West'},
#               {'id': 209809850,
#                'key': 'street:type',
#                'type': 'addr',
#                'value': 'Street'},
#               {'id': 209809850,
#                'key': 'building',
#                'type': 'regular',
#                'value': 'yes'},
#               {'id': 209809850,
#                'key': 'levels',
#                'type': 'building',
#                'value': '1'},
#               {'id': 209809850,
#                'key': 'building_id',
#                'type': 'chicago',
#                'value': '366409'}]}
# """

# In[3]:


import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET
import urllib.request
from http import HTTPStatus
import cerberus

from my_schema import schema


# In[4]:


OSM_PATH = "sample.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema


# In[5]:


# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


# ## Shape Element:
# This is the function that was completed as part of the assignment. 

# In[35]:



def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements
    
    way_dict = {}
    node_dict = {}
    nd_dict = {}
    pos_counter = 0
    
    
    if element.tag == 'node':
        for child in element.iter("node"):
            node_attribs = child.attrib
            
            
        for child in element:  
            #Skip any records with problem characters
            if not PROBLEMCHARS.search(child.attrib['k']):
                node_dict = {}
                node_dict['id'] = node_attribs['id']
                
                #If there is a lower colon (ie. addr:street), split the first part to type, second to key. Type=addr, Key=street
                if LOWER_COLON.search(child.attrib['k']):
                    fix_key = child.attrib['k']
                    col_index = fix_key.find(':') + 1
                    new_key = fix_key[col_index:].strip()
                    node_dict['key'] = new_key
                    
                    node_dict['value'] = child.attrib['v']
                    
                    type_index = fix_key.find(':')
                    new_type = fix_key[:type_index].strip()
                    node_dict['type'] = new_type
                    
                #If there is no lower colon, populate the node dictionary
                else:
                    node_dict['key'] = child.attrib['k']
                    node_dict['value'] = child.attrib['v']
                    node_dict['type'] = 'regular'
                
                
                #Send for cleaning- update street abbreviation, state, phone number
                node_dict['value'] = clean_up(node_dict['key'], node_dict['value'])
                
                tags.append(node_dict)
                
       
        
        
        return {'node': node_attribs, 'node_tags': tags}
    
       
    elif element.tag == 'way':
        for child in element.iter("way"):

                way_attribs = child.attrib
        
        for child in element:
                
                 
                
               
                    if child.tag == 'tag':
                    
                        #Skip any records with problem characters
                        if not PROBLEMCHARS.search(child.attrib['k']):
                            way_dict = {}
                            way_dict['id'] = way_attribs['id']
                            
                            
                            #If there is a lower colon (ie. addr:street), split the first part to type, second to key.
                            if LOWER_COLON.search(child.attrib['k']):
                                fix_key = child.attrib['k']
                                col_index = fix_key.find(':') + 1
                                new_key = fix_key[col_index:].strip()
                                way_dict['key'] = new_key
                                
                                way_dict['value'] = child.attrib['v']
                                
                                type_index = fix_key.find(':')
                                new_type = fix_key[:type_index].strip()
                                way_dict['type'] = new_type

                            #update way_dict for items with no lower colon.
                            else:
                                way_dict['key'] = child.attrib['k']
                                way_dict['value'] = child.attrib['v']
                                way_dict['type'] = 'regular'
                            
                            way_dict['value'] = clean_up(way_dict['key'], way_dict['value'])
                            tags.append(way_dict) 
                
                    #For nd tags, count the position of the reference.
                    else:
                        nd_dict ={}
                        nd_dict['id'] = way_attribs['id']
                        nd_dict['node_id'] = child.attrib['ref']
                        nd_dict['position']= pos_counter
                        way_nodes.append(nd_dict)
                        pos_counter += 1
        
       
        
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# # ================================================== #
# #               Helper Functions                     #
# # ================================================== #

# In[41]:


#Cleaning function.
def clean_up(k,v):
    """Function main explanation.
    This function will clean up the ways and nodes tags for street names, state and phone number.
    Streets will be updated to full name. State will be updated to abbreviation. Phone number will be put in
    standard format but only if valid. 

    Unit testing:
    Below code runs function_name with parameter k = street and v = "Jessup Mill Rd",
    then it expects to return "Jessup Mill Road"
    >>>clean_up("street", "Jessup Mill Rd")
    Jessup Mill Rd

    Args:
        param_1(string): This is the k value of the tag.
        param_2(string): This is the value of the tag that will be updated if it meets qualifications.
    Returns:
        string: Updated value if cleaned, same value if not cleaned.
    """
    #Updates street names for consistency.
    if k == 'street':
        
        for abbv, name in {"Ave":"Avenue", "Rd":"Road", "Dr":"Drive",  "Ter":"Terrace", "St":"Street" }.items():
            v = re.sub(r"\b" + abbv + r"\b", name , v)
        
    #Updates state for consistency
    elif k == 'state':
        
        v = v.replace("Jersey", "NJ")
        
   
    elif k == 'phone':
        
        num = v.replace('+1','')
        strip_num = re.sub('[^0-9]', '', num)
    
        
        if len(strip_num) == 11:
            v = ("("+strip_num[1:4]+")"+strip_num[4:7]+"-"+ strip_num[7:])
        elif len(strip_num) == 10:
            v = ("("+strip_num[:3]+")"+strip_num[3:6]+"-"+ strip_num[6:])
        elif len(strip_num) == 7:
            v = ("("+strip_num[:3]+")"+strip_num[3:])
        
      
    return v
    
        
        


# In[42]:


def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


# In[43]:


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(iter(validator.errors.items()))
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


# In[44]:


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            #k: (v.encode('utf-8') if isinstance(v, str) else v) for k, v in row.items()
            k: v for k, v in row.items()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# # ================================================== #
# #               Main Function                        #
# # ================================================== #

# In[45]:


def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w', "utf-8") as nodes_file,          codecs.open(NODE_TAGS_PATH, 'w',"utf-8") as nodes_tags_file,          codecs.open(WAYS_PATH, 'w',"utf-8") as ways_file,          codecs.open(WAY_NODES_PATH, 'w',"utf-8") as way_nodes_file,          codecs.open(WAY_TAGS_PATH, 'w',"utf-8") as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            
            
            
            el = shape_element(element)
            
           
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating. Change to true to check
    process_map(OSM_PATH, validate=True)


# In[ ]:




