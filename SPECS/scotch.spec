Summary:	Graph, mesh and hypergraph partitioning library
Name:		scotch
Version:	6.0.0
Release:	3.b%{?dist}
License:	CeCILL-C
Group:		Development/Libraries
URL:		http://www.labri.fr/perso/pelegrin/scotch/
Source0:	https://gforge.inria.fr/frs/download.php/31831/%{name}_%{version}.tar.gz
Source1:	scotch-Makefile.static.inc.in
Source2:	scotch-Makefile.shared.inc.in
BuildRequires:	flex bison zlib-devel bzip2-devel lzma-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%global _unpackaged_files_terminate_build 0

%description
Scotch is a software package for graph and mesh/hypergraph partitioning and
sparse matrix ordering.

%package devel
Summary:	Development libraries for scotch
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains development libraries for scotch.

%package static
Summary:	Development libraries for scotch
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains libscotch static libraries.

%package mpich2
Summary: Scotch libraries compiled against mpich2
Group: Development/Libraries
BuildRequires: mpich2-devel
Requires: %{name} = %{version}-%{release}
Requires: environment-modules mpich2

%description mpich2
Scotch is a software package for graph and mesh/hypergraph partitioning and
sparse matrix ordering.

%package mpich2-devel
Summary: Development libraries for Scotch (mpich2)
Group: Development/Libraries
Requires: %{name}-mpich2 = %{version}-%{release}

%description mpich2-devel
This package contains development libraries for Scotch, compiled against mpich2.

%package mpich2-static
Summary: Static Scotch libraries compiled against mpich2
Group: Development/Libraries
Requires: %{name}-mpich2-devel = %{version}-%{release}

%description mpich2-static
This package contains static libraries for Scotch, compiled against mpich2.

%package openmpi
Summary: Scotch libraries compiled against openmpi
Group: Development/Libraries
BuildRequires: openmpi-devel
Requires: %{name} = %{version}-%{release}
Requires: environment-modules openmpi

%description openmpi
Scotch is a software package for graph and mesh/hypergraph partitioning and
sparse matrix ordering.

%package openmpi-devel
Summary: Development libraries for Scotch (openmpi)
Group: Development/Libraries
Requires: %{name}-openmpi = %{version}-%{release}

%description openmpi-devel
This package contains development libraries for Scotch, compiled against openmpi.

%package openmpi-static
Summary: Static Scotch libraries compiled against openmpi
Group: Development/Libraries
Requires: %{name}-openmpi-devel = %{version}-%{release}

%description openmpi-static
This package contains static libraries for Scotch, compiled against openmpi.

%prep
%setup -c -q -n scotch_%{version}
pushd scotch_%{version}
sed s/@RPMFLAGS@/'%{optflags} -fPIC'/ < %SOURCE1 > src/Makefile.static.inc
sed s/@RPMFLAGS@/'%{optflags} -fPIC'/ < %SOURCE2 > src/Makefile.shared.inc
popd

cp -ap scotch_%{version} scotch_%{version}_mpich2
cp -ap scotch_%{version} scotch_%{version}_openmpi

%build
module purge

%define dosingle() \
rm -f Makefile.inc; \
ln -s Makefile.static.inc Makefile.inc; \
make %{?_smp_mflags}; \
rm -f Makefile.inc; \
ln -s Makefile.shared.inc Makefile.inc; \
make %{?_smp_mflags}

%define dobuild() \
rm -f Makefile.inc; \
ln -s Makefile.static.inc Makefile.inc; \
make %{?_smp_mflags} ptscotch; \
rm Makefile.inc; \
ln -s Makefile.shared.inc Makefile.inc; \
make %{?_smp_mflags} ptscotch

pushd scotch_%{version}/src/
%dosingle
popd

pushd scotch_%{version}_mpich2/src/
%{_mpich2_load}
%dobuild
%{_mpich2_unload}
popd

module purge

pushd scotch_%{version}_openmpi/src/
%{_openmpi_load}
%dobuild
%{_openmpi_unload}
popd

%install
rm -rf %{buildroot}
module purge

%define doinst() \
pushd src/; \
rm -f Makefile.inc; \
ln -s Makefile.static.inc Makefile.inc; \
make %{?_smp_mflags} install %*; \
rm -f Makefile.inc; \
ln -s Makefile.shared.inc Makefile.inc; \
make %{?_smp_mflags} install %*; \
popd \
pushd $libdir; \
for lib in *.so; do \
	mv $lib $lib.0.0; \
	ln -s $lib.0.0 $lib; \
	ln -s $lib.0.0 $lib.0; \
done; \
popd

pushd scotch_%{version}/
export libdir=%{buildroot}%{_libdir}
%doinst prefix=%{buildroot}%{_prefix} libdir=%{buildroot}%{_libdir}

pushd %{buildroot}%{_bindir}/
for prog in *; do
	mv $prog scotch_$prog
done
popd
pushd %{buildroot}%{_mandir}/man1/
rm -f d*
for prog in *; do
	mv $prog scotch_$prog
done
popd
pushd %{buildroot}%{_bindir}
	rm -f scotch_gpart && ln -s ./scotch_gmap scotch_gpart
popd

