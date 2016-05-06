# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
%global branch 1.14

# Settings used for build from snapshots.
%{!?rel_build:%global commit cdb0d70862035cd1b65c4deb495ea1016ea2d206}
%{!?rel_build:%global commit_date 20150530}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Name:           mate-icon-theme
Version:        %{branch}.0
%if 0%{?rel_build}
Release:        1%{?dist}
%else
Release:        0.6%{?git_rel}%{?dist}
%endif
Summary:        Icon theme for MATE Desktop
License:        GPLv2+ and LGPLv2+
URL:            http://mate-desktop.org

# for downloading the tarball use 'spectool -g -R mate-icon-theme.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%{name}/snapshot/%{name}-%{commit}.tar.xz#/%{git_tar}}

BuildArch:      noarch

BuildRequires:  mate-common 
BuildRequires:  icon-naming-utils

Obsoletes: mate-icon-theme-devel

%description
Icon theme for MATE Desktop


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
%configure  --enable-icon-mapping

make %{?_smp_mflags} V=1


%install
%{make_install}

%post
/bin/touch --no-create %{_datadir}/icons/mate &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/menta &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/mate &> /dev/null
    /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/mate &> /dev/null || :
    /bin/touch --no-create %{_datadir}/icons/menta &> /dev/null
    /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/menta &> /dev/null || :

fi

%posttrans
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/mate &> /dev/null || :
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/menta &> /dev/null || :

%files
%doc AUTHORS COPYING README
%{_datadir}/icons/mate
%{_datadir}/icons/menta


%changelog
* Fri May 06 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 1.14.0-1
- 1.14.0
