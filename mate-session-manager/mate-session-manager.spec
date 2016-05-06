# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
%global branch 1.14

# Settings used for build from snapshots.
%{!?rel_build:%global commit af58c2ecd98fe68360635f0e566b81e4b8c7be4d}
%{!?rel_build:%global commit_date 20151006}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Name:           mate-session-manager
Summary:        MATE Desktop session manager
License:        GPLv2+
Version:        %{branch}.0
%if 0%{?rel_build}
Release:        2%{?dist}
%else
Release:        0.2%{?git_rel}%{?dist}
%endif
URL:            http://mate-desktop.org

# for downloading the tarball use 'spectool -g -R mate-session-manager.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%{name}/snapshot/%{name}-%{commit}.tar.xz#/%{git_tar}}

BuildRequires:  dbus-glib-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gtk3-devel
BuildRequires:  libSM-devel
BuildRequires:  mate-common
BuildRequires:  pangox-compat-devel
BuildRequires:  systemd-devel
BuildRequires:  xmlto
BuildRequires:  libXtst-devel
BuildRequires:  xorg-x11-xtrans-devel
BuildRequires:  tcp_wrappers-devel

#Requires: system-logos
# Needed for mate-settings-daemon
Requires: mate-control-center
# we need an authentication agent in the session
Requires: mate-polkit
# and we want good defaults
Requires: polkit-desktop-policy
# for gsettings shemas
Requires: mate-desktop-libs

%description
This package contains a session that can be started from a display
manager such as MDM. It will load all necessary applications for a
full-featured user session.

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
%configure                    \
    --disable-static          \
    --enable-ipv6             \
    --with-gtk=3.0            \
    --with-default-wm=marco   \
    --with-systemd            \
    --disable-upower          \
    --enable-docbook-docs     \
    --disable-schemas-compile \
    --with-x

make %{?_smp_mflags} V=1

%install
%{make_install}

desktop-file-install                               \
        --delete-original                          \
        --dir=%{buildroot}%{_datadir}/applications \
%{buildroot}%{_datadir}/applications/mate-session-properties.desktop

%find_lang %{name} --with-gnome --all-name

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
      /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
      /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :
      /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_mandir}/man1/*
%{_bindir}/mate-session
%{_bindir}/mate-session-inhibit
%{_bindir}/mate-session-properties
%{_bindir}/mate-session-save
%{_bindir}/mate-wm
%{_datadir}/applications/mate-session-properties.desktop
%{_datadir}/mate-session-manager
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/icons/hicolor/scalable/apps/mate-session-properties.svg
%{_datadir}/glib-2.0/schemas/org.mate.session.gschema.xml
%{_datadir}/xsessions/mate.desktop

%changelog
* Fri May 06 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 1.14.0-2
- 1.14.0
- Remove system-logos require.
