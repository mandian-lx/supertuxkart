#
# FIXME: basically it works but with the following error at running time
#        [error  ] SFXManager: SFXOpenAL OpenAL error while positioning AL_INVALID_OPERATION
#

#global _privatelibs libstkirrlicht[.]so.*
#global __provides_exclude ^(%{_privatelibs})$
#global __requires_exclude ^(%{_privatelibs})$

Summary:        Kart racing game
Name:           supertuxkart
Version:        0.9.2
Release:        2
License:        GPLv2+ and GPLv3+ and CC-BY and CC-BY-SA and Public Domain
Group:          Games/Arcade
URL:            http://supertuxkart.sourceforge.net/
Source0:        https://downloads.sourceforge.net/supertuxkart/%{name}-%{version}-src.tar.xz
Source1:        %{name}.6
Patch0:         supertuxkart-0.8.1-desktop.patch
Patch1:         supertuxkart-0.8.1-static.patch
Patch2:         supertuxkart-0.9.2-libs.patch
Patch3:         supertuxkart-0.9.2-irrlicht.patch
Patch4:         supertuxkart-0.9.2-angelscript.patch
Patch5:         supertuxkart-0.9-wiiuse.patch
BuildRequires:  cmake
BuildRequires:  imagemagick
BuildRequires:  desktop-file-utils
BuildRequires:  %{_lib}angelscript-devel # NEW::
BuildRequires:  jpeg-devel
BuildRequires:  %{_lib}wiiuse-devel # NEW::
BuildRequires:  pkgconfig(bluez)
BuildRequires:  pkgconfig(freealut)
BuildRequires:  pkgconfig(fribidi)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glew)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libenet)
BuildRequires:  pkgconfig(openal)
BuildRequires:  pkgconfig(vorbis)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(zlib)

Requires:   %{name}-data = %{version}

%description
SuperTuxKart is an improved version of TuxKart, a kart racing game
featuring Tux and friends. SuperTuxKart contains new characters, new
tracks and a reworked user interface.

%files
%{_gamesbindir}/%{name}*
#%{_libdir}/libstkirrlicht.so
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}_*.png
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_mandir}/man6/%{name}.6*
%doc README.md
%doc CHANGELOG.md
%doc AUTHORS
%doc TODO.md
%doc COPYING

#----------------------------------------------------------------------------

%package data
Summary:    Data files for Super Tux Kart
BuildArch:  noarch

%description data
Data files for Super Tux Kart.

%files data
%{_gamesdatadir}/%{name}

#----------------------------------------------------------------------------

%prep
%setup -q

# fix line endings
%__find lib/irrlicht/source/ -type f -exec %__sed -i -e 's|\r||g' '{}' \;

#%%patch0 -p1
#%%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

# remove unused bundled libs
%__rm -fr \
        lib/angelscript/ \
        lib/enet/ \
        lib/glew/ \
        lib/jpeglib/ \
        lib/libpng/ \
        lib/wiiuse \
        lib/zlib

# remove backup
%__find . -name "*~" -delete

%build
export LDFLAGS="$LDFLAGS -lm"
%cmake \
        -DCMAKE_BUILD_TYPE:STRING="STKRelease" \
	-DBUILD_SHARED_LIBS:BOOL=OFF \
	-DBUILD_STATIC_LIBS:BOOL=ON \
        -DSTK_INSTALL_BINARY_DIR:STRING=%{_gamesbindir} \
        -DSTK_INSTALL_DATA_DIR:STRING=%{_gamesdatadir}/%{name} \
        -DUSE_SYSTEM_ANGELSCRIPT:BOOL=ON \
        -DENABLE_NETWORK_MULTIPLAYER:BOOL=OFF \
	-DCHECK_ASSETS:BOOL=OFF
%make

%install
%make_install -C build

# shared lib
#%__install -dm 755 %{buildroot}%{_libdir}/
#%__install -pm 755 build/lib/irrlicht/libstkirrlicht.so %{buildroot}%{_libdir}/

# manpage (from the Debian package)
%__install -dm 755 %{buildroot}%{_mandir}/man6/
%__install -pm 644 %{SOURCE1} %{buildroot}%{_mandir}/man6/

# missing icons
%__install -dm 755  %{buildroot}%{_iconsdir}/hicolor/{16x16,48x48,64x64}/apps/
convert -scale 16x16 data/%{name}_32.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
convert -scale 48x48 data/%{name}_128.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -scale 64x64 data/%{name}_128.png %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{name}.png

# https://github.com/supertuxkart/stk-code/issues/2533
#convert -strip <input filename> <output filename>

%check
# desktop file
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%post
/sbin/ldconfig
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

