%define glib2_version 2.6.0
%define pango_version 1.1.3
%define gtk2_version 2.6.0
%define libgnomeui_version 2.6.0
%define eel2_version 2.15.91
%define gnome_icon_theme_version 1.1.5
%define libxml2_version 2.4.20
%define gail_version 0.17-2
%define desktop_backgrounds_version 2.0-4
%define desktop_file_utils_version 0.7
%define gnome_desktop_version 2.9.91
%define redhat_menus_version 0.25
%define redhat_artwork_version 0.41
%define gnome_vfs2_version 2.14.2
%define startup_notification_version 0.5
%define libexif_version 0.5.12
%define gconf_version 2.14

Name:		nautilus
Summary:        Nautilus is a file manager for GNOME
Version: 	2.17.90
Release:	4%{?dist}
License: 	GPL
Group:          User Interface/Desktops
Source: 	ftp://ftp.gnome.org/pub/GNOME/sources/2.7/%{name}/%{name}-%{version}.tar.bz2

URL: 		http://www.gnome.org/projects/nautilus/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)	
Requires:	gamin
Requires:       filesystem >= 2.1.1-1
Requires:       desktop-backgrounds-basic >= %{desktop_backgrounds_version}
Requires:       redhat-menus >= %{redhat_menus_version}
Requires:       redhat-artwork >= %{redhat_artwork_version}
Requires:       gnome-vfs2 >= %{gnome_vfs2_version}
Requires:       gnome-vfs2-smb
Requires:       eel2 >= %{eel2_version}
Requires:       gnome-icon-theme >= %{gnome_icon_theme_version}
Requires:       libexif >= %{libexif_version}
%ifnarch s390 s390x
Requires: 	eject
%endif
PreReq:    scrollkeeper >= 0.1.4

BuildRequires:	glib2-devel >= %{glib2_version}
BuildRequires:	pango-devel >= %{pango_version}
BuildRequires:	gtk2-devel >= %{gtk2_version}
BuildRequires:	libgnomeui-devel >= %{libgnomeui_version}
BuildRequires:	libxml2-devel >= %{libxml2_version}
BuildRequires:  eel2-devel >= %{eel2_version}
BuildRequires:  gail-devel >= %{gail_version}
BuildRequires:  gnome-desktop-devel >= %{gnome_desktop_version}
BuildRequires:  gnome-vfs2-devel >= %{gnome_vfs2_version}
BuildRequires:	gamin-devel
BuildRequires:  librsvg2
BuildRequires:  intltool
BuildRequires:  libX11-devel
BuildRequires:  libXt-devel
BuildRequires:  fontconfig
BuildRequires:  desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires:  libtool >= 1.4.2-10
BuildRequires:  startup-notification-devel >= %{startup_notification_version}
BuildRequires:  libexif-devel >= %{libexif_version}
BuildRequires:  gettext
# For intltool:
BuildRequires: perl-XML-Parser >= 2.31-16

Requires(pre): GConf2 >= %{gconf_version}
Requires(preun): GConf2 >= %{gconf_version}
Requires(post): GConf2 >= %{gconf_version}

Obsoletes:      nautilus-extras
Obsoletes:      nautilus-suggested
Obsoletes:      nautilus-mozilla < 2.0
Obsoletes:      nautilus-media

# Some changes to default config
Patch1:         nautilus-2.5.7-rhconfig.patch
Patch2:         nautilus-2.15.2-format.patch
Patch3:		background-no-delay.patch
Patch5:		nautilus-2.17.90-selinux.patch
Patch6:         nautilus-2.16.2-dynamic-search.patch

%description
Nautilus integrates access to files, applications, media,
Internet-based resources and the Web. Nautilus delivers a dynamic and
rich user experience. Nautilus is an free software project developed
under the GNU General Public License and is a core component of the
GNOME desktop project.

%package extensions
Summary: Nautilus extensions library
Group: Development/Libraries

%description extensions
This package provides the libraries used by nautilus extensions.

%package devel
Summary: Libraries and include files for developing nautilus extensions
Group: Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   pkgconfig

%description devel
This package provides the necessary development libraries and headers
for writing nautilus extensions.

%prep
%setup -q -n %{name}-%{version}

%patch1 -p1 -b .rhconfig
#%patch2 -p1 -b .format
%patch3 -p1 -b .no-delay
%patch5 -p1 -b .selinux
%patch6 -p1 -b .dynamic-search

