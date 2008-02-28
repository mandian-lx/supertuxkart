%define pre rc1a
%if %pre
%define release %mkrel 0.%pre.1
%else
%define release %mkrel 1
%endif

Summary: Kart racing game
Name: supertuxkart
Version: 0.4
Release: %{release}
%if %pre
Source0: http://prdownload.berlios.de/supertuxkart/%{name}-%{version}%{pre}-src.tar.bz2
%else
Source0: http://prdownload.berlios.de/supertuxkart/%{name}-%{version}-src.tar.bz2
%endif
License: GPLv2+
Group: Games/Arcade
Url: http://supertuxkart.berlios.de/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: freealut-devel
BuildRequires: libmikmod-devel
BuildRequires: mesagl-devel
BuildRequires: plib-devel
BuildRequires: oggvorbis-devel
BuildRequires: SDL-devel
BuildRequires: desktop-file-utils
BuildRequires: ImageMagick

%description
SuperTuxKart is an improved version of TuxKart, a kart racing game
featuring Tux and friends. SuperTuxKart contains new characters, new
tracks and a reworked user interface.

%prep
%setup -q -n %{name}-0.4rc1
sed -i -e 's,%{name}_64.xpm,%{name},g' data/%{name}.desktop

%build
%configure2_5x --bindir=%{_gamesbindir}
%make

%install
rm -rf %{buildroot}
%makeinstall bindir=%{buildroot}%{_gamesbindir}

rm -f %{buildroot}%{_datadir}/pixmaps/%{name}_*.xpm
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48,64x64}/apps
convert -scale 16x16 data/%{name}_32.xpm %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
convert data/%{name}_32.xpm %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 48x48 data/%{name}_64.xpm %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert data/%{name}_64.xpm %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{name}.png

desktop-file-install --vendor='' \
	--dir=%{buildroot}%{_datadir}/applications \
	--remove-category='3DGraphics' \
	%{buildroot}%{_datadir}/applications/*.desktop

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README TODO
%{_gamesbindir}/%{name}
%dir %{_gamesdatadir}/%{name}
%{_gamesdatadir}/%{name}/*
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop
