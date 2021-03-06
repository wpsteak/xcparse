import os

class Path(object):    
    """
    This is a path object to allow for root, base, and full path storage to create relative paths
    """
    # base_path = '';
    # obj_path = '';
    # root_path = '';
    
    def __init__(self, path, root):
        self.obj_path = os.path.normpath(path);
        self.base_path = os.path.dirname(self.obj_path);
        if root == '':
            self.root_path = self.obj_path;
        else:
            self.root_path = os.path.join(self.obj_path, root);
    
    def __attrs(self):
        return (self.obj_path, self.base_path, self.root_path);

    def __eq__(self, other):
        return isinstance(other, Path) and self.__attrs() == other.__attrs();

    def __hash__(self):
        return hash(self.__attrs());