#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	gjs		# GJS loader
%bcond_without	luajit		# LuaJIT implementation of lua 5.1
%bcond_without	static_libs	# static libraries
%bcond_without	lua		# Lua (5.1) loader
%bcond_without	python		# Python (3.x) loader

# luajit is not supported on x32
%ifarch x32
%undefine	with_luajit
%endif

Summary:	GObject Plugin System
Summary(pl.UTF-8):	System wtyczek GObject
Name:		libpeas2
Version:	2.0.2
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://download.gnome.org/sources/libpeas/2.0/libpeas-%{version}.tar.xz
# Source0-md5:	67d4ffcc50eca121d3a480bac44d4883
URL:		https://wiki.gnome.org/Libpeas
BuildRequires:	gettext-tools >= 0.19.7
%{?with_apidocs:BuildRequires:	gi-docgen >= 2021.7}
%{?with_gjs:BuildRequires:	gjs-devel >= 1.77.1}
BuildRequires:	glib2-devel >= 1:2.74
BuildRequires:	gobject-introspection-devel >= 1.40.0
BuildRequires:	libstdc++-devel >= 6:7
%if %{with lua}
BuildRequires:	lua-lgi >= 0.9.0
%if %{without luajit}
BuildRequires:	lua51 >= 5.1.0
BuildRequires:	lua51-devel >= 5.1.0
%else
BuildRequires:	luajit >= 2.0
BuildRequires:	luajit-devel >= 2.0
%endif
%endif
BuildRequires:	meson >= 0.50.0
%{?with_gjs:BuildRequires:	mozjs115-devel >= 115}
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
%if %{with python}
BuildRequires:	python3-devel >= 1:3.2.0
BuildRequires:	python3-pygobject3-devel >= 3.2.0
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.029
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala
BuildRequires:	xz
%{!?with_luajit:BuildConflicts:	luajit-devel}
Requires:	glib2 >= 1:2.74
Requires:	gobject-introspection >= 1.40.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libpeas is a gobject-based plugins engine, and is targetted at giving
every application the chance to assume its own extensibility. It also
has a set of features including, but not limited to:
 - multiple extension points
 - on demand (lazy) programming language support for C, Python and Lua
 - simplicity of the API

%description -l pl.UTF-8
libpeas to silnik wtyczek oparty na bibliotece GObject; jego celem
jest zapewnienie każdej aplikacji własnej rozszerzalności. Ma także
pewien zbiór możliwości, w tym:
 - wiele punktów rozszerzeń
 - wsparcie dla leniwego programowania dla języków C, Python i Lua
 - prostota API

%package loader-gjs
Summary:	JavaScript (GJS) loader for libpeas 2 library
Summary(pl.UTF-8):	Moduł ładujący dla JavaScriptu (GJS) do biblioteki libpeas 2
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gjs >= 1.77.1

%description loader-gjs
JavaScript (GJS) loader for libpeas 2 library.

%description loader-gjs -l pl.UTF-8
Moduł ładujący dla JavaScriptu (GJS) do biblioteki libpeas 2.

%package loader-lua
Summary:	Lua loader for libpeas 2 library
Summary(pl.UTF-8):	Moduł ładujący dla języka Lua do biblioteki libpeas 2
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	lua-lgi >= 0.9.0

%description loader-lua
Lua loader for libpeas 2 library.

%description loader-lua -l pl.UTF-8
Moduł ładujący dla języka Lua do biblioteki libpeas 2.

%package loader-python
Summary:	Python 3.x loader for libpeas 2 library
Summary(pl.UTF-8):	Moduł ładujący dla Pythona 3.x do biblioteki libpeas 2
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description loader-python
Python 3.x loader for libpeas 2 library.

%description loader-python -l pl.UTF-8
Moduł ładujący dla Pythona 3.x do biblioteki libpeas 2.

%package devel
Summary:	Header files for libpeas 2 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libpeas 2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.74
Requires:	gobject-introspection-devel >= 1.40.0

%description devel
Header files for libpeas 2 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libpeas 2.

%package static
Summary:	Static libpeas 2 library
Summary(pl.UTF-8):	Statyczna biblioteka libpeas 2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libpeas 2 library.

%description static -l pl.UTF-8
Statyczna biblioteka libpeas 2.

%package -n vala-libpeas2
Summary:	Vala API for libpeas 2 library
Summary(pl.UTF-8):	API języka Vala do biblioteki libpeas 2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala
BuildArch:	noarch

%description -n vala-libpeas2
Vala API for libpeas 2 library.

%description -n vala-libpeas2 -l pl.UTF-8
API języka Vala do biblioteki libpeas 2.

%package apidocs
Summary:	libpeas API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libpeas
Group:		Documentation
BuildArch:	noarch

%description apidocs
API and internal documentation for libpeas library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libpeas.

%prep
%setup -q -n libpeas-%{version}

%if %{with lua}
# meson buildsystem expects .pc file for lua-lgi detection
install -d fake-pkgconfig
cat >fake-pkgconfig/lua5.1-lgi.pc <<'EOF'
Name: lua-lgi
Description: Lua LGI
Version: %(rpm -q --qf '%%{V}\n' lua-lgi)
EOF
%endif

%build
export PKG_CONFIG_PATH=$(pwd)/fake-pkgconfig
%meson build \
	%{!?with_static_libs:--default-library=shared} \
	%{!?with_gjs:-Dgjs=false} \
	%{?with_apidocs:-Dgtk_doc=true} \
	%{!?with_lua:-Dlua51=false} \
	%{!?with_python:-Dpython3=false} \
	-Dvapi=true

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/libpeas-* $RPM_BUILD_ROOT%{_gidocdir}
%endif

# not supported by glibc (as of 2.37)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang libpeas-2

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f libpeas-2.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md
%attr(755,root,root) %{_libdir}/libpeas-2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpeas-2.so.0
%dir %{_libdir}/libpeas-2
%dir %{_libdir}/libpeas-2/loaders
%{_libdir}/girepository-1.0/Peas-2.typelib

%if %{with gjs}
%files loader-gjs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpeas-2/loaders/libgjsloader.so
%endif

%if %{with lua}
%files loader-lua
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpeas-2/loaders/liblua51loader.so
%endif

%if %{with python}
%files loader-python
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpeas-2/loaders/libpythonloader.so
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpeas-2.so
%{_includedir}/libpeas-2
%{_pkgconfigdir}/libpeas-2.pc
%{_datadir}/gir-1.0/Peas-2.gir

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libpeas-2.a
%endif

%files -n vala-libpeas2
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libpeas-2.deps
%{_datadir}/vala/vapi/libpeas-2.vapi

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/libpeas-2
%endif
