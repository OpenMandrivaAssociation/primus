# Package should be built in nonfree only, as it only provides features for nvidia-current

%define driver nvidia

%define libname %mklibname %{name}
%global __provides_exclude \\.so

Name:		primus
Version:	0.2
Release:	3
Summary:	Minimalistic and efficient OpenGL offloading for Bumblebee
Group:		System/Kernel and hardware
License:	ISC
URL:		https://github.com/amonakov/primus
Source0:	https://github.com/amonakov/primus/archive/v%{version}/%{name}-%{version}.tar.gz
Patch1:		primus-0.1-mga-libgl-nvidia.patch
Patch2:		primus-git-build-with-ldflags.patch
Patch3:		primus-0.2-mga-libglfork-dl-linking.patch

BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(x11)

Requires:	%{libname} = %{EVRD}
Requires:	%{name}-bin = %{EVRD}

%ifarch x86_64
Suggests:     lib%{name} = %{EVRD}
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

%package -n %{libname}
Summary:	Shared library for Primus
Group:		System/Libraries
Requires:	%{name}

%description -n %{libname}
Libraries injected by Primus into applications that are ran through it.
Lib packages allow installing 32 and 64 bit libraries at the same time.

%files -n %{libname}
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libGL.so.1

#--------------------------------------------------------------------

%package %{driver}
Summary:	primusrun script adapted to %{driver} driver
Group:		System/Kernel and hardware
Requires:	%{name}
Requires:	bumblebee-%{driver}
Obsoletes:	primus-nouveau < 0.1-3.20150328.3
Provides:	%{name}-bin = %{EVRD}

%description %{driver}
primusrun script patched against the %{driver} driver.

%files %{driver}
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
