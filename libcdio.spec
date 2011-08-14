Name: libcdio
Version: 0.81
Release: 3.1%{?dist}
Summary: CD-ROM input and control library
Group: System Environment/Libraries
License: GPLv3+
URL: http://www.gnu.org/software/libcdio/
Source0: http://ftp.gnu.org/gnu/libcdio/libcdio-0.81.tar.gz
Source1: http://ftp.gnu.org/gnu/libcdio/libcdio-0.81.tar.gz.sig
Source2: libcdio-no_date_footer.hml
Patch0: libcdio-0.81-cdio_get_default_device_linux.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: pkgconfig doxygen
BuildRequires: ncurses-devel
BuildRequires: help2man
Requires(post): /sbin/ldconfig
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
BuildRequires: gettext-devel


%description
This library provides an interface for CD-ROM access. It can be used
by applications that need OS- and device-independent access to CD-ROM
devices.

%package        devel
Summary:        Header files and static libraries for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
This package contains header files and static libraries for %{name}.


%prep
%setup -q
%patch0 -p1

f=src/cd-paranoia/doc/ja/cd-paranoia.1.in
iconv -f euc-jp -t utf-8 -o $f.utf8 $f && mv $f.utf8 $f


%build
%configure \
	--disable-vcd-info \
	--disable-dependency-tracking \
	--disable-cddb \
	--disable-rpath
make %{?_smp_mflags}

# another multilib fix; remove the architecture information from version.h
sed -i -e "s,%{version}.*$,%{version}\\\",g" include/cdio/version.h

cd doc/doxygen
sed -i -e "s,HTML_FOOTER.*$,HTML_FOOTER = libcdio-no_date_footer.hml,g" Doxyfile
cp %{SOURCE2} .
./run_doxygen

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_infodir}/dir
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

mv $RPM_BUILD_ROOT%{_mandir}/{jp,ja}

rm -rf examples
mkdir -p examples/C++
cp -a example/{*.c,README} examples
cp -a example/C++/{*.cpp,README} examples/C++

# fix timestamps of generated man-pages
for i in cd-info iso-read iso-info cd-read cd-drive; do 
	# remove build architecture information from man pages
	sed -i -e 's, version.*linux-gnu,,g' $RPM_BUILD_ROOT%{_mandir}/man1/$i.1
	# remove libtool leftover from man pages
	sed -i -e 's,lt-,,g;s,LT-,,g' $RPM_BUILD_ROOT%{_mandir}/man1/$i.1
	# fix timestamps to be the same in all packages
	touch -r src/$i.help2man $RPM_BUILD_ROOT%{_mandir}/man1/$i.1
done

%check
# disable test using local CDROM
%{__sed} -i -e "s,testiso9660\$(EXEEXT),,g" \
	    -e "s,testisocd\$(EXEEXT),,g" \
            -e "s,check_paranoia.sh check_opts.sh, check_opts.sh,g" \
            test/Makefile
make check


%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/ldconfig
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir 2>/dev/null || :

%preun
if [ $1 = 0 ]; then
	/sbin/install-info --delete %{_infodir}/%{name}.info \
		%{_infodir}/dir 2>/dev/null || :
