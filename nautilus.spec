# Note that this is NOT a relocatable package
%define name		nautilus
%define ver		1.0.3
%define RELEASE		4
%define rel		%{?CUSTOM_RELEASE} %{!?CUSTOM_RELEASE:%RELEASE}

Name:		%name
Vendor:		Eazel Inc.
Distribution:	Eazel 1.0.3
Summary:	Nautilus is a network user environment
Version: 	%ver
Release: 	%rel
Copyright: 	GPL
Group:		User Interface/Desktop
Source: 	ftp://ftp.gnome.org/pub/GNOME/stable/sources/%{name}-%{ver}.tar.gz
URL: 		http://nautilus.eazel.com/
BuildRoot:	/var/tmp/%{name}-%{ver}-root
Requires:	glib >= 1.2.9
Requires:	gtk+ >= 1.2.9
Requires:	imlib >= 1.9.8
Requires:	libxml >= 1.8.10
Requires:	gnome-libs >= 1.2.11
Requires:	GConf >= 0.12
Requires:	ORBit >= 0.5.7
Requires:	oaf >= 0.6.5
Requires:	gnome-vfs >= 1.0.1
Requires:	gdk-pixbuf >= 0.10.0
Requires:	bonobo >= 0.37
Requires:	popt >= 1.5
Requires:	freetype >= 2.0.1
Requires:	esound >= 0.2.22
Requires:	libpng
Requires:	control-center >= 1.3
Requires:	librsvg >= 1.0.0
Requires:	eel >= 1.0
Requires:	ammonite >= 1.0.2
Requires:       indexhtml

PreReq:         scrollkeeper >= 0.1.4

BuildRequires:	glib-devel >= 1.2.9
BuildRequires:	gtk+-devel >= 1.2.9
BuildRequires:	imlib-devel >= 1.9.8
BuildRequires:	libxml-devel >= 1.8.10
BuildRequires:	gnome-libs-devel >= 1.2.11
BuildRequires:	GConf-devel >= 0.12
BuildRequires:	ORBit-devel >= 0.5.7
BuildRequires:	oaf-devel >= 0.6.5
BuildRequires:	gnome-vfs-devel >= 1.0.1
BuildRequires:	gdk-pixbuf-devel >= 0.10.0
BuildRequires:	bonobo-devel >= 0.37
BuildRequires:	popt >= 1.5
BuildRequires:	freetype-devel >= 2.0.1
BuildRequires:	esound-devel >= 0.2.22
BuildRequires:	scrollkeeper >= 0.1.4
BuildRequires:	libpng-devel
BuildRequires:	control-center-devel >= 1.3
BuildRequires:	librsvg-devel >= 1.0.0
BuildRequires:	eel-devel >= 1.0
BuildRequires:	mozilla-devel >= 0.8
BuildRequires:	xpdf >= 0.90
ExcludeArch:    ia64
Obsoletes: nautilus-extras
Obsoletes: nautilus-suggested

Patch1: 	nautilus-1.0.3-bookmarks.patch
Patch2:		nautilus-1.0.3-new_theme.patch
Patch3:		nautilus-1.0.3-no-dialog.patch

%description
Nautilus integrates access to files, applications, media, Internet-based
resources and the Web.  Nautilus delivers a dynamic and rich user
experience.  Nautilus is an free software project developed under the
GNU General Public License and is a core component of the GNOME desktop
project.

%package devel
Summary:	Libraries and include files for developing Nautilus components
Group:		Development/Libraries
Requires:	%name = %{PACKAGE_VERSION}

%description devel
This package provides the necessary development libraries and include
files to allow you to develop Nautilus components.

%package mozilla
Summary:        Nautilus component for use with Mozilla
Group:          User Interface/Desktop
Requires:       %name = %{PACKAGE_VERSION}
Requires:	mozilla >= 0.8
Conflicts:	mozilla = M18
Conflicts:	mozilla = M17

%description mozilla
This enables the use of embedded Mozilla as a Nautilus component.


%prep
%setup
%patch1 -p1 -b .bookmarks
%patch2 -p1 -b .new_theme
%patch3 -p1 -b .no-dialog

