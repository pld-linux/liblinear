#
# Conditional build:
%bcond_without	octave	# Octave (MATLAB) module
%bcond_without	python	# Python (any) interface
%bcond_without	python2	# Python 2.x interface
%bcond_without	python3	# Python 3.x interface
#
%if %{without python}
%undefine	with_python2
%undefine	with_python3
%endif
Summary:	LIBLINEAR - a Library for Large Linear Classification
Summary(pl.UTF-8):	LIBLINEAR - biblioteka do liniowej klasyfikacji dużych danych
Name:		liblinear
Version:	2.49
Release:	1
License:	BSD
Group:		Libraries
Source0:	https://www.csie.ntu.edu.tw/~cjlin/liblinear/%{name}-%{version}.tar.gz
# Source0-md5:	43361775e2b0231f101d36d39cda110a
Patch0:		%{name}-python.patch
Patch1:		%{name}-make.patch
Patch2:		%{name}-matlab.patch
URL:		https://www.csie.ntu.edu.tw/~cjlin/liblinear/
BuildRequires:	blas-devel
BuildRequires:	libstdc++-devel
%{?with_octave:BuildRequires:	octave-devel}
%{?with_python2:BuildRequires:	python-devel >= 1:2.7}
%{?with_python2:BuildRequires:	python-setuptools}
%{?with_python3:BuildRequires:	python3-devel >= 1:3.5}
%{?with_python3:BuildRequires:	python3-setuptools}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		octave_oct_dir	%(octave-config --oct-site-dir)

%description
LIBLINEAR is a simple package for solving large-scale regularized
linear classification and regression. It currently supports:
- L2-regularized logistic regression/L2-loss support vector
  classification/L1-loss support vector classification
- L1-regularized L2-loss support vector classification/L1-regularized
  logistic regression
- L2-regularized L2-loss support vector regression/L1-loss support
  vector regression.

%description -l pl.UTF-8
LIBLINEAR to prosty pakiet do rozwiązywania zagadnień regularnej
klasyfikacji liniowej i regresji. Obecnie obsługuje:
- regresję logistyczną z regularyzacją L2
- regresję logistyczną z regularyzacją L1
- regresję wektorową z regularyzacją L2

%package devel
Summary:	Header files for LIBLINEAR library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki LIBLINEAR
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for LIBLINEAR library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki LIBLINEAR.

%package -n octave-liblinear
Summary:	MATLAB/Octave interface for LIBLINEAR library
Summary(pl.UTF-8):	Interfejs MATLAB-a/Octave do biblioteki LIBLINEAR
Group:		Libraries
Requires:	octave

%description -n octave-liblinear
MATLAB/Octave interface for LIBLINEAR library.

%description -n octave-liblinear -l pl.UTF-8
Interfejs MATLAB-a/Octave do biblioteki LIBLINEAR.

%package -n python-liblinear
Summary:	Python 2 interface for LIBLINEAR library
Summary(pl.UTF-8):	Interfejs Pythona 2 do biblioteki LIBLINEAR
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-libs >= 1:2.7
BuildArch:	noarch

%description -n python-liblinear
Python 2 interface for LIBLINEAR library.

%description -n python-liblinear -l pl.UTF-8
Interfejs Pythona 2 do biblioteki LIBLINEAR.

%package -n python3-liblinear
Summary:	Python 3 interface for LIBLINEAR library
Summary(pl.UTF-8):	Interfejs Pythona 3 do biblioteki LIBLINEAR
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python3-libs >= 1:3.5
BuildArch:	noarch

%description -n python3-liblinear
Python 3 interface for LIBLINEAR library.

%description -n python3-liblinear -l pl.UTF-8
Interfejs Pythona 3 do biblioteki LIBLINEAR.

%prep
%setup -q
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1

%build
%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} -fPIC -Wall" \
	LIBS="-lblas"

%if %{with octave}
%{__make} -C matlab \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} -fPIC -I.. -I/usr/include/octave -Wall" \
	MEX=mkoctfile \
	MEX_OPTION=--mex \
	MEX_EXT=mex
%endif

%if %{with python2}
cd python
%py_build
cd ..
%endif

%if %{with python3}
cd python
%py3_build
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir}}

install liblinear.so.* $RPM_BUILD_ROOT%{_libdir}
ln -sf $(basename $RPM_BUILD_ROOT%{_libdir}/liblinear.so.*) $RPM_BUILD_ROOT%{_libdir}/liblinear.so
cp -p linear.h newton.h $RPM_BUILD_ROOT%{_includedir}
install train $RPM_BUILD_ROOT%{_bindir}/liblinear-train
install predict $RPM_BUILD_ROOT%{_bindir}/liblinear-predict

%if %{with octave}
install -d $RPM_BUILD_ROOT%{octave_oct_dir}/liblinear
install matlab/*.mex $RPM_BUILD_ROOT%{octave_oct_dir}/liblinear
%endif

%if %{with python2}
cd python
%py_install

%py_postclean
cd ..
%endif

%if %{with python3}
cd python
%py3_install
cd ..
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYRIGHT README
%attr(755,root,root) %{_bindir}/liblinear-predict
%attr(755,root,root) %{_bindir}/liblinear-train
%attr(755,root,root) %{_libdir}/liblinear.so.6

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblinear.so
%{_includedir}/linear.h
%{_includedir}/newton.h

%if %{with octave}
%files -n octave-liblinear
%defattr(644,root,root,755)
%dir %{octave_oct_dir}/liblinear
%attr(755,root,root) %{octave_oct_dir}/liblinear/libsvmread.mex
%attr(755,root,root) %{octave_oct_dir}/liblinear/libsvmwrite.mex
%attr(755,root,root) %{octave_oct_dir}/liblinear/predict.mex
%attr(755,root,root) %{octave_oct_dir}/liblinear/train.mex
%endif

%if %{with python2}
%files -n python-liblinear
%defattr(644,root,root,755)
%doc python/README
%{py_sitescriptdir}/liblinear
%{py_sitescriptdir}/liblinear_official-%{version}.0-py*.egg-info
%endif

%if %{with python3}
%files -n python3-liblinear
%defattr(644,root,root,755)
%doc python/README
%{py3_sitescriptdir}/liblinear
%{py3_sitescriptdir}/liblinear_official-%{version}.0-py*.egg-info
%endif
