%global insidedir opentyrian-d4f5aff9144de4bb23ebc1c391e7fcf8085a27f1
%global tyriandir /usr/share/games/opentyrian/data
%global debug_package %{nil}

Name: opentyrian
Epoch: 1
Version: 2.1
Release: 13.20220105gd4f5aff%{?dist}
Summary: OpenTyrian is a port of the DOS shoot-em-up Tyrian.

Group: Games
License: GPLv2
URL: https://bitbucket.org/opentyrian/opentyrian
# Fetched from https://codeload.github.com/opentyrian/opentyrian/zip/d4f5aff9144de4bb23ebc1c391e7fcf8085a27f1
Source: opentyrian-d4f5aff9144de4bb23ebc1c391e7fcf8085a27f1.zip
# Fetched from http://camanis.net/tyrian/tyrian21.zip
Source1: tyrian21.zip
Patch: opentyrian-lowerscript.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: gcc
BuildRequires: SDL2-devel
BuildRequires: SDL2_net-devel
Requires: SDL2
Requires: SDL2_net

%description
OpenTyrian is a port of the DOS shoot-em-up Tyrian.

Jason Emery generously gave the OpenTyrian developers a copy of the Tyrian 2.1
source code, which has since been ported from Turbo Pascal to C.The port uses
SDL, making it easily cross-platform.

Tyrian is an arcade-style vertical scrolling shooter.
The story is set in 20,031 where you play as Trent Hawkins,
a skilled fighter-pilot employed to fight Microsol and save the galaxy.

%prep
%setup -n %{insidedir} -q
%setup -q -n %{insidedir} -a 1 -T -D
%patch

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
%{__mkdir} -p $RPM_BUILD_ROOT/usr/share/applications
%{__mkdir} -p $RPM_BUILD_ROOT/usr/share/icons/locolor/22x22/apps
%{__mkdir} -p $RPM_BUILD_ROOT/usr/share/icons/hicolor/22x22/apps
%{__mkdir} -p $RPM_BUILD_ROOT/usr/share/icons/hicolor/24x24/apps
%{__mkdir} -p $RPM_BUILD_ROOT/usr/share/icons/hicolor/32x32/apps
%{__mkdir} -p $RPM_BUILD_ROOT/usr/share/icons/locolor/48x48/apps
%{__mkdir} -p $RPM_BUILD_ROOT/usr/share/icons/hicolor/48x48/apps
%{__mkdir} -p $RPM_BUILD_ROOT/usr/share/icons/hicolor/128x128/apps
%{__install} -m 0644 %_builddir/%{insidedir}/linux/%{name}.desktop $RPM_BUILD_ROOT/usr/share/applications/%{name}.desktop
%{__install} -m 0644 %_builddir/%{insidedir}/linux/icons/tyrian-22.png $RPM_BUILD_ROOT/usr/share/icons/locolor/22x22/apps/%{name}.png
%{__install} -m 0644 %_builddir/%{insidedir}/linux/icons/tyrian-22.png $RPM_BUILD_ROOT/usr/share/icons/hicolor/22x22/apps/%{name}.png
%{__install} -m 0644 %_builddir/%{insidedir}/linux/icons/tyrian-24.png $RPM_BUILD_ROOT/usr/share/icons/hicolor/24x24/apps/%{name}.png
%{__install} -m 0644 %_builddir/%{insidedir}/linux/icons/tyrian-32.png $RPM_BUILD_ROOT/usr/share/icons/hicolor/32x32/apps/%{name}.png
%{__install} -m 0644 %_builddir/%{insidedir}/linux/icons/tyrian-48.png $RPM_BUILD_ROOT/usr/share/icons/locolor/48x48/apps/%{name}.png
%{__install} -m 0644 %_builddir/%{insidedir}/linux/icons/tyrian-48.png $RPM_BUILD_ROOT/usr/share/icons/hicolor/48x48/apps/%{name}.png
%{__install} -m 0644 %_builddir/%{insidedir}/linux/icons/tyrian-128.png $RPM_BUILD_ROOT/usr/share/icons/hicolor/128x128/apps/%{name}.png


%files
%defattr(-,root,root)
%doc %attr(0644,-,-) CREDITS
%doc NEWS
%doc README
%doc COPYING
/usr/bin/%{name}
%doc /usr/share/man/man6/%{name}.6.gz
%{tyriandir}
/usr/share/applications/%{name}.desktop
/usr/share/icons/locolor/22x22/apps/%{name}.png
/usr/share/icons/hicolor/22x22/apps/%{name}.png
/usr/share/icons/hicolor/24x24/apps/%{name}.png
/usr/share/icons/hicolor/32x32/apps/%{name}.png
/usr/share/icons/locolor/48x48/apps/%{name}.png
/usr/share/icons/hicolor/48x48/apps/%{name}.png
/usr/share/icons/hicolor/128x128/apps/%{name}.png


%changelog
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