%build

libtoolize --force --copy
CFLAGS="$RPM_OPT_FLAGS -g -DUGLY_HACK_TO_DETECT_KDE -DNAUTILUS_OMIT_SELF_CHECK" %configure --disable-more-warnings --disable-update-mimedb

export tagname=CC
LANG=en_US make LIBTOOL=/usr/bin/libtool %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
export tagname=CC
LANG=en_US %makeinstall LIBTOOL=/usr/bin/libtool
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

## these are in desktop-backgrounds-basic
## (uncomment when we patch the source to look in the right place)
## /bin/rm -rf $RPM_BUILD_ROOT%{_datadir}/nautilus/patterns

# make sure desktop files validate by ignoring sr@Latn
perl -pi -e 's/sr\@Latn/sp/g' $RPM_BUILD_ROOT%{_datadir}/applications/*.desktop

desktop-file-install --vendor gnome --delete-original       \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications             \
  --add-only-show-in GNOME                                  \
  --add-category X-Red-Hat-Base                             \
  $RPM_BUILD_ROOT%{_datadir}/applications/*

desktop-file-install --vendor gnome --delete-original       \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications             \
  --add-category DesktopSettings                            \
  $RPM_BUILD_ROOT%{_datadir}/applications/nautilus-file-management-properties.desktop

rm -f $RPM_BUILD_ROOT%{_libdir}/bonobo/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

rm -f $RPM_BUILD_ROOT%{_libdir}/bonobo/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/icon-theme.cache

mkdir -p $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-1.0

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
scrollkeeper-update
%{_bindir}/update-mime-database %{_datadir}/mime &> /dev/null

export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/apps_nautilus_preferences.schemas > /dev/null || :

%pre
if [ "$1" -gt 1 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/apps_nautilus_preferences.schemas > /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/apps_nautilus_preferences.schemas > /dev/null || :
fi

%postun
/sbin/ldconfig
scrollkeeper-update

%files  -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING COPYING-DOCS COPYING.LIB ChangeLog NEWS README

%{_libdir}/nautilus
%{_libdir}/bonobo/servers
%{_datadir}/nautilus
%{_datadir}/pixmaps
%{_datadir}/applications
%{_datadir}/mime/packages/nautilus.xml
#%{_datadir}/gnome
#%{_datadir}/omf
%{_bindir}/*
%{_sysconfdir}/gconf/schemas/*
%{_datadir}/icons/hicolor/*/apps/nautilus.png
%{_datadir}/icons/hicolor/scalable/apps/nautilus.svg

%files extensions
%defattr(-, root, root)
%{_libdir}/libnautilus-extension.so.*

