# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
%global branch 1.14

# Settings used for build from snapshots.
%{!?rel_build:%global commit 83fe1f587f5c6328b10a899a880275d79bf88921}
%{!?rel_build:%global commit_date 20141215}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Name:           mate-settings-daemon
Version:        %{branch}.0
%if 0%{?rel_build}
Release:        1%{?dist}
%else
Release:        0.2%{?git_rel}%{?dist}
%endif
Summary:        MATE Desktop settings daemon
License:        GPLv2+
URL:            http://mate-desktop.org

# for downloading the tarball use 'spectool -g -R mate-settings-daemon.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%{name}/snapshot/%{name}-%{commit}.tar.xz#/%{git_tar}}

BuildRequires:  dbus-glib-devel
BuildRequires:  dconf-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gtk2-devel
BuildRequires:  libmatemixer-devel
BuildRequires:  libcanberra-devel
BuildRequires:  libmatekbd-devel
BuildRequires:  libnotify-devel
BuildRequires:  libSM-devel
BuildRequires:  libXxf86misc-devel
BuildRequires:  mate-common
BuildRequires:  mate-desktop-devel
BuildRequires:  mate-polkit-devel
BuildRequires:  nss-devel
BuildRequires:  pulseaudio-libs-devel

Requires:       libmatekbd%{?_isa} >= 0:1.6.1-1
# needed for xrandr capplet
Requires:       mate-control-center-filesystem

%description
This package contains the daemon which is responsible for setting the
various parameters of a MATE session and the applications that run
under it.

%package devel
Summary:        Development files for mate-settings-daemon
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the daemon which is responsible for setting the
various parameters of a MATE session and the applications that run
under it.

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
%configure                             \
   --enable-pulse                      \
   --disable-static                    \
   --disable-schemas-compile           \
   --enable-polkit                     \
   --with-x                            \
   --with-nssdb                        \
   --with-gtk=2.0

make %{?_smp_mflags} V=1

%install
%{make_install}

find %{buildroot} -name '*.la' -exec rm -rf {} ';'

desktop-file-validate %{buildroot}%{_sysconfdir}/xdg/autostart/mate-settings-daemon.desktop

%find_lang %{name} --with-gnome --all-name