%build
%configure --disable-more-warnings

make

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%makeinstall

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%post
if ! grep %{_libdir} /etc/ld.so.conf > /dev/null ; then
	echo "%{_libdir}" >> /etc/ld.so.conf
fi
/sbin/ldconfig
scrollkeeper-update

%postun -p /sbin/ldconfig
scrollkeeper-update

%files

%defattr(0555, bin, bin)
%doc AUTHORS COPYING COPYING-DOCS COPYING.LIB TRADEMARK_NOTICE ChangeLog NEWS README
%{_bindir}/nautilus-clean.sh
%{_bindir}/nautilus-verify-rpm.sh
%{_bindir}/nautilus-restore-settings-to-default.sh
%{_bindir}/gnome-db2html2
%{_bindir}/gnome-info2html2
%{_bindir}/gnome-man2html2
%{_bindir}/hyperbola
%{_bindir}/nautilus
%{_bindir}/nautilus-adapter
%{_bindir}/nautilus-content-loser
%{_bindir}/nautilus-error-dialog
%{_bindir}/nautilus-hardware-view
%{_bindir}/nautilus-history-view
%{_bindir}/nautilus-image-view
# %{_bindir}/nautilus-mpg123
%{_bindir}/nautilus-music-view
%{_bindir}/nautilus-news
%{_bindir}/nautilus-notes
%{_bindir}/nautilus-sample-content-view
%{_bindir}/nautilus-sidebar-loser
%{_bindir}/nautilus-text-view
%{_bindir}/nautilus-throbber
%{_bindir}/run-nautilus
%{_bindir}/nautilus-launcher-applet
%{_bindir}/nautilus-xml-migrate
#%{prefix}/idl/*.idl
%{_libdir}/libnautilus-adapter.so.0
%{_libdir}/libnautilus-adapter.so.0.0.0
%{_libdir}/libnautilus-private.so.0
%{_libdir}/libnautilus-private.so.0.0.0
%{_libdir}/libnautilus-tree-view.so.0
%{_libdir}/libnautilus-tree-view.so.0.0.0
%{_libdir}/libnautilus.so.0
%{_libdir}/libnautilus.so.0.0.0
%{_libdir}/libnautilus-adapter.so
%{_libdir}/libnautilus-private.so
%{_libdir}/libnautilus-tree-view.so
%{_libdir}/libnautilus.so



