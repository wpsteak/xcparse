import os
import sys
import subprocess
from subprocess import CalledProcessError


class xcrun(object):
    """
    This class exists to execute 'xcrun' tools.
    """
    
    @classmethod
    def resolvePathFromLocation(cls, location_string, path, base_path):
        path_type, item_path = location_string.split(':');
        if path_type == 'group':
            return os.path.join(path, item_path);
        elif path_type == 'absolute':
            return item_path;
        elif path_type == 'developer':
            return os.path.join(resolve_developer_path(), item_path);
        elif path_type == 'container':
            return os.path.join(base_path, item_path);
        else:
            print 'Invalid item path name!';
            return item_path;
    
    @classmethod
    def make_subprocess_call(cls, call_args, shell_state=False):
        error = 0;
        output = '';
        try:
            output = subprocess.check_output(call_args, shell=shell_state);
            error = 0;
        except CalledProcessError as e:
            output = e.output;
            error = e.returncode;
        return (output, error);
    
    @classmethod
    def resolve_developer_path(cls):
        platform_path = '';
        xcrun_result = xcrun.make_subprocess_call(('xcode-select', '-p'));
        if xcrun_result[1] != 0:
            print 'Please run Xcode first!';
            sys.exit();
        developer_path = xcrun_result[0].rstrip('\n');
        return developer_path;
    
    @classmethod
    def perform_xcodebuild(cls, project, scheme_name, type, scheme_config_settings):
        build_command = 'xcodebuild -project "'+project.path.obj_path+'" -scheme "'+scheme_name+'" ';
        for item in scheme_config_settings:
            build_command+=str(item)+' ';
        build_command+=' '+type;
        result = xcrun.make_subprocess_call(build_command, True);
        print result[0];