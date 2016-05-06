# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
%global branch 1.14

# Settings used for build from snapshots.
%{!?rel_build:%global commit 8e0c8e17e0138afa7757a1bdf8edd6f2c7b47a14}
%{!?rel_build:%global commit_date 20150930}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Name:		mate-polkit
Version:    %{branch}.0
%if 0%{?rel_build}
Release:	1%{?dist}
%else
Release:    0.2%{?git_rel}%{?dist}
%endif
Summary:	Integrates polkit authentication for MATE desktop
License:	LGPLv2+
URL:		http://mate-desktop.org

# for downloading the tarball use 'spectool -g -R mate-polkit.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%{name}/snapshot/%{name}-%{commit}.tar.xz#/%{git_tar}}

BuildRequires:	gtk3-devel
BuildRequires:	mate-common
BuildRequires:	polkit-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	dbus-glib-devel
# needed for gobject-introspection support somehow,
# https://bugzilla.redhat.com/show_bug.cgi?id=847419#c17 asserts this is a bug (elsewhere)
# but I'm not entirely sure -- rex
BuildRequires: 	cairo-gobject-devel

Provides:	PolicyKit-authentication-agent


%description
Integrates polkit with the MATE Desktop environment

%package devel
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary:	Integrates polkit with the MATE Desktop environment

%description devel
Development libraries for mate-polkit


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
%configure  \
        --disable-static       \
        --with-gtk=3.0         \
        --enable-introspection \
        --enable-accountsservice \
        --enable-gtk-doc-html

make %{?_smp_mflags} V=1

%install
%{make_install}

%find_lang %{name}

find %{buildroot} -name '*.la' -exec rm -fv {} ';'


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files -f %{name}.lang
# yes, license really is LGPLv2+, despite included COPYING is about GPL, poke upstreamo
# to include COPYING.LIB here instead  -- rex
%doc AUTHORS COPYING README
%{_sysconfdir}/xdg/autostart/polkit-mate-authentication-agent-1.desktop
%{_libdir}/libpolkit-gtk-mate-1.so.0
%{_libdir}/libpolkit-gtk-mate-1.so.0.0.0
%{_libdir}/girepository-1.0/PolkitGtkMate-1.0.typelib
%{_libexecdir}/polkit-mate-authentication-agent-1

%files devel
%{_libdir}/libpolkit-gtk-mate-1.so
%{_libdir}/pkgconfig/polkit-gtk-mate-1.pc
%{_includedir}/polkit-gtk-mate-1
%{_datadir}/gir-1.0/PolkitGtkMate-1.0.gir


%changelog
* Fri May 06 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 1.14.0-1
- 1.14.0
