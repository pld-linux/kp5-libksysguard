%define		kdeplasmaver	5.15.3
%define		qtver		5.9.0
%define		kpname		libksysguard

Summary:	Library for monitoring your system
Name:		kp5-%{kpname}
Version:	5.15.3
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	http://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	94d5a8505d3ecc69726aa9deb592bf97
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	cmake >= 2.8.12
BuildRequires:	kf5-kauth-devel
BuildRequires:	kf5-kcompletion-devel
BuildRequires:	kf5-kconfig-devel
BuildRequires:	kf5-kconfigwidgets-devel
BuildRequires:	kf5-kcoreaddons-devel
BuildRequires:	kf5-ki18n-devel
BuildRequires:	kf5-kiconthemes-devel
BuildRequires:	kf5-kservice-devel
BuildRequires:	kf5-kwidgetsaddons-devel
BuildRequires:	kf5-kwindowsystem-devel
BuildRequires:	kf5-plasma-framework-devel
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
Library for monitoring your system.

%package devel
Summary:	Header files for %{kpname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kpname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kpname}.

%prep
%setup -q -n %{kpname}-%{version}

%build
install -d build
cd build
%cmake -G Ninja \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	../
%ninja_build

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kpname}5 --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kpname}5.lang
%defattr(644,root,root,755)
/etc/dbus-1/system.d/org.kde.ksysguard.processlisthelper.conf
/etc/xdg/libksysguard.categories
%attr(755,root,root) %{_libexecdir}/kauth/ksysguardprocesslist_helper
%attr(755,root,root) %{_libdir}/libksgrd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libksgrd.so.7
%attr(755,root,root) %{_libdir}/libksignalplotter.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libksignalplotter.so.7
%attr(755,root,root) %{_libdir}/liblsofui.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblsofui.so.7
%attr(755,root,root) %{_libdir}/libprocesscore.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libprocesscore.so.7
%attr(755,root,root) %{_libdir}/libprocessui.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libprocessui.so.7
%{_datadir}/dbus-1/system-services/org.kde.ksysguard.processlisthelper.service
%{_datadir}/ksysguard
%{_datadir}/polkit-1/actions/org.kde.ksysguard.processlisthelper.policy

%files devel
%defattr(644,root,root,755)
%{_includedir}/ksysguard
%{_libdir}/cmake/KF5SysGuard
%attr(755,root,root) %{_libdir}/libksgrd.so
%attr(755,root,root) %{_libdir}/libksignalplotter.so
%attr(755,root,root) %{_libdir}/liblsofui.so
%attr(755,root,root) %{_libdir}/libprocesscore.so
%attr(755,root,root) %{_libdir}/libprocessui.so
