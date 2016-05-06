# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
%global branch 1.14

# Settings used for build from snapshots.
%{!?rel_build:%global commit c3b48ea39ab358b45048e300deafaa3f569748ad}
%{!?rel_build:%global commit_date 20140211}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Name:           mate-applets
Version:        %{branch}.0
%if 0%{?rel_build}
Release:        1%{?dist}
%else
Release:        0.2%{?git_rel}%{?dist}
%endif
Summary:        MATE Desktop panel applets
License:        GPLv2+ and LGPLv2+
URL:            http://mate-desktop.org

# for downloading the tarball use 'spectool -g -R mate-applets.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%{name}/snapshot/%{name}-%{commit}.tar.xz#/%{git_tar}}

BuildRequires: libgtop2-devel
BuildRequires: libnotify-devel
BuildRequires: libmateweather-devel
BuildRequires: libwnck-devel
BuildRequires: libxml2-devel
BuildRequires: libICE-devel
BuildRequires: libSM-devel
BuildRequires: mate-common
BuildRequires: mate-settings-daemon-devel
BuildRequires: mate-desktop-devel
BuildRequires: mate-notification-daemon
BuildRequires: mate-panel-devel
BuildRequires: polkit-devel
BuildRequires: unique-devel
BuildRequires: pygobject3-devel
BuildRequires: startup-notification-devel
Buildrequires: upower-devel
Buildrequires: gtksourceview2-devel
%ifnarch s390 s390x sparc64
BuildRequires: kernel-tools-libs-devel
%endif

Provides:   mate-netspeed%{?_isa} = %{version}-%{release}
Provides:   mate-netspeed = %{version}-%{release}
Obsoletes:  mate-netspeed < %{version}-%{release}

%description
MATE Desktop panel applets

%prep
%setup -q%{!?rel_build:n %{name}-%{commit}}

%if 0%{?rel_build}
#NOCONFIGURE=1 ./autogen.sh
%else # 0%{?rel_build}
# needed for git snapshots
NOCONFIGURE=1 ./autogen.sh
%endif # 0%{?rel_build}

%build
%configure   \
    --disable-schemas-compile                \
    --with-gtk=2.0                           \
    --disable-static                         \
    --with-x                                 \
    --enable-polkit                          \
    --enable-ipv6                            \
    --enable-stickynotes                     \
    --libexecdir=%{_libexecdir}/mate-applets \
    --with-cpufreq-lib=cpupower

make %{?_smp_mflags} V=1

%install
%{make_install}

# remove of gsettings,convert file, no need for this in fedora
# because MATE starts with gsettings in fedora.
rm -f %{buildroot}%{_datadir}/MateConf/gsettings/stickynotes-applet.convert

#make python script executable
#http://forums.fedoraforum.org/showthread.php?t=284962
chmod a+x %{buildroot}%{python_sitelib}/mate_invest/chart.py

%find_lang %{name} --with-gnome --all-name

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
/bin/touch --no-create %{_datadir}/mate-applets/icons/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null
    /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &> /dev/null || :
    /usr/bin/gtk-update-icon-cache -f %{_datadir}/mate-applets/icons/hicolor &> /dev/null || :
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &> /dev/null || :
/usr/bin/gtk-update-icon-cache -f %{_datadir}/mate-applets/icons/hicolor &> /dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_bindir}/mate-invest-chart
%{_bindir}/mate-cpufreq-selector
%{python_sitelib}/mate_invest
%{_libexecdir}/mate-applets
%config(noreplace) %{_sysconfdir}/sound/events/mate-battstat_applet.soundlist
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.mate.CPUFreqSelector.conf
%{_datadir}/mate-applets
%{_datadir}/mate-panel/applets
%{_datadir}/dbus-1/services/org.mate.panel.applet.CommandAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.TimerAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.AccessxStatusAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.BattstatAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.CharpickerAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.DriveMountAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.GeyesAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.StickyNotesAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.TrashAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.InvestAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.MateWeatherAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.MultiLoadAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.NetspeedAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.CPUFreqAppletFactory.service
%{_datadir}/dbus-1/system-services/org.mate.CPUFreqSelector.service
%{_datadir}/glib-2.0/schemas/org.mate.panel.applet.battstat.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.panel.applet.charpick.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.panel.applet.geyes.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.panel.applet.multiload.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.stickynotes.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.panel.applet.cpufreq.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.panel.applet.command.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.panel.applet.timer.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.panel.applet.netspeed.gschema.xml
%{_datadir}/polkit-1/actions/org.mate.cpufreqselector.policy
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/icons/hicolor/*/devices/*.png
%{_datadir}/icons/hicolor/*/status/*.png
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_mandir}/man1/*
%{_datadir}/mate/ui/accessx-status-applet-menu.xml
%{_datadir}/mate/ui/battstat-applet-menu.xml
%{_datadir}/mate/ui/charpick-applet-menu.xml
%{_datadir}/mate/ui/drivemount-applet-menu.xml
%{_datadir}/mate/ui/geyes-applet-menu.xml
%{_datadir}/mate/ui/stickynotes-applet-menu.xml
%{_datadir}/mate/ui/trashapplet-menu.xml
%{_datadir}/mate/ui/mateweather-applet-menu.xml
%{_datadir}/mate/ui/multiload-applet-menu.xml
%{_datadir}/mate/ui/cpufreq-applet-menu.xml
%{_datadir}/mate/ui/netspeed-menu.xml
%{_datadir}/pixmaps/mate-accessx-status-applet
%{_datadir}/pixmaps/mate-cpufreq-applet


%changelog
* Fri May 06 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 1.14.0-1
- 1.14.0
