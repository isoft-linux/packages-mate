Name:           mate-common
Summary:        mate common build files
Version:        1.14.0
Release:        1%{?dist}
License:        GPLv3+
URL:            http://mate-desktop.org
Source0:        http://pub.mate-desktop.org/releases/1.14/mate-common-%{version}.tar.xz
BuildArch:      noarch
BuildRequires:  automake autoconf
Requires:       automake 
Requires:       autoconf 
Requires:       gettext 
Requires:       intltool 
Requires:       libtool 
Requires:       glib2-devel 
Requires:       gtk-doc 
Requires:       itstool 
Requires:       yelp-tools

%description
binaries for building all MATE desktop sub components

%prep
%setup -q

%build
%configure

make %{?_smp_mflags} V=1


%install
%{make_install}


%files
%{_bindir}/mate-*
%{_datadir}/aclocal/mate-*.m4
%{_datadir}/mate-common
%{_mandir}/man1/*

%changelog
* Fri May 06 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 1.14.0-1
- 1.14.0
