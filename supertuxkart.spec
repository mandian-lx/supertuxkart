%define rname SuperTuxKart
%define name supertuxkart
%define version 0.2
%define release %mkrel 2

Summary: Kart racing game
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://prdownload.berlios.de/supertuxkart/%{rname}-%{version}.tar.bz2
Source1: %{name}.png
License: GPL
Group: Games/Arcade
Url: http://supertuxkart.berlios.de/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: mesagl-devel
BuildRequires: plib-devel

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
%makeinstall bindir=$RPM_BUILD_ROOT%{_gamesbindir}

install -D -m 644 %{SOURCE1} %{buildroot}%{_datadir}/icons/%{name}.png

install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=SuperTuxKart
Comment=Kart racing game
Exec=soundwrapper %_gamesbindir/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;ArcadeGame;X-MandrivaLinux-MoreApplications-Games-Arcade;
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS CHANGES NEWS README TODO
%{_gamesbindir}/%{name}
%dir %{_gamesdatadir}/%{name}
%{_gamesdatadir}/%{name}/*
%{_datadir}/icons/%{name}.png
%{_datadir}/applications/mandriva-%{name}.desktop