fi

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README README.libcdio THANKS TODO
%{_bindir}/*
%{_libdir}/*.so.*
%{_infodir}/*
%{_mandir}/man1/*
%lang(ja) %{_mandir}/ja/man1/*


%files devel
%defattr(-,root,root,-)
%doc doc/doxygen/html examples
%{_includedir}/cdio
%{_includedir}/cdio++
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.81-3.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.81-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.81-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Oct 07 2008 Adrian Reber <adrian@lisas.de> - 0.81-1
- updated to 0.81
- license changed to GPLv3+
- fixed #477288 (libcdio-devel multilib conflict)
- applied patch to fix endless loop in mock

* Tue Oct 07 2008 Adrian Reber <adrian@lisas.de> - 0.80-5
- fixed #462125 (Multilib conflict) - really, really, really
  (also remove architecture information from man pages)

* Thu Oct 02 2008 Adrian Reber <adrian@lisas.de> - 0.80-4
- fixed #462125 (Multilib conflict) - this time for real

* Fri Sep 12 2008 Adrian Reber <adrian@lisas.de> - 0.80-3
- fixed #462125 (Multilib conflict)

* Wed Jun  4 2008 Tomas Bzatek <tbzatek@redhat.com> - 0.80-2
- added patch enabling libcdio_paranoia.pc

* Thu May 29 2008 Adrian Reber <adrian@lisas.de> - 0.80-1
- updated to 0.80
- removed upstreamed patches
- last GPLv2+ release

* Thu Feb 14 2008 Adrian Reber <adrian@lisas.de> - 0.79-3
- added patch to compile with gcc43

* Fri Jan 04 2008 Adrian Reber <adrian@lisas.de> - 0.79-2
- fixed security fix (was off by two)

* Wed Jan 02 2008 Adrian Reber <adrian@lisas.de> - 0.79-1
- updated to 0.79
- fixes #427197 (Long Joliet file name overflows cdio's buffer)
- fixes #341981 (multiarch conflicts in libcdio)

* Fri Aug 24 2007 Adrian Reber <adrian@lisas.de> - 0.78.2-3
- rebuilt

* Mon Jul 23 2007 Adrian Reber <adrian@lisas.de> - 0.78.2-2
- updated to 0.78.2 (#221359) (this time for real)

* Thu Jan 04 2007 Adrian Reber <adrian@lisas.de> - 0.78.2-1
- updated to 0.78.2 (#221359)

* Thu Oct 05 2006 Adrian Reber <adrian@lisas.de> - 0.77-3
- disabled iso9660 test case (fails for some reason with date problems)
  this seems to be a known problem according to the ChangeLog

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.77-2
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Fri Sep 22 2006 Adrian Reber <adrian@lisas.de> - 0.77-1
- Updated to 0.77

* Mon Sep 18 2006 Adrian Reber <adrian@lisas.de> - 0.76-3
- Rebuilt

* Mon Sep 26 2005 Adrian Reber <adrian@lisas.de> - 0.76-2
- Rebuilt

* Mon Sep 26 2005 Adrian Reber <adrian@lisas.de> - 0.76-1
- Updated to 0.76.
- Included doxygen generated documentation into -devel
- Included examples into -devel

* Mon Aug 01 2005 Adrian Reber <adrian@lisas.de> - 0.75-4
- disable test accessing local CDROM drive (#164266)

* Wed Jul 27 2005 Adrian Reber <adrian@lisas.de> - 0.75-3
- Rebuilt without libcddb dependency (#164270)

* Tue Jul 26 2005 Adrian Reber <adrian@lisas.de> - 0.75-2
- Rebuilt

* Thu Jul 14 2005 Adrian Reber <adrian@lisas.de> - 0.75-1
- Updated to 0.75.

* Fri Jun 03 2005 Adrian Reber <adrian@lisas.de> - 0.74-2
- Updated to 0.74.

* Sun Apr 24 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.73-2
- BuildRequire ncurses-devel (for cdda-player and cd-paranoia).
- Run test suite during build.
- Install Japanese man pages.

* Sun Apr 24 2005 Adrian Reber <adrian@lisas.de> - 0.73-1
- Updated to 0.73.

* Fri Mar 18 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.70-2
- Fix FC4 build (#151468).
- Build with dependency tracking disabled.

* Sun Sep  5 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.70-0.fdr.1
- Updated to 0.70.

* Sat Jul 17 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.69-0.fdr.1
- Updated to 0.69.
- Removed broken iso-read.
- Split Requires(pre,post).
- Added BuildReq pkgconfig.

* Mon Mar 29 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.68-0.fdr.1
- Initial RPM release.

