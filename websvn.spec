%define name	websvn
%define version	2.2.1
%define release	%mkrel 4

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
Patch0:     websvn-2.2.1-fhs.patch
Patch1:     websvn-2.2.1-use-external-geshi.patch
Requires:	subversion
Requires:	apache-mod_php
Requires:	php-iconv
Requires:	php-xml
Requires:	php-geshi
Obsoletes:	WebSVN
# webapp macros and scriptlets
Requires(post):		rpm-helper >= 0.16
Requires(postun):	rpm-helper >= 0.16
BuildRequires:	rpm-helper >= 0.16
BuildRequires:	rpm-mandriva-setup >= 1.23
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

install -d -m 755 %{buildroot}/%{_datadir}/%{name}/lib
cp lib/feedcreator.class.php %{buildroot}/%{_datadir}/%{name}/lib

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

%post
%if %mdkversion < 201010
%_post_webapp
%endif

%postun
%if %mdkversion < 201010
%_postun_webapp
%endif

%clean
rm -rf  %{buildroot} 

%files
%defattr(-,root,root)
%doc license.txt changes.txt
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_webappconfdir}/%{name}.conf
%{_datadir}/%{name}
%attr(0755,apache,apache) %{_localstatedir}/cache/%{name}
