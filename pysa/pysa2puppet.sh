#!/bin/bash
#
# deploy pysa module to puppet
#

TARBALL=false           # default not compression
REMOTE=false            # default local copy
CERTIFICATION=false     # default not use certificate key

MADEIRA=/madeira
DEPS=${MADEIRA}/deps
PUPPET_HOME=/etc/puppet

SUPPORTED_DISTRO=(redhat centos ubuntu debian amazon)
SUPPORTED_REDHAT=(5 6)
SUPPORTED_CENTOS=(5 6)
SUPPORTED_UBUNTU=(8.04 10.04 11.10 12.04 12.10 13.04)
SUPPORTED_DEBIAN=(6 7)
SUPPORTED_AMAZON=(2013.03)
PACKAGE_MANAGERS=(yum apt-get aptitude)
ARCHS=(i386 i686 x86_64)
OS=""
VER=""
ARCH=""
PM=""

PYSA_SRC=""
CERT_KEY=""

# get the system's basic information: os, version
function check_os() {
    echo "check the system basic information"

    # get the package manager
    for pm in ${PACKAGE_MANAGERS[@]}; do
        PM=${pm}
        which ${PM}
        if [ $? -eq 0 ]; then
            break
        fi
    done

    # install the lsb package
    ${PM} -y install lsb

    # get the distro name and the version
    OS=`lsb_release -i | awk -F":" '{print $2}'`
    if [ -z ${OS} ]; then
        echo "ERROR: Could not get the distribution information"
	echo "CRITICAL"
        return 1
    fi
    OS=${OS#"${OS%%[![:space:]]*}"} # remove leading whitespace characters
    OS=${OS#"${OS##[![:space:]]*}"} # remove trailing whitespace characters
    OS=${OS,,}  # lower case

    # check distro name
    local flag=false
    for os in ${SUPPORTED_DISTRO[@]}; do
        if [[ "$OS" == *"$os"* ]]; then
            flag=true
            OS=${os}
            break
        fi
    done
    if ! ${flag}; then
        echo "ERROR:This distribution isn't supported yet"
        return 2
    fi

    # get os version
    VER=`lsb_release -sr`
    if [ -z ${VER} ]; then
        echo "ERROR:Get the distribution version failed"
        return 3
    fi

    # get architecture
    flag=false
    ARCH=${HOSTTYPE}
    for arch in ${ARCHS[@]}; do
        if [ ${ARCH} == ${arch} ]; then
            flag=true
            break
        fi
    done
    if ! ${flag}; then
        echo "ERROR:Get system architecture failed"
        return 4
    fi

    echo -e "OS:${OS}\nVER:${VER}\nARCH:${ARCH}\nPM:${PM}"

    return 0
}

# check the ruby version(1.8.7, http://docs.puppetlabs.com/guides/platforms.html)
function check_ruby() {
    echo "install and check ruby package"
    which ruby
    if [ $? -ne 0 ]; then
        # install ruby1.8.7
        case ${PM} in
            yum)
                ${PM} install ruby-1.8.7.352
                ;;
            apt-get|aptitude)
                ${PM} install ruby1.8-full
                ;;
            *)
                echo "ERROR:Package manager unsupported"
                return 1
        esac

        if [ $? -ne 0 ]; then
            echo "ERROR:Install ruby1.8.7 failed"
            return 2
        fi
    fi

    return 0
}

# install puppet master
function check_puppet() {
    echo "check puppet package"
    case ${OS} in
        centos|redhat )
            add_epel_repo
            if [ $? -ne 0 ]; then
                echo "ERROR:Add epel repo failed"
                return 1
            fi
            ;;
        ubuntu|debian )
            add_puppet_repo
            if [ $? -ne 0 ]; then
                echo "ERROR:Add puppet labs repo failed"
                return 1
            fi
            ;;
        amazon )
            ;;
    esac

    ${PM} install puppet puppetmaster facter
    if [ $? -eq 0 ]; then
        echo "Install puppet successfully!"
    else
        echo "Install puppet failed!"
        return 1
    fi

    # check puppet manifest and module directory
    if [ ! -d ${PUPPET_HOME}/manifests ]; then
        mkdir -p ${PUPPET_HOME}/manifests
    fi
    if [ ! -d ${PUPPET_HOME}/modules ]; then
        mkdir -p ${PUPPET_HOME}/modules
    fi

    return 0
}

