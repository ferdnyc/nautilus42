Name:		nautilus
Summary: Nautilus is a network user environment
Version: 	1.0.4
Release: 	46.1
Copyright: 	GPL
Group: User Interface/Desktops
Source: 	ftp://ftp.gnome.org/pub/GNOME/stable/sources/%{name}-%{version}-snapshot.tar.gz
Source2:        nautilus-redhat-theme.xml
Source3:        desktop-folders.tar.gz
Source4:        reset.png
Source5:        nautilus-pofiles.tar.gz
URL: 		http://nautilus.eazel.com/
BuildRoot:	/var/tmp/%{name}-%{version}-root
Requires:	glib >= 1.2.9
Requires:	gtk+ >= 1.2.9
Requires:	imlib >= 1.9.8
Requires:	libxml >= 1.8.10
Requires:	gnome-libs >= 1.2.11
Requires:	GConf >= 0.12
Requires:	ORBit >= 0.5.7
Requires:	oaf >= 0.6.5
Requires:	gnome-vfs >= 1.0.1-13
Requires:	gdk-pixbuf >= 0.10.0
Requires:	bonobo >= 0.37
Requires:	popt >= 1.5
Requires:	freetype >= 2.0.1
Requires:	esound >= 0.2.22
Requires:	libpng
Requires:	control-center >= 1.3
Requires:	librsvg >= 1.0.0
Requires:	eel >= 1.0.1-10
Requires:       indexhtml
Requires:	fam
Requires:       filesystem >= 2.1.1-1
Requires:	hwbrowser

%ifarch i386 alpha
Requires:	nautilus-mozilla
%endif

PreReq:         scrollkeeper >= 0.1.4

BuildRequires:	glib-devel >= 1.2.9
BuildRequires:	gtk+-devel >= 1.2.9
BuildRequires:	imlib-devel >= 1.9.8
BuildRequires:	libxml-devel >= 1.8.10
BuildRequires:  gnome-print-devel
BuildRequires:  libghttp-devel
BuildRequires:	gnome-libs-devel >= 1.2.11
BuildRequires:	GConf-devel >= 0.12
BuildRequires:	ORBit-devel >= 0.5.7
BuildRequires:	oaf-devel >= 0.6.5
BuildRequires:  gnome-core-devel
BuildRequires:	gnome-vfs-devel >= 1.0.1-4
BuildRequires:	gdk-pixbuf-devel >= 0.10.0
BuildRequires:	bonobo-devel >= 0.37
BuildRequires:	popt >= 1.5
BuildRequires:	freetype-devel >= 2.0.1
BuildRequires:	esound-devel >= 0.2.22
BuildRequires:	scrollkeeper >= 0.1.4
BuildRequires:	libpng-devel
BuildRequires:	control-center-devel >= 1.3
BuildRequires:	librsvg-devel >= 1.0.0
BuildRequires:	eel-devel >= 1.0.1-8
#This is commented out becaus RPM doesn't support ifarch BuildRequires
#BuildRequires:	mozilla-devel >= 0.9.2-10
BuildRequires:	xpdf >= 0.90
BuildRequires:	fam-devel
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:  librsvg

Obsoletes: nautilus-extras
Obsoletes: nautilus-suggested

Patch1: 	nautilus-1.0.3-bookmarks.patch
Patch2:		nautilus-1.0.3-new_theme.patch
Patch3:		nautilus-1.0.3-no-dialog.patch
Patch4:         nautilus-1.0.3.2-useredhattheme.patch
Patch8:		nautilus-1.0.4-noflash.patch
# Fixes and hacks for more efficient desktop backgrounds
Patch13:	nautilus-1.0.4-bghack.patch
Patch16:        nautilus-1.0.4-norootwarning.patch
Patch17:        nautilus-snap-directory.patch
Patch18:        nautilus-1.0.4-removeicons.patch
Patch19:	nautilus-1.0.4-newmozilla.patch
Patch20:	nautilus-1.0.4-1.0.6-mozilla.patch
Patch21:        nautilus-1.0.6-metafilerace.patch
Patch22:        nautilus-1.0.4-noglobalmetadata.patch
Patch23:        nautilus-1.0.6-fixperms.patch

%description
Nautilus integrates access to files, applications, media,
Internet-based resources and the Web. Nautilus delivers a dynamic and
rich user experience. Nautilus is an free software project developed
under the GNU General Public License and is a core component of the
GNOME desktop project.

