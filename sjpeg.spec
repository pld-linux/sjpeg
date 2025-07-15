#
# Conditional build:
%bcond_with	simd		# x86 SSE2 / ARM NEON instructions
#
%ifarch %{x8664} x32
%define	with_simd	1
%endif
Summary:	Simple JPEG library and utilities
Summary(pl.UTF-8):	Biblioteka i narzędzia Simple JPEG
Name:		sjpeg
Version:	0.1
%define	gitref	676de227d75877eb5863ec805ba0a4b97fc2fc6c
%define	snap	20210423
%define	rel	1
Release:	0.%{snap}.1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/webmproject/sjpeg/releases
Source0:	https://github.com/webmproject/sjpeg/archive/%{gitref}/%{name}-%{snap}.tar.gz
# Source0-md5:	e9a5386cca1baccb26d077b338ca3391
Patch0:		%{name}-cmake.patch
URL:		https://github.com/webmproject/sjpeg
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-glut-devel
BuildRequires:	cmake >= 2.8.7
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel >= 6:4.7
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Simple JPEG library and utilities.

%description -l pl.UTF-8
Biblioteka i narzędzia Simple JPEG.

%package libs
Summary:	Simple encoding library for baseline JPEG files
Summary(pl.UTF-8):	Prosta biblioteka kodująca do podstawowego formatu JPEG
Group:		Libraries

%description libs
Simple encoding library for baseline JPEG files.

%description libs -l pl.UTF-8
Prosta biblioteka kodująca do podstawowego formatu JPEG.

%package devel
Summary:	Header files for sjpeg library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki sjpeg
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for sjpeg library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki sjpeg.

%prep
%setup -q -n %{name}-%{gitref}
%patch -P0 -p1

%build
install -d build
cd build
%cmake .. \
	%{!?with_simd:-DSJPEG_ENABLE_SIMD=OFF}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/sjpeg
%attr(755,root,root) %{_bindir}/vjpeg
%{_mandir}/man1/sjpeg.1*
%{_mandir}/man1/vjpeg.1*

%files libs
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md
%attr(755,root,root) %{_libdir}/libsjpeg.so.0.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsjpeg.so
%{_includedir}/sjpeg.h
%dir %{_datadir}/sjpeg
%{_datadir}/sjpeg/cmake
