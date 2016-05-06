# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
%global branch 3.20

%global rel_ver 3.20.6

# Settings used for build from snapshots.
%{!?rel_build:%global commit 5fec16803c5ff06fa31b7cab47c6d51a99f1acc7}
%{!?rel_build:%global commit_date 20151005}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Name:           mate-themes
Version:        %{rel_ver}
%if 0%{?rel_build}
Release:        1%{?dist}
%else
Release:        0.2%{?git_rel}%{?dist}
%endif
Summary:        MATE Desktop themes
License:        GPLv2+
URL:            http://mate-desktop.org
BuildArch:      noarch

# for downloading the tarball use 'spectool -g -R mate-themes.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/themes/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%{name}/snapshot/%{name}-%{commit}.tar.xz#/%{git_tar}}

BuildRequires:  mate-common
BuildRequires:  gtk2-devel
BuildRequires:  gdk-pixbuf2-devel

Requires:       mate-icon-theme
Requires:       gtk2-engines
Requires:       gtk-murrine-engine

%description
MATE Desktop themes

%prep
%if 0%{?rel_build}
# for releases
%setup -qn %{name}-%{version}
%else # 0%{?rel_build}
# for snapshots
%setup -qn %{name}-%{commit}
# needed for git snapshots
NOCONFIGURE=1 ./autogen.sh
%endif # 0%{?rel_build}

%build
%configure --enable-icon-mapping

make %{?_smp_mflags} V=1

%install
%{make_install}

find %{buildroot} -name '*.la' -exec rm -rf {} ';'
find %{buildroot} -name '*.a' -exec rm -rf {} ';'

%post
for icon_theme in \
  ContrastHigh ;
do
  /bin/touch --no-create %{_datadir}/icons/${icon_theme} &> /dev/null || :
done

%postun
if [ $1 -eq 0 ]; then
for icon_theme in \
  ContrastHigh ;
do
  /bin/touch --no-create %{_datadir}/icons/${icon_theme} &> /dev/null || :
  /usr/bin/gtk-update-icon-cache %{_datadir}/icons/${icon_theme} &> /dev/null || :
done
fi

%posttrans
for icon_theme in \
  ContrastHigh ;
do
  /usr/bin/gtk-update-icon-cache %{_datadir}/icons/${icon_theme} &> /dev/null || :
done


%files
%doc AUTHORS COPYING README ChangeLog
%{_datadir}/themes/BlackMATE/
%{_datadir}/themes/BlueMenta/
%{_datadir}/themes/Blue-Submarine/
%{_datadir}/themes/ContrastHighInverse/
%{_datadir}/themes/GreenLaguna/
%{_datadir}/themes/Green-Submarine/
%{_datadir}/themes/HighContrast/metacity-1/metacity-theme-1.xml
%{_datadir}/themes/Menta/
%{_datadir}/themes/TraditionalOk/
%{_datadir}/themes/TraditionalGreen/
%{_datadir}/themes/Shiny/
%{_datadir}/icons/ContrastHigh/
%{_datadir}/icons/mate/cursors/


%changelog
* Fri May 06 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 3.20.6-1
- 3.20.6
