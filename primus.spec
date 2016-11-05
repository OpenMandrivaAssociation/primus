# Package should be built in nonfree only, as it only provides features for nvidia-current

%define driver  nvidia

%define libname %mklibname %{name}
%global __provides_exclude \\.so

Name:           primus
Version:        0.2
Release:        2
Summary:        Minimalistic and efficient OpenGL offloading for Bumblebee
Group:          System/Kernel and hardware
License:        ISC
URL:            https://github.com/amonakov/primus
Source0:        https://github.com/amonakov/primus/archive/v%{version}/%{name}-%{version}.tar.gz
Patch1:         primus-0.1-mga-libgl-nvidia.patch
Patch2:         primus-git-build-with-ldflags.patch
Patch3:         primus-0.2-mga-libglfork-dl-linking.patch

BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(x11)

Requires:       %{libname} = %{version}-%{release}
Requires:       %{name}-bin = %{version}-%{release}

%ifarch x86_64
Suggests:     lib%{name} = %{version}-%{release}
%endif

%description
Primus is a shared library that provides OpenGL and GLX APIs and
implements low-overhead local-only client-side OpenGL offloading via GLX
forking, similar to VirtualGL. It intercepts GLX calls and redirects GL
rendering to a secondary X display, presumably driven by a faster GPU.
On swapping buffers, rendered contents are read back using a PBO and
copied onto the drawable it was supposed to be rendered on in the first
place.

%files
%doc README.md technotes.md
%{_mandir}/man1/primusrun.1*
%{_sysconfdir}/bash_completion.d/%{name}

#--------------------------------------------------------------------

%package -n     %{libname}
Summary:        Shared library for Primus
Group:          System/Libraries
Requires:       %{name}

%description -n %{libname}
Libraries injected by Primus into applications that are ran through it.
Lib packages allow installing 32 and 64 bit libraries at the same time.

%files -n       %{libname}
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libGL.so.1

#--------------------------------------------------------------------

%package        %{driver}
Summary:        primusrun script adapted to %{driver} driver
Group:          System/Kernel and hardware
Requires:       %{name}
Requires:       bumblebee-%{driver}
Obsoletes:      primus-nouveau < 0.1-3.20150328.3
Provides:       %{name}-bin = %{version}-%{release}

%description    %{driver}
primusrun script patched against the %{driver} driver.

%files          %{driver}
%{_bindir}/primusrun

#--------------------------------------------------------------------
%prep
%setup -q
%apply_patches

%build
export CXX=g++
%setup_compile_flags
%make \
  LIBDIR=%{_lib} \
  PRIMUS_libGLa=%{_libdir}/nvidia-current/libGL.so.1 \
  PRIMUS_libGLd=%{_libdir}/libGL.so.1

%install
install -Dm755 primusrun %{buildroot}%{_bindir}/primusrun
install -Dm755 %{_lib}/libGL.so.1 %{buildroot}%{_libdir}/%{name}/libGL.so.1
install -Dm644 primusrun.1 %{buildroot}%{_mandir}/man1/primusrun.1
install -Dm644 primus.bash-completion %{buildroot}%{_sysconfdir}/bash_completion.d/%{name}



%changelog
* Mon Oct 17 2016 akien <akien> 0.2-1.mga6
+ Revision: 1061238
- Version 0.2 (same as before, but finally tagged after 1.5 years)
- Add patch to use our LDFLAGS and fix underlinking

* Sat Jul 16 2016 akien <akien> 0.1-3.20150328.3.mga6.nonfree
+ Revision: 1042284
- Drop and obsolete the -nouveau flavour
  o nouveau developers mentioned that using nouveau with Bumblebee was pointless,
    users would get much better performance using DRI Prime: https://nouveau.freedesktop.org/wiki/Optimus

* Fri Apr 15 2016 akien <akien> 0.1-3.20150328.2.mga6.nonfree
+ Revision: 1002734
+ rebuild (emptylog)

* Sat Nov 28 2015 akien <akien> 0.1-3.20150328.1.mga6
+ Revision: 906847
- Recommend 32bit library for 64bit package
- Package latest snapshot (one new bugfix commit)

* Sun Feb 01 2015 akien <akien> 0.1-2.20150201.1.mga5
+ Revision: 813067
- New snapshot fixing potential segfaults (upstream#160)
- Remove mesa 10.1 workaround

* Sat Jan 10 2015 akien <akien> 0.1-1.20141228.1.mga5
+ Revision: 809720
- New snapshot 20141228

* Wed Oct 15 2014 umeabot <umeabot> 0.1-0.20131127.7.mga5
+ Revision: 746348
- Second Mageia 5 Mass Rebuild

  + tv <tv>
    - use %%global for req/prov exclude
    - autoconvert to new prov/req excludes

* Fri Mar 07 2014 akien <akien> 0.1-0.20131127.6.mga5
+ Revision: 600879
- Use %%optflags for CXXFLAGS
- Pass the same arguments to the Makefile than set in the primusrun script
- Add the Mesa 10.1.0 workaround to the primus bridge (for optirun)

* Fri Mar 07 2014 akien <akien> 0.1-0.20131127.5.mga5.nonfree
+ Revision: 600782
- Add workaround to primus/mesa bug introduced with Mesa 10.1.0

* Mon Feb 10 2014 akien <akien> 0.1-0.20131127.3.mga5
+ Revision: 589157
- Fix wrong path for libGL with nouveau

* Fri Feb 07 2014 akien <akien> 0.1-0.20131127.2.mga5.nonfree
+ Revision: 585670
- Version the Provides
- Adapt spec to package both nouveau (core) and nvidia (nonfree) versions
- Add _provides_exceptions to prevent from providing libGL.so.1
- Remove explicit Requires on libmesagl
- Rename patch

* Thu Feb 06 2014 akien <akien> 0.1-0.20131127.1.mga5
+ Revision: 584823
- Add Requires on lib(64)primus to the binary package
- imported package primus