%files devel
%defattr(-, root, root)
%{_includedir}/nautilus
%{_libdir}/pkgconfig/*
%{_libdir}/*.so

%changelog
* Wed Feb  7 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.90-4
- Add DesktopSettings category to nautilus-file-management-properties.desktop

* Tue Feb  6 2007 Alexander Larsson <alexl@redhat.com> - 2.17.90-3
- update tracker dynamic search patch to new .so name

* Tue Jan 23 2007 Alexander Larsson <alexl@redhat.com> - 2.17.90-2
- Fix gnome bug #362302 in selinux patch

* Mon Jan 22 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.90-1
- Update to 2.17.90

* Tue Dec 19 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.1-1
- Update to 2.17.1

* Wed Nov 22 2006 Alexander Larsson <alexl@redhat.com> - 2.16.2-7
- Look for beagle before tracker, because tracker autostarts
  This lets us support having both installed at the same time.
- Remove buildreqs for beagle, as they are not necessary with
  the dynamic work.

* Tue Nov 14 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.2-6
- Detect tracker dynamically, too

* Mon Nov 13 2006 Alexander Larsson <alexl@redhat.com> - 2.16.2-5.fc7
- Fix commonly reported NautilusDirectory crash

* Wed Nov  8 2006 Alexander Larsson <alexl@redhat.com> - 2.16.2-4.fc7
- Revert upstream icon placement patch as it seems broken

* Tue Nov  7 2006 Alexander Larsson <alexl@redhat.com> - 2.16.2-2.fc7
- Update to 2.16.2

* Sat Oct 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.1-1 
- Update to 2.16.1

* Wed Oct 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-6
- Fix scripts according to the packaging guidelines
- Require GConf2 for the scripts
- Require pkgconfig for the -devel package

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 2.16.0-5
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 19 2006 Alexander Larsson <alexl@redhat.com> - 2.16.0-4
- Support changing selinux contexts (#204030)

* Thu Sep 14 2006 Alexander Larsson <alexl@redhat.com> - 2.16.0-3
- Fix crash when opening custom icon dialog (#205352)

* Tue Sep  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-2
- Add a %%preun script (#205260)

* Mon Sep  4 2006 Alexander Larsson <alexl@redhat.com> - 2.16.0-1
- Update to 2.16.0

* Fri Aug 25 2006 Alexander Larsson <alexl@redhat.com> - 2.15.92.1-2
- Omit self check code in build

* Tue Aug 22 2006 Alexander Larsson <alexl@redhat.com> - 2.15.92.1-1
- update to 2.15.92.1

* Mon Aug 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.92-1.fc6
- Update to 2.15.92

* Sat Aug 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.91-2.fc6
- Don't Provide/Obsolete nautilus-devel from the main package (#202322)

* Thu Aug 10 2006 Alexander Larsson <alexl@redhat.com> - 2.15.91-1.fc6
- Update to 2.15.91
- Split package into devel and extensions (#201967)

* Thu Aug  3 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.90-1.fc6
- Update to 2.15.90

* Tue Jul 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.4-3
- Spec file cleanups

* Wed Jul 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.4-2
- Don't require nautilus-cd-burner, to avoid a 
  BuildRequires-Requires loop

* Wed Jul 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.4-1
- Update to 2.15.4

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.15.2-1.1
- rebuild

* Tue Jun 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.2-1
- Update to 2.15.1

* Sun May 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.1-2
- Add missing BuildRequires (#129184)

* Wed May 17 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.1-1
- Update to 2.15.1

* Fri May 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.1-3
- Close the about dialog

* Tue Apr 11 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.1-2
- Update to 2.14.1

* Mon Mar 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.0-1
- Update to 2.14.0

* Mon Mar  6 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.92-2
- Reinstate the format patch which was accidentally dropped

* Mon Feb 27 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.92-1
- Update to 2.13.92

* Mon Feb 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.91-1
- Update to 2.13.91

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.13.90-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.13.90-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Feb  6 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.90-2
- Avoid delays in rendering the background

* Tue Jan 31 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.90-1
- Update to 2.13.90

* Tue Jan 17 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.4-1
- Update to 2.13.4

* Mon Jan  9 2006 Alexander Larsson <alexl@redhat.com> - 2.13.3-2
- Buildrequire libbeagle

* Tue Dec 13 2005 Alexander Larsson <alexl@redhat.com> 2.13.3-1
- Update to 2.13.3

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Dec  2 2005 Matthias Clasen <mclasen@redhat.com> 2.13.2-1
- Update to 2.13.2
- Update patches

* Tue Nov  1 2005 Alexander Larsson <alexl@redhat.com> - 2.12.1-6
- Switch XFree86-devel buildrequirement to libX11-devel

* Sat Oct 28 2005 Matthias Clasen <mclasen@redhat.com> 2.12.1-5
- Implement icon stretching keynav
- Support formatting non-floppy devices

* Sat Oct 22 2005 Matthias Clasen <mclasen@redhat.com> 2.12.1-4
- Improve icon stretching ui

* Fri Oct 21 2005 Matthias Clasen <mclasen@redhat.com> 2.12.1-3
- Only show the "Format menu item if gfloppy is present

* Fri Oct 21 2005 Matthias Clasen <mclasen@redhat.com> 2.12.1-2
- Add a "Format" context menu item to the floppy in "Computer"

* Thu Oct  6 2005 Matthias Clasen <mclasen@redhat.com> 2.12.1-1
- Update to 2.12.1

* Wed Sep  7 2005 Matthias Clasen <mclasen@redhat.com> 2.12.0-1
- Update to 2.12.0

* Tue Aug 16 2005 Matthias Clasen <mclasen@redhat.com> 
- New upstream release

* Wed Aug  3 2005 Matthias Clasen <mclasen@redhat.com> 2.11.90-1
- New upstream release

* Mon Jul 11 2005 Matthias Clasen <mclasen@redhat.com> 2.11.3-1
- Update to 2.11.3

* Wed May 11 2005 David Zeuthen <davidz@redhat.com> 2.10.0-4
- Fix default font for zh_TW (#154185)

* Sun Apr  3 2005 David Zeuthen <davidz@redhat.com> 2.10.0-3
- Include patches for desktop background memory saving (GNOME bug #169347)
- Obsoletes: nautilus-media (#153223)

* Mon Mar 28 2005 Matthias Clasen <mclasen@redhat.com> 2.10.0-2
- Rebuild against newer libexif

* Mon Mar 21 2005 David Zeuthen <davidz@redhat.com> 2.10.0-1
- Update to latest upstream version; tweak requires

* Thu Mar  3 2005 Alex Larsson <alexl@redhat.com> 2.9.91-2
- Rebuild

* Fri Feb 11 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.91-1
- Update to 2.9.91

* Tue Nov  9 2004 Marco Pesenti Gritti <mpg@redhat.com> - 2.8.1-5
- Remove eog dependency. The bonobo component is no more used.

* Mon Oct 18 2004 Marco Pesenti Gritti <mpg@redhat.com> - 2.8.1-4
- #135824 Fix throbber position

* Fri Oct 15 2004 Alexander Larsson <alexl@redhat.com> - 2.8.1-3
- Slightly less bad error dialog when there is no handler for a file.
  Not ideal, but this change doesn't change any strings.

* Tue Oct 12 2004 Alexander Larsson <alexl@redhat.com> - 2.8.1-2
- Fix open with menu on mime mismatch
- Create desktop links ending with .desktop (#125104)
- Remove old cruft from specfile

* Mon Oct 11 2004 Alexander Larsson <alexl@redhat.com> - 2.8.1-1
- update to 2.8.1

* Fri Oct  8 2004 Alexander Larsson <alexl@redhat.com> - 2.8.0-3
- Backport more fixes from cvs

* Mon Oct  4 2004 Alexander Larsson <alexl@redhat.com> - 2.8.0-2
- Backport various bugfixes from HEAD

* Mon Sep 13 2004 Alexander Larsson <alexl@redhat.com> - 2.8.0-1
- Update to 2.8.0

* Fri Sep 10 2004 Alexander Larsson <alexl@redhat.com> - 2.7.92-3
- Don't require eject on s390(x), since there is none (#132228)

* Tue Sep  7 2004 Alexander Larsson <alexl@redhat.com> - 2.7.92-2
- Add patch to fix desktop keynav (#131894)

* Tue Aug 31 2004 Alex Larsson <alexl@redhat.com> 2.7.92-1
- update to 2.7.92

* Thu Aug 26 2004 Alexander Larsson <alexl@redhat.com> - 2.7.4-3
- Added requires eject
- Depend on gnome-vfs2-smb instead of -extras

* Tue Aug 24 2004 Alexander Larsson <alexl@redhat.com> - 2.7.4-2
- backport cvs fixes, including default view fix

* Thu Aug 19 2004 Alex Larsson <alexl@redhat.com> 2.7.4-1
- update to 2.7.4

* Fri Aug  6 2004 Ray Strode <rstrode@redhat.com> 2.7.2-1
- update to 2.7.2

* Tue Aug 3 2004 Matthias Clasen <mclasen@redhat.com> 2.6.0-7
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri May 21 2004 Matthias Clasen <mclasen@redhat.com> 2.6.0-5
- rebuild

* Wed Apr 14 2004 Alexander Larsson <alexl@redhat.com> 2.6.0-4
- update cvs backport, now handles kde trash dir better

* Wed Apr 14 2004 Alexander Larsson <alexl@redhat.com> 2.6.0-3
- add cvs backport

* Wed Apr  7 2004 Alex Larsson <alexl@redhat.com> 2.6.0-2
- Make network servers go to network:// again

* Thu Apr  1 2004 Alex Larsson <alexl@redhat.com> 2.6.0-1
- update to 2.6.0

* Tue Mar 16 2004 Mike A. Harrisn <mharris@redhat.com> 2.5.91-2
- Changed BuildRequires: XFree86-libs >= 4.2.99 to BuildRequires: XFree86-devel
- Fixed BuildRoot to use _tmppath instead of /var/tmp

* Mon Mar 15 2004 Alex Larsson <alexl@redhat.com> 2.5.91-1
- update to 2.5.91

* Mon Mar  8 2004 Alexander Larsson <alexl@redhat.com> 2.5.90-1
- update to 2.5.90

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 25 2004 Alexander Larsson <alexl@redhat.com>
- update libgnomeui required version to 2.5.3 (#116229)

* Tue Feb 24 2004 Alexander Larsson <alexl@redhat.com> 2.5.8-1
- update to 2.5.8

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Alexander Larsson <alexl@redhat.com> 2.5.7-1
- update to 2.5.7

* Fri Jan 30 2004 Alexander Larsson <alexl@redhat.com> 2.5.6-1
- update to 2.5.6

* Tue Jan 27 2004 Alexander Larsson <alexl@redhat.com> 2.5.5-1
- update to 2.5.5

* Tue Oct 28 2003 Than Ngo <than@redhat.com> 2.4.0-7
- fix start-here desktop file

* Mon Oct 27 2003 Than Ngo <than@redhat.com> 2.4.0-6
- rebuild against new librsvg2

* Fri Oct  3 2003 Alexander Larsson <alexl@redhat.com> 2.4.0-5
- Update cvs backport, now have the better desktop icon layout

* Mon Sep 29 2003 Alexander Larsson <alexl@redhat.com> 2.4.0-4
- Update cvs backport, fixes #105869

* Fri Sep 19 2003 Alexander Larsson <alexl@redhat.com> 2.4.0-3
- Backport bugfixes from the gnome-2-4 branch

* Tue Sep 16 2003 Alexander Larsson <alexl@redhat.com> 2.4.0-2
- Add patch that fixes crash when deleting in listview

* Tue Sep  9 2003 Alexander Larsson <alexl@redhat.com> 2.4.0-1
- 2.4.0

* Thu Sep  4 2003 Alexander Larsson <alexl@redhat.com> 2.3.90-2
- Add desktop icons patch

* Tue Sep  2 2003 Alexander Larsson <alexl@redhat.com> 2.3.90-1
- update to 2.3.90

* Tue Aug 26 2003 Alexander Larsson <alexl@redhat.com> 2.3.9-1
- update
- Add patch to ignore kde desktop links
- Re-enable kdesktop detection hack.
  kde doesn't seem to support the manager selection yet

* Wed Aug 20 2003 Alexander Larsson <alexl@redhat.com> 2.3.8-2
- don't require fontilus

* Mon Aug 18 2003 Alexander Larsson <alexl@redhat.com> 2.3.8-1
- update to gnome 2.3

* Wed Aug  6 2003 Elliot Lee <sopwith@redhat.com> 2.2.4-5
- Fix libtool

* Tue Jul  8 2003 Alexander Larsson <alexl@redhat.com> 2.2.4-4.E
- Rebuild

* Tue Jul  8 2003 Alexander Larsson <alexl@redhat.com> 2.2.4-4
- Backport fixes from cvs
- Change some default configurations

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 27 2003 Alexander Larsson <alexl@redhat.com> 2.2.4-2
- Add performance increase backport
- Add desktop manager selection backport

* Mon May 19 2003 Alexander Larsson <alexl@redhat.com> 2.2.4-1
- update to 2.2.4

* Tue May  6 2003 Alexander Larsson <alexl@redhat.com> 2.2.3-2
- Fix scrollkeeper pre-requires

* Mon Mar 31 2003 Alexander Larsson <alexl@redhat.com> 2.2.3-1
- Update to 2.2.3

* Tue Feb 25 2003 Alexander Larsson <alexl@redhat.com> 2.2.1-5
- Change the default new window size to fit in 800x600 (#85037)

* Thu Feb 20 2003 Alexander Larsson <alexl@redhat.com>
- Require gnome-vfs2-extras, since network menu item uses it (#84145)

* Tue Feb 18 2003 Alexander Larsson <alexl@redhat.com>
- Update to the latest bugfixes from cvs.
- Fixes #84291 for nautilus, context menu duplication and some other small bugs.

* Thu Feb 13 2003 Alexander Larsson <alexl@redhat.com> 2.2.1-2
- Add a patch to fix the forkbomb-under-kde bug (#81520)
- Add a patch to fix thumbnail memory leak
- require libXft.so.2 instead of Xft, since that changed in the XFree86 package

* Tue Feb 11 2003 Alexander Larsson <alexl@redhat.com> 2.2.1-1
- 2.2.1, lots of bugfixes

* Fri Jan 31 2003 Alexander Larsson <alexl@redhat.com> 2.2.0.2-2
- remove nautilus-server-connect since it broke without editable vfolders

* Fri Jan 31 2003 Alexander Larsson <alexl@redhat.com> 2.2.0.2-1
- Update to 2.2.0.2, fixes bg crasher
- parallelize build
- Added patch from cvs that fixes password hang w/ smb

* Thu Jan 23 2003 Alexander Larsson <alexl@redhat.com> 2.2.0.1-1
- Update to 2.2.0.1

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 2.2.0-2
- rebuilt

* Tue Jan 21 2003 Alexander Larsson <alexl@redhat.com> 2.2.0-1
- update to 2.2.0

* Fri Jan 17 2003 Alexander Larsson <alexl@redhat.com> 2.1.91-8
- Add requirement on fontilus and nautilus-cd-burner to get them
  on an upgrade.

* Fri Jan 17 2003 Alexander Larsson <alexl@redhat.com> 2.1.91-7
- Added patch to enable the look for kde desktop hack
- Removed patches that were fixed upstream

* Fri Jan 17 2003 Alexander Larsson <alexl@redhat.com> 2.1.91-6
- Removed the requirement of nautilus-cd-burner, since
  that is now on by default in comps

* Thu Jan 16 2003 Alexander Larsson <alexl@redhat.com> 2.1.91-5
- Require(post,postun) scrollkeeper (#67340)
- Add dot to end of summary

* Tue Jan 14 2003 Havoc Pennington <hp@redhat.com> 2.1.91-4
- use system-group.png not network-server.png for "Network Servers"

* Tue Jan 14 2003 Alexander Larsson <alexl@redhat.com> 2.1.91-3
- Correct filename in last change

* Tue Jan 14 2003 Alexander Larsson <alexl@redhat.com> 2.1.91-2
- change the network menu item to go to smb:

* Tue Jan 14 2003 Alexander Larsson <alexl@redhat.com> 2.1.91-1
- Update to 2.1.91
- Updated URL

* Tue Jan 14 2003 Havoc Pennington <hp@redhat.com>
- perl-munge the icon names in a couple desktop files
  to find redhat-network-server.png and redhat-file-manager.png.
  Upstream icon names here were weird and seem broken. 

* Thu Jan  9 2003 Alexander Larsson <alexl@redhat.com>
- 2.1.6
- Removed mp3 stripping script. Thats gone upstream now.

* Wed Dec 18 2002 Alexander Larsson <alexl@redhat.com> 2.1.5-2
- Add cdburn patch.
- Remove nautilus-1.1.19-starthere-hang-hackaround.patch
- Require nautilus-cd-burner

* Mon Dec 16 2002 Alexander Larsson <alexl@redhat.com> 2.1.5-1
- Update to 2.1.5. Require gnome-icon-theme >= 0.1.5, gnome-vfs >= 2.1.5

* Tue Dec  3 2002 Havoc Pennington <hp@redhat.com>
- add explicit startup-notification dependency because build system is
  dumb 
- 2.1.3

* Wed Nov 13 2002 Havoc Pennington <hp@redhat.com>
- 2.1.2

* Thu Oct 10 2002 Havoc Pennington <hp@redhat.com>
- 2.0.7
- remove patches that are upstream

* Tue Sep  3 2002 Alexander Larsson <alexl@redhat.com>  2.0.6-6
- Add badhack to make weblinks on desktop work

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
- Add LANG=en_US to %%makeinstall as well
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
- Moved %%description sections closer to their %package sections
- Moved %%changelog to the end, where so that it's not in the way
- Changed configure and make install options to allow moving of
  libraries, includes, binaries more easily
- Removed hard-coded paths (don't define %%prefix or %%docdir)
- replace %%{prefix}/bin with %%{_bindir}
- replace %%{prefix}/share with %%{_datadir}
- replace %%{prefix}/lib with %%{_libdir}
- replace %%{prefix}/include with %%{_includedir}

* Tue Oct 10 2000 Robin Slomkowski <rslomkow@eazel.com>
- removed obsoletes from sub packages and added mozilla and trilobite
subpackages

* Wed Apr 26 2000 Ramiro Estrugo <ramiro@eazel.com>
- created this thing