# Convert the license files to utf8
pushd doc
iconv -f iso8859-1 -t utf-8 < CeCILL-C_V1-en.txt > CeCILL-C_V1-en.txt.conv
iconv -f iso8859-1 -t utf-8 < CeCILL-C_V1-fr.txt > CeCILL-C_V1-fr.txt.conv
mv -f CeCILL-C_V1-en.txt.conv CeCILL-C_V1-en.txt
mv -f CeCILL-C_V1-fr.txt.conv CeCILL-C_V1-fr.txt
popd

popd

pushd scotch_%{version}_mpich2
%{_mpich2_load}
export libdir=%{buildroot}/${MPI_LIB}
%doinst prefix=%{buildroot}/${MPI_HOME} libdir=%{buildroot}/${MPI_LIB} includedir=%{buildroot}/${MPI_INCLUDE} mandir=%{buildroot}/${MPI_MAN} bindir=%{buildroot}/${MPI_BIN}

pushd %{buildroot}/${MPI_BIN}
for prog in *; do
    mv $prog scotch_${prog}
done
rm -f scotch_dgpart && ln -s ./scotch_dgmap scotch_dgpart
popd

pushd %{buildroot}/${MPI_MAN}/man1/
rm -f {a,g,m}*
for man in *; do
    mv ${man} scotch_${man}
done
popd
%{_mpich2_unload}
popd

module purge

pushd scotch_%{version}_openmpi
%{_openmpi_load}
export libdir=%{buildroot}/${MPI_LIB}
%doinst prefix=%{buildroot}/${MPI_HOME} libdir=%{buildroot}/${MPI_LIB} includedir=%{buildroot}/${MPI_INCLUDE} mandir=%{buildroot}/${MPI_MAN} bindir=%{buildroot}/${MPI_BIN}

pushd %{buildroot}/${MPI_BIN}
for prog in *; do
    mv $prog scotch_${prog}
done
rm -f scotch_dgpart && ln -s ./scotch_dgmap scotch_dgpart
popd

pushd %{buildroot}/${MPI_MAN}/man1/
rm -f {a,g,m}*
for man in *; do
    mv ${man} scotch_${man}
done
popd
%{_openmpi_unload}
popd

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post mpich2 -p /sbin/ldconfig

%postun mpich2 -p /sbin/ldconfig

%post openmpi -p /sbin/ldconfig

%postun openmpi -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc scotch_%{version}/README.txt scotch_%{version}/doc/*
%{_bindir}/*
%{_libdir}/libscotch*.so.*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libscotch*.so
%{_includedir}/*scotch*.h

%files static
%defattr(-,root,root,-)
%{_libdir}/libscotch*.a

%files mpich2
%defattr(-,root,root,-)
%{_libdir}/mpich2*/lib/libptscotch*.so.*
%{_libdir}/mpich2*/bin/*
%{_mandir}/mpich2*/*

%files openmpi
%defattr(-,root,root,-)
%{_libdir}/openmpi*/lib/libptscotch*.so.*
%{_libdir}/openmpi*/bin/*
%{_mandir}/openmpi*/*

%files mpich2-devel
%defattr(-,root,root,-)
%{_includedir}/mpich2*/*scotch*.h
%{_libdir}/mpich2*/lib/libptscotch*.so

%files openmpi-devel
%defattr(-,root,root,-)
%{_includedir}/openmpi*/*scotch*.h
%{_libdir}/openmpi*/lib/libptscotch*.so

%files mpich2-static
%defattr(-,root,root,-)
%{_libdir}/mpich2*/lib/libptscotch*.a

%files openmpi-static
%defattr(-,root,root,-)
%{_libdir}/openmpi*/lib/libptscotch*.a

%changelog
* Mon Oct 08 2012 Erik Zeek <eczeek@sandia.gov> - 5.1.11-3
- Use internal build machinery to build shared libraries.
- A bunch of MPI love.
-   Install Mpich2 libraries in the proper path.
-   Provide Mpich2 and OpenMPI libraries.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Mar 29 2011 Deji Akingunola <dakingun@gmail.com> - 5.1.11-1
- Update to 5.1.11

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.10b-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 19 2010 Deji Akingunola <dakingun@gmail.com> - 5.1.10b-1
- Update to 5.1.10b

* Thu Aug 12 2010 Deji Akingunola <dakingun@gmail.com> - 5.1.9-1
- Update to 5.1.9
- No more static builds

* Tue Apr 27 2010 Deji Akingunola <dakingun@gmail.com> - 5.1.8-1
- Update to 5.1.8

* Wed Nov 04 2009 Deji Akingunola <dakingun@gmail.com> - 5.1.7-2
- Fix the Source url

* Sun Sep 20 2009 Deji Akingunola <dakingun@gmail.com> - 5.1.7-1
- Update to 5.1.7
- Put the library under libdir

* Thu Jun 11 2009 Deji Akingunola <dakingun@gmail.com> - 5.1.6-3
- Further spec fixes from package review (convert license files to utf8)
- Prefix binaries and their corresponding manpages with scotch_ .
- Link in appropriates libraries when creating shared libs

* Thu Jun 04 2009 Deji Akingunola <dakingun@gmail.com> - 5.1.6-2
- Add zlib-devel as BR

* Wed May 13 2009 Deji Akingunola <dakingun@gmail.com> - 5.1.6-1
- Update to 5.1.6

* Sat Nov 21 2008 Deji Akingunola <dakingun@gmail.com> - 5.1.2-1
- Update to 5.1.2

* Tue Sep 19 2008 Deji Akingunola <dakingun@gmail.com> - 5.1.1-1
- initial package creation
