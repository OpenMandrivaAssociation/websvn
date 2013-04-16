%define name	websvn
%define version	2.3.2
%define release:	3

%define _requires_exceptions pear(.*geshi.php)

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	PHP based web interface of Subversion repositories
Epoch:		1
License:	GPL
Group:		System/Servers
URL:		http://websvn.tigris.org/
Source:		http://websvn.tigris.org/files/documents/1380/39378/%{name}-%{version}.tar.gz
Patch0:     websvn-2.3.2-fhs.patch
Patch1:     websvn-2.3.0-use-external-geshi.patch
Requires:	subversion
Requires:	apache-mod_php
Requires:	php-iconv
Requires:	php-xml
Requires:	php-geshi
%if %mdkversion < 201010
Requires(post):   rpm-helper
Requires(postun):   rpm-helper
%endif
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
WebSVN offers a view onto your subversion repositories that's been designed to
reflect the Subversion methodology. You can view the log of any file or
directory and see a list of all the files changed, added or deleted in any
given revision. You can also view the differences between 2 versions of a file
so as to see exactly what was changed in a particular revision.

WebSVN offers the following features:

    * Easy to use interface
    * Highly customisable templating system
    * Log message searching
    * Colourisation of file listings
    * Blame support
    * Tar ball downloads
    * Directory comparisons
    * RSS Feed support
    * Fast browsing thanks to internal caching feature
    * Apache MultiViews support
    * Support for bugtraq:properties 

%prep
%setup -q
%patch0 -p 1
%patch1 -p 1

%build

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}/%{_datadir}/%{name}
install -d -m 755 %{buildroot}/%{_datadir}/%{name}/www
cp -pr *.php %{buildroot}%{_datadir}/%{name}/www
cp -pr templates %{buildroot}%{_datadir}/%{name}/www

cp -pr include %{buildroot}%{_datadir}/%{name}
cp -pr languages %{buildroot}%{_datadir}/%{name}

install -d -m 755 %{buildroot}%{_sysconfdir}
mv %{buildroot}/%{_datadir}/%{name}/include/distconfig.php \
   %{buildroot}%{_sysconfdir}/%{name}.conf

install -d -m 755 %{buildroot}%{_localstatedir}/cache/%{name}

pushd %{buildroot}%{_datadir}/%{name}/www
ln -sf ../include .
ln -sf ../languages .
ln -sf ../lib .
ln -sf ../../../..%{_localstatedir}/cache/%{name} cache
popd

pushd %{buildroot}%{_datadir}/%{name}/include
ln -sf ../../../..%{_sysconfdir}/%{name}.conf config.php
popd

# Create apache conf file
install -d -m 755 %{buildroot}%{_webappconfdir}

cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
Alias /%{name} %{_datadir}/%{name}/www

<Directory %{_datadir}/%{name}/www>
    Options -FollowSymLinks
    allow from all
</Directory>
EOF

cat > README.mdv <<EOF
Mandriva RPM specific notes

setup
-----
The setup used here differs from default one, to achieve better FHS compliance.
- the constant files are in /usr/share/websvn
- the generated files are in /var/cache/websvn
- the configuration file is /etc/websvn.conf
EOF



%clean
rm -rf  %{buildroot} 

%files
%defattr(-,root,root)
%doc license.txt changes.txt
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_webappconfdir}/%{name}.conf
%{_datadir}/%{name}
%attr(0755,apache,apache) %{_localstatedir}/cache/%{name}


%changelog
* Mon Dec 20 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.3.2-1mdv2011.0
+ Revision: 623314
- new version

* Sun Jul 25 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.3.1-1mdv2011.0
+ Revision: 558814
- new version

* Sun Feb 07 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.3.0-1mdv2010.1
+ Revision: 501826
- new version

* Sun Jan 17 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.2.1-4mdv2010.1
+ Revision: 492695
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise

* Thu Sep 03 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.2.1-3mdv2010.0
+ Revision: 428993
- fix dependencies

* Wed Aug 19 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.2.1-2mdv2010.0
+ Revision: 418295
- fix include path for geshi

* Sun Jul 19 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.2.1-1mdv2010.0
+ Revision: 397429
- new version
- reduce FHS patch to documentation, and use symlinks instead
- move web files under %%{_datadir}/www

* Wed Mar 04 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.1.0-2mdv2009.1
+ Revision: 348651
- don't forget to ship lib directory

* Tue Mar 03 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.1.0-1mdv2009.1
+ Revision: 347890
- new version
- rediff FHS patch

* Sun Aug 03 2008 Thierry Vignaud <tv@mandriva.org> 1:2.0-4mdv2009.0
+ Revision: 261929
- rebuild

* Wed Jul 30 2008 Thierry Vignaud <tv@mandriva.org> 1:2.0-3mdv2009.0
+ Revision: 255894
- rebuild

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 1:2.0-1mdv2008.1
+ Revision: 136572
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Aug 17 2007 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.0-1mdv2008.0
+ Revision: 65298
- spec cleanup
- new version
- import websvn


* Thu Jun 29 2006 Jerome Martin <jmartin@mandriva.org> 2.0-0.rc1.4mdv2006.0
- Fix require for backport

* Mon Jun 26 2006 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.0-0.rc1.3mdv2007.0
- %%mkrel
- new webapp macros
- better EOL correction
- use heredoc for README.mdv
- fix requires

* Thu May 11 2006 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.0-0.rc1.2mdk
- more complete FHS patch

* Wed May 10 2006 Franck Villaume <fvill@mandriva.org> 1:2.0-0.rc1.1mdk
- 2.0rc1

* Fri Apr 07 2006 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.0-0.beta7.9mdk
- revert to FHS compliant setup
- split templates content between webroot and data dir
- backport compatible apache configuration file
- requires php-xml too

* Fri Mar 31 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.0-0.beta7.8mdk
- more fixes to make it work as intended

* Fri Mar 31 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.0-0.beta7.7mdk
- fix one missing absolute path in P0

* Fri Mar 24 2006 Guillaume Rousse <guillomovitch@mandriva.org> 1:2.0-0.beta7.6mdk
- use a pristine source tarball  
- rediff fhs patch
- spec cleanup
- remove useless details in description: all webapps use the same scheme

* Fri Mar 17 2006 Franck Villaume <fvill@mandriva.org> 1:2.0-0.beta7.5mdk
- package rename

* Thu Mar 16 2006 Franck Villaume <fvill@mandriva.org> 1:2.0-0.beta7.4mdk
- sync with websvn-1.61 package from guillomovitch@mandriva.org

* Mon Nov 28 2005 Franck Villaume <fvill@mandriva.org> 1:2.0-0.beta7.3mdk
- fix bug 19966 from J.P. Pasnak <pasnak@warpedsystems.sk.ca>

* Sun Nov 13 2005 Franck Villaume <fvill@mandriva.fr> 1:2.0-0.beta7.2mdk
- fix url
  from jamagallon@able.es

* Thu Nov 10 2005 Franck Villaume <fvill@mandriva.fr> 1:2.0-0.beta7.1mdk
- new release
- versioning
- config file for apache

* Thu Sep 2 2004 Franck Villaume <fvill@freesurf.fr> 161-1mdk
- First package

