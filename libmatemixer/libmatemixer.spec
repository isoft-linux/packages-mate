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

Name:        libmatemixer
Summary:     Mixer library for MATE desktop
Version:     %{branch}.0
%if 0%{?rel_build}
Release:     1%{?dist}
%else
Release:     0.2%{?git_rel}%{?dist}
%endif
License:     GPLv2+
URL:         http://mate-desktop.org

# for downloading the tarball use 'spectool -g -R libmatemixer.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%%{name}/snapshot/%%{name}-%%{commit}.tar.xz#/%%{git_tar}}

BuildRequires:  mate-common
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  alsa-lib-devel


%description
libmatemixer is a mixer library for MATE desktop.
It provides an abstract API allowing access to mixer functionality
available in the PulseAudio, ALSA and OSS sound systems.

%package devel
Summary:  Development libraries for libmatemixer
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development libraries for libmatemixer

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
%configure \
        --disable-static \
        --enable-pulseaudio \
        --enable-alsa \
        --enable-gtk-doc

#drop unneeded direct library deps with --as-needed
# libtool doesn't make this easy, so we do it the hard way
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' libtool

make %{?_smp_mflags} V=1

%install
%{make_install}

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%find_lang %{name} --with-gnome --all-name


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f %{name}.lang
%doc AUTHORS COPYING NEWS README
%{_libdir}/libmatemixer.so.*
%{_libdir}/libmatemixer/

%files devel
%{_includedir}/mate-mixer/
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_datadir}/gtk-doc/html/libmatemixer/


%changelog
* Fri May 06 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 1.14.0-1
- 1.14.0
