Name:		mate-backgrounds
Version:	1.14.0
Release:	1%{?dist}
Summary:	MATE Desktop backgrounds
License:	GPLv2+
URL:		http://mate-desktop.org
Source0:	http://pub.mate-desktop.org/releases/1.14/%{name}-%{version}.tar.xz

BuildArch:	noarch
BuildRequires:	mate-common

%description
Backgrounds for MATE Desktop

%prep
%setup -q

%build
%configure

make %{?_smp_mflags} V=1


%install
%{make_install}

%find_lang %{name} --with-gnome --all-name

%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_datadir}/mate-background-properties
%{_datadir}/backgrounds/mate


%changelog
* Fri May 06 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 1.14.0-1
- 1.14.0
