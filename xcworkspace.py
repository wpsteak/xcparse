from __future__ import absolute_import
import xml.etree.ElementTree as xml

from .xcodeproj import *
from .xcrun import *
from .xc_base import *

class xcworkspace(xc_base):
    # path = {};
    # data = {};
    
    def __init__(self, xcworkspace_path):
        """
        Pass the path to a 'xcworkspace' file to initialize the xcworkspace object.
        """
        self.data = None;
        if xcworkspace_path.endswith('.xcworkspace'):
            self.path = Path(xcworkspace_path, 'contents.xcworkspacedata');
            
            if os.path.exists(self.path.root_path) == True:
                try:
                    self.data = xml.parse(self.path.root_path);
                except:
                    self.data = None;
            else:
                print 'Could not find xcworkspacedata file!';
        else:
            print 'Invalid xcworkspace file!';
    
    def isValid(self):
        return self.data != None;
    
    def __resolvePathFromXMLItem(self, node, path):
        if self.isValid():
            file_relative_path = node.attrib['location'];
            return xcrun.resolvePathFromLocation(file_relative_path, path, self.path.base_path);
        else:
            return None;
    
    def __parsePathsFromXMLItem(self, node, path):
        results = [];
        if self.isValid():
            item_path = self.__resolvePathFromXMLItem(node, path);
            if node.tag == 'FileRef':
                if os.path.exists(item_path) == True:
                    project_parse = xcodeproj(item_path);
                    if project_parse.isValid() == True:
                        results.append(project_parse);
            if node.tag == 'Group':
                path = os.path.join(path, item_path);
                for child in node:
                    group_results = self.__parsePathsFromXMLItem(child, path);
                    for item in group_results:
                        results.append(item);
        return results;
    
    def projects(self):
        """
        This will return a list of projects referenced in this workspace.
        """
        indexed_projs = [];
        if self.isValid():
            workspace_base_path = self.path.base_path;
            workspace_root = self.data.getroot();
            for child in workspace_root:
                results = self.__parsePathsFromXMLItem(child, workspace_base_path);
                for item in results:
                    indexed_projs.append(item);
        return indexed_projs;
    