# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
%global branch 1.14

# Settings used for build from snapshots.
%{!?rel_build:%global commit 62a708d461e08275d6b85985f5fa13fa8fbc85f7}
%{!?rel_build:%global commit_date 20131212}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Name:          marco
Version:       %{branch}.1
%if 0%{?rel_build}
Release:       1%{?dist}
%else
Release:       0.3%{?git_rel}%{?dist}
%endif
Summary:       MATE Desktop window manager
License:       LGPLv2+ and GPLv2+
URL:           http://mate-desktop.org

# for downloading the tarball use 'spectool -g -R marco.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%{name}/snapshot/%{name}-%{commit}.tar.xz#/%{git_tar}}

BuildRequires: desktop-file-utils
BuildRequires: gtk2-devel
BuildRequires: libcanberra-devel
BuildRequires: libgtop2-devel
BuildRequires: libSM-devel
BuildRequireS: libsoup-devel
BuildRequires: libXdamage-devel
BuildRequires: mate-common
BuildRequires: zenity
BuildRequires: startup-notification-devel
BuildRequires: yelp-tools

Requires:      mate-desktop-libs
Requires:      %{name}-libs%{?_isa} = %{version}-%{release}

# http://bugzilla.redhat.com/873342
# https://bugzilla.redhat.com/962009
Provides: firstboot(windowmanager) = marco

Provides: mate-window-manager%{?_isa} = %{version}-%{release}
Provides: mate-window-manager = %{version}-%{release}
Obsoletes: mate-window-manager < %{version}-%{release}
# rhbz (#1297958)
Obsoletes:     %{name} < 1.12.1-2

%description
MATE Desktop window manager

# to avoid that marco will install in other DE's by compiz-0.8.10
%package libs
Summary:       Libraries for marco
License:       LGPLv2+
# rhbz (#1297958)
Conflicts:     %{name} < 1.12.1-2

%description libs
This package provides Libraries for marco.

%package devel
Summary:       Development files for marco
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      %{name}-libs%{?_isa} = %{version}-%{release}
Provides:      mate-window-manager-devel%{?_isa} = %{version}-%{release}
Provides:      mate-window-manager-devel = %{version}-%{release}
Obsoletes:     mate-window-manager-devel < %{version}-%{release}

%description devel
Development files for marco

%prep
%setup -q%{!?rel_build:n %{name}-%{commit}}

%if 0%{?rel_build}
#NOCONFIGURE=1 ./autogen.sh
%else # 0%{?rel_build}
# needed for git snapshots
NOCONFIGURE=1 ./autogen.sh
%endif # 0%{?rel_build}

%build
%configure --disable-static           \
           --disable-schemas-compile  \
           --with-gtk=2.0             \
           --with-x

# fix rpmlint unused-direct-shlib-dependency warning
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags} V=1


%install
%{make_install}

find %{buildroot} -name '*.la' -exec rm -vf {} ';'

desktop-file-install                                \
        --delete-original                           \
        --dir=%{buildroot}%{_datadir}/applications  \
%{buildroot}%{_datadir}/applications/marco.desktop

%find_lang %{name} --with-gnome --all-name


%post libs -p /sbin/ldconfig

%postun libs
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans libs
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files
%doc AUTHORS COPYING README ChangeLog
%{_bindir}/marco
%{_bindir}/marco-message
%{_datadir}/applications/marco.desktop
%{_datadir}/themes/ClearlooksRe
%{_datadir}/themes/Dopple-Left
%{_datadir}/themes/Dopple
%{_datadir}/themes/DustBlue
%{_datadir}/themes/Spidey-Left
%{_datadir}/themes/Spidey
%{_datadir}/themes/Splint-Left
%{_datadir}/themes/Splint
%{_datadir}/themes/WinMe
%{_datadir}/themes/eOS
%dir %{_datadir}/marco
%dir %{_datadir}/marco/icons
%{_datadir}/marco/icons/marco-window-demo.png
%{_datadir}/mate-control-center/keybindings/50-marco*.xml
%{_datadir}/mate/wm-properties
%{_mandir}/man1/*

%files libs -f %{name}.lang
%{_libdir}/libmarco-private.so.0*
%{_datadir}/glib-2.0/schemas/org.mate.marco.gschema.xml

%files devel
%{_bindir}/marco-theme-viewer
%{_bindir}/marco-window-demo
%{_includedir}/marco-1
%{_libdir}/libmarco-private.so
%{_libdir}/pkgconfig/libmarco-private.pc
%{_mandir}/man1/marco-theme-viewer.1.*
%{_mandir}/man1/marco-window-demo.1.*


%changelog
* Fri May 06 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 1.14.1.1
- 1.14.1