%post
/sbin/ldconfig
/bin/touch --no-create %{_datadir}/icons/mate &> /dev/null || :
/bin/touch --no-create %{_datadir}/hicolor/mate &> /dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/mate &> /dev/null || :
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/mate &> /dev/null || :
    /usr/bin/gtk-update-icon-cache %{_datadir}/hicolor/mate &> /dev/null || :
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/mate &> /dev/null || :
/usr/bin/gtk-update-icon-cache %{_datadir}/hicolor/mate &> /dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS COPYING README
%dir %{_sysconfdir}/mate-settings-daemon
%dir %{_sysconfdir}/mate-settings-daemon/xrandr
%config %{_sysconfdir}/dbus-1/system.d/org.mate.SettingsDaemon.DateTimeMechanism.conf
%{_sysconfdir}/xdg/autostart/mate-settings-daemon.desktop
%{_sysconfdir}/xrdb/
%{_libdir}/mate-settings-daemon
%{_libexecdir}/mate-settings-daemon
%{_libexecdir}/msd-datetime-mechanism
%{_libexecdir}/msd-locate-pointer
%{_datadir}/mate-control-center/keybindings/50-accessibility.xml
%{_datadir}/dbus-1/services/org.mate.SettingsDaemon.service
%{_datadir}/dbus-1/system-services/org.mate.SettingsDaemon.DateTimeMechanism.service
%{_datadir}/icons/mate/*/*/*
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/mate-settings-daemon
%{_datadir}/glib-2.0/schemas/org.mate.*.xml
%{_datadir}/polkit-1/actions/org.mate.settingsdaemon.datetimemechanism.policy
%{_mandir}/man1/*

%files devel
%{_includedir}/mate-settings-daemon
%{_libdir}/pkgconfig/mate-settings-daemon.pc


%changelog
* Wed Apr 06 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.14.0-1
- update to 1.14.0 release

* Sun Feb 07 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.13.0-1
- update to 1.13.0 release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 04 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> 1.12.1-1
- update to 1.12.1 release

* Fri Nov 06 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.0-1
- update to 1.12.0 release

* Wed Oct 21 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.11.0-1
- update to 1.11.0 release

* Mon Aug 31 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.2-1
- update to 1.10.2 release
- remove upstreamed patches
- add upstream touchpad improvement

* Wed Aug 19 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.1-2
- another fix for glib2/gsettings regression

* Tue Jul 14 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.1.1
- update to 1.10.1 release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 07 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.0-1
- update to 1.10.0 release

* Thu Feb 26 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.90-1
- update to 1.9.90 release

* Wed Jan 21 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.6-1
- update to 1.9.6 release

* Thu Nov 20 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.5-1
- update to 1.9.5 release

* Tue Nov 11 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.4-1
- update to 1.9.4 release

* Mon Oct 27 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.3-1
- update to 1.9.3 release

* Sun Oct 12 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.2-1
- update to 1.9.2 release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 12 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.1-1
- update to 1.9.1 release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 06 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.1-1
- update to 1.8.1

* Wed Mar 05 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Tue Feb 18 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90
- use --with-gnome --all-name for find locale
- use modern 'make install' macro
- add man dir

* Sun Feb 09 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.1-1
- Update to 1.7.1

* Thu Dec 05 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.0-1
- Update to 1.7.0

* Thu Oct 03 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-0.3.gitd2d3aa7
- enable pulsaudio support

* Tue Oct 01 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-0.2.gitd2d3aa7
- add misssing directory for xrandr-capplet function 'system-wide installation'
- add runtime requires mate-control-center-filesystem for xrandr-capplet

* Mon Sep 23 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-0.1.gitd2d3aa7
- update to latest snapshot
- fix https://github.com/mate-desktop/mate-settings-daemon/issues/32
- remove runtime require mate-icon-theme, no need of it
- remove %%config from desktop file
- remove needless find '*.a'
- switch to pulseaudio, fix rhbz (#1008011)
- cleanup BRs

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 28 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1.2
- remove BR gsettings-desktop-schemas-devel
- remove needless gsettings convert file
- clean up BR's
- add versioned runtime require libmatekbd

* Mon Jun 24 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-1
- Update to latest upstream release.

* Sat Jun 22 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-3
- Update libnotify.patch with latest upstream commits

* Tue Jun 11 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-2
- Add libnotify patch

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to latest 1.6.0 stable release.

* Tue Mar 26 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.7-1
- Update to latest upstream release

* Fri Feb 08 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.5-1
-Update to latest upstream release
-Convert back to old BR style
-Own dirs we are supposed to own

* Tue Jan 15 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.4-3
- Fix icon scriptlets

* Fri Dec 21 2012 Nelson Marques <nmarques@fedoraproject.org> - 1.5.4-2
- Fix broken gstreamer support:
  + add gstreamer BuildRequires
  + disable pulse so we build with gstreamer support
- Add '--disable-static' to %%configure and remove find entries
- Improve description, overall readability, order dependencies and
  minor improvements

* Mon Dec 03 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.4-1
- Latest upstream release

* Fri Nov 23 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.3-5
- Remove archlinux configure.ac bits.
- REALLY fix CVE-2012-5560

* Fri Nov 23 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.3-4
- stop generating version specific libdirs for plugins and fix CVE-2012-5560

* Thu Nov 22 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.3-3
- fix build failures

* Thu Nov 22 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.3-2
- drop mate-corba from br as it is deprecated

* Mon Oct 29 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.3-1
- update to 1.5.3 release

* Mon Oct 29 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-1
- update to 1.5.0 release
- add schema scriptlets and remove mateconf scriptlets
- add requires gsettings-desktop-schemas
- add build requires gsettings-desktop-schemas-devel
- change build requires style

* Wed Oct 10 2012 Rex Dieter <rdieter@fedoraproject.org> 1.4.0-6
- fix icon scriptlets

* Fri Sep 28 2012 Rex Dieter <rdieter@fedoraproject.org> - 1.4.0-5
- remove local quirks not needed for fedora buildsys
- simplify %%files, fix some dir-ownership
- cosmetics: move scriptlets to be next to %%files

* Tue Sep 25 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-4
- Own mate-settings-daemon directory, update build requires and configure flags

* Tue Sep 25 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-3
- Fix mateconf scritplets, switch back to upstream source.

* Sat Sep 15 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-2
- Move shared libs to main package and update buildrequires to add libSM-devel add mateconf scriptlets

* Sat Sep 01 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-1
- Initial build
