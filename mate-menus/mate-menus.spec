Name:           mate-menus
Version:        1.14.0
Release:        1%{?dist}
Summary:        Displays menus for MATE Desktop
License:        GPLv2+ and LGPLv2+
URL:            http://mate-desktop.org
Source0:        http://pub.mate-desktop.org/releases/1.14/%{name}-%{version}.tar.xz

BuildRequires:  chrpath
BuildRequires:  gobject-introspection-devel
BuildRequires:  mate-common
BuildRequires:  python-devel

Requires:		%{name}-libs%{?_isa} = %{version}-%{release}

# we don't want to provide private python extension libs
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_setup
}

%description
Displays menus for MATE Desktop

%package libs
Summary: Shared libraries for mate-menus
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description libs
Shared libraries for mate-menus

%package preferences-category-menu
Summary: Categories for the preferences menu
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description preferences-category-menu
Categories for the preferences menu

%package devel
Summary: Development files for mate-menus
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description devel
Development files for mate-menus

%prep
%setup -q

%build
%configure \
 --disable-static \
 --enable-python \
 --enable-introspection=yes

make %{?_smp_mflags} V=1


%install
%{make_install}

find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name '*.a' -exec rm -f {} ';'
chrpath --delete $RPM_BUILD_ROOT%{python_sitearch}/matemenu.so

%find_lang %{name} --with-gnome --all-name

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files -f %{name}.lang
%doc AUTHORS COPYING README
%config %{_sysconfdir}/xdg/menus/mate-applications.menu
%config %{_sysconfdir}/xdg/menus/mate-settings.menu
%{_datadir}/mate-menus
%{_datadir}/mate/desktop-directories

%files preferences-category-menu
%config %{_sysconfdir}/xdg/menus/mate-preferences-categories.menu

%files libs
%{_libdir}/girepository-1.0/MateMenu-2.0.typelib
%{_libdir}/libmate-menu.so.2
%{_libdir}/libmate-menu.so.2.4.9
%{python_sitearch}/matemenu.so

%files devel
%{_datadir}/gir-1.0/MateMenu-2.0.gir
%{_libdir}/libmate-menu.so
%{_includedir}/mate-menus
%{_libdir}/pkgconfig/libmate-menu.pc


%changelog
* Fri May 06 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 1.14.0-1
- 1.14.0
