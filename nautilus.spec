%define glib2_version 2.0.3
%define pango_version 1.0.99
%define gtk2_version 2.0.5
%define libgnomeui_version 2.0.0
%define eel2_version 2.0.6
%define libxml2_version 2.4.20
%define eog_version 1.0.0
%define gail_version 0.17-2
%define desktop_backgrounds_version 2.0-4
%define desktop_file_utils_version 0.2.90
%define gnome_desktop_version 2.0.5
%define redhat_menus_version 0.25
%define redhat_artwork_version 0.41
%define gnome_vfs2_version 2.0.2-5

Name:		nautilus
Summary:        Nautilus is a file manager for GNOME
Version: 	2.0.6
Release:        5
Copyright: 	GPL
Group:          User Interface/Desktops
Source: 	ftp://ftp.gnome.org/pub/GNOME/pre-gnome2/sources/%{name}-%{version}.tar.bz2

## this is used to mangle the upstream tarball.
Source2:        nautilus-remove-music-view.sh

URL: 		http://www.gnome.org
BuildRoot:	/var/tmp/%{name}-%{version}-root

Requires:	fam
Requires:       filesystem >= 2.1.1-1
Requires:       eog >= %{eog_version}
PreReq:         scrollkeeper >= 0.1.4
Requires:       desktop-backgrounds-basic >= %{desktop_backgrounds_version}
Requires:       redhat-menus >= %{redhat_menus_version}
Requires:       redhat-artwork >= %{redhat_artwork_version}
Requires:       gnome-vfs2 >= %{gnome_vfs2_version}
Requires:       eel2 >= %{eel2_version}

BuildRequires:	glib2-devel >= %{glib2_version}
BuildRequires:	pango-devel >= %{pango_version}
BuildRequires:	gtk2-devel >= %{gtk2_version}
BuildRequires:	libgnomeui-devel >= %{libgnomeui_version}
BuildRequires:	libxml2-devel >= %{libxml2_version}
BuildRequires:  eel2-devel >= %{eel2_version}
BuildRequires:  gail-devel >= %{gail_version}
BuildRequires:  gnome-desktop-devel >= %{gnome_desktop_version}
BuildRequires:  gnome-vfs2-devel >= %{gnome_vfs2_version}
BuildRequires:	fam-devel
BuildRequires:  librsvg2
BuildRequires:  intltool
BuildRequires:  Xft
BuildRequires:  fontconfig
BuildRequires:  desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires:  libtool >= 1.4.2-10

Obsoletes:      nautilus-extras
Obsoletes:      nautilus-suggested
Obsoletes:      nautilus-devel
Provides:       nautilus-devel
Obsoletes:      nautilus-mozilla < 2.0

Patch1:         nautilus-2.0.3-rhconfig.patch
## http://bugzilla.gnome.org/show_bug.cgi?id=91543
Patch4:         nautilus-2.0.5-session-pref.patch
## http://bugzilla.gnome.org/show_bug.cgi?id=91547
Patch5:         nautilus-2.0.5-left-margin.patch
# If the _NAUTILUS_DISABLE_MOUNT_WINDOW selection has an
# owner, don't open new windows.
Patch7:         nautilus-2.0.5-disablemountwindow.patch
Patch8:         nautilus-2.0.6-cdloopback.patch
## should be upstream bugzilla.redhat.com #70667
Patch9:         nautilus-2.0.6-assertions.patch

# this patch is because libc had something wrong with it in 
# an early beta; safe to remove later.
Patch31:        nautilus-1.1.19-starthere-hang-hackaround.patch

Patch42:        nautilus-2.0.6-triple-click.patch
Patch43:        nautilus-2.0.6-dblclickfix.patch

%description
Nautilus integrates access to files, applications, media,
Internet-based resources and the Web. Nautilus delivers a dynamic and
rich user experience. Nautilus is an free software project developed
under the GNU General Public License and is a core component of the
GNOME desktop project.

%prep
%setup -q -n %{name}-%{version}

%patch1 -p1 -b .rhconfig
%patch4 -p1 -b .session-pref
%patch5 -p1 -b .left-margin
%patch7 -p1 -b .disablemountwindow
%patch8 -p0 -b .cdloopback
%patch9 -p1 -b .assertions
%patch31 -p1 -b .starthere-hang-hackaround
%patch42 -p1 -b .triple-click
%patch43 -p1 -b .dblclickfix

