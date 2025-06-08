#
# Conditional build:
%bcond_with	tests		# test suite
%bcond_without	qtwebengine	# WebEngine scripting

%ifnarch %{ix86} %{x8664} %{arm} aarch64
%undefine	with_qtwebengine
%endif

%define		kdeplasmaver	5.27.12
%define		kf_ver		5.102.0
%define		qt_ver		5.15.2
%define		kpname		libksysguard

Summary:	Library for monitoring your system
Summary(pl.UTF-8):	Biblioteka do monitorowania systemu
Name:		kp5-%{kpname}
Version:	5.27.12
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	b59ea2998ded2e9b42ce30c2d0884376
URL:		https://kde.org/
BuildRequires:	Qt5Core-devel >= %{qt_ver}
BuildRequires:	Qt5DBus-devel >= %{qt_ver}
BuildRequires:	Qt5Gui-devel >= %{qt_ver}
BuildRequires:	Qt5Network-devel >= %{qt_ver}
BuildRequires:	Qt5Qml-devel >= %{qt_ver}
BuildRequires:	Qt5Quick-devel >= %{qt_ver}
BuildRequires:	Qt5Sensors-devel >= %{qt_ver}
%{?with_qtwebengine:BuildRequires:	Qt5WebEngine-devel >= %{qt_ver}}
%{?with_qtwebengine:BuildRequires:	Qt5WebChannel-devel >= %{qt_ver}}
BuildRequires:	Qt5Widgets-devel >= %{qt_ver}
BuildRequires:	Qt5X11Extras-devel >= %{qt_ver}
BuildRequires:	cmake >= 3.16.0
BuildRequires:	kf5-extra-cmake-modules >= %{kf_ver}
BuildRequires:	kf5-kauth-devel >= %{kf_ver}
BuildRequires:	kf5-kconfig-devel >= %{kf_ver}
BuildRequires:	kf5-kconfigwidgets-devel >= %{kf_ver}
BuildRequires:	kf5-kcoreaddons-devel >= %{kf_ver}
BuildRequires:	kf5-kglobalaccel-devel >= %{kf_ver}
BuildRequires:	kf5-ki18n-devel >= %{kf_ver}
BuildRequires:	kf5-kiconthemes-devel >= %{kf_ver}
BuildRequires:	kf5-kio-devel >= %{kf_ver}
BuildRequires:	kf5-kjobwidgets-devel >= %{kf_ver}
BuildRequires:	kf5-knewstuff-devel >= %{kf_ver}
BuildRequires:	kf5-kpackage-devel >= %{kf_ver}
BuildRequires:	kf5-kservice-devel >= %{kf_ver}
BuildRequires:	kf5-kwidgetsaddons-devel >= %{kf_ver}
BuildRequires:	kf5-kwindowsystem-devel >= %{kf_ver}
# only in autotests and disabled code in signalplotter
%{?with_tests:BuildRequires:	kf5-plasma-framework-devel >= %{pf_ver}}
BuildRequires:	kf5-solid-devel >= %{kf_ver}
BuildRequires:	libnl-devel >= 3.2
BuildRequires:	libpcap-devel
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	lm_sensors-devel
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXres-devel
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	Qt5Core-devel >= %{qt_ver}
Requires:	Qt5DBus-devel >= %{qt_ver}
Requires:	Qt5Gui-devel >= %{qt_ver}
Requires:	Qt5Network-devel >= %{qt_ver}
Requires:	Qt5Qml-devel >= %{qt_ver}
Requires:	Qt5Quick-devel >= %{qt_ver}
%{?with_qtwebengine:Requires:	Qt5WebEngine >= %{qt_ver}}
%{?with_qtwebengine:Requires:	Qt5WebChannel >= %{qt_ver}}
Requires:	Qt5Widgets-devel >= %{qt_ver}
Requires:	Qt5X11Extras-devel >= %{qt_ver}
Requires:	kf5-kauth >= %{kf_ver}
Requires:	kf5-kconfig >= %{kf_ver}
Requires:	kf5-kconfigwidgets >= %{kf_ver}
Requires:	kf5-kcoreaddons >= %{kf_ver}
Requires:	kf5-kglobalaccel >= %{kf_ver}
Requires:	kf5-ki18n >= %{kf_ver}
Requires:	kf5-kio >= %{kf_ver}
Requires:	kf5-kjobwidgets >= %{kf_ver}
Requires:	kf5-kpackage >= %{kf_ver}
Requires:	kf5-kservice >= %{kf_ver}
Requires:	kf5-solid >= %{kf_ver}
Requires:	kf5-kwidgetsaddons >= %{kf_ver}
Requires:	kf5-kwindowsystem >= %{kf_ver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Library for monitoring your system.

%description -l pl.UTF-8
Biblioteka do monitorowania systemu.

%package devel
Summary:	Header files for %{kpname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt5Core-devel >= %{qt_ver}
Requires:	Qt5Network-devel >= %{qt_ver}
Requires:	Qt5Widgets-devel >= %{qt_ver}
Requires:	kf5-kconfig-devel >= %{kf_ver}
Requires:	kf5-ki18n-devel >= %{kf_ver}
Requires:	kf5-kiconthemes-devel >= %{kf_ver}
Requires:	libstdc++-devel >= 6:7

%description devel
Header files for %{kpname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kpname}.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DHTML_INSTALL_DIR=%{_kdedocdir}

%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%find_lang %{kpname}5 --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kpname}5.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/kauth/ksysguardprocesslist_helper
%dir %{_libexecdir}/ksysguard
%attr(755,root,root) %{_libexecdir}/ksysguard/ksgrd_network_helper
%attr(755,root,root) %{_libdir}/libKSysGuardFormatter.so.5.*.*
%ghost %{_libdir}/libKSysGuardFormatter.so.1
%attr(755,root,root) %{_libdir}/libKSysGuardSensorFaces.so.5.*.*
%ghost %{_libdir}/libKSysGuardSensorFaces.so.1
%attr(755,root,root) %{_libdir}/libKSysGuardSensors.so.5.*.*
%ghost %{_libdir}/libKSysGuardSensors.so.1
%attr(755,root,root) %{_libdir}/libKSysGuardSystemStats.so.*.*.*
%ghost %{_libdir}/libKSysGuardSystemStats.so.1
%attr(755,root,root) %{_libdir}/libksgrd.so.*.*.*
%ghost %{_libdir}/libksgrd.so.9
%attr(755,root,root) %{_libdir}/libksignalplotter.so.*.*.*
%ghost %{_libdir}/libksignalplotter.so.9
%attr(755,root,root) %{_libdir}/liblsofui.so.*.*.*
%ghost %{_libdir}/liblsofui.so.9
%attr(755,root,root) %{_libdir}/libprocesscore.so.*.*.*
%ghost %{_libdir}/libprocesscore.so.9
%attr(755,root,root) %{_libdir}/libprocessui.so.*.*.*
%ghost %{_libdir}/libprocessui.so.9
%attr(755,root,root) %{_libdir}/qt5/plugins/designer/ksignalplotter5widgets.so
%attr(755,root,root) %{_libdir}/qt5/plugins/designer/ksysguard5widgets.so
%attr(755,root,root) %{_libdir}/qt5/plugins/designer/ksysguardlsof5widgets.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kpackage/packagestructure/sensorface_packagestructure.so
%dir %{_libdir}/qt5/plugins/ksysguard
%dir %{_libdir}/qt5/plugins/ksysguard/process
%attr(755,root,root) %{_libdir}/qt5/plugins/ksysguard/process/ksysguard_plugin_network.so
%attr(755,root,root) %{_libdir}/qt5/plugins/ksysguard/process/ksysguard_plugin_nvidia.so
%dir %{_libdir}/qt5/qml/org/kde/ksysguard
%dir %{_libdir}/qt5/qml/org/kde/ksysguard/faces
%{_libdir}/qt5/qml/org/kde/ksysguard/faces/*.qml
%attr(755,root,root) %{_libdir}/qt5/qml/org/kde/ksysguard/faces/libFacesPlugin.so
%{_libdir}/qt5/qml/org/kde/ksysguard/faces/qmldir
%dir %{_libdir}/qt5/qml/org/kde/ksysguard/formatter
%attr(755,root,root) %{_libdir}/qt5/qml/org/kde/ksysguard/formatter/libFormatterPlugin.so
%{_libdir}/qt5/qml/org/kde/ksysguard/formatter/qmldir
%dir %{_libdir}/qt5/qml/org/kde/ksysguard/process
%attr(755,root,root) %{_libdir}/qt5/qml/org/kde/ksysguard/process/libProcessPlugin.so
%{_libdir}/qt5/qml/org/kde/ksysguard/process/qmldir
%dir %{_libdir}/qt5/qml/org/kde/ksysguard/sensors
%attr(755,root,root) %{_libdir}/qt5/qml/org/kde/ksysguard/sensors/libSensorsPlugin.so
%{_libdir}/qt5/qml/org/kde/ksysguard/sensors/qmldir
%{_datadir}/dbus-1/interfaces/org.kde.ksystemstats.xml
%{_datadir}/dbus-1/system.d/org.kde.ksysguard.processlisthelper.conf
%{_datadir}/dbus-1/system-services/org.kde.ksysguard.processlisthelper.service
%{_datadir}/knsrcfiles/systemmonitor-faces.knsrc
%{_datadir}/knsrcfiles/systemmonitor-presets.knsrc
%{_datadir}/ksysguard
%{_datadir}/polkit-1/actions/org.kde.ksysguard.processlisthelper.policy
%{_datadir}/qlogging-categories5/libksysguard.categories

%files devel
%defattr(644,root,root,755)
%{_libdir}/libKSysGuardFormatter.so
%{_libdir}/libKSysGuardSensorFaces.so
%{_libdir}/libKSysGuardSensors.so
%{_libdir}/libKSysGuardSystemStats.so
%{_libdir}/libksgrd.so
%{_libdir}/libksignalplotter.so
%{_libdir}/liblsofui.so
%{_libdir}/libprocesscore.so
%{_libdir}/libprocessui.so
%{_includedir}/ksysguard
%{_libdir}/cmake/KF5SysGuard
%{_libdir}/cmake/KSysGuard
