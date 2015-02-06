#Module-Specific definitions
%define mod_name mod_chroot
%define mod_conf A85_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Mod_chroot makes running Apache in a secure chroot environment easy
Name:		apache-%{mod_name}
Version:	0.5
Release:	13
Group:		System/Servers
License:	GPL
URL:		http://core.segfault.pl/~hobbit/mod_chroot/
Source0:	http://core.segfault.pl/~hobbit/mod_chroot/dist/%{mod_name}-%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
Patch0:		mod_chroot-0.5-no_version_component.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0

%description
mod_chroot makes running Apache in a secure chroot environment easy. You don't
need to create a special directory hierarchy containing /dev, /lib, /etc...

%prep

%setup -q -n %{mod_name}-%{version}
%patch0 -p0

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type d -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type d -name .svn` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -r $i; fi >&/dev/null
done
    
# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

%{_bindir}/apxs -c %{mod_name}.c

%install

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/apache-extramodules

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
 %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
 if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
 fi
fi

%clean

%files
%doc CAVEATS ChangeLog INSTALL LICENSE README README.Apache20
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}




%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 0.5-12mdv2012.0
+ Revision: 772607
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.5-11
+ Revision: 678293
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.5-10mdv2011.0
+ Revision: 587951
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 0.5-9mdv2010.1
+ Revision: 516079
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.5-8mdv2010.0
+ Revision: 406563
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 0.5-7mdv2009.1
+ Revision: 325677
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 0.5-6mdv2009.0
+ Revision: 234854
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.5-5mdv2009.0
+ Revision: 215558
- fix rebuild

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 0.5-4mdv2008.1
+ Revision: 181713
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 0.5-3mdv2008.0
+ Revision: 82546
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 0.5-2mdv2007.1
+ Revision: 140658
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 0.5-1mdv2007.1
+ Revision: 79390
- Import apache-mod_chroot

* Fri Aug 04 2006 Oden Eriksson <oeriksson@mandriva.com> 0.5-1mdv2007.0
- initial Mandriva package

