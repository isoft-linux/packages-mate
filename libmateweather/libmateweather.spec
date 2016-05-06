Name:          libmateweather
Version:       1.14.0
Release:       1%{?dist}
Summary:       Libraries to allow MATE Desktop to display weather information
License:       GPLv2+ and LGPLv2+
URL:           http://mate-desktop.org
Source0:       http://pub.mate-desktop.org/releases/1.14/%{name}-%{version}.tar.xz

BuildRequires: gtk2-devel
BuildRequires: libsoup-devel
BuildRequires: mate-common
BuildRequires: pygtk2-devel
BuildRequires: pygobject2-devel

Requires:      %{name}-data = %{version}-%{release}

%description
Libraries to allow MATE Desktop to display weather information

%package data
Summary: Data files for the libmateweather
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

%description data
This package contains shared data needed for libmateweather.

%package devel
Summary:  Development files for libmateweather
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for libmateweather


%prep
%setup -q


%build
%configure --disable-static           \
           --disable-schemas-compile  \
           --with-gtk=2.0             \
           --enable-gtk-doc-html      \
           --enable-python

# fix unused-direct-shlib-dependency
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' libtool 

make %{?_smp_mflags} V=1

%install
%{make_install}

find %{buildroot} -name '*.la' -exec rm -fv {} ';'
find %{buildroot} -name '*.a' -exec rm -fv {} ';'

%find_lang %{name} --with-gnome --all-name


%post -p /sbin/ldconfig

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%post data
/bin/touch --no-create %{_datadir}/icons/mate &>/dev/null || :

%postun data
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/mate &>/dev/null
    /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/mate &>/dev/null || :
fi

%posttrans data
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/mate &>/dev/null || :


%files
%doc AUTHORS COPYING README
%{_datadir}/glib-2.0/schemas/org.mate.weather.gschema.xml
%{_libdir}/libmateweather.so.1*
%{python2_sitearch}/mateweather/

%files data -f %{name}.lang
%{_datadir}/icons/mate/*/status/*
%{_datadir}/libmateweather/

%files devel
%doc %{_datadir}/gtk-doc/html/libmateweather/
%{_libdir}/libmateweather.so
%{_includedir}/libmateweather/
%{_libdir}/pkgconfig/mateweather.pc


%changelog
* Fri May 06 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 1.14.0-1
- 1.14.0
