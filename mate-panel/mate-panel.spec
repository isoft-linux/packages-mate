# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
%global branch 1.14

# Settings used for build from snapshots.
%{!?rel_build:%global commit 838555a41dc08a870b408628f529b66e2c8c4054}
%{!?rel_build:%global commit_date 20140222}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Name:           mate-panel
Version:        %{branch}.0
%if 0%{?rel_build}
Release:        2%{?dist}
%else
Release:        0.3%{?git_rel}%{?dist}
%endif
Summary:        MATE Desktop panel and applets
#libs are LGPLv2+ applications GPLv2+
License:        GPLv2+
URL:            http://mate-desktop.org

# for downloading the tarball use 'spectool -g -R mate-panel.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%{name}/snapshot/%{name}-%{commit}.tar.xz#/%{git_tar}}

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
# needed as nothing else requires it
Requires:       mate-session-manager
#for fish
Requires:       fortune-mod
Requires:       hicolor-icon-theme
# rhbz (#1007219)
#Requires:       caja-schemas

BuildRequires:  dbus-glib-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk2-devel
BuildRequires:  libcanberra-devel
BuildRequires:  libmateweather-devel
BuildRequires:  libwnck-devel
BuildRequires:  librsvg2-devel
BuildRequires:  libSM-devel
BuildRequires:  mate-common
BuildRequires:  mate-desktop-devel
BuildRequires:  mate-menus-devel
BuildRequires:  yelp-tools
BuildRequires:  libcanberra-gtk2-devel

%description
MATE Desktop panel applets


%package libs
Summary:     Shared libraries for mate-panel
License:     LGPLv2+
Requires:    %{name}%{?_isa} = %{version}-%{release}

%description libs
Shared libraries for libmate-desktop

%package devel
Summary:     Development files for mate-panel
Requires:    %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
Development files for mate-panel

%prep
%setup -q%{!?rel_build:n %{name}-%{commit}}

%if 0%{?rel_build}
#NOCONFIGURE=1 ./autogen.sh
%else # 0%{?rel_build}
# needed for git snapshots
NOCONFIGURE=1 ./autogen.sh
%endif # 0%{?rel_build}

%build

#libexecdir needed for gnome conflicts
%configure                                        \
           --disable-static                       \
           --disable-schemas-compile              \
           --with-x                               \
           --libexecdir=%{_libexecdir}/mate-panel \
           --with-gtk=2.0                         \
           --enable-introspection                 \
           --enable-gtk-doc

# remove unused-direct-shlib-dependency
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

make  %{?_smp_mflags} V=1


%install
%{make_install}

find %{buildroot} -name '*.la' -exec rm -rf {} ';'
find %{buildroot} -name '*.a' -exec rm -rf {} ';'

desktop-file-install \
        --dir=%{buildroot}%{_datadir}/applications \
%{buildroot}%{_datadir}/applications/mate-panel.desktop

# remove needless gsettings convert file
rm -f  %{buildroot}%{_datadir}/MateConf/gsettings/mate-panel.convert

%find_lang %{name} --with-gnome --all-name


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi
update-desktop-database &> /dev/null || :

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig


%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_mandir}/man1/*
%{_bindir}/mate-desktop-item-edit
%{_bindir}/mate-panel
%{_bindir}/mate-panel-test-applets
%{_libexecdir}/mate-panel
%{_datadir}/glib-2.0/schemas/org.mate.panel.*.xml
%{_datadir}/applications/mate-panel.desktop
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/mate-panel
%{_datadir}/dbus-1/services/org.mate.panel.applet.ClockAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.FishAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.NotificationAreaAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.WnckletFactory.service

%files libs
%doc COPYING.LIB
%{_libdir}/libmate-panel-applet-4.so.1*
%{_libdir}/girepository-1.0/MatePanelApplet-4.0.typelib

%files devel
%doc %{_datadir}/gtk-doc/html/mate-panel-applet/
%{_libdir}/libmate-panel-applet-4.so
%{_includedir}/mate-panel-4.0
%{_libdir}/pkgconfig/libmatepanelapplet-4.0.pc
%{_datadir}/gir-1.0/MatePanelApplet-4.0.gir


%changelog
* Fri May 06 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 1.14.0-2
- 1.14.0
- Remove caja-schemas require temporarily.
