Summary:	Kart racing game
Name:		supertuxkart
Version:	0.8.1
Release:	1
License:	GPLv2+
Group:		Games/Arcade
URL:		http://supertuxkart.sourceforge.net/
Source0:	http://downloads.sourceforge.net/supertuxkart/%{name}-%{version}-src.tar.bz2
Patch0:		supertuxkart-0.8.1-desktop.patch
Patch1:		supertuxkart-0.8.1-static.patch
BuildRequires:	cmake
BuildRequires:	imagemagick
BuildRequires:	pkgconfig(freealut)
BuildRequires:	pkgconfig(fribidi)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libenet)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(vorbis)

%description
SuperTuxKart is an improved version of TuxKart, a kart racing game
featuring Tux and friends. SuperTuxKart contains new characters, new
tracks and a reworked user interface.

%files
%doc AUTHORS ChangeLog README TODO
%{_gamesbindir}/%{name}
%{_gamesdatadir}/%{name}
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}_*.png

#----------------------------------------------------------------------------

%prep
%setup -q -n SuperTuxKart-%{version}
%patch0 -p1
%patch1 -p1

%build
%cmake \
	-DSTK_INSTALL_BINARY_DIR=%{_gamesbindir} \
	-DSTK_INSTALL_DATA_DIR=%{_gamesdatadir}/%{name}
%make

%install
%makeinstall_std -C build

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48,64x64,128x128}/apps
convert -scale 16x16 data/%{name}_32.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
convert data/%{name}_32.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 48x48 data/%{name}_128.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -scale 64x64 data/%{name}_128.png %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{name}.png
convert data/%{name}_128.png %{buildroot}%{_iconsdir}/hicolor/128x128/apps/%{name}.png

