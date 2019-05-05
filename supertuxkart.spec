%ifarch %{ix86}
%define _disable_ld_no_undefined 1
%define _disable_lto 1
%endif

Summary:	Kart racing game
Name:		supertuxkart
Version:	1.0
Release:	1
License:	GPLv2+ and GPLv3+ and CC-BY and CC-BY-SA and Public Domain
Group:		Games/Arcade
Url:		http://supertuxkart.sourceforge.net/
Source0:	https://downloads.sourceforge.net/supertuxkart/%{name}-%{version}-src.tar.xz
Source100:	%{name}.rpmlintrc
#Patch0:		supertuxkart-0.9-static.patch
#Patch1:		supertuxkart-0.9-aarch64.patch
Patch2:         supertuxkart-0.9.2-libs.patch
Patch3:         supertuxkart-0.9.2-irrlicht.patch
Patch4:         supertuxkart-0.9.2-angelscript.patch
Patch5:         supertuxkart-0.9-wiiuse.patch
BuildRequires:	cmake
BuildRequires:	imagemagick
BuildRequires:	angelscript-devel
BuildRequires:	glesv3-devel
BuildRequires:	jpeg-devel
BuildRequires:  wiiuse-devel
BuildRequires:	pkgconfig(bluez)
BuildRequires:  pkgconfig(egl)
BuildRequires:	pkgconfig(freealut)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(fribidi)
BuildRequires:	pkgconfig(gl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(glew)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(libcrypto)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libenet)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(zlib)

# dirty fix for now...
#Requires:	wiiuse-devel

%description
SuperTuxKart is an improved version of TuxKart, a kart racing game
featuring Tux and friends. SuperTuxKart contains new characters, new
tracks and a reworked user interface.

%files
%doc CHANGELOG.md README.md
%{_gamesbindir}/%{name}
%{_gamesdatadir}/%{name}
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%{_datadir}/metainfo/%{name}.appdata.xml

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
%autosetup -q
%autopatch -p1

# remove bundled library, use system instead.
rm -rf lib/{angelscript,enet,glew,jpeglib,libpng,wiiuse,zlib}

%build
%ifarch %{ix86}
export CC=gcc
export CXX=g++
%endif

%cmake \
	-DBUILD_RECORDER:BOOL=OFF \
	-DSTK_INSTALL_BINARY_DIR:STRING=%{_gamesbindir} \
	-DSTK_INSTALL_DATA_DIR:STRING=%{_gamesdatadir}/%{name} \
	-DBUILD_SHARED_LIBS:BOOL=OFF \
	-DBUILD_STATIC_LIBS:BOOL=ON \
	-DUSE_SYSTEM_ANGELSCRIPT:BOOL=ON \
	-DUSE_SYSTEM_ENET:BOOL=ON \
        -DUSE_SYSTEM_GLEW:BOOL=ON \
	-DUSE_SYSTEM_WIIUSE:BOOL=ON
%make_build

%install
%make_install -C build

# missing icons
install -dm 0755  %{buildroot}%{_iconsdir}/hicolor/{16x16,48x48,64x64}/apps/
convert -scale 16x16 data/%{name}_32.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
convert -scale 48x48 data/%{name}_128.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -scale 64x64 data/%{name}_128.png %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{name}.png
