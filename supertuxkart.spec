%define name supertuxkart
%define version 0.3
%define release %mkrel 2

Summary: Kart racing game
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://prdownload.berlios.de/supertuxkart/%{name}-%{version}-src.tar.bz2
License: GPL
Group: Games/Arcade
Url: http://supertuxkart.berlios.de/
BuildRequires: freealut-devel
BuildRequires: libmikmod-devel
BuildRequires: mesagl-devel
BuildRequires: plib-devel
BuildRequires: oggvorbis-devel
BuildRequires: SDL-devel
BuildRequires: desktop-file-utils

%description
SuperTuxKart is an improved version of TuxKart, a kart racing game
featuring Tux and friends. SuperTuxKart contains new characters, new
tracks and a reworked userinterface.

%prep
%setup -q

%build
%configure2_5x --bindir=%{_gamesbindir}
%make

%install
rm -rf %{buildroot}
%makeinstall bindir=%{buildroot}%{_gamesbindir}

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
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}_*.xpm