if test -f components/music/mpg123.c ; then
        echo "Must run %{SOURCE2} on upstream tarball prior to creating the SRPM"
        exit 1
fi

%build

libtoolize --force --copy
CFLAGS="$RPM_OPT_FLAGS -g" %configure --disable-more-warnings

LANG=en_US make

%install
rm -rf $RPM_BUILD_ROOT

export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
LANG=en_US %makeinstall
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

## these are in desktop-backgrounds-basic
## (uncomment when we patch the source to look in the right place)
## /bin/rm -rf $RPM_BUILD_ROOT%{_datadir}/nautilus/patterns

desktop-file-install --vendor gnome --delete-original       \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications             \
  --add-only-show-in GNOME                                  \
  --add-category X-Red-Hat-Base                             \
  $RPM_BUILD_ROOT%{_datadir}/applications/*

rm -f $RPM_BUILD_ROOT%{_libdir}/bonobo/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

rm -r $RPM_BUILD_ROOT%{_sysconfdir}/X11/starthere
rm -r $RPM_BUILD_ROOT%{_sysconfdir}/X11/serverconfig
rm -r $RPM_BUILD_ROOT%{_sysconfdir}/X11/sysconfig

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
scrollkeeper-update

export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="apps_nautilus_preferences.schemas"
for S in $SCHEMAS; do
  gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S > /dev/null
done

%postun
/sbin/ldconfig
scrollkeeper-update

%files  -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING COPYING-DOCS COPYING.LIB ChangeLog NEWS README

%{_libexecdir}/*
%{_libdir}/*.so.*
%{_libdir}/*.so
%{_libdir}/bonobo/*.so
%{_libdir}/bonobo/servers
%{_datadir}/gnome-2.0
%{_datadir}/nautilus
%{_datadir}/idl
%{_datadir}/pixmaps
%{_datadir}/applications
#%{_datadir}/gnome
#%{_datadir}/omf
%{_bindir}/*
%{_sysconfdir}/gconf/schemas/*
%{_libdir}/pkgconfig/*
%{_includedir}/libnautilus

%changelog
* Mon Sep  2 2002 Havoc Pennington <hp@redhat.com>
- fix #70667 assertion failures
- fix triple click patch

* Mon Sep  2 2002 Jonathan Blandford <jrb@redhat.com>
- don't activate on double click

* Sat Aug 31 2002 Havoc Pennington <hp@redhat.com>
- put button press mask in triple-click patch, maybe it will work
- remove html-hack patch as it does nothing useful

* Sat Aug 31 2002 Havoc Pennington <hp@redhat.com>
- require newer redhat-artwork, -menus, eel2, gnome-vfs2 to avoid
  bogus bug reports
- add hack for HTML mime type handling in a web browser, not 
  nautilus

* Thu Aug 29 2002 Alexander Larsson <alexl@redhat.com>
- Updated to 2.0.6. Removed the patches I put upstream.
- Added patch that fixes #72410

* Wed Aug 28 2002 Owen Taylor <otaylor@redhat.com>
- Add a simple patch so that redhat-config-packages can disable 
  the new window behavior for mounted CDs behavior.

* Wed Aug 28 2002 Alexander Larsson <alexl@redhat.com> 2.0.5-4
- Add patch to fix bug #70667

* Sun Aug 25 2002 Havoc Pennington <hp@redhat.com>
- remove mp3

* Fri Aug 23 2002 Havoc Pennington <hp@redhat.com>
- ignore the "add_to_session" preference as it only broke stuff
- pad the left margin a bit to cope with poor word wrapping

* Fri Aug 23 2002 Alexander Larsson <alexl@redhat.com> 2.0.5-1
- Update to 2.0.5, remove topleft icon patch

* Thu Aug 15 2002 Alexander Larsson <alexl@redhat.com> 2.0.4-2
- Add patch to fix the bug where desktop icons get
  stuck in the top left corner on startup

* Wed Aug 14 2002 Alexander Larsson <alexl@redhat.com> 2.0.4-1
- 2.0.4

* Tue Aug 13 2002 Havoc Pennington <hp@redhat.com>
- obsolete nautilus-mozilla < 2.0 #69839

* Mon Aug 12 2002 Havoc Pennington <hp@redhat.com>
- add rhconfig patch to Bluecurve theme and disable sidebar by default

* Wed Aug  7 2002 Havoc Pennington <hp@redhat.com>
- drop start here files, require redhat-menus that has them

* Tue Aug  6 2002 Havoc Pennington <hp@redhat.com>
- 2.0.3

* Sat Jul 27 2002 Havoc Pennington <hp@redhat.com>
- build for new eel2, gail

* Wed Jul 24 2002 Havoc Pennington <hp@redhat.com>
- and add the libexec components, mumble

* Wed Jul 24 2002 Havoc Pennington <hp@redhat.com>
- put the components in the file list, were moved upstream

* Tue Jul 23 2002 Havoc Pennington <hp@redhat.com>
- 2.0.1

* Thu Jun 27 2002 Owen Taylor <otaylor@redhat.com>
- Relibtoolize to fix relink problems for solib components
- Add LANG=en_US to %makeinstall as well
- Back out previous change, force locale to en_US to prevent UTF-8 problems
- Add workaround for intltool-merge bug on ia64

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 16 2002 Havoc Pennington <hp@redhat.com>
- 2.0.0
- use desktop-file-install
- require desktop-backgrounds-basic

* Wed Jun 12 2002 Havoc Pennington <hp@redhat.com>
- add wacky hack in hopes of fixing the hang-on-login thing

* Sat Jun  8 2002 Havoc Pennington <hp@redhat.com>
- add build requires on new gail
- rebuild to try to lose broken libgailutil.so.13 dependency

* Sat Jun 08 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Wed Jun  5 2002 Havoc Pennington <hp@redhat.com>
- 1.1.19

* Fri May 31 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Thu May 30 2002 Havoc Pennington <hp@redhat.com>
- really remove nautilus-devel if we are going to obsolete it
- don't require hwbrowser

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May 21 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Tue May 21 2002 Havoc Pennington <hp@redhat.com>
- 1.1.17

* Fri May  3 2002 Havoc Pennington <hp@redhat.com>
- 1.1.14

* Thu Apr 25 2002 Havoc Pennington <hp@redhat.com>
- require eog
- obsolete nautilus-devel
- fix name of schemas file in post

* Mon Apr 22 2002 Alex Larsson <alexl@redhat.com>
- Update to 1.1.13

* Fri Apr 19 2002 Havoc Pennington <hp@redhat.com>
- put tree view in file list

* Thu Apr 18 2002 Havoc Pennington <hp@redhat.com>
- nautilus for gnome 2
- clean up the spec file and file list a bit

* Mon Apr 15 2002 Havoc Pennington <hp@redhat.com>
- merge translations

* Thu Apr  4 2002 Alex Larsson <alexl@redhat.com>
- Add patch to fix trash crash

* Mon Apr  1 2002 Havoc Pennington <hp@redhat.com>
- fix for metadata tmp race
- backport thumbnail speed fix and thumbnail inf. loop fix

* Mon Mar 25 2002 Havoc Pennington <hp@redhat.com>
- add some fixes from CVS version, including one for #61819 and a couple segfaults

* Wed Mar 20 2002 Havoc Pennington <hp@redhat.com>
- fix thumbnails for files with future timestamp, #56862

* Mon Mar 11 2002 Havoc Pennington <hp@redhat.com>
- buildrequires intltool #60633
- apply Alex's pixbuf cache patch to save a few megs #60581

* Wed Feb 27 2002 Havoc Pennington <hp@redhat.com>
- drop Milan-specific features, including png10 and ac25 patches
- copy in 1.0.5 help component to avoid large risky patch
- remove .la files
- drop mozilla from ia64 again
- remove oaf file from nautilus-mozilla that was also in the base 
  package

* Mon Jan 28 2002 Bill Nottingham <notting@redhat.com>
- enable mozilla support on ia64

* Fri Dec 28 2001 Christopher Blizzard <blizzard@redhat.com>
- require Mozilla 0.9.7
- Add patch that puts mozilla profile startup before embedding is initialized

* Tue Nov 20 2001 Havoc Pennington <hp@redhat.com>
- 1.0.6, require Mozilla 0.9.6

* Tue Oct 23 2001 Alex Larsson <alexl@redhat.com>
- Update to 1.0.5

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
