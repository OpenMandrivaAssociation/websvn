%define name	websvn
%define version	2.0
%define release	%mkrel 4

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	PHP based web interface of Subversion repositories
Epoch:		1
License:	GPL
Group:		System/Servers
URL:		http://websvn.tigris.org/
Source:		http://websvn.tigris.org/files/documents/1380/39378/%{name}-%{version}.tar.gz
Patch0:		websvn-2.0.fhs.patch
Requires:	subversion
Requires:	apache-mod_php
Requires:	php-iconv
Requires:	php-xml
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
%patch0 -p1
find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;

%build

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}/var/www/%{name}
cp -pr *.php %{buildroot}/var/www/%{name}

install -d -m 755 %{buildroot}/%{_datadir}/%{name}
cp -pr include %{buildroot}/%{_datadir}/%{name}
cp -pr languages %{buildroot}/%{_datadir}/%{name}

# distribut template content
find templates -type f -a -name '*.tmpl' | \
    tar --create --files-from - --remove-files | \
    (cd %{buildroot}%{_datadir}/%{name} && tar --preserve --extract)
find templates -type f -a -not -name '*.tmpl' | \
    tar --create --files-from - --remove-files | \
    (cd %{buildroot}/var/www/%{name} && tar --preserve --extract)

install -d -m 755 %{buildroot}%{_sysconfdir}
mv %{buildroot}/%{_datadir}/%{name}/include/distconfig.php \
   %{buildroot}%{_sysconfdir}/%{name}.conf

install -d -m 755 %{buildroot}/var/cache/%{name}

# Create apache conf file
install -d -m 755 %{buildroot}%{_webappconfdir}

cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
Alias /%{name} /var/www/%{name}

<Directory /var/www/%{name}>
    allow from all
</Directory>
EOF

cat > README.mdv <<EOF
Mandriva RPM specific notes

setup
-----
The setup used here differs from default one, to achieve better FHS compliance.
- the files accessibles from the web are in /var/www/websvn
- the files non accessibles from the web are in /usr/share/websvn
- generated files are in /var/cache/websvn
- the configuration file is /etc/websvn.conf
EOF

%post
%_post_webapp

%postun
%_postun_webapp

%clean
rm -rf  %{buildroot} 

%files
%defattr(-,root,root)
%doc licence.txt changes.txt
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_webappconfdir}/%{name}.conf
%{_datadir}/%{name}
/var/www/%{name}
%attr(0755,apache,apache) /var/cache/%{name}
