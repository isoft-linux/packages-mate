# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
%global branch 1.14

# Settings used for build from snapshots.
%{!?rel_build:%global commit 5e8b69cf7c6d031cbb0b0f01a7518e72146c0af1}
%{!?rel_build:%global commit_date 20151009}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Name:           libmatekbd
Version:        %{branch}.0
%if 0%{?rel_build}
Release:        1%{?dist}
%else
Release:        0.2%{?git_rel}%{?dist}
%endif
Summary:        Libraries for mate kbd
License:        LGPLv2+
URL:            http://mate-desktop.org

# for downloading the tarball use 'spectool -g -R libmatekbd.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%{name}/snapshot/%{name}-%{commit}.tar.xz#/%{git_tar}}

BuildRequires:  desktop-file-utils
BuildRequires:  gsettings-desktop-schemas-devel
BuildRequires:  gtk2-devel
BuildRequires:  libICE-devel
BuildRequires:  libxklavier-devel
BuildRequires:  mate-common
BuildRequires:  gobject-introspection-devel

%description
Libraries for matekbd

%package devel
Summary:  Development libraries for libmatekbd
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development libraries for libmatekbd

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

%configure                   \
   --disable-static          \
   --with-gtk=2.0            \
   --disable-schemas-compile \
   --with-x                  \
   --enable-introspection=yes
  
make %{?_smp_mflags} V=1


%install
%{make_install}

find %{buildroot} -name '*.la' -exec rm -fv {} ';'

%find_lang %{name} --with-gnome --all-name


%post -p /sbin/ldconfig

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_datadir}/libmatekbd
%{_datadir}/glib-2.0/schemas/org.mate.peripherals-keyboard-xkb.gschema.xml
%{_libdir}/libmatekbd.so.4*
%{_libdir}/libmatekbdui.so.4*
%{_libdir}/girepository-1.0/Matekbd-1.0.typelib
%{_datadir}/gir-1.0/Matekbd-1.0.gir

%files devel
%{_includedir}/libmatekbd
%{_libdir}/pkgconfig/libmatekbd.pc
%{_libdir}/pkgconfig/libmatekbdui.pc
%{_libdir}/libmatekbdui.so
%{_libdir}/libmatekbd.so

%changelog
* Fri May 06 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 1.14.0-1
- 1.14.0
