#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	5.93.0
%define		qtver		5.15.2
%define		kpname		libksysguard

Summary:	Library for monitoring your system
Name:		kp5-%{kpname}
Version:	5.93.0
Release:	0.1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/unstable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	81f186860cad33266e46dc8baf7667c3
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Sensors-devel >= %{qtver}
BuildRequires:	cmake >= 3.16.0
BuildRequires:	kf6-kauth-devel
BuildRequires:	kf6-kcompletion-devel
BuildRequires:	kf6-kconfig-devel
BuildRequires:	kf6-kconfigwidgets-devel
BuildRequires:	kf6-kcoreaddons-devel
BuildRequires:	kf6-ki18n-devel
BuildRequires:	kf6-kiconthemes-devel
BuildRequires:	kf6-kservice-devel
BuildRequires:	kf6-kwidgetsaddons-devel
BuildRequires:	kf6-kwindowsystem-devel
BuildRequires:	libnl-devel
BuildRequires:	libpcap-devel
BuildRequires:	lm_sensors-devel
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

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

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kpname}5.lang
%defattr(644,root,root,755)
%{_datadir}/dbus-1/system.d/org.kde.ksysguard.processlisthelper.conf
%attr(755,root,root) %{_libdir}/libksgrd.so.*.*.*
%ghost %{_libdir}/libksgrd.so.10
%attr(755,root,root) %{_libdir}/libksignalplotter.so.*.*.*
%ghost %{_libdir}/libksignalplotter.so.10
%attr(755,root,root) %{_libdir}/liblsofui.so.*.*.*
%ghost %{_libdir}/liblsofui.so.10
%attr(755,root,root) %{_libdir}/libprocesscore.so.*.*.*
%ghost %{_libdir}/libprocesscore.so.10
%attr(755,root,root) %{_libdir}/libprocessui.so.*.*.*
%ghost %{_libdir}/libprocessui.so.10
%{_datadir}/dbus-1/system-services/org.kde.ksysguard.processlisthelper.service
%{_datadir}/ksysguard
%{_datadir}/polkit-1/actions/org.kde.ksysguard.processlisthelper.policy
%{_datadir}/qlogging-categories6/libksysguard.categories

%ghost %{_libdir}/libKSysGuardFormatter.so.2
%attr(755,root,root) %{_libdir}/libKSysGuardFormatter.so.5.*.*
%ghost %{_libdir}/libKSysGuardSensorFaces.so.2
%attr(755,root,root) %{_libdir}/libKSysGuardSensorFaces.so.5.*.*
%ghost %{_libdir}/libKSysGuardSensors.so.2
%attr(755,root,root) %{_libdir}/libKSysGuardSensors.so.5.*.*
%attr(755,root,root) %{_libdir}/qt6/plugins/designer/ksignalplotter5widgets.so
%attr(755,root,root) %{_libdir}/qt6/plugins/designer/ksysguard5widgets.so
%attr(755,root,root) %{_libdir}/qt6/plugins/designer/ksysguardlsof5widgets.so
%dir %{_libdir}/qt6/qml/org/kde/ksysguard
%dir %{_libdir}/qt6/qml/org/kde/ksysguard/faces
%dir %{_libdir}/qt6/qml/org/kde/ksysguard/formatter
%dir %{_libdir}/qt6/qml/org/kde/ksysguard/process
%dir %{_libdir}/qt6/qml/org/kde/ksysguard/sensors
%{_libdir}/qt6/qml/org/kde/ksysguard/faces/ExtendedLegend.qml
%{_libdir}/qt6/qml/org/kde/ksysguard/faces/SensorFace.qml
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/ksysguard/faces/libFacesPlugin.so
%{_libdir}/qt6/qml/org/kde/ksysguard/faces/qmldir
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/ksysguard/formatter/libFormatterPlugin.so
%{_libdir}/qt6/qml/org/kde/ksysguard/formatter/qmldir
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/ksysguard/process/libProcessPlugin.so
%{_libdir}/qt6/qml/org/kde/ksysguard/process/qmldir
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/ksysguard/sensors/libSensorsPlugin.so
%{_libdir}/qt6/qml/org/kde/ksysguard/sensors/qmldir
%{_datadir}/knsrcfiles/systemmonitor-faces.knsrc
%{_datadir}/knsrcfiles/systemmonitor-presets.knsrc

%ghost %{_libdir}/libKSysGuardSystemStats.so.2
%attr(755,root,root) %{_libdir}/libKSysGuardSystemStats.so.*.*.*
%dir %{_libdir}/qt6/plugins/ksysguard
%dir %{_libdir}/qt6/plugins/ksysguard/process
%attr(755,root,root) %{_libdir}/qt6/plugins/ksysguard/process/ksysguard_plugin_network.so
%attr(755,root,root) %{_libdir}/qt6/plugins/ksysguard/process/ksysguard_plugin_nvidia.so
%dir %{_prefix}/libexec/ksysguard
%attr(755,root,root) %{_prefix}/libexec/ksysguard/ksgrd_network_helper

%{_libdir}/qt6/qml/org/kde/ksysguard/faces/SensorRangeSpinBox.qml

%{_libdir}/qt6/qml/org/kde/ksysguard/faces/Choices.qml
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/packagestructure/ksysguard_sensorface.so
%attr(755,root,root) %{_prefix}/libexec/kf6/kauth/ksysguardprocesslist_helper
%{_datadir}/dbus-1/interfaces/org.kde.ksystemstats1.xml

%files devel
%defattr(644,root,root,755)
%{_includedir}/ksysguard
%{_libdir}/cmake/KSysGuard
%{_libdir}/libksgrd.so
%{_libdir}/libksignalplotter.so
%{_libdir}/liblsofui.so
%{_libdir}/libprocesscore.so
%{_libdir}/libprocessui.so
%{_libdir}/libKSysGuardFormatter.so
%{_libdir}/libKSysGuardSensorFaces.so
%{_libdir}/libKSysGuardSensors.so
%{_libdir}/libKSysGuardSystemStats.so
