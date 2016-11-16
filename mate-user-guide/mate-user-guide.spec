# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
%global branch 1.14

# Settings used for build from snapshots.
%{!?rel_build:%global commit 61aec06d978154fea42f1f42d845fdb710c924f7}
%{!?rel_build:%global commit_date 20150618}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Name:        mate-user-guide
Summary:     User Guide for MATE desktop
Version:     %{branch}.0
%if 0%{?rel_build}
Release:     1%{?dist}
%else
Release:     0.2%{?git_rel}%{?dist}
%endif
License:     GPLv2+
URL:         http://mate-desktop.org
BuildArch:   noarch

# for downloading the tarball use 'spectool -g -R mate-user-guide.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%{name}/snapshot/%{name}-%{commit}.tar.xz#/%{git_tar}}

BuildRequires:  mate-common
BuildRequires:  desktop-file-utils

Requires: yelp

%description
Documentations for MATE desktop.

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
%configure

make %{?_smp_mflags} V=1

%install
%{make_install}

desktop-file-install                               \
  --delete-original                                \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications    \
$RPM_BUILD_ROOT%{_datadir}/applications/mate-user-guide.desktop

%find_lang %{name} --with-gnome --all-name


%files -f %{name}.lang
%doc AUTHORS COPYING NEWS README ChangeLog
%{_datadir}/applications/mate-user-guide.desktop


%changelog
* Wed Sep 21 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.14.0-1
- update to 1.14.0 release
