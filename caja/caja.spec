# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
%global branch 1.14

# Settings used for build from snapshots.
%{!?rel_build:%global commit ee0a62c8759040d84055425954de1f860bac8652}
%{!?rel_build:%global commit_date 20140223}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Name:        caja
Summary:     File manager for MATE
Version:     %{branch}.0
%if 0%{?rel_build}
Release:     1%{?dist}
%else
Release:     0.3%{?git_rel}%{?dist}
%endif
License:     GPLv2+ and LGPLv2+
Group:       User Interface/Desktops
URL:         http://mate-desktop.org

# for downloading the tarball use 'spectool -g -R caja.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%{name}/snapshot/%{name}-%{commit}.tar.xz#/%{git_tar}}

Patch0:        caja_add-xfce-to-desktop-file.patch
# rhbz (#1291540), https://github.com/mate-desktop/caja/commit/3d29330

BuildRequires:  dbus-glib-devel
BuildRequires:  desktop-file-utils
#BuildRequires:  exempi-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  cairo-gobject-devel
BuildRequires:  libexif-devel
#BuildRequires:  libselinux-devel
BuildRequires:  libSM-devel
BuildRequires:  libxml2-devel
BuildRequires:  mate-common
BuildRequires:  mate-desktop-devel
BuildRequires:  pangox-compat-devel
BuildRequires:  startup-notification-devel
BuildRequires:  unique-devel

Requires:   gamin
Requires:   filesystem
Requires:   redhat-menus
Requires:   gvfs

# the main binary links against libcaja-extension.so
# don't depend on soname, rather on exact version
Requires:       %{name}-extensions%{?_isa} = %{version}-%{release}

# needed for using mate-text-editor as stanalone in another DE
Requires:       %{name}-schemas%{?_isa} = %{version}-%{release}

Provides: mate-file-manager%{?_isa} = %{version}-%{release}
Provides: mate-file-manager = %{version}-%{release}
Obsoletes: mate-file-manager < %{version}-%{release}

%description
Caja (mate-file-manager) is the file manager and graphical shell
for the MATE desktop,
that makes it easy to manage your files and the rest of your system.
It allows to browse directories on local and remote file systems, preview
files and launch applications associated with them.
It is also responsible for handling the icons on the MATE desktop.

%package extensions
Summary:  Mate-file-manager extensions library
Requires: %{name}%{?_isa} = %{version}-%{release}
Provides: mate-file-manager-extensions%{?_isa} = %{version}-%{release}
Provides: mate-file-manager-extensions = %{version}-%{release}
Obsoletes: mate-file-manager-extensions < %{version}-%{release}

%description extensions
This package provides the libraries used by caja extensions.

# needed for using mate-text-editor (pluma) as stanalone in another DE
%package schemas
Summary:  Mate-file-manager schemas
License:  LGPLv2+
Provides: mate-file-manager-schemas%{?_isa} = %{version}-%{release}
Provides: mate-file-manager-schemas = %{version}-%{release}
Obsoletes: mate-file-manager-schemas < %{version}-%{release}

%description schemas
This package provides the gsettings schemas for caja.

%package devel
Summary:  Support for developing mate-file-manager extensions
Requires: %{name}%{?_isa} = %{version}-%{release}
Provides: mate-file-manager-devel%{?_isa} = %{version}-%{release}
Provides: mate-file-manager-devel = %{version}-%{release}
Obsoletes: mate-file-manager-devel < %{version}-%{release}

%description devel
This package provides libraries and header files needed
for developing caja extensions.

%prep
%setup -q%{!?rel_build:n %{name}-%{commit}}

%patch0 -p1 -b .add-xfce-to-desktop-file

%if 0%{?rel_build}
#NOCONFIGURE=1 ./autogen.sh
%else # 0%{?rel_build}
# for snapshots
# needed for git snapshots
NOCONFIGURE=1 ./autogen.sh
%endif # 0%{?rel_build}


%build
%configure \
        --disable-static \
        --enable-unique \
        --disable-schemas-compile \
        --with-x \
        --with-gtk=2.0 \
        --disable-update-mimedb

#drop unneeded direct library deps with --as-needed
# libtool doesn't make this easy, so we do it the hard way
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' libtool

make %{?_smp_mflags} V=1

%install
%{make_install}

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} ';'

rm -f $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/icon-theme.cache
rm -f $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/.icon-theme.cache

mkdir -p $RPM_BUILD_ROOT%{_libdir}/caja/extensions-2.0

desktop-file-install                              \
    --delete-original                             \
    --dir=$RPM_BUILD_ROOT%{_datadir}/applications \
$RPM_BUILD_ROOT%{_datadir}/applications/*.desktop

# remove needless gsettings convert file
rm -f  $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/caja.convert

# Avoid prelink to mess with caja - rhbz (#1228874)
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/prelink.conf.d
cat << EOF > ${RPM_BUILD_ROOT}%{_sysconfdir}/prelink.conf.d/caja.conf
-b %{_libdir}/caja/
-b %{_libdir}/libcaja-extension.so.*
-b %{_libexecdir}/caja-convert-metadata
-b %{_bindir}/caja
-b %{_bindir}/caja-autorun-software
-b %{_bindir}/caja-connect-server
-b %{_bindir}/caja-file-management-properties
EOF

%find_lang %{name}


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
/bin/touch --no-create %{_datadir}/mime/packages &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  /bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
  /bin/touch --no-create %{_datadir}/mime/packages &> /dev/null || :
  /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
  /usr/bin/update-desktop-database &> /dev/null || :
  /usr/bin/update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :
/usr/bin/update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :

%post extensions -p /sbin/ldconfig

%postun extensions -p /sbin/ldconfig

%postun schemas
if [ $1 -eq 0 ]; then
  /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans schemas
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files
%doc AUTHORS COPYING COPYING.LIB NEWS README
%{_bindir}/*
%{_datadir}/caja
%{_libdir}/caja/
%{_sysconfdir}/prelink.conf.d/caja.conf
%{_datadir}/pixmaps/caja/
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/caja.*
%{_datadir}/icons/hicolor/*/emblems/emblem-note.png
%{_mandir}/man1/*
%{_libexecdir}/caja-convert-metadata
%{_datadir}/appdata/caja.appdata.xml
%{_datadir}/mime/packages/caja.xml
%{_datadir}/dbus-1/services/org.mate.freedesktop.FileManager1.service

%files extensions
%{_libdir}/libcaja-extension.so.*
%{_libdir}/girepository-1.0/*.typelib

%files schemas -f %{name}.lang
%{_datadir}/glib-2.0/schemas/org.mate.*.gschema.xml

%files devel
%{_includedir}/caja/
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_datadir}/gir-1.0/*.gir
%{_datadir}/gtk-doc/html/libcaja-extension


%changelog
* Fri May 06 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 1.14.0-1
- 1.14.0
