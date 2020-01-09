%define kmod_name		bnx2x
%define kmod_driver_version	1.72.00_0
%define kmod_rpm_release	1
%define kmod_git_hash		b7fab1d776e25e08af4a79d1976eedf94ef40ab0
%define kmod_kernel_version	2.6.32-220.el6
%define kmod_kbuild_dir		drivers/net/bnx2x/
%define kmod_firmware_version	7.2.16.0

%{!?dist: %define dist .el6}

Source0:	%{kmod_name}-%{kmod_driver_version}.tar.bz2			
Source1:	%{kmod_name}.files			
Source2:	%{kmod_name}.conf			
Source3:	find-requires.ksyms			
Source4:	find-provides.ksyms			
Source5:	kmodtool			
Source6:	symbols.greylist			
Source7:	bnx2x-firmware.files			
Source8:	bnx2x.preamble			
Source9:	Module.symvers-i686			
Source10:	Module.symvers-x86_64			

%define __find_requires %_sourcedir/find-requires.ksyms
%define __find_provides %_sourcedir/find-provides.ksyms %{kmod_name} %{?epoch:%{epoch}:}%{version}-%{release}

Name:		%{kmod_name}
Version:	%{kmod_driver_version}
Release:	%{kmod_rpm_release}%{?dist}
Summary:	%{kmod_name} kernel module

Group:		System/Kernel
License:	GPLv2
URL:		http://www.kernel.org/
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	%kernel_module_package_buildreqs
ExclusiveArch:  i686 x86_64


# firmware package
%package -n kmod-%{kmod_name}-firmware
Summary:       %{kmod_name} kernel module firmware
Provides:      firmware(%{kmod_name}) = %{kmod_firmware_version}
# firmware package has to provide kernel-modules to be recognized and
# unpacked by Anaconda during installation
Provides:      kernel-modules = %{kmod_kernel_version}.%{_target_cpu}

%description -n kmod-%{kmod_name}-firmware
%{kmod_name} - driver update firmware

%files -n kmod-%{kmod_name}-firmware -f %{SOURCE7}

# Build only for standard kernel variant(s); for debug packages, append "debug"
# after "default" (separated by space)
%kernel_module_package -s %{SOURCE5} -f %{SOURCE1} -p %{SOURCE8} default

%description
%{kmod_name} - driver update

%prep
%setup
set -- *
mkdir source
mv "$@" source/
cp %{SOURCE9} source/
cp %{SOURCE10} source/
mkdir obj

%build
for flavor in %flavors_to_build; do
	rm -rf obj/$flavor
	cp -r source obj/$flavor

	# update symvers file if existing
	symvers=source/Module.symvers-%{_target_cpu}
	if [ -e $symvers ]; then
		cp $symvers obj/$flavor/%{kmod_kbuild_dir}/Module.symvers
	fi

	make -C %{kernel_source $flavor} M=$PWD/obj/$flavor/%{kmod_kbuild_dir} \
		NOSTDINC_FLAGS="-I $PWD/obj/$flavor/include"
done

if [ -d source/firmware ]; then
	make -C source/firmware
fi

%install
export INSTALL_MOD_PATH=$RPM_BUILD_ROOT
export INSTALL_MOD_DIR=extra/%{name}
for flavor in %flavors_to_build ; do
	make -C %{kernel_source $flavor} modules_install \
		M=$PWD/obj/$flavor/%{kmod_kbuild_dir}
	# Cleanup unnecessary kernel-generated module dependency files.
	find $INSTALL_MOD_PATH/lib/modules -iname 'modules.*' -exec rm {} \;
done

install -m 644 -D %{SOURCE2} $RPM_BUILD_ROOT/etc/depmod.d/%{kmod_name}.conf
install -m 644 -D %{SOURCE6} $RPM_BUILD_ROOT/usr/share/doc/kmod-%{kmod_name}/greylist.txt

if [ -d source/firmware ]; then
	make -C source/firmware INSTALL_PATH=$RPM_BUILD_ROOT INSTALL_DIR= install
fi

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Apr 04 2012 Jiri Benc <jbenc@redhat.com> 1.72.00_0 1
- updated to new driver version

* Fri Jan 27 2012 Jiri Benc <jbenc@redhat.com> 1.70.00_0.1 9
- synced with 6.2 GA

* Wed Jan 25 2012 Jiri Benc <jbenc@redhat.com> 1.70.00_0.1 8
- fixed firmware installation path

* Wed Jan 11 2012 Jiri Benc <jbenc@redhat.com> 1.70.00_0.1 7
- fixed firmware subpackage Provides

* Tue Nov 01 2011 Jiri Benc <jbenc@redhat.com> 1.70.00_0.1 6
- code fixes, newer firmware

* Fri Oct 21 2011 Jiri Olsa <jolsa@redhat.com> 1.70.00_0.1 5
- new spec version

* Fri Sep 30 2011 Jiri Olsa <jolsa@redhat.com> 1.70.00_0.1 4
- new spec version

* Thu Sep 22 2011 Jiri Benc <jbenc@redhat.com> 1.70.00_0.1 3
- build fix

* Wed Sep 21 2011 Jiri Benc <jbenc@redhat.com> 1.70.00_0.1 1
- updated to new driver version

* Fri Aug 12 2011 Jiri Olsa <jolsa@redhat.com> 1.70.00_0 1
- zstream build changes

* Fri Jun 10 2011 Jiri Olsa <jolsa@redhat.com> 1.62.00_6 1
- bnx2x DUP module