%package devel
Summary: Libraries and include files for developing Nautilus components
Group: Development/Libraries
Requires:	%name = %{version}

%description devel
This package provides the necessary development libraries and include
files to allow you to develop Nautilus components.

%package mozilla
Summary: Nautilus component for use with Mozilla
Group: User Interface/Desktops
Requires:       %name = %{version}
Requires:	mozilla >= 0.9.2-10
Conflicts:	mozilla = M18
Conflicts:	mozilla = M17

%description mozilla
This enables the use of embedded Mozilla as a Nautilus component.


%prep
%setup -q -n %{name}-%{version}-snapshot

## give us something to patch
touch libnautilus-private/nautilus-desktop-file.h
touch libnautilus-private/nautilus-desktop-file.c

cp %{SOURCE4} data/patterns

## unpack pofiles
tar zxf %{SOURCE5}

%patch1 -p1 -b .bookmarks
%patch2 -p1 -b .new_theme
%patch3 -p1 -b .no-dialog
%patch4 -p1 -b .useredhattheme
%patch8 -p1 -b .noflash
%patch13 -p1 -b .bghack
%patch16 -p0 -b .norootwarning
%patch17 -p1 -b .directory
%patch18 -p1 -b .removeicons
%patch19 -p1 -b .sopwith
%patch20 -p1 -b .1.0.6-mozilla
%patch21 -p1 -b .metafilerace
%patch22 -p1 -b .noglobalmetadata
%patch23 -p1 -b .fixperms

## desktop-folders
tar zxf %{SOURCE3}

%build
autoheader
automake
autoconf
%ifarch ia64
CFLAGS="$RPM_OPT_FLAGS -g" %configure --disable-more-warnings --disable-mozilla-component
%else
CFLAGS="$RPM_OPT_FLAGS -g" %configure --disable-more-warnings
%endif

# Hack things so that a build with smp_mflags will be more likely to work
make -C libnautilus nautilus_view_component_idl_stamp \
	 nautilus_distributed_undo_idl_stamp
make -C libnautilus-adapter nautilus_adapter_factory_idl_stamp
make -C libnautilus-private nautilus_metafile_server_idl_stamp
make -C src nautilus_shell_interface_idl_stamp

make %{?_smp_mflags}

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%makeinstall

