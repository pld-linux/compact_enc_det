Summary:	Compact Encoding Detection library
Summary(pl.UTF-8):	Compact Encoding Detection library - niewielka biblioteka do wykrywania kodowania
Name:		compact_enc_det
Version:	0
%define	gitref	d127078cedef9c6642cbe592dacdd2292b50bb19
%define	snap	20240213
%define	rel	2
Release:	0.%{snap}.%{rel}
License:	Apache v2.0
Group:		Libraries
Source0:	https://github.com/google/compact_enc_det/archive/%{gitref}/%{name}-%{snap}.tar.gz
# Source0-md5:	4ae1f65399bcd7517e854635832e7a5d
Patch0:		%{name}-gtest.patch
URL:		https://github.com/google/compact_enc_det
BuildRequires:	cmake >= 2.8.7
BuildRequires:	gtest-devel
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Compact Encoding Detection (CED for short) is a library written in C++
that scans given raw bytes and detect the most likely text encoding.

%description -l pl.UTF-8
Compact Encoding Detection (w skrócie CED) to napisana w C++
biblioteka skanująca przekazane surowe bajty i wykrywająca najbardziej
prawdopodobne kodowanie tekstu.

%package devel
Summary:	Header files for CED library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki CED
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for CED library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki CED.

%prep
%setup -q -n %{name}-%{gitref}
%patch0 -p1

# because of gtest
%{__sed} -i -e 's/-std=c++11/-std=c++14/' CMakeLists.txt

%build
install -d build
cd build
%cmake ..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/ced/{compact_enc_det,util/{encodings,languages}},%{_pkgconfigdir}}

# missing install target, do it manually
install build/lib/libced.so $RPM_BUILD_ROOT%{_libdir}
cp -p compact_enc_det/compact_enc_det.h $RPM_BUILD_ROOT%{_includedir}/ced/compact_enc_det
cp -p util/encodings/*.h $RPM_BUILD_ROOT%{_includedir}/ced/util/encodings
cp -p util/languages/*.h $RPM_BUILD_ROOT%{_includedir}/ced/util/languages

cat >$RPM_BUILD_ROOT%{_pkgconfigdir}/ced.pc <<'EOF'
prefix=%{_prefix}
includedir=%{_includedir}/ced
libdir=%{_libdir}

Name: ced
Description: Compact Encoding Detection library
Version: %{version}
Libs: -L${libdir} -lced
Cflags: -I${includedir}
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libced.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/ced
%{_pkgconfigdir}/ced.pc
