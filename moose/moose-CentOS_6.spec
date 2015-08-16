%global branch 3.0.2
%global version 3.0.2
%define _unpackaged_files_terminate_build 0 
Name: moose-src
Group: Applications/Biology
Summary: MOOSE is the Multiscale Object-Oriented Simulation Environment
Version: 3.0.2
Release: 1%{?dist}
Url: http://sourceforge.net/projects/moose
Source0: moose-%{version}.tar.gz

License: GPL-3.0

BuildRequires: gsl-devel
BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: python-devel
BuildRequires: python-setuptools
BuildRequires: libbz2-devel
BuildRequires: python-matplotlib
BuildRequires: python-networkx
BuildRequires: libxml2-devel
%if 0%{?openscenegraph_dist}

%endif

%description
MOOSE is the base and numerical core for large, detailed simulations
including Computational Neuroscience and Systems Biology. MOOSE spans
the range from single molecules to subcellular networks, from single
cells to neuronal networks, and to still larger systems. It is
backwards-compatible with GENESIS, and forward compatible with Python
and XML-based model definition standards like SBML and NeuroML.

MOOSE uses Python as its primary scripting language. For backward
compatibility we have a GENESIS scripting module, but this is
deprecated. MOOSE uses Qt/OpenGL for its graphical interface. The
entire GUI is written in Python, and the MOOSE numerical code is
written in C++.

Requires: moose-core
Requires: moose-gui
Requires: moose-python
%if 0%{?openscenegraph_dist} 
Requires: moose-moogli
%endif

%package -n moose
Summary: Meta package of MOOSE simulator.
Group: Application/Biology
%description -n moose
This is meta package of MOOSE simulator. Its contains python bindings and GUI.
Requires: moose-python
Requires: moose-gui

%package -n moose-core
Summary: MOOSE simulator, C++ core
Group: Applications/Biology
%description -n moose-core
This package contains C++ core of MOOSE simulator. For general use you should
try moose-python.

Requires: libbz2
Requires: libxml2
Requires: gsl
Requires: bzip2

%package -n moose-python
Summary: Python-2 interface for %{name}
Group: Applications/Biology
%description -n moose-python
This package contains python interface of MOOSE simulator.

Requires: python-matplotlib
Requires: numpy, atlas
Requires: moose-core

%package -n moose-gui
Summary: GUI frontend
Group: Applications/Biology
%description -n moose-gui
GUI frontend. It uses openscenegraph to visualize neural networks.

Requires: python-qt4
Requires: moose-python
Requires: python-networkx
Requires: python-suds

%if 0%{?openscenegraph_dist} 

%package -n moose-moogli
Summary: Visualizer for neural simulators
%description -n moose-moogli
Moogli (a sister project of MOOSE) is a simulator independent openGL based
visualization tool for neural simulations. Moogli can visualize morphology of
single/multiple neurons or network of neurons, and can also visualize activity
in these cells.



%endif

%prep
%setup -q -n moose-%{version}

%build
mkdir -p _build
cd _build
%if 0%{?openscenegraph_dist} 
cmake -DWITH_DOC=OFF-DBUILD_MOOGLI=TRUE  -DCMAKE_INSTALL_PREFIX=%buildroot/usr ..  && make -j`nproc`
%else
cmake -DWITH_DOC=OFF -DCMAKE_INSTALL_PREFIX=%buildroot/usr .. && make -j`nproc`
%endif

%install
cd _build
ctest --output-on-failure && make install
mkdir -p %buildroot/%{_prefix}/lib/moose/gui
cd .. &&  cp -r moose-gui/* %buildroot/%{_prefix}/lib/moose/gui/
install package_data/moosegui %buildroot/%{_prefix}/bin/

%files -n moose

%files -n moose-core
%{_prefix}/bin/moose.bin

%files -n moose-python
%defattr(-,root,root)
%dir %{_prefix}/share/moose
%{_prefix}/share/moose/moose-%{version}.tar.gz

%post -n moose-python
tar xvf ${_prefix}/share/moose/moose-3.0.2.tar.gz -C /tmp
cd /tmp/moose-3.0.2 
python setup.py instlal --record=/etc/moose/installed_files.txt

%preun -n moose-python
if [ -f /etc/moose/installed_files.txt ]; then
    tr '\n' '\0' < /etc/moose/installed_files.txt | xargs -0 rm -f --
fi
if [ -d /etc/moose ]; then
    rm -rf /etc/moose
fi
if [ -d %{_prefix}/share/moose ]; then
    rm -rf ${_prefix}/share/moose 
fi

%files -n moose-gui
%defattr(-,root,root)
%dir %{_prefix}/lib/moose
%dir %{_prefix}/lib/moose/gui
%{_prefix}/lib/moose/gui
%{_prefix}/bin/moosegui
%{_prefix}/share/applications/moose.desktop
%{_prefix}/share/icons/moose/moose.png

%if 0%{?openscenegraph_dist}
%files -n moose-moogli
%dir %{_prefix}/share/moogli
%dir %{_prefix}/share/moogli/moogli-1.0.tar.gz

%post -n moose-moogli
mkdir -p /etc/moogli
tar xvf ${_prefix}/share/moogli/moogli-1.0.tar.gz -C /tmp
cd /tmp/moogli-1.0 && python setup.py install --record /etc/moogli/installed_files.txt

%preun -n moose-moogli
tr '\n' '\0' < /etc/moogli/installed_files.txt | xargs -0 rm -f --
if [ -d /etc/moogli ]; then
    rm -rf /etc/moogli
fi
if [ -d %{_prefix}/share/moogli ]; then
    rm -rf %{_prefix}/share/moogli 
fi
%endif