# config pysa module: add site.pp, copy and extract the pysa module
function config_pysa() {
    echo "config the pysa module"

    if [ -d ${DEPS}/pysa ]; then
        rm -rf ${DEPS}/pysa
    fi
    if [ -f ${DEPS}/pysa.tar.gz ]; then
        rm -f ${DEPS}/pysa.tar.gz
    fi
    mkdir -p ${DEPS}/pysa
    # copy the pysa module
    if ${REMOTE}; then
	if ${TARBALL}; then
            echo "Remote copy the zipped pysa module"
            if ${CERTIFICATION}; then
		scp -i ${CERT_KEY} ${PYSA_SRC} ${DEPS}/pysa.tar.gz
            else
		scp ${PYSA_SRC} ${DEPS}/pysa.tar.gz
            fi
	    
            if [ -f ${DEPS}/pysa.tar.gz ]; then
		tar zxvf ${DEPS}/pysa.tar.gz -C ${DEPS}/pysa
            else
		echo "ERROR:Remote copy failed"
		return 1
            fi
	else
            echo "Remote copy the pysa module"
            if ${CERTIFICATION}; then
		scp -i ${CERT_KEY} -r ${PYSA_SRC} ${DEPS}/pysa
            else
		scp -r ${PYSA_SRC} ${DEPS}/pysa
            fi
	fi
    elif ${TARBALL}; then
        tar zxvf ${PYSA_SRC} -C ${DEPS}/pysa
    else
        cp -r ${PYSA_SRC} ${DEPS}/pysa

    fi

    subdircount=`find ${DEPS}/pysa -maxdepth 1 -type d | wc -l`
    if [ ${subdircount} -lt 1 ]; then
        echo "ERROR:Copy pysa module failed"
        return 2
    fi

    # check the pysa module directory
    for dir in $(find ${DEPS}/pysa -type d); do
        if [[ "${dir}" == *"/manifests" ]]; then
            MANIFESTS_DIR=${dir}
            break
        fi;
    done

    for dir in $(find ${DEPS}/pysa -type d); do
        if [[ "${dir}" == *"/templates" ]]; then
            TEMPLATES_DIR=${dir}
            break;
        fi;
    done

    # puppet module
    mkdir -p ${PUPPET_HOME}/modules/pysa
    if [ -d ${MANIFESTS_DIR} ]; then
        ln -s ${MANIFESTS_DIR} ${PUPPET_HOME}/modules/pysa/manifests
    else
        echo "ERROR:Invalid pysa module"
        return 1
    fi

    if [ -d ${TEMPLATES_DIR} ]; then
        ln -s ${TEMPLATES_DIR} ${PUPPET_HOME}/modules/pysa/templates
    fi

    # install additional modules
    local times=3
    local i=0
    local flag_nodejs=false
    local flag_php=false
    local flag_vcsrepo=false
    while [ ${i} -lt ${times} ]; do
        # nodejs
        if ! ${flag_nodejs}; then
            puppet module install willdurand/nodejs

            if [ $? -ne 0 ]; then
                rm -rf ${PUPPET_HOME}/modules/nodejs
                if [ ${i} -eq 2 ]; then
                    echo "Install puppet moudle willdurand/nodejs failed!"
                fi
            else
                flag_nodejs=true
                echo "Install puppet module willdurand/nodejs successfully!"
            fi
        fi

        # php
        if ! ${flag_php}; then
            puppet module install nodes/php

            if [ $? -ne 0 ]; then
                rm -rf ${PUPPET_HOME}/modules/apt
                rm -rf ${PUPPET_HOME}/modules/php
                rm -rf ${PUPPET_HOME}/modules/stdlib
                if [ ${i} -eq 2 ]; then
                    echo "Install puppet moudle nodes/php failed!"
                fi
            else
                flag_php=true
                echo "Install puppet module nodes/php successfully!"
            fi
        fi

        # vcsrepo
        if ! ${flag_vcsrepo}; then
            puppet module install puppetlabs/vcsrepo

            if [ $? -ne 0 ]; then
                rm -rf ${PUPPET_HOME}/modules/vcsrepo
                if [ ${i} -eq 2 ]; then
                    echo "Install puppet moudle puppetlabs/vcsrepo failed!"
                fi
            else
                flag_vcsrepo=true
                echo "Install puppet module puppetlabs/vcsrepo successfully!"
            fi
        fi

        i=$(( ${i} + 1 ))
    done
    if ! ${flag_nodejs} || ! ${flag_php} || ! ${flag_vcsrepo}; then
        echo "ERROR:Install puppetlabs modules failed!"
        return 3
    fi

    # prepare the site.pp file
    if [ -f ${PUPPET_HOME}/manifests/site.pp ]; then
        rm -f ${PUPPET_HOME}/manifests/site.pp
    fi
    echo "node default { include pysa }">>${PUPPET_HOME}/manifests/site.pp

    return 0
}

