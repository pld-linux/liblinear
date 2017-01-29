Summary:	LIBLINEAR - a Library for Large Linear Classification
Summary(pl.UTF-8):	LIBLINEAR - biblioteka do liniowej klasyfikacji dużych danych
Name:		liblinear
Version:	2.1
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://www.csie.ntu.edu.tw/~cjlin/liblinear/%{name}-%{version}.tar.gz
# Source0-md5:	0d87a71d054ed17c5ee7656efba06e89
Patch0:		%{name}-python.patch
Patch1:		%{name}-make.patch
URL:		http://www.csie.ntu.edu.tw/~cjlin/liblinear/
BuildRequires:	blas-devel
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%package -n python-liblinear
Summary:	Python interface for LIBLINEAR library
Summary(pl.UTF-8):	Interfejs Pythona do biblioteki LIBLINEAR
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-liblinear
Python interface for LIBLINEAR library.

%description -n python-liblinear -l pl.UTF-8
Interfejs Pythona do biblioteki LIBLINEAR.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} -fPIC -Wall" \
	LIBS="-lblas"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir},%{py_sitescriptdir}}

install liblinear.so.* $RPM_BUILD_ROOT%{_libdir}
ln -sf $(basename $RPM_BUILD_ROOT%{_libdir}/liblinear.so.*) $RPM_BUILD_ROOT%{_libdir}/liblinear.so
cp -p linear.h tron.h $RPM_BUILD_ROOT%{_includedir}
install train $RPM_BUILD_ROOT%{_bindir}/liblinear-train
install predict $RPM_BUILD_ROOT%{_bindir}/liblinear-predict
cp -p python/*.py $RPM_BUILD_ROOT%{py_sitescriptdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYRIGHT README
%attr(755,root,root) %{_bindir}/liblinear-predict
%attr(755,root,root) %{_bindir}/liblinear-train
%attr(755,root,root) %{_libdir}/liblinear.so.3

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblinear.so
%{_includedir}/linear.h
%{_includedir}/tron.h

%files -n python-liblinear
%defattr(644,root,root,755)
%{py_sitescriptdir}/liblinear.py
%{py_sitescriptdir}/liblinearutil.py