## Dynamically create Red Hat theme which is just the GNOME theme 
## with some small tweaks 
mkdir -p $RPM_BUILD_ROOT%{_prefix}/share/pixmaps/nautilus/redhat
cp -a $RPM_BUILD_ROOT%{_prefix}/share/pixmaps/nautilus/gnome/* \
      $RPM_BUILD_ROOT%{_prefix}/share/pixmaps/nautilus/redhat
cp -af $RPM_BUILD_ROOT%{_prefix}/share/pixmaps/nautilus/sidebar_tab_pieces/* \
      $RPM_BUILD_ROOT%{_prefix}/share/pixmaps/nautilus/redhat/sidebar_tab_pieces
rm $RPM_BUILD_ROOT%{_prefix}/share/pixmaps/nautilus/redhat/gnome.xml
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_prefix}/share/pixmaps/nautilus/redhat/redhat.xml

(cd desktop-folders && DESTDIR=$RPM_BUILD_ROOT ./run-install.sh)

%find_lang %name

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
scrollkeeper-update

%postun
/sbin/ldconfig
scrollkeeper-update

%files  -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING COPYING-DOCS COPYING.LIB TRADEMARK_NOTICE ChangeLog NEWS README
%config /etc/X11/*/*.desktop
%config /etc/X11/*/.directory
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
%{_libdir}/libnautilus-tree-view.so



%{_libdir}/vfs/modules/*.so


%config %{_sysconfdir}/vfs/modules/*.conf
%config %{_sysconfdir}/CORBA/servers/nautilus-launcher-applet.gnorba
%{_datadir}/gnome/apps/Applications/*.desktop
%{_datadir}/gnome/apps/*.desktop
%{_datadir}/gnome/ui
%{_datadir}/nautilus
%{_datadir}/pixmaps/*.png
%{_datadir}/pixmaps/nautilus
%{_datadir}/oaf
%{_datadir}/gnome/help
%{_datadir}/omf/nautilus

%files devel
%defattr(-,root,root)
%{_libdir}/libnautilus.so
%{_libdir}/*.la
%{_libdir}/vfs/modules/*.la
%{_libdir}/*.sh
%{_bindir}/nautilus-config
%{_includedir}/libnautilus

%ifnarch ia64
%files mozilla
%defattr(-,root,root)
%{_bindir}/nautilus-mozilla-content-view
%{_datadir}/oaf/Nautilus_View_mozilla.oaf
%endif

%changelog
* Mon Apr 29 2002 Havoc Pennington <hp@redhat.com>
- port patch to use mode 600 even for metadata stored in homedir

* Sun Apr 28 2002 Havoc Pennington <hp@redhat.com>
- port patch to totally disable global metadata

* Mon Apr 15 2002 Havoc Pennington <hp@redhat.com>
- backport patch for metafile race condition

* Wed Mar 27 2002 Elliot Lee <sopwith@redhat.com> 1.0.4-43.1
- Patch19 - build with mozilla 0.9.9
- Patch20 - finish building with mozilla 0.9.9 by patching to the
  1.0.6 mozilla component

* Thu Sep  6 2001 Owen Taylor <otaylor@redhat.com>
- Fix handling of GnomeVFSFileInfo structure (#53315)

* Wed Sep  5 2001 Owen Taylor <otaylor@redhat.com>
- Change handling of names on unmount to fix #52325

* Tue Sep  4 2001 Havoc Pennington <hp@redhat.com>
- put nautilus-help.desktop in file list; #53109

* Fri Aug 31 2001 Havoc Pennington <hp@redhat.com>
- Add po files from sources.redhat.com

* Mon Aug 27 2001 Havoc Pennington <hp@redhat.com>
- Add po files from sources.redhat.com

* Thu Aug 23 2001 Alex Larsson <alexl@redhat.com> 1.0.4-38
- Added patch to fix the .directory issuer

* Thu Aug 23 2001 Havoc Pennington <hp@redhat.com>
- I screwed up the build yesterday, so it didn't actually contain the
  fixes mentioned. This build should contain them.

* Wed Aug 22 2001 Havoc Pennington <hp@redhat.com>
- fix bug causing 32000 stats or so in large directories, 
  should speed things up somewhat
- fix #52104 via gruesome kdesktop-detection hack and setting
  window type hint on our desktop window
- fix so Start Here icon displays in sidebar
- don't load non-local .desktop files

* Mon Aug 20 2001 Havoc Pennington <hp@redhat.com>
- make Programs icon into a link, to match the other .desktop files
- own various directories #51164
- web page titles in Japanese, #51709
- tree defaults to only directories #51850

* Wed Aug 15 2001 Havoc Pennington <hp@redhat.com>
- make start here icon work again
- kill some warning spew, #51661
- cache getpwnam() results to speed things up a bit

* Tue Aug 14 2001 Owen Taylor <otaylor@redhat.com>
- Fix problem with missing desktop starthere.desktop file
- New snapshot from our branch, fixes:
  - On upgrade, icons migrated from GNOME desktop are not properly lined up
    (#51436)
  - icons dropped on the desktop don't end up where dropped. (#51441)
  - Nautilus shouldn't have fam monitor read-only windows. This
    keeps CDROMS from being unmounted until you close all

    nautilus windows pointing to them. (#51442)
  - Warnings about 'cannot statfs...' when moving items to trash.
- Use separate start-here.desktop for panel, since the one used
  for the root window only works from Nautilus.

* Fri Aug 10 2001 Alexander Larsson <alexl@redhat.com>
- Changed starthere .desktop files to be links instead
- of spawning a new nautilus. This makes start-here:
- much faster.

* Thu Aug  9 2001 Alexander Larsson <alexl@redhat.com>
- Added hwbrowser dependency
- New snapshot, fixes the mozilla-view submit form problem

* Wed Aug  8 2001 Jonathan Blandford <jrb@redhat.com>
- Rebuild with new xml-i18n-tools
- fix crash in creating new desktop files

* Tue Aug  7 2001 Jonathan Blandford <jrb@redhat.com>
- Fix up DnD code some more

* Thu Aug 02 2001 Havoc Pennington <hp@redhat.com>
- Sync our CVS version; fixes some MUSTFIX
  (the one about drawing background on startup, 
   properly translate desktop files, etc.)

* Wed Aug  1 2001 Alexander Larsson <alexl@redhat.com> 1.0.4-24
- Fix 64bit cleanness issue
- Fix NULL mimetype crash
- Disable additional_text for .desktop files

* Tue Jul 31 2001 Alexander Larsson <alexl@redhat.com> 1.0.4-23
- Fix unmounting devices.

* Tue Jul 31 2001 Alexander Larsson <alexl@redhat.com> 1.0.4-22
- Make it depend on gnome-vfs-1.0.1-13. Needed for .desktop
- mimetype sniffing.

* Mon Jul 30 2001 Alexander Larsson <alexl@redhat.com> 1.0.4-21
- Remove the "don't run as root" warning.
- Remove eazel from bookmarks
- langified (again? did someone change it?)

* Fri Jul 27 2001 Alexander Larsson <alexl@redhat.com>
- Apply a patch that makes nautilus dnd reset work with the latest
- eel release.

* Thu Jul 26 2001 Alexander Larsson <alexl@redhat.com>
- Build on ia64 without the mozilla component.

* Wed Jul 25 2001 Havoc Pennington <hp@redhat.com>
- Fix crash-on-startup showstopper
- Fix can't-find-images bug (this one was only showing up
  when built with debug symbols, since it was an uninitialized memory
  read)

* Tue Jul 24 2001 Havoc Pennington <hp@redhat.com>
- sync new tarball from our CVS branch, 
  fixes some drag-and-drop, changes URI scheme names,
  etc.

* Tue Jul 24 2001 Owen Taylor <otaylor@redhat.com>
- Add BuildRequires (#49539, 49537)
- Fix %%post, %%postun (#49720)
- Background efficiency improvements and hacks

* Fri Jul 13 2001 Alexander Larsson <alexl@redhat.com>
- Don't launch esd on each mouseover.

* Wed Jul 11 2001 Havoc Pennington <hp@redhat.com>
- move first time druid patch into my "CVS outstanding" patch
- try to really remove Help/Feedback
- try to really fix Help/Community Support
- try again to get Start Here in the Go menu
- try again to get Start Here on the desktop
- don't show file sizes for .desktop files

* Tue Jul 10 2001 Havoc Pennington <hp@redhat.com>
- add newline to ends of .desktop files that were missing them

* Tue Jul 10 2001 Havoc Pennington <hp@redhat.com>
- update to my latest 'cvs diff -u' (adds default 
  Start Here link, displays .directory name in sidebar)
- include /etc/X11/* links (starthere, sysconfig, serverconfig)

* Tue Jul 10 2001 Jonathan Blandford <jrb@redhat.com>
- Patch to remove firsttime druid and flash

* Mon Jul 09 2001 Havoc Pennington <hp@redhat.com>
- add hacks for displaying desktop files
- add hack to turn off the "unwriteable" emblem

* Sun Jul  8 2001 Tim Powers <timp@redhat.com>
- added defattr to the files lists to be (-,root,root)
- languified

* Sat Jul  7 2001 Alexander Larsson <alexl@redhat.com>
- Need to run autoheader too.

* Fri Jul  6 2001 Alexander Larsson <alexl@redhat.com>
- Make the fam dependency a real runtime dependency
- by linking to libfam (nautilus-1.0.4-fam-lib.patch)
- Cleaned up specfile.

* Fri Jul  6 2001 Alexander Larsson <alexl@redhat.com>
- Change default background and rubberband color.
- Use the sidebar tabs from the default theme
- BuildDepend on fam-devel, depend on fam
- Disable the eazel update pages in the first-time druid.
- Remove the eazel logo from the first-time druid

* Thu Jul 05 2001 Havoc Pennington <hp@redhat.com>
- 1.0.4, removes eazel services icon and wizard page
- Eazel logo is still in startup wizard for now, needs fixing

* Tue Jul 03 2001 Havoc Pennington <hp@redhat.com>
- fix group (s/Desktop/Desktops/) #47134
- remove ammonite dependency

* Wed Jun 27 2001 Havoc Pennington <hp@redhat.com>
- add a different default theme
- clean up file list overspecificity a bit

* Tue Jun 26 2001 Havoc Pennington <hp@redhat.com>
- move to a CVS snapshot of nautilus for now
  (Darin is my hero for having distcheck work out of CVS)

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
