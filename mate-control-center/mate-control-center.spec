# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
%global branch 1.14

# Settings used for build from snapshots.
%{!?rel_build:%global commit 922d0e0219b1bedcece8624e4b5fd7e15e7a9bd5}
%{!?rel_build:%global commit_date 20131113}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Name:          mate-control-center
Version:       %{branch}.0
%if 0%{?rel_build}
Release:       1%{?dist}
%else
Release:       0.6%{?git_rel}%{?dist}
%endif
Summary:       MATE Desktop control-center
License:       LGPLv2+ and GPLv2+
URL:           http://mate-desktop.org

# for downloading the tarball use 'spectool -g -R mate-control-center.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%{name}/snapshot/%{name}-%{commit}.tar.xz#/%{git_tar}}

BuildRequires: dconf-devel
BuildRequires: desktop-file-utils
BuildRequires: gtk2-devel
BuildRequires: libcanberra-devel
BuildRequires: libmatekbd-devel
BuildRequires: librsvg2-devel
BuildRequires: libSM-devel
BuildRequires: libXScrnSaver-devel
BuildRequires: libXxf86misc-devel
BuildRequires: mate-common
BuildRequires: mate-desktop-devel
BuildRequires: mate-menus-devel
BuildRequires: mate-settings-daemon-devel
BuildRequires: marco-devel
BuildRequires: unique-devel

Requires: gsettings-desktop-schemas
# rhbz (#1234438)
Requires: mate-settings-daemon
# keyring support
Requires: gnome-keyring
Requires: %{name}-filesystem%{?_isa} = %{version}-%{release}


%description 
MATE Control Center configures system settings such as themes,
keyboards shortcuts, etc.

%package filesystem
Summary:      MATE Control Center directories
# NOTE: this is an "inverse dep" subpackage. It gets pulled in
# NOTE: by the main package an MUST not depend on the main package

%description filesystem
The MATE control-center provides a number of extension points
for applications. This package contains directories where applications
can install configuration files that are picked up by the control-center
utilities.

%package devel
Summary:      Development files for mate-settings-daemon
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for mate-control-center


%prep
%setup -q%{!?rel_build:n %{name}-%{commit}}

%if 0%{?rel_build}
#NOCONFIGURE=1 ./autogen.sh
%else # 0%{?rel_build}
# for snapshots
# needed for git snapshots
NOCONFIGURE=1 ./autogen.sh
%endif # 0%{?rel_build}

%build
%configure                           \
           --disable-static          \
           --disable-schemas-compile \
           --disable-update-mimedb

# remove unused-direct-shlib-dependency
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags} V=1


%install
%{make_install}

find %{buildroot} -name '*.la' -exec rm -rf {} ';'
find %{buildroot} -name '*.a' -exec rm -rf {} ';'

desktop-file-install                                \
    --delete-original                               \
    --dir=%{buildroot}%{_datadir}/applications      \
%{buildroot}%{_datadir}/applications/*.desktop

# delete mime cache
rm %{buildroot}%{_datadir}/applications/mimeinfo.cache

# mate-preferences-categories.menu is back in mate-menus
rm -f  %{buildroot}%{_sysconfdir}/xdg/menus/mate-preferences-categories.menu

# remove needless gsettings convert file
rm -f  %{buildroot}%{_datadir}/MateConf/gsettings/mate-control-center.convert

%find_lang %{name} --with-gnome --all-name


%post
/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
/bin/touch --no-create %{_datadir}/mime/packages &> /dev/null || :

%postun
/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
    /bin/touch --no-create %{_datadir}/mime/packages &> /dev/null || :
    /usr/bin/update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
/usr/bin/update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS COPYING README
%config %{_sysconfdir}/xdg/menus/matecc.menu
%{_bindir}/mate-*
%{_libdir}/libmate-window-settings.so.*
%{_libdir}/window-manager-settings
%{_libdir}/libmate-slab.so.*
%{_sbindir}/mate-display-properties-install-systemwide
%{_datadir}/applications/*.desktop
%{_datadir}/desktop-directories/matecc.directory
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/icons/hicolor/scalable/apps/mate-*.svg
%{_datadir}/glib-2.0/schemas/org.mate.*.xml
%{_datadir}/mate-control-center/*
%{_datadir}/mate/cursor-fonts/*.pcf
%{_datadir}/mime/packages/mate-theme-package.xml
%{_datadir}/thumbnailers/mate-font-viewer.thumbnailer
%{_datadir}/polkit-1/actions/org.mate.randr.policy
%{_mandir}/man1/mate-*.1.*

%files filesystem
%dir %{_datadir}/mate-control-center
%dir %{_datadir}/mate-control-center/keybindings

%files devel
%{_includedir}/mate-window-settings-2.0
%{_libdir}/pkgconfig/mate-window-settings-2.0.pc
%{_libdir}/libmate-window-settings.so
%{_libdir}/pkgconfig/mate-default-applications.pc
%{_libdir}/pkgconfig/mate-keybindings.pc
%{_includedir}/libmate-slab/
%{_libdir}/libmate-slab.so
%{_libdir}/pkgconfig/mate-slab.pc


%changelog
* Fri May 06 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 1.14.0-1
- 1.14.0
