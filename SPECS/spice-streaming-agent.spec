Name:           spice-streaming-agent
Version:        0.3
Release:        2%{?dist}
Summary:        SPICE streaming agent
Group:          Applications/System
License:        ASL 2.0
URL:            https://www.redhat.com
Source0:        %{name}-%{version}.tar.xz
BuildRequires:  spice-protocol >= 0.12.16
BuildRequires:  libX11-devel libXfixes-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  catch-devel
BuildRequires:  pkgconfig(udev)
BuildRequires:  libdrm-devel
BuildRequires:  libXrandr-devel
BuildRequires:  gcc-c++
BuildRequires:  diffutils
BuildRequires:  gstreamer1-devel gstreamer1-plugins-base-devel
# we need /usr/sbin/semanage program which is available on different
# packages depending on distribution
Requires(post): /usr/sbin/semanage
Requires(postun): /usr/sbin/semanage

ExclusiveArch: x86_64

# Downstream: remove H264 and set VP8 as the default codec
Patch0100: 0100-gst-plugin-make-VP8-the-default-codec-downstream.patch
Patch0101: 0101-gst-plugin-remove-H264-and-H265-downstream.patch

%description
An agent, running on a guest, sending video streams of the X display to a
remote client (over SPICE).

%package devel
Requires: spice-protocol >= 0.12.16
Requires: pkgconfig
Requires: libX11-devel
Summary:  SPICE streaming agent development files

%description devel
This package contains necessary header files to build SPICE streaming
agent plugins.

%prep
%setup -q
%patch100 -p1
%patch101 -p1

%build
%configure --enable-tests --with-udevrulesdir=%{_udevrulesdir} --enable-gst-plugin=yes
make %{?_smp_mflags} V=1

%check
make check

%install
make install DESTDIR=%{buildroot} V=1
if test -d "%{buildroot}/%{_libdir}/%{name}/plugins"; then
    find %{buildroot}/%{_libdir}/%{name}/plugins -name '*.la' -delete
fi

%post
semanage fcontext -a -t xserver_exec_t %{_bindir}/spice-streaming-agent 2>/dev/null || :
restorecon %{_bindir}/spice-streaming-agent || :

%postun
if [ $1 -eq 0 ] ; then  # final removal
semanage fcontext -d -t xserver_exec_t %{_bindir}/spice-streaming-agent 2>/dev/null || :
fi


%files
%doc COPYING NEWS README
%{_udevrulesdir}/90-spice-guest-streaming.rules
%{_bindir}/spice-streaming-agent
%{_sysconfdir}/xdg/autostart/spice-streaming.desktop
%{_datadir}/gdm/greeter/autostart/spice-streaming.desktop
%{_mandir}/man1/spice-streaming-agent.1.gz
%{_libdir}/%{name}/plugins/*.so


%files devel
%defattr(-,root,root,-)
%{_includedir}
%{_libdir}/pkgconfig

%changelog
* Thu Dec 12 2019 Uri Lublin <uril@redhat.com> - 0.3-2
- Update to 0.3 release
- Resolves: rhbz#1774123
- Resolves: rhbz#1774129

* Wed Aug  1 2018 Uri Lublin <uril@redhat.com> - 0.2-3
- Rebuild for rhel-8
  Related: rhbz#1614485

* Wed Aug 16 2017 Frediano Ziglio <fziglio@redhat.com> - 0.1-1
- Initial package (pre-release)