%{_libdir}/vfs/modules/*.so


%defattr (0444, bin, bin)
%config %{_sysconfdir}/vfs/modules/*.conf
%config %{_sysconfdir}/CORBA/servers/nautilus-launcher-applet.gnorba
%{_datadir}/gnome/apps/Applications/*.desktop
%{_datadir}/gnome/ui/*.xml
%{_datadir}/nautilus/components/hyperbola/maps/*.map
%{_datadir}/nautilus/components/hyperbola/*.xml
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/nautilus/*.xml
%{_datadir}/nautilus/emblems/*.png
%{_datadir}/nautilus/linksets/*.xml
%{_datadir}/nautilus/patterns/*.jpg
%{_datadir}/nautilus/patterns/*.png
%{_datadir}/nautilus/patterns/.*.png
%{_datadir}/nautilus/services/text/*.xml
%{_datadir}/pixmaps/*.png
%{_datadir}/pixmaps/nautilus/*.gif
%{_datadir}/pixmaps/nautilus/*.png
%{_datadir}/pixmaps/nautilus/*.svg
%{_datadir}/pixmaps/nautilus/*.xml
%{_datadir}/pixmaps/nautilus/tahoe/*.png
%{_datadir}/pixmaps/nautilus/tahoe/*.xml
%{_datadir}/pixmaps/nautilus/crux_teal/*.png
%{_datadir}/pixmaps/nautilus/crux_teal/*.xml
%{_datadir}/pixmaps/nautilus/crux_teal/throbber/*.png
%{_datadir}/pixmaps/nautilus/crux_teal/backgrounds/*.png
%{_datadir}/pixmaps/nautilus/crux_teal/sidebar_tab_pieces/*.png
%{_datadir}/pixmaps/nautilus/crux_eggplant/*.png
%{_datadir}/pixmaps/nautilus/crux_eggplant/*.xml
%{_datadir}/pixmaps/nautilus/crux_eggplant/throbber/*.png
%{_datadir}/pixmaps/nautilus/crux_eggplant/backgrounds/*.png
%{_datadir}/pixmaps/nautilus/crux_eggplant/sidebar_tab_pieces/*.png
%{_datadir}/pixmaps/nautilus/eazel-logos/*.png
%{_datadir}/pixmaps/nautilus/eazel-logos/*.xml
#%{_datadir}/pixmaps/nautilus/eazel-logos/throbber/*.png
%{_datadir}/pixmaps/nautilus/eazel-logos/LICENSE
%{_datadir}/pixmaps/nautilus/gnome/*.png
%{_datadir}/pixmaps/nautilus/gnome/*.xml
%{_datadir}/pixmaps/nautilus/gnome/throbber/*.png
%{_datadir}/pixmaps/nautilus/sidebar_tab_pieces/*.png
%{_datadir}/pixmaps/nautilus/throbber/*.png
%{_datadir}/pixmaps/nautilus/sierra/*.xml
%{_datadir}/pixmaps/nautilus/sierra/*.png
%{_datadir}/oaf/Nautilus_View_help.oaf
%{_datadir}/oaf/Nautilus_ComponentAdapterFactory_std.oaf
%{_datadir}/oaf/Nautilus_View_content-loser.oaf
%{_datadir}/oaf/Nautilus_View_hardware.oaf
%{_datadir}/oaf/Nautilus_View_history.oaf
%{_datadir}/oaf/Nautilus_View_image.oaf
%{_datadir}/oaf/Nautilus_View_music.oaf
%{_datadir}/oaf/Nautilus_View_news.oaf
%{_datadir}/oaf/Nautilus_View_notes.oaf
%{_datadir}/oaf/Nautilus_View_sample.oaf
%{_datadir}/oaf/Nautilus_View_sidebar-loser.oaf
%{_datadir}/oaf/Nautilus_View_text.oaf
%{_datadir}/oaf/Nautilus_View_tree.oaf
%{_datadir}/oaf/Nautilus_shell.oaf
%{_datadir}/oaf/Nautilus_Control_throbber.oaf

%defattr (-, root, root)
%{_datadir}/gnome/help
%{_datadir}/omf/nautilus

%files devel

%defattr(0555, bin, bin)
%{_libdir}/*.la
%{_libdir}/vfs/modules/*.la
%{_libdir}/*.sh
%{_bindir}/nautilus-config

%defattr(0444, bin, bin)
%{_includedir}/libnautilus/*.h

%files mozilla

%defattr(0555, bin, bin)
%{_bindir}/nautilus-mozilla-content-view

%defattr(0444, bin, bin)
%{_datadir}/oaf/Nautilus_View_mozilla.oaf


%changelog
* Thu May 10 2001 Jonathan Blandford <jrb@redhat.com>
- clean up defaults a bit

* Wed May  9 2001 Jonathan Blandford <jrb@redhat.com>
- New version

* Tue Apr 17 2001 Gregory Leblanc <gleblanc@grego1.cu-portland.edu>
- Added BuildRequires lines
- Changed Source to point to ftp.gnome.org instead of just the tarball name
- Moved %description sections closer to their %package sections
- Moved %changelog to the end, where so that it's not in the way
- Changed configure and make install options to allow moving of
  libraries, includes, binaries more easily
- Removed hard-coded paths (don't define %prefix or %docdir)
- replace %{prefix}/bin with %{_bindir}
- replace %{prefix}/share with %{_datadir}
- replace %{prefix}/lib with %{_libdir}
- replace %{prefix}/include with %{_includedir}

* Tue Oct 10 2000 Robin Slomkowski <rslomkow@eazel.com>
- removed obsoletes from sub packages and added mozilla and trilobite
subpackages

* Wed Apr 26 2000 Ramiro Estrugo <ramiro@eazel.com>
- created this thing
