#!/usr/bin/env python
# coding: utf-8

# # Audit and Clean

# This combines code from the Udacity Data Nano Degree with additional cleaning functions to wrangle an open street map.

# In[1]:


import xml.etree.ElementTree as ET  
import pprint
import unicodecsv 
from collections import defaultdict
##Default dict will stop you from getting an error if you try to reference a key that doesn't exist in dictionary yet.
import re
import codecs
from bs4 import BeautifulSoup
import csv
import urllib.request
from http import HTTPStatus


# In[19]:


# Map of Gloucester County, NJ
OSM_FILE = "map_GC_NJ.xml"  


# In[20]:


#Function to review a small amount of the file. 
# Change counter number to increase/ descrease size.
def parse_file(OSM_FILE):
    data = []
    with open(OSM_FILE, "r", encoding='utf-8', errors='replace') as f:
  
        header = f.readline().split(",")
        counter = 0
        for line in f:
            if counter == 10:
                break
        
            fields = line.split(",")
            entry = {}
        
            for i, value in enumerate(fields):
                entry[header[i].strip()] = value.strip()
            data.append(entry)
            counter +=1
            
            print(line)


# In[21]:


parse_file(OSM_FILE)


# ### Audit Street Names:
# The following code was taken from the case study for how to cleanse the street names. 

# In[22]:


##Code Taken from lesson as an audit
street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
street_types = defaultdict(int)


# In[23]:


def is_street_name(elem):
    return(elem.tag == "tag") and (elem.attrib['k'] == "addr:street")


# In[24]:


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        street_types[street_type] += 1
        
def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key= lambda s: s.lower())
    for k in keys:
        v = d[k]
        print("%s:%d"  % (k,v))
        
     


# In[25]:


def audit():
    for event, elem in ET.iterparse(OSM_FILE):
        if is_street_name(elem):
            audit_street_type(street_types, elem.attrib['v'])
    print_sorted_dict(street_types)
    
if __name__ == '__main__':
    audit()


# ### Audit Other Fields
# This will show some of the other options in the data set that may need to be audited. 

# In[26]:


def is_name(elem):
    return(elem.tag == "tag") and (elem.attrib['k'] == "name")


# In[27]:


name_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
name_types = defaultdict(int)

def audit_name(name_types, name_name):
    m = name_type_re.search(name_name)
    if m:
        name_type = m.group()
        name_types[name_type] += 1
def audit_n():
    for event, elem in ET.iterparse(OSM_FILE):
        if is_name(elem):
            audit_name(name_types, elem.attrib['v'])
    print_sorted_dict(name_types)
    
if __name__ == '__main__':
    audit_n()


# ### Audit States:
# The map pulled was only for New Jersey. This will audit to check if the state field is accurate and if all results are the same: *** In the original file there is Jersey, but the sample did not pull that.

# In[28]:


def is_state(elem):
    return(elem.tag == "tag") and (elem.attrib['k'] == "addr:state")


# In[29]:


state_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
state_types = defaultdict(int)

def audit_state(state_types, state_name):
    m = state_type_re.search(state_name)
    if m:
        state_type = m.group()
        state_types[state_type] += 1


# In[30]:


def audit_s():
    for event, elem in ET.iterparse(OSM_FILE):
        if is_state(elem):
            audit_state(state_types, elem.attrib['v'])
    print_sorted_dict(state_types)
    
if __name__ == '__main__':
    audit_s()


# ### Audit Websites
# This will check the websites and count them.

# In[31]:


def is_website(elem):
    return(elem.tag == "tag") and (elem.attrib['k'] == "website")


# In[32]:


website_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
website_types = defaultdict(int)

def audit_website(website_types, website_name):
    m = website_type_re.search(website_name)
    if m:
        website_type = m.group()
        website_types[website_type] += 1
def audit_w():
    for event, elem in ET.iterparse(OSM_FILE):
        if is_website(elem):
            audit_website(website_types, elem.attrib['v'])
    print_sorted_dict(website_types)
    
if __name__ == '__main__':
    audit_w()


# ### Audit Crafts

# In[33]:


def is_craft(elem):
    return(elem.tag == "tag") and (elem.attrib['k'] == "craft")


# In[34]:


craft_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
craft_types = defaultdict(int)

def audit_craft(craft_types, craft_name):
    m = craft_type_re.search(craft_name)
    if m:
        craft_type = m.group()
        craft_types[craft_type] += 1
def audit_c():
    for event, elem in ET.iterparse(OSM_FILE):
        if is_craft(elem):
            audit_craft(craft_types, elem.attrib['v'])
    print_sorted_dict(craft_types)
    
if __name__ == '__main__':
    audit_c()


# ### Audit Phone Numbers
# This shows a lot of different phone number formats including a lot of invalid numbers.

# In[37]:


def is_phone(elem):
    return(elem.tag == "tag") and (elem.attrib['k'] == "phone")


# In[36]:


phone_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
phone_types = defaultdict(int)

def audit_phone(phone_types, phone_name):
    m = phone_type_re.search(phone_name)
    if m:
        phone_type = m.group()
        phone_types[phone_type] += 1
def audit_p():
    for event, elem in ET.iterparse(OSM_FILE):
        if is_phone(elem):
            audit_phone(phone_types, elem.attrib['v'])
    print_sorted_dict(phone_types)
    
if __name__ == '__main__':
    audit_p()

