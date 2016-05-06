# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
%global branch 1.14

# Settings used for build from snapshots.
%{!?rel_build:%global commit a6a0a5879533b0915901ab69703eaf327bbca846 }
%{!?rel_build:%global commit_date 20141215}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Summary:        Shared code for mate-panel, mate-session, mate-file-manager, etc
Name:           mate-desktop
License:        GPLv2+ and LGPLv2+ and MIT
Version:        %{branch}.0
%if 0%{?rel_build}
Release:        1%{?dist}
%else
Release:        0.2%{?git_rel}%{?dist}
%endif
URL:            http://mate-desktop.org

# for downloading the tarball use 'spectool -g -R mate-desktop.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%{name}/snapshot/%{name}-%{commit}.tar.xz#/%{git_tar}}

BuildRequires:  dconf-devel
BuildRequires:  desktop-file-utils
BuildRequires:  mate-common
BuildRequires:  startup-notification-devel
BuildRequires:  unique-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  cairo-gobject-devel

Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: redhat-menus
Requires: pygtk2
Requires: xdg-user-dirs-gtk
Requires: mate-control-center-filesystem
Requires: mate-panel
Requires: mate-notification-daemon
Requires: mate-user-guide

%description
The mate-desktop package contains an internal library
(libmatedesktop) used to implement some portions of the MATE
desktop, and also some data files and other shared components of the
MATE user environment.

%package libs
Summary:   Shared libraries for libmate-desktop
License:   LGPLv2+

%description libs
Shared libraries for libmate-desktop

%package devel
Summary:    Libraries and headers for libmate-desktop
License:    LGPLv2+
Requires:   %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
Libraries and header files for the MATE-internal private library
libmatedesktop.


%prep
%setup -q%{!?rel_build:n %{name}-%{commit}}

%if 0%{?rel_build}
# for releases
#NOCONFIGURE=1 ./autogen.sh
%else
# needed for git snapshots
NOCONFIGURE=1 ./autogen.sh
%endif

%build
%configure                                                 \
     --enable-desktop-docs                                 \
     --disable-schemas-compile                             \
     --with-gtk=2.0                                        \
     --with-x                                              \
     --disable-static                                      \
     --enable-unique                                       \
     --enable-mpaste                                       \
     --with-pnp-ids-path="%{_datadir}/hwdata/pnp.ids"      \
     --enable-gtk-doc-html                                 \
     --enable-introspection=yes

make %{?_smp_mflags} V=1


%install
%{make_install}
find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name '*.a' -exec rm -f {} ';'


desktop-file-install                                         \
        --delete-original                                    \
        --dir=%{buildroot}%{_datadir}/applications           \
%{buildroot}%{_datadir}/applications/mate-about.desktop

desktop-file-install                                         \
        --delete-original                                    \
        --dir=%{buildroot}%{_datadir}/applications           \
%{buildroot}%{_datadir}/applications/mate-color-select.desktop

%find_lang %{name} --with-gnome --all-name


%post libs -p /sbin/ldconfig

%postun libs
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans libs
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
    /bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null
    /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &> /dev/null || :


%files
%doc AUTHORS COPYING COPYING.LIB NEWS README
%{_bindir}/mate-about
%{_bindir}/mpaste
%{_bindir}/mate-color-select
%{_datadir}/applications/mate-about.desktop
%{_datadir}/applications/mate-color-select.desktop
%{_datadir}/applications/mate-mimeapps.list
%{_datadir}/mate-about
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/icons/hicolor/scalable/apps/mate-symbolic.svg
%{_mandir}/man1/*

%files libs -f %{name}.lang
%{_libdir}/libmate-desktop-2.so.*
%{_datadir}/glib-2.0/schemas/org.mate.*.gschema.xml
%{_libdir}/girepository-1.0/MateDesktop-2.0.typelib

%files devel
%{_libdir}/libmate-desktop-2.so
%{_libdir}/pkgconfig/mate-desktop-2.0.pc
%{_includedir}/mate-desktop-2.0
%doc %{_datadir}/gtk-doc/html/mate-desktop
%{_datadir}/gir-1.0/MateDesktop-2.0.gir


%changelog
* Fri May 06 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 1.14.0-1
- 1.14.0