# usage
function usage() {
    echo -e "\nUsage:\n$0 [-z -r] [pysa_module_path]\n \
        -z:pysa module compressed flag;\n \
        -r:pysa module is on the remote server;\n \
        pysa_module_path:pysa module's path. If trig -z flag then the pysa_module_path should compressed(now only support tar.gz format),\n \
        and if trig -r flag then the pysa_module_path should contain completed connection string;\n \
        example:\n $0 -z -r root@your_server_ip:/your_pysa_module_path/pysa.tar.gz"
}

# add epel repo
function add_epel_repo() {
    # check the os
    if [ ${OS} -ne "redhat" -o ${OS} -ne "centos" ]; then
        echo "ERROR:Invalid distribution for epel repo:${OS}"
        return 1
    fi

    # check epel
    NEED_INSTALL=0  # 0 no need install 1 new install 2 re-install
    if [ `rpm -qa | grep epel-release | wc -l` -eq 0 ]
    then
      echo "EPEL repo is not installed ,need install."
      NEED_INSTALL=1
    else
      if [ ! -f "/etc/yum.repos.d/epel.repo" ]
      then
        echo "epel repo installed already,but /etc/yum.repos.d/epel.repo doesn't exists and needs to be re-installed "
        NEED_INSTALL=2
      else
        echo "epel repo installed already"
        return 0
      fi
    fi

    case ${VER} in
        6)
            EPELREPO_URL="http://dl.fedoraproject.org/pub/epel/${OS_VER}/${ARCH}/epel-release-6-8.noarch.rpm"
            EPELREPO="epel-release-6-8.noarch"
            REMI_URL="http://rpms.famillecollet.com/enterprise/remi-release-${OS_VER}.rpm"
            REMI="remi-release-${OS_VER}"
            ;;
        5)
            EPELREPO_URL="http://dl.fedoraproject.org/pub/epel/${OS_VER}/${ARCH}/epel-release-5-4.noarch.rpm"
            EPELREPO="epel-release-5-4.noarch"
            REMI_URL="http://rpms.famillecollet.com/enterprise/remi-release-${OS_VER}.rpm"
            REMI="remi-release-${OS_VER}"
            ;;
        *)
            echo "Unsupported os version:${OS}"
            return 1
    esac

    #un-install first
    if [ $NEED_INSTALL -eq 2 ]
    then
        echo "Uninstall ${EPELREPO} and ${REMI} ..."
        rpm -e ${REMI}
        rpm -e ${EPELREPO}
    fi

    # install the epel repo
    if [ $NEED_INSTALL -eq 1 -o $NEED_INSTALL -eq 2 ]; then
        echo "Install ${EPELREPO} repo"
        rpm -Uvh ${EPELREPO}
        if [ $? -eq 0 ]; then
            echo "Install ${EPELREPO} succeed!"
        else
            echo "Install ${EPELREPO} failed!"
            return 2
        fi

        echo "Install ${REMI} repo"
        rpm -Uvh ${REMI}
        if [ $? -eq 0 ]
        then
          echo "Install ${REMI} succeed!"
          return 0
        else
          echo "ERROR:Install ${REMI} failed!"
          return 3
        fi
    fi
}

