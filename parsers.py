import xml.etree.ElementTree as ET
import ConfigParser, os
import platform

class FakeSecHead(object):
    """Taken from: 
    http://stackoverflow.com/questions/2819696/
    parsing-properties-file-in-python/2819788#2819788 
    to fake a section header"""
    def __init__(self, fp):
        self.fp = fp
        self.sechead = '[asection]\n'

    def readline(self):
        if self.sechead:
            try: 
                return self.sechead
            finally: 
                self.sechead = None
        else: 
            return self.fp.readline()

class DUConfigParser:
    """A config file parser that uses ConfigParser"""

    _config_file = "/etc/default/distroshare-updater"
    _config = None
    def __init__(self):
        """Initialize the ConfigParser"""

        self._config = ConfigParser.ConfigParser()
        self._config.readfp(FakeSecHead(open(self._config_file)))
        self.validate()

    def validate(self):
        self.get_git_dir()
        self.get_git_base_repo()
        self.get_git_machine_repo()

    def get_git_dir(self):
        """Returns the local directory to store the git repo"""

        return self._config.get('asection', 'git_dir', 0)

    def get_git_common_dir(self):
        return self.get_git_dir() + "/common"

    def get_git_machine_dir(self):
        return self.get_git_dir() + "/machine"

    def get_git_base_repo(self):
        """Returns the base location for the git repo. This is
        used for initializing/updating the repo. Example: 
        https://github.com/Distroshare/"""

        return self._config.get('asection', 'base_repo', 0)

    def get_git_machine_repo(self):
        """Returns the base location for the git repo. This is
        used for initializing/updating the repo. Example: 
        https://github.com/Distroshare/"""

        return self._config.get('asection', 'machine_repo', 0)

class DUReleaseParser:
    """A config file parser that uses ConfigParser"""

    _config_file = "/etc/distroshare_release"
    _config = None
    def __init__(self):
        """Initialize the ConfigParser"""

        self._config = ConfigParser.ConfigParser()
        try:
            self._config.readfp(FakeSecHead(open(self._config_file)))
        except IOError as e:
            self._config = None

    def get_base_version(self):
        """Returns the version of this release"""

        if self._config is None:
            return "0"

        try:
            version = self._config.get('asection', 'base_version', 0)
        except ConfigParser.NoOptionError:
            version = "0"

        return version

    def get_machine_version(self):
        """Returns the version of this release"""

        if self._config is None:
            return "0"

        try:
            version = self._config.get('asection', 'machine_version', 0)
        except ConfigParser.NoOptionError:
            version = "0"

        return version

class DUManifestParser:
    """A manifest file parser that uses ElementTree"""

    _config = None
    _tree = None
    _root = None
    def __init__(self, git_dir):
        """Save the local directory"""
        self._git_dir = git_dir
        self._tree = ET.parse(git_dir + '/manifest.xml')
        self._root = self._tree.getroot()

    def get_packages_to_hold(self):
        """Returns a list of packages to hold"""
        
        if self._root is None:
            return None

        packages = self._root.find('packages_to_hold')
        if packages is None:
               return None

        hold = []
        for package in packages:
            hold.append(package.get('name'))

        return hold

    def get_packages_to_install(self):
        """Returns a list of packages to install"""

        if self._root is None:
            return None

        packages = self._root.find('packages_to_install')
        if packages is None:
            return None

        install = []
        for package in packages:
            install.append(package.get('name'))

        return install

    def get_version(self):
        if self._root is None:
            return None

        version = self._root.find('version')
        if version is None:
            return None

        return version.get('number')
        
