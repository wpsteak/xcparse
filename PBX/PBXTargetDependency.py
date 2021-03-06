from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBXResolver import *
from .PBX_Base import *

class PBXTargetDependency(PBX_Base):
    # target = {};
    # proxy = {};
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        self.identifier = identifier;
        if 'target' in dictionary.keys():
            self.target = self.parseProperty('target', lookup_func, dictionary, project, False);
        if 'targetProxy' in dictionary.keys():
            self.proxy = self.parseProperty('targetProxy', lookup_func, dictionary, project, False);