# add puppetlabs repo
function add_puppet_repo() {
    # check the os
    if [ ${OS} != "ubuntu" -a ${OS} != "debian" ]; then
        echo "ERROR:Invalid distribution for puppetlab repo:${OS}"
        return 1
    fi

    NEED_INSTALL=0  # 0 no need install 1 new install 2 re-install
    if [ `dpkg-query -l | grep puppetlabs-release | wc -l` -eq 0 ]; then
      echo "Puppetlabs repo is not installed, need install."
      NEED_INSTALL=1
    else
      if [ ! -f "/etc/apt/source.list.d/puppetlabs.list" ]
      then
        echo "Puppetlabs repo installed already,but /etc/apt/source.list.d/puppetlabs.list is not exist, need re-install "
        NEED_INSTALL=2
      else
        echo "Puppetlabs repo repo installed already"
        return 0
      fi
    fi

    if [ "${OS}" == "ubuntu" ]; then
        case ${VER} in
            8.04 )
                PUPPET_URL="http://apt.puppetlabs.com/puppetlabs-release-hardy.deb"
                PUPPET_DEB="puppetlabs-release-hardy.deb"
                ;;
            10.04 )
                PUPPET_URL="http://apt.puppetlabs.com/puppetlabs-release-lucid.deb"
                PUPPET_DEB="puppetlabs-release-lucid.deb"
                ;;
            11.10 )
                PUPPET_URL="http://apt.puppetlabs.com/puppetlabs-release-oneiric.deb"
                PUPPET_DEB="puppetlabs-release-oneiric.deb"
                ;;
            12.04 )
                PUPPET_URL="http://apt.puppetlabs.com/puppetlabs-release-precise.deb"
                PUPPET_DEB="puppetlabs-release-precise.deb"
                ;;
            12.10 )
                PUPPET_URL="http://apt.puppetlabs.com/puppetlabs-release-quantal.deb"
                PUPPET_DEB="puppetlabs-release-quantal.deb"
                ;;
            13.04 )
                PUPPET_URL="http://apt.puppetlabs.com/puppetlabs-release-raring.deb"
                PUPPET_DEB="puppetlabs-release-raring.deb"
                ;;
            * )
                echo "Not supported ${OS}-${VER}"
                return 2
        esac
    elif [ "${OS}" == "debian" ]; then
        case ${VER} in
            6 )
                PUPPET_URL="http://apt.puppetlabs.com/puppetlabs-release-squeeze.deb"
                PUPPET_DEB="puppetlabs-release-squeeze.deb"
                ;;
            7 )
                PUPPET_URL="http://apt.puppetlabs.com/puppetlabs-release-wheezy.deb"
                PUPPET_DEB="puppetlabs-release-wheezy.deb"
                ;;
            * )
                echo "Not supported ${OS}-${VER}"
                return 2
        esac
    fi

    # install puppetlabs repo
    #un-install first
    if [ $NEED_INSTALL -eq 2 ]
    then
      echo "Uninstall ${PUPPET_DEB} first"
      dpkg --purge puppetlabs-release
    fi

    # download and install the puppetlabs repo
    if [ $NEED_INSTALL -eq 1 -o $NEED_INSTALL -eq 2 ]; then

        cd ${DEPS}
        if [ ! -f ${PUPPET_DEB} ]; then
            rm -f ${PUPPET_DEB}
        fi

        echo "Download ${PUPPET_DEB}"
        wget ${PUPPET_URL}
        echo "Install ${PUPPET_DEB}"
        dpkg -i ${PUPPET_DEB}
        if [ $? -eq 0 ]; then
          echo "Install ${PUPPET_DEB} succeed!"
        else
          echo "Install ${PUPPET_DEB} failed!"
          return 2
        fi
    fi

    ${PM} update

    return 0
}

###############################################################
# The main process
#

# check whether root account
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root"
   exit 1
fi

# check the input params
if [ $# -lt 1 ]; then
    echo "please input arguments"
    usage
    exit 2
fi

# parse user's input options
while getopts "zri:" opt; do
    case $opt in
        z)
            echo "Compressed the pysa modules"
            TARBALL=true
            ;;
        r)
            echo "Remote copy the pysa module"
            REMOTE=true
            ;;
        i)
            echo "Use public key"
            CERTIFICATION=true
            CERT_KEY=${OPTARG}
            if [ -z ${CERT_KEY} ]; then
                echo "ERROR:Invalid public key"
                exit 1
            fi
            # check the relative path
            if [[ "${CERT_KEY}" != /* ]]; then
                CERT_KEY="$PWD"/${CERT_KEY}
            fi
            ;;
        ?)
            echo "Invalid option: -${OPTARG}"
            usage
            exit 1
            ;;
    esac
done

shift $((OPTIND - 1))
echo "input args:$1"
PYSA_SRC=$1
if [ -z ${PYSA_SRC} ]; then
    echo "ERROR:Input pysa module path is null"
    exit 3
fi
if ${TARBALL}; then
    if [[ "${PYSA_SRC}" != *".tar.gz" ]]; then
        echo "ERROR:Invalid compressed format!"
        exit 4
    fi
fi
if ${REMOTE}; then     ### need to improve
    if [[ "${PYSA_SRC}" != *"@"*":/"* ]]; then
        echo "ERROR:Invalid remote connection string!"
        exit 5
    fi
fi
if ! ${REMOTE} -a ${CERTIFICATION}; then
    echo "ERROR:Use public key but not from remote server"
    exit 6
fi

# check the os information
check_os
if [ $? -ne 0 ]; then
    echo "ERROR:Check system info failed"
    exit 7
fi

# create directory
if [ ! -d ${DEPS} ]; then
    mkdir -p ${DEPS}
fi
cd ${DEPS}

# check ruby
check_ruby
if [ $? -ne 0 ]; then
    echo "ERROR:Check ruby package failed"
    exit 8
fi

# check puppet
check_puppet
if [ $? -ne 0 ]; then
    echo "ERROR:Check puppet package failed"
    exit 9
fi

#check pysa module
config_pysa
if [ $? -ne 0 ]; then
    echo "ERROR:Check Pysa module failed"
    exit 10
fi

while true; do
    echo "Do you want to apply configuration immediately?[y/n]"
    read yn
    case $yn in
        [yY]* )
            echo "Starting replication ..."
            # apply the pysa module
            puppet apply ${PUPPET_HOME}/manifests/site.pp
            break
            ;;
        [nN]* )
            echo "Exiting ..."
            break
            ;;
        * )
            echo "Please answer yes or no."
            ;;
    esac
done
