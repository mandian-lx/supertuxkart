%define name	supertuxkart
%define version	0.7

%define pre	0
%define rel	2

%if %pre
%define release		%mkrel 0.%pre.%rel
%define distname	%name-%version%pre-src.tar.bz2
%define dirname		%name-%version%pre
%else
%define release		%mkrel %rel
%define distname	%name-%version-src.tar.bz2
%define dirname		%name-%version
%endif

Summary:	Kart racing game
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://downloads.sourceforge.net/supertuxkart/%{distname}
Patch0:		supertuxkart-0.6-fix-desktop.patch
License:	GPLv2+
Group:		Games/Arcade
URL:		http://supertuxkart.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	freealut-devel
BuildRequires:	libmikmod-devel
BuildRequires:	mesagl-devel
BuildRequires:	mesaglut-devel
BuildRequires:	plib-devel
BuildRequires:	oggvorbis-devel
BuildRequires:	SDL-devel
BuildRequires:	desktop-file-utils
BuildRequires:	imagemagick
BuildRequires:	openal-devel
BuildRequires:	irrlicht-devel >= 1.7
BuildRequires:	fribidi-devel

%description
SuperTuxKart is an improved version of TuxKart, a kart racing game
featuring Tux and friends. SuperTuxKart contains new characters, new
tracks and a reworked user interface.

%prep
%setup -q -n %{dirname}
%patch0 -p1

#fix rights
chmod -x AUTHORS ChangeLog NEWS README

%build
%configure2_5x \
	--bindir=%{_gamesbindir} \
	--disable-rpath
%make

%install
rm -rf %{buildroot}
%makeinstall_std

rm -f %{buildroot}%{_datadir}/pixmaps/%{name}_*.xpm
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48,64x64}/apps
convert -scale 16x16 data/%{name}_32.xpm %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
convert data/%{name}_32.xpm %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 48x48 data/%{name}_64.xpm %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert data/%{name}_64.xpm %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{name}.png

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README TODO
%{_gamesbindir}/%{name}
%{_gamesdatadir}/%{name}
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop
