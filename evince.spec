Summary:	Document viewer for multiple document formats
Name:		evince
Version:	3.8.3
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/evince/3.8/evince-%{version}.tar.xz
# Source0-md5:	81a8b0ffc427f2e3bde4056286e3a27a
Patch0:		evince-correct-return.patch
Patch1:		evince-lz.patch
URL:		http://www.gnome.org/projects/evince/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel
BuildRequires:	djvulibre-devel
BuildRequires:	ghostscript
BuildRequires:	gnome-doc-utils
BuildRequires:	gnome-icon-theme-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	intltool
#BuildRequires:	kpathsea-devel
BuildRequires:	libgnome-keyring-devel
BuildRequires:	libspectre-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
BuildRequires:	libxslt-progs
BuildRequires:	nautilus-devel
BuildRequires:	pkg-config
BuildRequires:	poppler-glib-devel
BuildRequires:	python-libxml2
Requires:	%{name}-libs = %{version}-%{release}
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib-gio-gsettings
Requires(post,postun):	hicolor-icon-theme
Requires:	xdg-icon-theme
Obsoletes:	evince2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/evince

%description
Evince is a document viewer for multiple document formats like pdf,
postscript, and many others. The goal of evince is to replace the
multiple document viewers that exist on the GNOME Desktop, like ggv,
gpdf, and xpdf with a single simple application.

%package libs
Summary:	Evince evbackend library
Group:		Libraries

%description libs
Evince backend library.

%package devel
Summary:	Header files for evbackend library
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for evbackend library.

%package -n nautilus-extension-evince
Summary:	Evince extension for Nautilus
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	nautilus

%description -n nautilus-extension-evince
Shows Evince document properties in Nautilus.

%package apidocs
Summary:	Evince API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
Evince API documentation.

%prep
%setup -qn evince-%{version}
%patch0 -p1
%patch1 -p1

# kill gnome common deps
sed -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_CXX_WARNINGS.*//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g' 		\
    -i -e 's/AM_GCONF_SOURCE_2//' configure.ac

%build
%{__gtkdocize}
%{__gnome_doc_prepare}
%{__libtoolize}
%{__intltoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-comics		\
	--disable-schemas-compile	\
	--disable-scrollkeeper		\
	--disable-silent-rules		\
	--disable-static		\
	--enable-djvu			\
	--enable-dvi			\
	--enable-ps			\
	--enable-t1lib			\
	--enable-tiff			\
	--enable-dbus			\
	--enable-introspection		\
	--enable-nautilus		\
	--with-keyring			\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/evince/?/backends/*.la
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw,ks,ps}

%if %{with simple}
rm -f $RPM_BUILD_ROOT%{_libdir}/*.{la,so}
rm -rf $RPM_BUILD_ROOT{%{_includedir},%{_gtkdocdir},%{_pkgconfigdir},%{_datadir}/{gnome,omf}}
%else
rm -rf $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-3.0/*.la
%endif

%find_lang evince --with-gnome --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%update_icon_cache hicolor
%update_gsettings_cache

%postun
%update_desktop_database_postun
%update_icon_cache hicolor
%update_gsettings_cache

%post	libs -p /usr/sbin/ldconfig
%postun libs -p /usr/sbin/ldconfig

%files -f evince.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO

%dir %{_libexecdir}
%dir %{_libexecdir}/?
%dir %{_libexecdir}/?/backends

%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/evince/?/backends/*.so
%{_libexecdir}/?/backends/*.evince-backend
%{_datadir}/evince
%{_datadir}/glib-2.0/schemas/org.gnome.Evince.gschema.xml
%{_datadir}/thumbnailers/evince.thumbnailer
%{_desktopdir}/*.desktop
%{_iconsdir}/*/*/*/*

%if !%{with simple}
%attr(755,root,root) %{_libdir}/evince/evinced
%{_datadir}/dbus-1/services/org.gnome.evince.Daemon.service
%endif

%{_mandir}/man1/evince.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libev*.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libev*.so.?
%{_libdir}/girepository-1.0/*.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libev*.so
%{_includedir}/evince
%{_pkgconfigdir}/*.pc
%{_datadir}/gir-1.0/*.gir

%files -n nautilus-extension-evince
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/nautilus/extensions-3.0/*.so*

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/*

