#!/usr/bin/env python
"""
write_spec_files.py: 

    This script generates spec file for various distributions.

    Last modified: Mon Aug 10 22:28:30 2015
"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2013, Dilawar Singh and NCBS Bangalore"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import re
import os
import sys

# name of the essentials required to build the moose-core and moose-python.
core_build_depend_list_ = [
        'gsl-devel'
        , 'gcc-c++'
        , 'cmake'
        , 'python-devel'
        , 'python-setuptools'
        , 'libbz2-devel'
        , 'numpy'
        , 'libxml2-devel'
        #, 'doxygen'
        #, 'python-sphinx'
        ]

# essentials to run the moose-core
core_depend_list_ = [
        'libbz2'
        , 'libxml2'
        , 'gsl'
        , 'bzip2'
        ]

# essentials to run the moose-python
py_depend_list_ = [
         'python-matplotlib'
        , 'numpy'
        , 'moose-core'
        ]

gui_depend_list_ = [
        'PyQt4'
        , 'moose-python'
        , 'python-networkx'
        , 'python-suds'
        ]

# Alternative names.
_alternative = {
        'openSUSE' : {'numpy' : 'python-numpy', 'PyQt4' : 'python-qt4' }
        , 'CentOS' : {'PyQt4' : 'python-qt4', 'numpy' : 'numpy, atlas' }
        , 'RHEL'  : { 'numpy' : 'numpy, atlas', 'PyQt4' : 'python-qt4' }
        , 'SLE' : { 'numpy' : 'python-numpy' }
        , 'ScientificLinux' : { 'numpy' : 'numpy, atlas, lapack' }
        }

repos_ = { "CentOS" : [6, 7]
        , "Fedora" : [20, 21, 22 ]
        , "RHEL" : [ 5, 6, 7 ]
        , "SLE" : [ "11_SP2", "11_SP3", "11_SP4", 12 ]
        , "ScientificLinux" : [6, 7]
        , "Arch" : ["Core", "Extra"]
        , "openSUSE" : [ "12.3", "13.1", "13.2", "Tumbleweed", "Factory_ARM" ]
        }

def get_alternative_name(repoName, name):
    global _alternative
    rep = _alternative.get(repoName, None)
    if rep:
        alt = rep.get(name, None)
        if alt:
            return alt
        else:
            return name
    else:
        return name


def get_build_require_text(repoName):
    global core_build_depend_list_
    buildList = [ get_alternative_name(repoName, x) for x in
            core_build_depend_list_]
    buildReqText = "\n".join(["BuildRequires: %s" % x for x in buildList])
    return buildReqText

def get_core_req_text(repoName):
    global core_depend_list_
    l = [ get_alternative_name(repoName,x) for x in core_depend_list_]
    return "\n".join(["Requires: %s" % x for x in l])

def get_gui_req_text(repoName):
    global gui_depend_list_
    l = [ get_alternative_name(repoName, x) for x in gui_depend_list_]
    return "\n".join(["Requires: %s" % x for x in l])

def get_py_req_text(repoName):
    global py_depend_list_
    l = [ get_alternative_name(repoName, x) for x in py_depend_list_]
    return "\n".join(["Requires: %s" % x for x in l])

class SpecFile():

    def __init__(self, repository, version):
        self.repository = repository
        self.version = version
        self.architecture = "i586"
        self.url = None
        self.specfileName = "moose-{}_{}.spec".format(self.repository, version)
        self.templateText = None
        with open("moose.spec.template", "r") as f:
            self.templateText = f.read()

    def writeSpecFile(self, **kwargs):
        print("++ Writing spec file for %s" % self.repository)
        buildRequiretext = get_build_require_text(self.repository)
        self.templateText = self.templateText.replace("<<MooseBuildRequires>>"
                , buildRequiretext
                )

        # moose-core
        coreReqText = get_core_req_text(self.repository)
        self.templateText = self.templateText.replace("<<moose-coreRequires>>"
                , coreReqText
                )

        # moose-python
        pyReqText = get_py_req_text(self.repository)
        self.templateText = self.templateText.replace("<<moose-pythonRequires>>"
                , pyReqText
                )

        # moose-gui
        guiReqText = get_gui_req_text(self.repository)
        self.templateText = self.templateText.replace("<<moose-guiRequires>>"
                , guiReqText
                )

        # moogli - build
        moogliBuildReqText = ""
        self.templateText = self.templateText.replace("<<MoogliBuildRequires>>"
                , moogliBuildReqText
                )

        moogliReqText = ""
        self.templateText = self.templateText.replace("<<moose-moogliRequires>>"
                , moogliReqText
                )

        # Just get the moose-core and moose-python build requirements.
        print("Writing specfile: {}".format(self.specfileName))
        with open(self.specfileName, "w") as specFile:
            specFile.write(self.templateText)
        
def main():
    global repos_
    for r in repos_:
        repo, versions = r, repos_[r]
        for version in versions:
            sl = SpecFile(repo, version)
            sl.writeSpecFile()
    
if __name__ == '__main__':
    main()
