import os
import time
import subprocess

from experiments import provenance


GIT_DIR = os.path.abspath(os.path.join(__file__, '../..'))

# planar arms
PA_RESEARCH_PKGS = ['experiments', 'clusterjobs', 'scicfg',
                    'learners', 'fastlearners', 'explorers', 'environments']
PA_THIRDPARTY_PY = ['scipy', 'numpy', 'sklearn', 'shapely']
PA_THIRDPARTY    = [('geos', 'geos-config --version')]

# object interaction
OI_RESEARCH_PKGS = PA_RESEARCH_PKGS + ['fastlearners', 'dovecot']
OI_THIRDPARTY_PY = PA_THIRDPARTY_PY + ['sympy']
OI_THIRDPARTY    = (PA_THIRDPARTY +
                    [('Eigen',  'pkg-config eigen3 --modversion'),
                     ('libccd', 'pkg-config ccd    --modversion'),
                     ('FCL',    'pkg-config fcl    --modversion'),
                     ('FLANN',  'pkg-config flann  --modversion')])
OI_MANUAL        = [('dmpbbo', '[4bbb90ae679053e04bb4604bee0acbaf75f64875]'),
                    ('V-REP', '3.2.3, rev 4'),
                    ('Boost', '1.55')]


class ProvenanceData(object):
    """An object that tracks provenance data"""

    def __init__(self, code_dir, research_pkgs=(),
                 thirdparty_py=(), thirdparty=(), manual=()):
        self.timestamp = time.time()
        self.dirty = False # has any of research_pkgs or code_dir a dirty repo?
        self.plat_info = provenance.platform_info()

        self._code          = None
        self._research_pkgs = []
        self._thirdparty_py = []
        self._thirdparty    = []

        self.register_code(code_dir)
        for pkg_name in research_pkgs:
            self.register_package(pkg_name, research=True)
        for pkg_name in thirdparty_py:
            self.register_package(pkg_name, research=False)
        for pkg_name, version_cmd in thirdparty:
            self.register_thirdparty(pkg_name, version_cmd)
        for pkg_name, version in manual:
            self.register_manual(pkg_name, version)

    def register_code(self, code_dir):
        assert os.path.isdir(code_dir)
        commit = provenance.git_commit(code_dir)
        dirty  = provenance.git_dirty(code_dir)
        self.dirty = self.dirty or dirty
        self._code = (code_dir, commit, dirty)

    def register_package(self, name, research=False):
        pkg_info = provenance.packages_info([name])
        for name, info in pkg_info._branches:
            self.dirty = self.dirty or info.dirty
            if research:
                self._research_pkgs.append((name, info.commit, info.dirty))
                self._research_pkgs.sort()
            else:
                self._thirdparty_py.append((name, info.version))
                self._thirdparty_py.sort()

    def register_thirdparty(self, name, version_cmd):
        p = subprocess.Popen(version_cmd.split(), stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
        version = stdout.decode('utf8').replace('\n', '')
        self._thirdparty.append((name, version))
        self._thirdparty.sort()

    def register_manual(self, name, version):
        self._thirdparty.append((name, version))
        self._thirdparty.sort()

    def message(self):
        s = ''

        # code text
        if not self.dirty:
            s += ('All the code involved in the computation is commited '
                  '(no git repository in dirty state).\n')
        else:
            s += ('Some code involved in the computation has not been commited '
                  '(some git repository in dirty state).\n')
        s += 'This code was executed with commit {}.\n\n'.format(self._code[1])

        # research package text
        s += 'Installed research packages (available in the submodules/ directory):\n'
        max_name = max(len(name) for name, commit, dirty, in self._research_pkgs)
        for name, commit, dirty, in self._research_pkgs:
            s += '    {}{} [{}]\n'.format(name, ' '*(max_name - len(name)), commit)
        s += '\n'

        # third-party python packages
        s += 'Installed third-party python packages:\n'
        for name, version in self._thirdparty_py:
            s += '    {} {}\n'.format(name, version)
        s += '\n'

        # non-python third-party packages
        s += 'Installed third-party non-python packages:\n'
        for name, version in self._thirdparty:
            s += '    {} {}\n'.format(name, version)
        s += '\n'

        # platform info
        s += 'Executed with:\n'
        s += '    {} {} {}\n'.format(self.plat_info.python.implementation,
                                     self.plat_info.python.version,
                                     self.plat_info.python.build)
        s += '    [{}]\n'.format(self.plat_info.python.compiler)
        s += '    on {}\n'.format(self.plat_info.uname[3])

        return s


def planar_arms():
    return ProvenanceData(GIT_DIR, PA_RESEARCH_PKGS,
                          PA_THIRDPARTY_PY, PA_THIRDPARTY)

def object_interaction():
    return ProvenanceData(GIT_DIR, OI_RESEARCH_PKGS,
                          OI_THIRDPARTY_PY, OI_THIRDPARTY, OI_MANUAL)
