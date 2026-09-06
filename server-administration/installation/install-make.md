## 17.3. Building and Installation with Autoconf and Make [#](#INSTALL-MAKE)

[17.3.1. Short Version](install-make.md#INSTALL-SHORT-MAKE)

[17.3.2. Installation Procedure](install-make.md#INSTALL-PROCEDURE-MAKE)

[17.3.3. `configure` Options](install-make.md#CONFIGURE-OPTIONS)

[17.3.4. `configure` Environment Variables](install-make.md#CONFIGURE-ENVVARS)

<a id="INSTALL-SHORT-MAKE"></a>

### 17.3.1. Short Version [#](#INSTALL-SHORT-MAKE)

```

./configure
make
su
make install
adduser postgres
mkdir -p /usr/local/pgsql/data
chown postgres /usr/local/pgsql/data
su - postgres
/usr/local/pgsql/bin/initdb -D /usr/local/pgsql/data
/usr/local/pgsql/bin/pg_ctl -D /usr/local/pgsql/data -l logfile start
/usr/local/pgsql/bin/createdb test
/usr/local/pgsql/bin/psql test
```

The long version is the rest of this
section.

<a id="INSTALL-PROCEDURE-MAKE"></a>

### 17.3.2. Installation Procedure [#](#INSTALL-PROCEDURE-MAKE)

<a id="CONFIGURE"></a>1. **Configuration**

   <a id="id-1.6.4.6.3.2.1.2"></a>

   The first step of the installation procedure is to configure the
   source tree for your system and choose the options you would like.
   This is done by running the `configure` script. For a
   default installation simply enter:

   ```

   ./configure
   ```

   This script will run a number of tests to determine values for various
   system dependent variables and detect any quirks of your
   operating system, and finally will create several files in the
   build tree to record what it found.

   You can also run `configure` in a directory outside
   the source tree, and then build there, if you want to keep the build
   directory separate from the original source files. This procedure is
   called a
   <a id="id-1.6.4.6.3.2.1.4.2"></a>*VPATH*
   build. Here's how:

   ```

   mkdir build_dir
   cd build_dir
   /path/to/source/tree/configure [options go here]
   make
   ```

   The default configuration will build the server and utilities, as
   well as all client applications and interfaces that require only a
   C compiler. All files will be installed under
   `/usr/local/pgsql` by default.

   You can customize the build and installation process by supplying one
   or more command line options to `configure`.
   Typically you would customize the install location, or the set of
   optional features that are built. `configure`
   has a large number of options, which are described in
   [Section 17.3.3](install-make.md#CONFIGURE-OPTIONS).

   Also, `configure` responds to certain environment
   variables, as described in [Section 17.3.4](install-make.md#CONFIGURE-ENVVARS).
   These provide additional ways to customize the configuration.
<a id="BUILD"></a>2. **Build**

   To start the build, type either of:

   ```

   make
   make all
   ```

   (Remember to use GNU make.)
   The build will take a few minutes depending on your
   hardware.

   If you want to build everything that can be built, including the
   documentation (HTML and man pages), and the additional modules
   (`contrib`), type instead:

   ```

   make world
   ```

   If you want to build everything that can be built, including the
   additional modules (`contrib`), but without
   the documentation, type instead:

   ```

   make world-bin
   ```

   If you want to invoke the build from another makefile rather than
   manually, you must unset `MAKELEVEL` or set it to zero,
   for instance like this:

   ```

   build-postgresql:
           $(MAKE) -C postgresql MAKELEVEL=0 all
   ```

   Failure to do that can lead to strange error messages, typically about
   missing header files.
3. **Regression Tests**

   <a id="id-1.6.4.6.3.2.3.2"></a>

   If you want to test the newly built server before you install it,
   you can run the regression tests at this point. The regression
   tests are a test suite to verify that PostgreSQL
   runs on your machine in the way the developers expected it
   to. Type:

   ```

   make check
   ```

   (This won't work as root; do it as an unprivileged user.)
   See [Chapter 31](../regress/README.md) for
   detailed information about interpreting the test results. You can
   repeat this test at any later time by issuing the same command.
<a id="INSTALL"></a>4. **Installing the Files**

   ### Note

   If you are upgrading an existing system be sure to read
   [Section 18.6](../runtime/upgrading.md),
   which has instructions about upgrading a
   cluster.

   To install PostgreSQL enter:

   ```

   make install
   ```

   This will install files into the directories that were specified
   in [Step 1](install-make.md#CONFIGURE). Make sure that you have appropriate
   permissions to write into that area. Normally you need to do this
   step as root. Alternatively, you can create the target
   directories in advance and arrange for appropriate permissions to
   be granted.

   To install the documentation (HTML and man pages), enter:

   ```

   make install-docs
   ```

   If you built the world above, type instead:

   ```

   make install-world
   ```

   This also installs the documentation.

   If you built the world without the documentation above, type instead:

   ```

   make install-world-bin
   ```

   You can use `make install-strip` instead of
   `make install` to strip the executable files and
   libraries as they are installed. This will save some space. If
   you built with debugging support, stripping will effectively
   remove the debugging support, so it should only be done if
   debugging is no longer needed. `install-strip`
   tries to do a reasonable job saving space, but it does not have
   perfect knowledge of how to strip every unneeded byte from an
   executable file, so if you want to save all the disk space you
   possibly can, you will have to do manual work.

   The standard installation provides all the header files needed for client
   application development as well as for server-side program
   development, such as custom functions or data types written in C.

   **Client-only installation:**
   If you want to install only the client applications and
   interface libraries, then you can use these commands:

   ```

   make -C src/bin install
   make -C src/include install
   make -C src/interfaces install
   make -C doc install
   ```

   `src/bin` has a few binaries for server-only use,
   but they are small.

**Uninstallation:**
To undo the installation use the command `make
uninstall`. However, this will not remove any created directories.

**Cleaning:**
After the installation you can free disk space by removing the built
files from the source tree with the command `make
clean`. This will preserve the files made by the `configure`
program, so that you can rebuild everything with `make`
later on. To reset the source tree to the state in which it was
distributed, use `make distclean`. If you are going to
build for several platforms within the same source tree you must do
this and re-configure for each platform. (Alternatively, use
a separate build tree for each platform, so that the source tree
remains unmodified.)

If you perform a build and then discover that your `configure`
options were wrong, or if you change anything that `configure`
investigates (for example, software upgrades), then it's a good
idea to do `make distclean` before reconfiguring and
rebuilding. Without this, your changes in configuration choices
might not propagate everywhere they need to.

<a id="CONFIGURE-OPTIONS"></a>

### 17.3.3. `configure` Options [#](#CONFIGURE-OPTIONS)

<a id="id-1.6.4.6.4.2"></a>

`configure`'s command line options are explained below.
This list is not exhaustive (use `./configure --help`
to get one that is). The options not covered here are meant for
advanced use-cases such as cross-compilation, and are documented in
the standard Autoconf documentation.

<a id="CONFIGURE-OPTIONS-LOCATIONS"></a>

#### 17.3.3.1. Installation Locations [#](#CONFIGURE-OPTIONS-LOCATIONS)

These options control where `make install` will put
the files. The `--prefix` option is sufficient for
most cases. If you have special needs, you can customize the
installation subdirectories with the other options described in this
section. Beware however that changing the relative locations of the
different subdirectories may render the installation non-relocatable,
meaning you won't be able to move it after installation.
(The `man` and `doc` locations are
not affected by this restriction.) For relocatable installs, you
might want to use the `--disable-rpath` option
described later.

<a id="CONFIGURE-OPTION-PREFIX"></a>

`--prefix=PREFIX` [#](#CONFIGURE-OPTION-PREFIX)
:   Install all files under the directory *`PREFIX`*
    instead of `/usr/local/pgsql`. The actual
    files will be installed into various subdirectories; no files
    will ever be installed directly into the
    *`PREFIX`* directory.
<a id="CONFIGURE-OPTION-EXEC-PREFIX"></a>

`--exec-prefix=EXEC-PREFIX` [#](#CONFIGURE-OPTION-EXEC-PREFIX)
:   You can install architecture-dependent files under a
    different prefix, *`EXEC-PREFIX`*, than what
    *`PREFIX`* was set to. This can be useful to
    share architecture-independent files between hosts. If you
    omit this, then *`EXEC-PREFIX`* is set equal to
    *`PREFIX`* and both architecture-dependent and
    independent files will be installed under the same tree,
    which is probably what you want.
<a id="CONFIGURE-OPTION-BINDIR"></a>

`--bindir=DIRECTORY` [#](#CONFIGURE-OPTION-BINDIR)
:   Specifies the directory for executable programs. The default
    is `EXEC-PREFIX/bin`, which
    normally means `/usr/local/pgsql/bin`.
<a id="CONFIGURE-OPTION-SYSCONFDIR"></a>

`--sysconfdir=DIRECTORY` [#](#CONFIGURE-OPTION-SYSCONFDIR)
:   Sets the directory for various configuration files,
    `PREFIX/etc` by default.
<a id="CONFIGURE-OPTION-LIBDIR"></a>

`--libdir=DIRECTORY` [#](#CONFIGURE-OPTION-LIBDIR)
:   Sets the location to install libraries and dynamically loadable
    modules. The default is
    `EXEC-PREFIX/lib`.
<a id="CONFIGURE-OPTION-INCLUDEDIR"></a>

`--includedir=DIRECTORY` [#](#CONFIGURE-OPTION-INCLUDEDIR)
:   Sets the directory for installing C and C++ header files. The
    default is `PREFIX/include`.
<a id="CONFIGURE-OPTION-DATAROOTDIR"></a>

`--datarootdir=DIRECTORY` [#](#CONFIGURE-OPTION-DATAROOTDIR)
:   Sets the root directory for various types of read-only data
    files. This only sets the default for some of the following
    options. The default is
    `PREFIX/share`.
<a id="CONFIGURE-OPTION-DATADIR"></a>

`--datadir=DIRECTORY` [#](#CONFIGURE-OPTION-DATADIR)
:   Sets the directory for read-only data files used by the
    installed programs. The default is
    `DATAROOTDIR`. Note that this has
    nothing to do with where your database files will be placed.
<a id="CONFIGURE-OPTION-LOCALEDIR"></a>

`--localedir=DIRECTORY` [#](#CONFIGURE-OPTION-LOCALEDIR)
:   Sets the directory for installing locale data, in particular
    message translation catalog files. The default is
    `DATAROOTDIR/locale`.
<a id="CONFIGURE-OPTION-MANDIR"></a>

`--mandir=DIRECTORY` [#](#CONFIGURE-OPTION-MANDIR)
:   The man pages that come with PostgreSQL will be installed under
    this directory, in their respective
    `manx` subdirectories.
    The default is `DATAROOTDIR/man`.
<a id="CONFIGURE-OPTION-DOCDIR"></a>

`--docdir=DIRECTORY` [#](#CONFIGURE-OPTION-DOCDIR)
:   Sets the root directory for installing documentation files,
    except “man” pages. This only sets the default for
    the following options. The default value for this option is
    `DATAROOTDIR/doc/postgresql`.
<a id="CONFIGURE-OPTION-HTMLDIR"></a>

`--htmldir=DIRECTORY` [#](#CONFIGURE-OPTION-HTMLDIR)
:   The HTML-formatted documentation for
    PostgreSQL will be installed under
    this directory. The default is
    `DATAROOTDIR`.

### Note

Care has been taken to make it possible to install
PostgreSQL into shared installation locations
(such as `/usr/local/include`) without
interfering with the namespace of the rest of the system. First,
the string “`/postgresql`” is
automatically appended to `datadir`,
`sysconfdir`, and `docdir`,
unless the fully expanded directory name already contains the
string “`postgres`” or
“`pgsql`”. For example, if you choose
`/usr/local` as prefix, the documentation will
be installed in `/usr/local/doc/postgresql`,
but if the prefix is `/opt/postgres`, then it
will be in `/opt/postgres/doc`. The public C
header files of the client interfaces are installed into
`includedir` and are namespace-clean. The
internal header files and the server header files are installed
into private directories under `includedir`. See
the documentation of each interface for information about how to
access its header files. Finally, a private subdirectory will
also be created, if appropriate, under `libdir`
for dynamically loadable modules.

<a id="CONFIGURE-OPTIONS-FEATURES"></a>

#### 17.3.3.2. PostgreSQL Features [#](#CONFIGURE-OPTIONS-FEATURES)

The options described in this section enable building of
various PostgreSQL features that are not
built by default. Most of these are non-default only because they
require additional software, as described in
[Section 17.1](install-requirements.md).

<a id="CONFIGURE-OPTION-ENABLE-NLS"></a>

`--enable-nls[=LANGUAGES]` [#](#CONFIGURE-OPTION-ENABLE-NLS)
:   Enables Native Language Support (NLS),
    that is, the ability to display a program's messages in a
    language other than English.
    *`LANGUAGES`* is an optional space-separated
    list of codes of the languages that you want supported, for
    example `--enable-nls='de fr'`. (The intersection
    between your list and the set of actually provided
    translations will be computed automatically.) If you do not
    specify a list, then all available translations are
    installed.

    To use this option, you will need an implementation of the
    Gettext API.
<a id="CONFIGURE-OPTION-WITH-PERL"></a>

`--with-perl` [#](#CONFIGURE-OPTION-WITH-PERL)
:   Build the PL/Perl server-side language.
<a id="CONFIGURE-OPTION-WITH-PYTHON"></a>

`--with-python` [#](#CONFIGURE-OPTION-WITH-PYTHON)
:   Build the PL/Python server-side language.
<a id="CONFIGURE-OPTION-WITH-TCL"></a>

`--with-tcl` [#](#CONFIGURE-OPTION-WITH-TCL)
:   Build the PL/Tcl server-side language.
<a id="CONFIGURE-OPTION-WITH-TCLCONFIG"></a>

`--with-tclconfig=DIRECTORY` [#](#CONFIGURE-OPTION-WITH-TCLCONFIG)
:   Tcl installs the file `tclConfig.sh`, which
    contains configuration information needed to build modules
    interfacing to Tcl. This file is normally found automatically
    at a well-known location, but if you want to use a different
    version of Tcl you can specify the directory in which to look
    for `tclConfig.sh`.
<a id="CONFIGURE-WITH-LLVM"></a>

`--with-llvm` [#](#CONFIGURE-WITH-LLVM)
:   Build with support for LLVM based
    JIT compilation (see [Chapter 30](../jit/README.md)). This
    requires the LLVM library to be installed.
    The minimum required version of LLVM is
    currently 14.

    `llvm-config`<a id="id-1.6.4.6.4.5.3.6.2.2.2"></a>
    will be used to find the required compilation options.
    `llvm-config` will be searched for in your
    `PATH`. If that would not yield the desired program,
    use `LLVM_CONFIG` to specify a path to the correct
    `llvm-config`. For example

    ```

    ./configure ... --with-llvm LLVM_CONFIG='/path/to/llvm/bin/llvm-config'
    ```

    LLVM support requires a compatible
    `clang` compiler (specified, if necessary, using the
    `CLANG` environment variable), and a working C++
    compiler (specified, if necessary, using the `CXX`
    environment variable).
<a id="CONFIGURE-OPTION-WITH-LZ4"></a>

`--with-lz4` [#](#CONFIGURE-OPTION-WITH-LZ4)
:   Build with LZ4 compression support.
<a id="CONFIGURE-OPTION-WITH-ZSTD"></a>

`--with-zstd` [#](#CONFIGURE-OPTION-WITH-ZSTD)
:   Build with Zstandard compression support.
<a id="CONFIGURE-OPTION-WITH-SSL"></a>

`--with-ssl=LIBRARY` <a id="id-1.6.4.6.4.5.3.9.1.2"></a> [#](#CONFIGURE-OPTION-WITH-SSL)
:   Build with support for SSL (encrypted)
    connections. The only *`LIBRARY`*
    supported is `openssl`, which is used for both
    OpenSSL
    and LibreSSL. This requires the
    OpenSSL package to be installed.
    `configure` will check for the required
    header files and libraries to make sure that your
    OpenSSL installation is sufficient
    before proceeding.
<a id="CONFIGURE-OPTION-WITH-OPENSSL"></a>

`--with-openssl` [#](#CONFIGURE-OPTION-WITH-OPENSSL)
:   Obsolete equivalent of `--with-ssl=openssl`.
<a id="CONFIGURE-OPTION-WITH-GSSAPI"></a>

`--with-gssapi` [#](#CONFIGURE-OPTION-WITH-GSSAPI)
:   Build with support for GSSAPI authentication. MIT Kerberos is required
    to be installed for GSSAPI. On many systems, the GSSAPI system (a part
    of the MIT Kerberos installation) is not installed in a location
    that is searched by default (e.g., `/usr/include`,
    `/usr/lib`), so you must use the options
    `--with-includes` and `--with-libraries` in
    addition to this option. `configure` will check
    for the required header files and libraries to make sure that
    your GSSAPI installation is sufficient before proceeding.
<a id="CONFIGURE-OPTION-WITH-LDAP"></a>

`--with-ldap` [#](#CONFIGURE-OPTION-WITH-LDAP)
:   Build with LDAP<a id="id-1.6.4.6.4.5.3.12.2.1.2"></a>
    support for authentication and connection parameter lookup (see
    <a id="INSTALL-LDAP-LINKS"></a>[Section 32.18](../../client-interfaces/libpq/libpq-ldap.md) and
    [Section 20.10](../client-authentication/auth-ldap.md) for more information). On Unix,
    this requires the OpenLDAP package to be
    installed. On Windows, the default WinLDAP
    library is used. `configure` will check for the required
    header files and libraries to make sure that your
    OpenLDAP installation is sufficient before
    proceeding.
<a id="CONFIGURE-OPTION-WITH-PAM"></a>

`--with-pam` [#](#CONFIGURE-OPTION-WITH-PAM)
:   Build with PAM<a id="id-1.6.4.6.4.5.3.13.2.1.2"></a>
    (Pluggable Authentication Modules) support.
<a id="CONFIGURE-OPTION-WITH-BSD-AUTH"></a>

`--with-bsd-auth` [#](#CONFIGURE-OPTION-WITH-BSD-AUTH)
:   Build with BSD Authentication support.
    (The BSD Authentication framework is
    currently only available on OpenBSD.)
<a id="CONFIGURE-OPTION-WITH-SYSTEMD"></a>

`--with-systemd` [#](#CONFIGURE-OPTION-WITH-SYSTEMD)
:   Build with support
    for systemd<a id="id-1.6.4.6.4.5.3.15.2.1.2"></a>
    service notifications. This improves integration if the server
    is started under systemd but has no impact
    otherwise; see [Section 18.3](../runtime/server-start.md) for more
    information. libsystemd and the
    associated header files need to be installed to use this option.
<a id="CONFIGURE-OPTION-WITH-BONJOUR"></a>

`--with-bonjour` [#](#CONFIGURE-OPTION-WITH-BONJOUR)
:   Build with support for Bonjour automatic service discovery.
    This requires Bonjour support in your operating system.
    Recommended on macOS.
<a id="CONFIGURE-OPTION-WITH-UUID"></a>

`--with-uuid=LIBRARY` [#](#CONFIGURE-OPTION-WITH-UUID)
:   Build the [uuid-ossp](../../appendixes/contrib/uuid-ossp.md) module
    (which provides functions to generate UUIDs), using the specified
    UUID library.<a id="id-1.6.4.6.4.5.3.17.2.1.2"></a>
    *`LIBRARY`* must be one of:

    * `bsd` to use the UUID functions found in FreeBSD
      and some other BSD-derived systems
    * `e2fs` to use the UUID library created by
      the `e2fsprogs` project; this library is present in most
      Linux systems and in macOS, and can be obtained for other
      platforms as well
    * `ossp` to use the [OSSP UUID library](http://www.ossp.org/pkg/lib/uuid/)
<a id="CONFIGURE-OPTION-WITH-OSSP-UUID"></a>

`--with-ossp-uuid` [#](#CONFIGURE-OPTION-WITH-OSSP-UUID)
:   Obsolete equivalent of `--with-uuid=ossp`.
<a id="CONFIGURE-OPTION-WITH-LIBCURL"></a>

`--with-libcurl` [#](#CONFIGURE-OPTION-WITH-LIBCURL)
:   Build with libcurl support for OAuth 2.0 client flows.
    Libcurl version 7.61.0 or later is required for this feature.
    Building with this will check for the required header files
    and libraries to make sure that your curl
    installation is sufficient before proceeding.
<a id="CONFIGURE-OPTION-WITH-LIBNUMA"></a>

`--with-libnuma` [#](#CONFIGURE-OPTION-WITH-LIBNUMA)
:   Build with libnuma support for basic NUMA support.
    Only supported on platforms for which the libnuma
    library is implemented.
<a id="CONFIGURE-OPTION-WITH-LIBURING"></a>

`--with-liburing` [#](#CONFIGURE-OPTION-WITH-LIBURING)
:   Build with liburing, enabling io_uring support for asynchronous I/O.

    To detect the required compiler and linker options, PostgreSQL will
    query `pkg-config`.

    To use a liburing installation that is in an unusual location, you
    can set `pkg-config`-related environment
    variables (see its documentation).
<a id="CONFIGURE-OPTION-WITH-LIBXML"></a>

`--with-libxml` [#](#CONFIGURE-OPTION-WITH-LIBXML)
:   Build with libxml2, enabling SQL/XML support. Libxml2 version 2.6.23 or
    later is required for this feature.

    To detect the required compiler and linker options, PostgreSQL will
    query `pkg-config`, if that is installed and knows
    about libxml2. Otherwise the program `xml2-config`,
    which is installed by libxml2, will be used if it is found. Use
    of `pkg-config` is preferred, because it can deal
    with multi-architecture installations better.

    To use a libxml2 installation that is in an unusual location, you
    can set `pkg-config`-related environment
    variables (see its documentation), or set the environment variable
    `XML2_CONFIG` to point to
    the `xml2-config` program belonging to the libxml2
    installation, or set the variables `XML2_CFLAGS`
    and `XML2_LIBS`. (If `pkg-config` is
    installed, then to override its idea of where libxml2 is you must
    either set `XML2_CONFIG` or set
    both `XML2_CFLAGS` and `XML2_LIBS` to
    nonempty strings.)
<a id="CONFIGURE-OPTION-WITH-LIBXSLT"></a>

`--with-libxslt` [#](#CONFIGURE-OPTION-WITH-LIBXSLT)
:   Build with libxslt, enabling the
    [xml2](../../appendixes/contrib/xml2.md)
    module to perform XSL transformations of XML.
    `--with-libxml` must be specified as well.
<a id="CONFIGURE-OPTION-WITH-SEPGSQL"></a>

`--with-selinux` [#](#CONFIGURE-OPTION-WITH-SEPGSQL)
:   Build with SElinux support, enabling the [sepgsql](../../appendixes/contrib/sepgsql.md)
    extension.

<a id="CONFIGURE-OPTIONS-ANTI-FEATURES"></a>

#### 17.3.3.3. Anti-Features [#](#CONFIGURE-OPTIONS-ANTI-FEATURES)

The options described in this section allow disabling
certain PostgreSQL features that are built
by default, but which might need to be turned off if the required
software or system features are not available. Using these options is
not recommended unless really necessary.

<a id="CONFIGURE-OPTION-WITHOUT-ICU"></a>

`--without-icu` [#](#CONFIGURE-OPTION-WITHOUT-ICU)
:   Build without support for the
    ICU<a id="id-1.6.4.6.4.6.3.1.2.1.2"></a>
    library, disabling the use of ICU collation features (see [Section 23.2](../charset/collation.md)).
<a id="CONFIGURE-OPTION-WITHOUT-READLINE"></a>

`--without-readline` [#](#CONFIGURE-OPTION-WITHOUT-READLINE)
:   Prevents use of the Readline library
    (and libedit as well). This option disables
    command-line editing and history in
    psql.
<a id="CONFIGURE-OPTION-WITH-LIBEDIT-PREFERRED"></a>

`--with-libedit-preferred` [#](#CONFIGURE-OPTION-WITH-LIBEDIT-PREFERRED)
:   Favors the use of the BSD-licensed libedit library
    rather than GPL-licensed Readline. This option
    is significant only if you have both libraries installed; the
    default in that case is to use Readline.
<a id="CONFIGURE-OPTION-WITHOUT-ZLIB"></a>

`--without-zlib` [#](#CONFIGURE-OPTION-WITHOUT-ZLIB)
:   <a id="id-1.6.4.6.4.6.3.4.2.1.1"></a>
    Prevents use of the Zlib library.
    This disables
    support for compressed archives in pg_dump
    and pg_restore.

<a id="CONFIGURE-OPTIONS-BUILD-PROCESS"></a>

#### 17.3.3.4. Build Process Details [#](#CONFIGURE-OPTIONS-BUILD-PROCESS)

<a id="CONFIGURE-OPTION-WITH-INCLUDES"></a>

`--with-includes=DIRECTORIES` [#](#CONFIGURE-OPTION-WITH-INCLUDES)
:   *`DIRECTORIES`* is a colon-separated list of
    directories that will be added to the list the compiler
    searches for header files. If you have optional packages
    (such as GNU Readline) installed in a non-standard
    location,
    you have to use this option and probably also the corresponding
    `--with-libraries` option.

    Example: `--with-includes=/opt/gnu/include:/usr/sup/include`.
<a id="CONFIGURE-OPTION-WITH-LIBRARIES"></a>

`--with-libraries=DIRECTORIES` [#](#CONFIGURE-OPTION-WITH-LIBRARIES)
:   *`DIRECTORIES`* is a colon-separated list of
    directories to search for libraries. You will probably have
    to use this option (and the corresponding
    `--with-includes` option) if you have packages
    installed in non-standard locations.

    Example: `--with-libraries=/opt/gnu/lib:/usr/sup/lib`.
<a id="CONFIGURE-OPTION-WITH-SYSTEM-TZDATA"></a>

`--with-system-tzdata=DIRECTORY` <a id="id-1.6.4.6.4.7.2.3.1.2"></a> [#](#CONFIGURE-OPTION-WITH-SYSTEM-TZDATA)
:   PostgreSQL includes its own time zone database,
    which it requires for date and time operations. This time zone
    database is in fact compatible with the IANA time zone
    database provided by many operating systems such as FreeBSD,
    Linux, and Solaris, so it would be redundant to install it again.
    When this option is used, the system-supplied time zone database
    in *`DIRECTORY`* is used instead of the one
    included in the PostgreSQL source distribution.
    *`DIRECTORY`* must be specified as an
    absolute path. `/usr/share/zoneinfo` is a
    likely directory on some operating systems. Note that the
    installation routine will not detect mismatching or erroneous time
    zone data. If you use this option, you are advised to run the
    regression tests to verify that the time zone data you have
    pointed to works correctly with PostgreSQL.

    <a id="id-1.6.4.6.4.7.2.3.2.2"></a>

    This option is mainly aimed at binary package distributors
    who know their target operating system well. The main
    advantage of using this option is that the PostgreSQL package
    won't need to be upgraded whenever any of the many local
    daylight-saving time rules change. Another advantage is that
    PostgreSQL can be cross-compiled more straightforwardly if the
    time zone database files do not need to be built during the
    installation.
<a id="CONFIGURE-OPTION-WITH-EXTRA-VERSION"></a>

`--with-extra-version=STRING` [#](#CONFIGURE-OPTION-WITH-EXTRA-VERSION)
:   Append *`STRING`* to the PostgreSQL version number. You
    can use this, for example, to mark binaries built from unreleased Git
    snapshots or containing custom patches with an extra version string,
    such as a `git describe` identifier or a
    distribution package release number.
<a id="CONFIGURE-OPTION-DISABLE-RPATH"></a>

`--disable-rpath` [#](#CONFIGURE-OPTION-DISABLE-RPATH)
:   Do not mark PostgreSQL's executables
    to indicate that they should search for shared libraries in the
    installation's library directory (see `--libdir`).
    On most platforms, this marking uses an absolute path to the
    library directory, so that it will be unhelpful if you relocate
    the installation later. However, you will then need to provide
    some other way for the executables to find the shared libraries.
    Typically this requires configuring the operating system's
    dynamic linker to search the library directory; see
    [Section 17.5.1](install-post.md#INSTALL-POST-SHLIBS) for more detail.

<a id="CONFIGURE-OPTIONS-MISC"></a>

#### 17.3.3.5. Miscellaneous [#](#CONFIGURE-OPTIONS-MISC)

It's fairly common, particularly for test builds, to adjust the
default port number with `--with-pgport`.
The other options in this section are recommended only for advanced
users.

<a id="CONFIGURE-OPTION-WITH-PGPORT"></a>

`--with-pgport=NUMBER` [#](#CONFIGURE-OPTION-WITH-PGPORT)
:   Set *`NUMBER`* as the default port number for
    server and clients. The default is 5432. The port can always
    be changed later on, but if you specify it here then both
    server and clients will have the same default compiled in,
    which can be very convenient. Usually the only good reason
    to select a non-default value is if you intend to run multiple
    PostgreSQL servers on the same machine.
<a id="CONFIGURE-OPTION-WITH-KRB-SRVNAM"></a>

`--with-krb-srvnam=NAME` [#](#CONFIGURE-OPTION-WITH-KRB-SRVNAM)
:   The default name of the Kerberos service principal used
    by GSSAPI.
    `postgres` is the default. There's usually no
    reason to change this unless you are building for a Windows
    environment, in which case it must be set to upper case
    `POSTGRES`.
<a id="CONFIGURE-OPTION-WITH-SEGSIZE"></a>

`--with-segsize=SEGSIZE` [#](#CONFIGURE-OPTION-WITH-SEGSIZE)
:   Set the *segment size*, in gigabytes. Large tables are
    divided into multiple operating-system files, each of size equal
    to the segment size. This avoids problems with file size limits
    that exist on many platforms. The default segment size, 1 gigabyte,
    is safe on all supported platforms. If your operating system has
    “largefile” support (which most do, nowadays), you can use
    a larger segment size. This can be helpful to reduce the number of
    file descriptors consumed when working with very large tables.
    But be careful not to select a value larger than is supported
    by your platform and the file systems you intend to use. Other
    tools you might wish to use, such as tar, could
    also set limits on the usable file size.
    It is recommended, though not absolutely required, that this value
    be a power of 2.
    Note that changing this value breaks on-disk database compatibility,
    meaning you cannot use `pg_upgrade` to upgrade to
    a build with a different segment size.
<a id="CONFIGURE-OPTION-WITH-BLOCKSIZE"></a>

`--with-blocksize=BLOCKSIZE` [#](#CONFIGURE-OPTION-WITH-BLOCKSIZE)
:   Set the *block size*, in kilobytes. This is the unit
    of storage and I/O within tables. The default, 8 kilobytes,
    is suitable for most situations; but other values may be useful
    in special cases.
    The value must be a power of 2 between 1 and 32 (kilobytes).
    Note that changing this value breaks on-disk database compatibility,
    meaning you cannot use `pg_upgrade` to upgrade to
    a build with a different block size.
<a id="CONFIGURE-OPTION-WITH-WAL-BLOCKSIZE"></a>

`--with-wal-blocksize=BLOCKSIZE` [#](#CONFIGURE-OPTION-WITH-WAL-BLOCKSIZE)
:   Set the *WAL block size*, in kilobytes. This is the unit
    of storage and I/O within the WAL log. The default, 8 kilobytes,
    is suitable for most situations; but other values may be useful
    in special cases.
    The value must be a power of 2 between 1 and 64 (kilobytes).
    Note that changing this value breaks on-disk database compatibility,
    meaning you cannot use `pg_upgrade` to upgrade to
    a build with a different WAL block size.

<a id="CONFIGURE-OPTIONS-DEVEL"></a>

#### 17.3.3.6. Developer Options [#](#CONFIGURE-OPTIONS-DEVEL)

Most of the options in this section are only of interest for
developing or debugging PostgreSQL.
They are not recommended for production builds, except
for `--enable-debug`, which can be useful to enable
detailed bug reports in the unlucky event that you encounter a bug.
On platforms supporting DTrace, `--enable-dtrace`
may also be reasonable to use in production.

When building an installation that will be used to develop code inside
the server, it is recommended to use at least the
options `--enable-debug`
and `--enable-cassert`.

<a id="CONFIGURE-OPTION-ENABLE-DEBUG"></a>

`--enable-debug` [#](#CONFIGURE-OPTION-ENABLE-DEBUG)
:   Compiles all programs and libraries with debugging symbols.
    This means that you can run the programs in a debugger
    to analyze problems. This enlarges the size of the installed
    executables considerably, and on non-GCC compilers it usually
    also disables compiler optimization, causing slowdowns. However,
    having the symbols available is extremely helpful for dealing
    with any problems that might arise. Currently, this option is
    recommended for production installations only if you use GCC.
    But you should always have it on if you are doing development work
    or running a beta version.
<a id="CONFIGURE-OPTION-ENABLE-CASSERT"></a>

`--enable-cassert` [#](#CONFIGURE-OPTION-ENABLE-CASSERT)
:   Enables *assertion* checks in the server, which test for
    many “cannot happen” conditions. This is invaluable for
    code development purposes, but the tests can slow down the
    server significantly.
    Also, having the tests turned on won't necessarily enhance the
    stability of your server! The assertion checks are not categorized
    for severity, and so what might be a relatively harmless bug will
    still lead to server restarts if it triggers an assertion
    failure. This option is not recommended for production use, but
    you should have it on for development work or when running a beta
    version.
<a id="CONFIGURE-OPTION-ENABLE-TAP-TESTS"></a>

`--enable-tap-tests` [#](#CONFIGURE-OPTION-ENABLE-TAP-TESTS)
:   Enable tests using the Perl TAP tools. This requires a Perl
    installation and the Perl module `IPC::Run`.
    See [Section 31.4](../regress/regress-tap.md) for more information.
<a id="CONFIGURE-OPTION-ENABLE-DEPEND"></a>

`--enable-depend` [#](#CONFIGURE-OPTION-ENABLE-DEPEND)
:   Enables automatic dependency tracking. With this option, the
    makefiles are set up so that all affected object files will
    be rebuilt when any header file is changed. This is useful
    if you are doing development work, but is just wasted overhead
    if you intend only to compile once and install. At present,
    this option only works with GCC.
<a id="CONFIGURE-OPTION-ENABLE-COVERAGE"></a>

`--enable-coverage` [#](#CONFIGURE-OPTION-ENABLE-COVERAGE)
:   If using GCC, all programs and libraries are compiled with
    code coverage testing instrumentation. When run, they
    generate files in the build directory with code coverage
    metrics.
    See [Section 31.5](../regress/regress-coverage.md)
    for more information. This option is for use only with GCC
    and when doing development work.
<a id="CONFIGURE-OPTION-ENABLE-PROFILING"></a>

`--enable-profiling` [#](#CONFIGURE-OPTION-ENABLE-PROFILING)
:   If using GCC, all programs and libraries are compiled so they
    can be profiled. On backend exit, a subdirectory will be created
    that contains the `gmon.out` file containing
    profile data.
    This option is for use only with GCC and when doing development work.
<a id="CONFIGURE-OPTION-ENABLE-DTRACE"></a>

`--enable-dtrace` [#](#CONFIGURE-OPTION-ENABLE-DTRACE)
:   <a id="id-1.6.4.6.4.9.4.7.2.1.1"></a>
    Compiles PostgreSQL with support for the
    dynamic tracing tool DTrace.
    See [Section 27.5](../monitoring/dynamic-trace.md) for more information.

    To point to the `dtrace` program, the
    environment variable `DTRACE` can be set. This
    will often be necessary because `dtrace` is
    typically installed under `/usr/sbin`,
    which might not be in your `PATH`.

    Extra command-line options for the `dtrace` program
    can be specified in the environment variable
    `DTRACEFLAGS`. On Solaris,
    to include DTrace support in a 64-bit binary, you must specify
    `DTRACEFLAGS="-64"`. For example,
    using the GCC compiler:

    ```

    ./configure CC='gcc -m64' --enable-dtrace DTRACEFLAGS='-64' ...
    ```

    Using Sun's compiler:

    ```

    ./configure CC='/opt/SUNWspro/bin/cc -xtarget=native64' --enable-dtrace DTRACEFLAGS='-64' ...
    ```
<a id="CONFIGURE-OPTION-ENABLE-INJECTION-POINTS"></a>

`--enable-injection-points` [#](#CONFIGURE-OPTION-ENABLE-INJECTION-POINTS)
:   Compiles PostgreSQL with support for
    injection points in the server. Injection points allow to run
    user-defined code from within the server in pre-defined code paths.
    This helps in testing and in the investigation of concurrency scenarios
    in a controlled fashion. This option is disabled by default. See
    [Section 36.10.14](../../server-programming/extend/xfunc-c.md#XFUNC-ADDIN-INJECTION-POINTS) for more details. This
    option is intended to be used only by developers for testing.
<a id="CONFIGURE-OPTION-WITH-SEGSIZE-BLOCKS"></a>

`--with-segsize-blocks=SEGSIZE_BLOCKS` [#](#CONFIGURE-OPTION-WITH-SEGSIZE-BLOCKS)
:   Specify the relation segment size in blocks. If both
    `--with-segsize` and this option are specified, this
    option wins.
    This option is only for developers, to test segment related code.

<a id="CONFIGURE-ENVVARS"></a>

### 17.3.4. `configure` Environment Variables [#](#CONFIGURE-ENVVARS)

<a id="id-1.6.4.6.5.2"></a>

In addition to the ordinary command-line options described above,
`configure` responds to a number of environment
variables.
You can specify environment variables on the
`configure` command line, for example:

```

./configure CC=/opt/bin/gcc CFLAGS='-O2 -pipe'
```

In this usage an environment variable is little different from a
command-line option.
You can also set such variables beforehand:

```

export CC=/opt/bin/gcc
export CFLAGS='-O2 -pipe'
./configure
```

This usage can be convenient because many programs' configuration
scripts respond to these variables in similar ways.

The most commonly used of these environment variables are
`CC` and `CFLAGS`.
If you prefer a C compiler different from the one
`configure` picks, you can set the
variable `CC` to the program of your choice.
By default, `configure` will pick
`gcc` if available, else the platform's
default (usually `cc`). Similarly, you can override the
default compiler flags if needed with the `CFLAGS` variable.

Here is a list of the significant variables that can be set in
this manner:

<a id="CONFIGURE-ENVVARS-BISON"></a>

`BISON` [#](#CONFIGURE-ENVVARS-BISON)
:   Bison program
<a id="CONFIGURE-ENVVARS-CC"></a>

`CC` [#](#CONFIGURE-ENVVARS-CC)
:   C compiler
<a id="CONFIGURE-ENVVARS-CFLAGS"></a>

`CFLAGS` [#](#CONFIGURE-ENVVARS-CFLAGS)
:   options to pass to the C compiler
<a id="CONFIGURE-ENVVARS-CLANG"></a>

`CLANG` [#](#CONFIGURE-ENVVARS-CLANG)
:   path to `clang` program used to process source code
    for inlining when compiling with `--with-llvm`
<a id="CONFIGURE-ENVVARS-CPP"></a>

`CPP` [#](#CONFIGURE-ENVVARS-CPP)
:   C preprocessor
<a id="CONFIGURE-ENVVARS-CPPFLAGS"></a>

`CPPFLAGS` [#](#CONFIGURE-ENVVARS-CPPFLAGS)
:   options to pass to the C preprocessor
<a id="CONFIGURE-ENVVARS-CXX"></a>

`CXX` [#](#CONFIGURE-ENVVARS-CXX)
:   C++ compiler
<a id="CONFIGURE-ENVVARS-CXXFLAGS"></a>

`CXXFLAGS` [#](#CONFIGURE-ENVVARS-CXXFLAGS)
:   options to pass to the C++ compiler
<a id="CONFIGURE-ENVVARS-DTRACE"></a>

`DTRACE` [#](#CONFIGURE-ENVVARS-DTRACE)
:   location of the `dtrace` program
<a id="CONFIGURE-ENVVARS-DTRACEFLAGS"></a>

`DTRACEFLAGS` [#](#CONFIGURE-ENVVARS-DTRACEFLAGS)
:   options to pass to the `dtrace` program
<a id="CONFIGURE-ENVVARS-FLEX"></a>

`FLEX` [#](#CONFIGURE-ENVVARS-FLEX)
:   Flex program
<a id="CONFIGURE-ENVVARS-LDFLAGS"></a>

`LDFLAGS` [#](#CONFIGURE-ENVVARS-LDFLAGS)
:   options to use when linking either executables or shared libraries
<a id="CONFIGURE-ENVVARS-LDFLAGS-EX"></a>

`LDFLAGS_EX` [#](#CONFIGURE-ENVVARS-LDFLAGS-EX)
:   additional options for linking executables only
<a id="CONFIGURE-ENVVARS-LDFLAGS-SL"></a>

`LDFLAGS_SL` [#](#CONFIGURE-ENVVARS-LDFLAGS-SL)
:   additional options for linking shared libraries only
<a id="CONFIGURE-ENVVARS-LLVM-CONFIG"></a>

`LLVM_CONFIG` [#](#CONFIGURE-ENVVARS-LLVM-CONFIG)
:   `llvm-config` program used to locate the
    LLVM installation
<a id="CONFIGURE-ENVVARS-MSGFMT"></a>

`MSGFMT` [#](#CONFIGURE-ENVVARS-MSGFMT)
:   `msgfmt` program for native language support
<a id="CONFIGURE-ENVVARS-PERL"></a>

`PERL` [#](#CONFIGURE-ENVVARS-PERL)
:   Perl interpreter program. This will be used to determine the
    dependencies for building PL/Perl. The default is
    `perl`.
<a id="CONFIGURE-ENVVARS-PYTHON"></a>

`PYTHON` [#](#CONFIGURE-ENVVARS-PYTHON)
:   Python interpreter program. This will be used to determine the
    dependencies for building PL/Python. If this is not set, the
    following are probed in this order:
    `python3 python`.
<a id="CONFIGURE-ENVVARS-TCLSH"></a>

`TCLSH` [#](#CONFIGURE-ENVVARS-TCLSH)
:   Tcl interpreter program. This will be used to
    determine the dependencies for building PL/Tcl.
    If this is not set, the following are probed in this
    order: `tclsh tcl tclsh8.6 tclsh86 tclsh8.5 tclsh85
    tclsh8.4 tclsh84`.
<a id="CONFIGURE-ENVVARS-XML2-CONFIG"></a>

`XML2_CONFIG` [#](#CONFIGURE-ENVVARS-XML2-CONFIG)
:   `xml2-config` program used to locate the
    libxml2 installation

Sometimes it is useful to add compiler flags after-the-fact to the set
that were chosen by `configure`. An important example is
that gcc's `-Werror` option cannot be included
in the `CFLAGS` passed to `configure`, because
it will break many of `configure`'s built-in tests. To add
such flags, include them in the `COPT` environment variable
while running `make`. The contents of `COPT`
are added to the `CFLAGS`, `CXXFLAGS`, and `LDFLAGS`
options set up by `configure`. For example, you could do

```

make COPT='-Werror'
```

or

```

export COPT='-Werror'
make
```

### Note

If using GCC, it is best to build with an optimization level of
at least `-O1`, because using no optimization
(`-O0`) disables some important compiler warnings (such
as the use of uninitialized variables). However, non-zero
optimization levels can complicate debugging because stepping
through compiled code will usually not match up one-to-one with
source code lines. If you get confused while trying to debug
optimized code, recompile the specific files of interest with
`-O0`. An easy way to do this is by passing an option
to make: `make PROFILE=-O0 file.o`.

The `COPT` and `PROFILE` environment variables are
actually handled identically by the PostgreSQL
makefiles. Which to use is a matter of preference, but a common habit
among developers is to use `PROFILE` for one-time flag
adjustments, while `COPT` might be kept set all the time.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/install-make.html)（英文原文，待翻譯）
