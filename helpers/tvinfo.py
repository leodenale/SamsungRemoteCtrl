import re
import xml.etree.ElementTree as ET
import urllib.request
import logging

# tv info related functions


def getMethod(model):
    models = {'C': 'legacy',
              'D': 'legacy',
              'E': 'legacy',
              'F': 'legacy'}
    method = models.get(model[4], 'websocket')
    logging.debug('Model: ' + model[4] + ' returns method: ' + method)
    return method


def namespace(element):
    m = re.match('\{.*\}', element.tag)
    return m.group(0) if m else ''


def get(url):
    ip = re.search(r'[0-9]+(?:\.[0-9]+){3}', url)
    xmlinfo = urllib.request.urlopen(url)
    xmlstr = xmlinfo.read().decode('utf-8')
    root = ET.fromstring(xmlstr)
    ns = namespace(root)
    fn = root.find('.//{}friendlyName'.format(ns)).text
    model = root.find('.//{}modelName'.format(ns)).text
    return {'fn': fn, 'ip': ip.group(0), 'model': model}
