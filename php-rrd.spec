%define modname rrd
%define dirname %{modname}
%define soname %{modname}.so
%define inifile B16_%{modname}.ini

Summary:	PHP bindings to rrd tool system
Name:		php-%{modname}
Version:	1.1.0
Release:	%mkrel 1
Group:		Development/PHP
License:	PHP
URL:		http://pecl.php.net/package/rrd
Source0:	http://pecl.php.net/get/rrd-%{version}.tgz
Source1:	B16_rrd.ini
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	rrdtool-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Procedural and simple OO wrapper for rrdtool - data logging and graphing
system for time series data.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

cp %{SOURCE1} %{inifile}

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make
mv modules/*.so .

%install
rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/
install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc package*.xml
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}



%changelog
* Wed Jun 20 2012 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-1mdv2012.0
+ Revision: 806394
- 1.1.0

* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.5-3
+ Revision: 795493
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.5-2
+ Revision: 761285
- rebuild

* Wed Nov 23 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.5-1
+ Revision: 732993
- 1.0.5

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.4-3
+ Revision: 696462
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.4-2
+ Revision: 695458
- rebuilt for php-5.3.7

* Sat Aug 13 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.4-1
+ Revision: 694327
- 1.0.4

* Tue May 17 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-1
+ Revision: 675428
- import php-rrd


* Tue May 17 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-1mdv2010.2
- initial Mandriva package
