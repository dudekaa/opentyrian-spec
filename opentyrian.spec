%global insidedir opentyrian-2.1.20221123
%global tyriandir /usr/share/games/opentyrian/data
%global debug_package %{nil}

Name:    opentyrian
Epoch:   1
Version: 2.1
Release: 18.20221123g50ba362%{?dist}
Summary: This is a port of the DOS shoot-em-up Tyrian.

Group:   Games
License: GPLv2
URL:     https://github.com/opentyrian/opentyrian
Source:  https://github.com/opentyrian/opentyrian/archive/refs/tags/v2.1.20221123.tar.gz
Source1: http://camanis.net/tyrian/tyrian21.zip
Patch0:  opentyrian-lowerscript.patch

BuildRequires: gcc
BuildRequires: SDL2-devel
BuildRequires: SDL2_net-devel
BuildRequires: desktop-file-utils
Requires: SDL2
Requires: SDL2_net
Requires: %{name}-data

%description
OpenTyrian is a port of the DOS shoot-em-up Tyrian.

Jason Emery generously gave the OpenTyrian developers a copy of the Tyrian 2.1
source code, which has since been ported from Turbo Pascal to C.The port uses
SDL, making it easily cross-platform.

Tyrian is an arcade-style vertical scrolling shooter.
The story is set in 20,031 where you play as Trent Hawkins,
a skilled fighter-pilot employed to fight Microsol and save the galaxy.

%package data
Summary: Data files for %{name}
BuildArch: noarch

%description data
Common data files for %{name} package.


%prep
%setup -n %{insidedir} -q
%setup -q -n %{insidedir} -a 1 -T -D
%patch -P 0

# run lower-script.sh
echo y|%_builddir/%{insidedir}/lower-script.sh %_builddir/%{insidedir}/tyrian21

# prune tyrian21.zip
%{__rm} -f %_builddir/%{insidedir}/tyrian21/*\.exe
%{__rm} -f %_builddir/%{insidedir}/tyrian21/*\.doc
%{__rm} -f %_builddir/%{insidedir}/tyrian21/setup\.*


%build
#configure
make %{?_smp_mflags} TYRIAN_DIR=%{tyriandir}


%install
rm -rf $RPM_BUILD_ROOT
make install prefix=/usr DESTDIR=$RPM_BUILD_ROOT

%{__mkdir} -p $RPM_BUILD_ROOT/%{tyriandir}

find %_builddir/%{insidedir}/tyrian21/ -type f -exec %{__install} -m 0644 {} $RPM_BUILD_ROOT/%{tyriandir}/ \;
%{__install} -m 0755 %_builddir/%{insidedir}/lower-script.sh $RPM_BUILD_ROOT/%{tyriandir}/

# menu item
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/locolor/22x22/apps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/22x22/apps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/24x24/apps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/locolor/48x48/apps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/128x128/apps
install -p %_builddir/%{insidedir}/linux/%{name}.desktop $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop
install -p %_builddir/%{insidedir}/linux/icons/tyrian-22.png $RPM_BUILD_ROOT%{_datadir}/icons/locolor/22x22/apps/%{name}.png
install -p %_builddir/%{insidedir}/linux/icons/tyrian-22.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/22x22/apps/%{name}.png
install -p %_builddir/%{insidedir}/linux/icons/tyrian-24.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
install -p %_builddir/%{insidedir}/linux/icons/tyrian-32.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
install -p %_builddir/%{insidedir}/linux/icons/tyrian-48.png $RPM_BUILD_ROOT%{_datadir}/icons/locolor/48x48/apps/%{name}.png
install -p %_builddir/%{insidedir}/linux/icons/tyrian-48.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
install -p %_builddir/%{insidedir}/linux/icons/tyrian-128.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop


# %check
# make test


%files
%license COPYING
%doc NEWS
%doc README
/usr/bin/%{name}
%doc %{_mandir}/man6/%{name}.6.gz
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/locolor/22x22/apps/%{name}.png
%{_datadir}/icons/hicolor/22x22/apps/%{name}.png
%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/locolor/48x48/apps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png


%files data
%{tyriandir}


%changelog
* Sun Aug 03 2025 Arnošt Dudek <arnost@arnostdudek.cz> - 2.1-18.20221123g50ba362
- Rebuild

* Sun Nov 19 2023 Arnošt Dudek <arnost@arnostdudek.cz> - 2.1-17.20221123g50ba362
- Split to app / data packages

* Sun Nov 19 2023 Arnošt Dudek <arnost@arnostdudek.cz> - 2.1-16.20221123g50ba362
- Fix package build for Fedora 39+

* Sat May 20 2023 Arnost Dudek <arnost@arnostdudek.cz> - 2.1-15.20221123g50ba362
- rebuild from github.com sources

* Sun Dec 11 2022 Arnost Dudek <arnost@arnostdudek.cz> - 2.1-14.20221123g50ba362
- git rev v2.1.201123
- Volume control is now on a logarithmic scale
- Fixed music fade (ex. when starting a level)
- Reworked audio mixing to reduce clipping
- Fixed some graphical glitches
- Mouse pointer is no longer locked to the window except during gameplay
- Upgraded from SDL to SDL2
- Redesigned OpenTyrian menu
- Reworked mouse behavior in menus so that pointer is now visible
- Replaced JSON configuration file format with custom configuration file format

* Wed Jan 5 2022 Arnost Dudek <arnost@arnostdudek.cz> - 2.1-13.20220105gd4f5aff
- git rev d4f5aff
- upstream project now using SDL2

* Sat May 2 2020 Arnost Dudek <arnost@arnostdudek.cz> - 2.1-12.20190323hg6b46ca6fa8f7
- fixes builds for F32+

* Fri May 1 2020 Arnost Dudek <arnost@arnostdudek.cz> - 2.1-11.20190323hg6b46ca6fa8f7
- git rev 6b46ca6fa8f7

* Wed Dec 26 2018 Arnost Dudek <arnost@arnostdudek.cz> - 2.1-10.20180925hg6edd3686f939
- fixed builds for F29+

* Wed Dec 26 2018 Arnost Dudek <arnost@arnostdudek.cz> - 2.1-9.20180925hg6edd3686f939
- git rev 6edd3686f939
- disabled debug build

* Sat Dec 24 2016 Arnost Dudek <arnost@arnostdudek.cz> - 2.1-8.20150528hg6edd3686f939
- updated sources

* Sat Mar 19 2016 Arnost Dudek <arnost@arnostdudek.cz> - 2.1.20130907-7
- rewrite for loop to find -exec, now building on COPR

* Fri Mar 18 2016 Arnost Dudek <arnost@arnostdudek.cz> - 2.1.20130907-6
- move icons to apps folder, readded lower-script

* Fri Mar 18 2016 Arnost Dudek <arnost@arnostdudek.cz> - 2.1.20130907-5
- more icons

* Fri Mar 18 2016 Arnost Dudek <arnost@arnostdudek.cz> - 2.1.20130907-4
- rebuild due to another build fail
- added CREDITS

* Thu Mar 17 2016 Arnost Dudek <arnost@arnostdudek.cz> - 2.1.20130907-3
- missed menu shortcut

* Thu Mar 17 2016 Arnost Dudek <arnost@arnostdudek.cz> - 2.1.20130907-2
- fixed TYRIAN_DIR path

* Wed Mar 16 2016 Arnost Dudek <arnost@arnostdudek.cz> - 2.1.20130907-1
- git rev 98afb31c7343
