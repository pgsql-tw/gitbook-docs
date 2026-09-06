## 17.4. Building and Installation with Meson [#](#INSTALL-MESON)

[17.4.1. Short Version](install-meson.md#INSTALL-SHORT-MESON)

[17.4.2. Installation Procedure](install-meson.md#INSTALL-PROCEDURE-MESON)

[17.4.3. `meson setup` Options](install-meson.md#MESON-OPTIONS)

[17.4.4. `meson` Build Targets](install-meson.md#TARGETS-MESON)

<a id="INSTALL-SHORT-MESON"></a>

### 17.4.1. Short Version [#](#INSTALL-SHORT-MESON)

```

meson setup build --prefix=/usr/local/pgsql
cd build
ninja
su
ninja install
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

<a id="INSTALL-PROCEDURE-MESON"></a>

### 17.4.2. Installation Procedure [#](#INSTALL-PROCEDURE-MESON)

<a id="MESON-CONFIGURE"></a>1. **Configuration**

   The first step of the installation procedure is to configure the
   build tree for your system and choose the options you would like. To
   create and configure the build directory, you can start with the
   `meson setup` command.

   ```

   meson setup build
   ```

   The setup command takes a `builddir` and a `srcdir`
   argument. If no `srcdir` is given, Meson will deduce the
   `srcdir` based on the current directory and the location
   of `meson.build`. The `builddir` is mandatory.

   Running `meson setup` loads the build configuration file and sets up the build directory.
   Additionally, you can also pass several build options to Meson. Some commonly
   used options are mentioned in the subsequent sections. For example:

   ```

   # configure with a different installation prefix
   meson setup build --prefix=/home/user/pg-install

   # configure to generate a debug build
   meson setup build --buildtype=debug

   # configure to build with OpenSSL support
   meson setup build -Dssl=openssl
   ```

   Setting up the build directory is a one-time step. To reconfigure before a
   new build, you can simply use the `meson configure` command

   ```

   meson configure -Dcassert=true
   ```

   `meson configure`'s commonly used command-line options
   are explained in [Section 17.4.3](install-meson.md#MESON-OPTIONS).
<a id="MESON-BUILD"></a>2. **Build**

   By default, Meson uses the [Ninja](https://ninja-build.org/) build tool. To build
   PostgreSQL from source using Meson, you can
   simply use the `ninja` command in the build directory.

   ```

   ninja
   ```

   Ninja will automatically detect the number of CPUs in your computer and
   parallelize itself accordingly. You can override the number of parallel
   processes used with the command line argument `-j`.

   It should be noted that after the initial configure step,
   `ninja` is the only command you ever need to type to
   compile. No matter how you alter your source tree (short of moving it to a
   completely new location), Meson will detect the changes and regenerate
   itself accordingly. This is especially handy if you have multiple build
   directories. Often one of them is used for development (the "debug" build)
   and others only every now and then (such as a "static analysis" build).
   Any configuration can be built just by cd'ing to the corresponding
   directory and running Ninja.

   If you'd like to build with a backend other than ninja, you can use
   configure with the `--backend` option to select the one you
   want to use and then build using `meson compile`. To
   learn more about these backends and other arguments you can provide to
   ninja, you can refer to the [Meson documentation](https://mesonbuild.com/Running-Meson.html#building-from-the-source).
3. **Regression Tests**

   <a id="id-1.6.4.7.3.2.3.2"></a>

   If you want to test the newly built server before you install it,
   you can run the regression tests at this point. The regression
   tests are a test suite to verify that PostgreSQL
   runs on your machine in the way the developers expected it
   to. Type:

   ```

   meson test
   ```

   (This won't work as root; do it as an unprivileged user.)
   See [Chapter 31](../regress/README.md) for
   detailed information about interpreting the test results. You can
   repeat this test at any later time by issuing the same command.

   To run pg_regress and pg_isolation_regress tests against a running
   postgres instance, specify **`--setup running`** as an
   argument to **`meson test`**.
<a id="MESON-INSTALL"></a>4. **Installing the Files**

   ### Note

   If you are upgrading an existing system be sure to read
   [Section 18.6](../runtime/upgrading.md),
   which has instructions about upgrading a
   cluster.

   Once PostgreSQL is built, you can install it by simply running the
   `ninja install` command.

   ```

   ninja install
   ```

   This will install files into the directories that were specified
   in [Step 1](install-meson.md#MESON-CONFIGURE). Make sure that you have appropriate
   permissions to write into that area. You might need to do this
   step as root. Alternatively, you can create the target directories
   in advance and arrange for appropriate permissions to be granted.
   The standard installation provides all the header files needed for client
   application development as well as for server-side program
   development, such as custom functions or data types written in C.

   `ninja install` should work for most cases, but if you'd
   like to use more options (such as `--quiet` to suppress
   extra output), you could also use `meson install`
   instead. You can learn more about [meson install](https://mesonbuild.com/Commands.html#install)
   and its options in the Meson documentation.

**Uninstallation:**
To undo the installation, you can use the `ninja
uninstall` command.

**Cleaning:**
After the installation, you can free disk space by removing the built
files from the source tree with the `ninja clean`
command.

<a id="MESON-OPTIONS"></a>

### 17.4.3. `meson setup` Options [#](#MESON-OPTIONS)

`meson setup`'s command-line options are explained below.
This list is not exhaustive (use `meson configure --help`
to get one that is). The options not covered here are meant for advanced
use-cases, and are documented in the standard [Meson
documentation](https://mesonbuild.com/Commands.html#configure). These arguments can be used with `meson
setup` as well.

<a id="MESON-OPTIONS-LOCATIONS"></a>

#### 17.4.3.1. Installation Locations [#](#MESON-OPTIONS-LOCATIONS)

These options control where `ninja install` (or `meson install`) will put
the files. The `--prefix` option (example
[Section 17.4.1](install-meson.md#INSTALL-SHORT-MESON)) is sufficient for
most cases. If you have special needs, you can customize the
installation subdirectories with the other options described in this
section. Beware however that changing the relative locations of the
different subdirectories may render the installation non-relocatable,
meaning you won't be able to move it after installation.
(The `man` and `doc` locations are
not affected by this restriction.) For relocatable installs, you
might want to use the `-Drpath=false` option
described later.

<a id="CONFIGURE-PREFIX-MESON"></a>

`--prefix=PREFIX` [#](#CONFIGURE-PREFIX-MESON)
:   Install all files under the directory *`PREFIX`*
    instead of `/usr/local/pgsql` (on Unix based systems) or
    `current drive letter:/usr/local/pgsql` (on Windows).
    The actual files will be installed into various subdirectories; no files
    will ever be installed directly into the
    *`PREFIX`* directory.
<a id="CONFIGURE-BINDIR-MESON"></a>

`--bindir=DIRECTORY` [#](#CONFIGURE-BINDIR-MESON)
:   Specifies the directory for executable programs. The default
    is `PREFIX/bin`.
<a id="CONFIGURE-SYSCONFDIR-MESON"></a>

`--sysconfdir=DIRECTORY` [#](#CONFIGURE-SYSCONFDIR-MESON)
:   Sets the directory for various configuration files,
    `PREFIX/etc` by default.
<a id="CONFIGURE-LIBDIR-MESON"></a>

`--libdir=DIRECTORY` [#](#CONFIGURE-LIBDIR-MESON)
:   Sets the location to install libraries and dynamically loadable
    modules. The default is
    `PREFIX/lib`.
<a id="CONFIGURE-INCLUDEDIR-MESON"></a>

`--includedir=DIRECTORY` [#](#CONFIGURE-INCLUDEDIR-MESON)
:   Sets the directory for installing C and C++ header files. The
    default is `PREFIX/include`.
<a id="CONFIGURE-DATADIR-MESON"></a>

`--datadir=DIRECTORY` [#](#CONFIGURE-DATADIR-MESON)
:   Sets the directory for read-only data files used by the
    installed programs. The default is
    `PREFIX/share`. Note that this has
    nothing to do with where your database files will be placed.
<a id="CONFIGURE-LOCALEDIR-MESON"></a>

`--localedir=DIRECTORY` [#](#CONFIGURE-LOCALEDIR-MESON)
:   Sets the directory for installing locale data, in particular
    message translation catalog files. The default is
    `DATADIR/locale`.
<a id="CONFIGURE-MANDIR-MESON"></a>

`--mandir=DIRECTORY` [#](#CONFIGURE-MANDIR-MESON)
:   The man pages that come with PostgreSQL will be installed under
    this directory, in their respective
    `manx` subdirectories.
    The default is `DATADIR/man`.

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

<a id="MESON-OPTIONS-FEATURES"></a>

#### 17.4.3.2. PostgreSQL Features [#](#MESON-OPTIONS-FEATURES)

The options described in this section enable building of
various optional PostgreSQL features.
Most of these require additional software, as described in
[Section 17.1](install-requirements.md), and will be automatically enabled if the
required software is found. You can change this behavior by manually
setting these features to `enabled` to require them
or `disabled` to not build with them.

To specify PostgreSQL-specific options, the name of the option
must be prefixed by `-D`.

<a id="CONFIGURE-WITH-NLS-MESON"></a>

`-Dnls={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-NLS-MESON)
:   Enables or disables Native Language Support (NLS),
    that is, the ability to display a program's messages in a language
    other than English. Defaults to auto and will be enabled
    automatically if an implementation of the Gettext
    API is found.
<a id="CONFIGURE-WITH-PLPERL-MESON"></a>

`-Dplperl={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-PLPERL-MESON)
:   Build the PL/Perl server-side language.
    Defaults to auto.
<a id="CONFIGURE-WITH-PLPYTHON-MESON"></a>

`-Dplpython={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-PLPYTHON-MESON)
:   Build the PL/Python server-side language.
    Defaults to auto.
<a id="CONFIGURE-WITH-PLTCL-MESON"></a>

`-Dpltcl={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-PLTCL-MESON)
:   Build the PL/Tcl server-side language.
    Defaults to auto.
<a id="CONFIGURE-WITH-TCL-VERSION-MESON"></a>

`-Dtcl_version=TCL_VERSION` [#](#CONFIGURE-WITH-TCL-VERSION-MESON)
:   Specifies the Tcl version to use when building PL/Tcl.
<a id="CONFIGURE-WITH-ICU-MESON"></a>

`-Dicu={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-ICU-MESON)
:   Build with support for the
    ICU<a id="id-1.6.4.7.4.4.4.6.2.1.2"></a>
    library, enabling use of ICU collation features (see [Section 23.2](../charset/collation.md)). Defaults to auto and requires the
    ICU4C package to be installed. The minimum
    required version of ICU4C is currently 4.2.
<a id="CONFIGURE-WITH-LLVM-MESON"></a>

`-Dllvm={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-LLVM-MESON)
:   Build with support for LLVM based
    JIT compilation (see [Chapter 30](../jit/README.md)).
    This requires the LLVM library to be
    installed. The minimum required version of
    LLVM is currently 14. Disabled by
    default.

    `llvm-config`<a id="id-1.6.4.7.4.4.4.7.2.2.2"></a>
    will be used to find the required compilation options.
    `llvm-config`, and then
    `llvm-config-$version` for all supported versions,
    will be searched for in your `PATH`. If that would not
    yield the desired program, use `LLVM_CONFIG` to specify a
    path to the correct `llvm-config`.
<a id="CONFIGURE-WITH-LZ4-MESON"></a>

`-Dlz4={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-LZ4-MESON)
:   Build with LZ4 compression support.
    Defaults to auto.
<a id="CONFIGURE-WITH-ZSTD-MESON"></a>

`-Dzstd={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-ZSTD-MESON)
:   Build with Zstandard compression support.
    Defaults to auto.
<a id="CONFIGURE-WITH-SSL-MESON"></a>

`-Dssl={ auto | LIBRARY }` <a id="id-1.6.4.7.4.4.4.10.1.2"></a> [#](#CONFIGURE-WITH-SSL-MESON)
:   Build with support for SSL (encrypted) connections.
    The only *`LIBRARY`* supported is
    `openssl`. This requires the
    OpenSSL package to be installed. Building
    with this will check for the required header files and libraries to
    make sure that your OpenSSL installation is
    sufficient before proceeding. The default for this option is auto.
<a id="CONFIGURE-WITH-GSSAPI-MESON"></a>

`-Dgssapi={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-GSSAPI-MESON)
:   Build with support for GSSAPI authentication. MIT Kerberos is required
    to be installed for GSSAPI. On many systems, the GSSAPI system (a part
    of the MIT Kerberos installation) is not installed in a location
    that is searched by default (e.g., `/usr/include`,
    `/usr/lib`). In
    those cases, PostgreSQL will query `pkg-config` to
    detect the required compiler and linker options. Defaults to auto.
    `meson configure` will check for the required
    header files and libraries to make sure that your GSSAPI installation
    is sufficient before proceeding.
<a id="CONFIGURE-WITH-LDAP-MESON"></a>

`-Dldap={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-LDAP-MESON)
:   Build with
    LDAP<a id="id-1.6.4.7.4.4.4.12.2.1.2"></a>
    support for authentication and connection parameter lookup (see
    <a id="INSTALL-LDAP-LINKS-MESON"></a>[Section 32.18](../../client-interfaces/libpq/libpq-ldap.md) and
    [Section 20.10](../client-authentication/auth-ldap.md) for more information). On Unix,
    this requires the OpenLDAP package to be
    installed. On Windows, the default WinLDAP
    library is used. Defaults to auto. `meson
    configure` will check for the required header files and
    libraries to make sure that your OpenLDAP
    installation is sufficient before proceeding.
<a id="CONFIGURE-WITH-PAM-MESON"></a>

`-Dpam={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-PAM-MESON)
:   Build with
    PAM<a id="id-1.6.4.7.4.4.4.13.2.1.2"></a>
    (Pluggable Authentication Modules) support. Defaults to auto.
<a id="CONFIGURE-WITH-BSD-AUTH-MESON"></a>

`-Dbsd_auth={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-BSD-AUTH-MESON)
:   Build with BSD Authentication support. (The BSD Authentication
    framework is currently only available on OpenBSD.) Defaults to auto.
<a id="CONFIGURE-WITH-SYSTEMD-MESON"></a>

`-Dsystemd={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-SYSTEMD-MESON)
:   Build with support for
    systemd<a id="id-1.6.4.7.4.4.4.15.2.1.2"></a>
    service notifications. This improves integration if the server is
    started under systemd but has no impact
    otherwise; see [Section 18.3](../runtime/server-start.md) for more information. Defaults to
    auto. libsystemd and the associated header
    files need to be installed to use this option.
<a id="CONFIGURE-WITH-BONJOUR-MESON"></a>

`-Dbonjour={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-BONJOUR-MESON)
:   Build with support for Bonjour automatic service discovery. Defaults
    to auto and requires Bonjour support in your operating system.
    Recommended on macOS.
<a id="CONFIGURE-WITH-UUID-MESON"></a>

`-Duuid=LIBRARY` [#](#CONFIGURE-WITH-UUID-MESON)
:   Build the [uuid-ossp](../../appendixes/contrib/uuid-ossp.md) module
    (which provides functions to generate UUIDs), using the specified
    UUID library.<a id="id-1.6.4.7.4.4.4.17.2.1.2"></a>
    *`LIBRARY`* must be one of:

    * `none` to not build the uuid module. This is the default.
    * `bsd` to use the UUID functions found in FreeBSD,
      and some other BSD-derived systems
    * `e2fs` to use the UUID library created by
      the `e2fsprogs` project; this library is present in most
      Linux systems and in macOS, and can be obtained for other
      platforms as well
    * `ossp` to use the [OSSP UUID library](http://www.ossp.org/pkg/lib/uuid/)
<a id="CONFIGURE-WITH-LIBCURL-MESON"></a>

`-Dlibcurl={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-LIBCURL-MESON)
:   Build with libcurl support for OAuth 2.0 client flows.
    Libcurl version 7.61.0 or later is required for this feature.
    Building with this will check for the required header files
    and libraries to make sure that your Curl
    installation is sufficient before proceeding. The default for this
    option is auto.
<a id="CONFIGURE-WITH-LIBURING-MESON"></a>

`-Dliburing={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-LIBURING-MESON)
:   Build with liburing, enabling io_uring support for asynchronous I/O.
    Defaults to auto.

    To use a liburing installation that is in an unusual location, you
    can set `pkg-config`-related environment
    variables (see its documentation).
<a id="CONFIGURE-WITH-LIBNUMA-MESON"></a>

`-Dlibnuma={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-LIBNUMA-MESON)
:   Build with libnuma support for basic NUMA support.
    Only supported on platforms for which the libnuma
    library is implemented. The default for this option is auto.
<a id="CONFIGURE-WITH-LIBXML-MESON"></a>

`-Dlibxml={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-LIBXML-MESON)
:   Build with libxml2, enabling SQL/XML support. Defaults to
    auto. Libxml2 version 2.6.23 or later is required for this feature.

    To use a libxml2 installation that is in an unusual location, you
    can set `pkg-config`-related environment
    variables (see its documentation).
<a id="CONFIGURE-WITH-LIBXSLT-MESON"></a>

`-Dlibxslt={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-LIBXSLT-MESON)
:   Build with libxslt, enabling the
    [xml2](../../appendixes/contrib/xml2.md)
    module to perform XSL transformations of XML.
    `-Dlibxml` must be specified as well. Defaults to
    auto.
<a id="CONFIGURE-WITH-SEPGSQL-MESON"></a>

`-Dselinux={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-SEPGSQL-MESON)
:   Build with SElinux support, enabling the [sepgsql](../../appendixes/contrib/sepgsql.md)
    extension. Defaults to auto.

<a id="MESON-OPTIONS-ANTI-FEATURES"></a>

#### 17.4.3.3. Anti-Features [#](#MESON-OPTIONS-ANTI-FEATURES)

<a id="CONFIGURE-READLINE-MESON"></a>

`-Dreadline={ auto | enabled | disabled }` [#](#CONFIGURE-READLINE-MESON)
:   Allows use of the Readline library (and
    libedit as well). This option defaults to
    auto and enables command-line editing and history in
    psql and is strongly recommended.
<a id="CONFIGURE-LIBEDIT-PREFERRED-MESON"></a>

`-Dlibedit_preferred={ true | false }` [#](#CONFIGURE-LIBEDIT-PREFERRED-MESON)
:   Setting this to true favors the use of the BSD-licensed
    libedit library rather than GPL-licensed
    Readline. This option is significant only
    if you have both libraries installed; the default is false, that is to
    use Readline.
<a id="CONFIGURE-ZLIB-MESON"></a>

`-Dzlib={ auto | enabled | disabled }` [#](#CONFIGURE-ZLIB-MESON)
:   <a id="id-1.6.4.7.4.5.2.3.2.1.1"></a>
    Enables use of the Zlib library.
    It defaults to auto and enables
    support for compressed archives in pg_dump,
    pg_restore and pg_basebackup and is recommended.

<a id="MESON-OPTIONS-BUILD-PROCESS"></a>

#### 17.4.3.4. Build Process Details [#](#MESON-OPTIONS-BUILD-PROCESS)

<a id="CONFIGURE-AUTO-FEATURES-MESON"></a>

`--auto-features={ auto | enabled | disabled }` [#](#CONFIGURE-AUTO-FEATURES-MESON)
:   Setting this option allows you to override the value of all
    “auto” features (features that are enabled automatically
    if the required software is found). This can be useful when you want
    to disable or enable all the “optional” features at once
    without having to set each of them manually. The default value for
    this parameter is auto.
<a id="CONFIGURE-BACKEND-MESON"></a>

`--backend=BACKEND` [#](#CONFIGURE-BACKEND-MESON)
:   The default backend Meson uses is ninja and that should suffice for
    most use cases. However, if you'd like to fully integrate with Visual
    Studio, you can set the *`BACKEND`* to
    `vs`.
<a id="CONFIGURE-C-ARGS-MESON"></a>

`-Dc_args=OPTIONS` [#](#CONFIGURE-C-ARGS-MESON)
:   This option can be used to pass extra options to the C compiler.
<a id="CONFIGURE-C-LINK-ARGS-MESON"></a>

`-Dc_link_args=OPTIONS` [#](#CONFIGURE-C-LINK-ARGS-MESON)
:   This option can be used to pass extra options to the C linker.
<a id="CONFIGURE-EXTRA-INCLUDE-DIRS-MESON"></a>

`-Dextra_include_dirs=DIRECTORIES` [#](#CONFIGURE-EXTRA-INCLUDE-DIRS-MESON)
:   *`DIRECTORIES`* is a comma-separated list of
    directories that will be added to the list the compiler searches for
    header files. If you have optional packages (such as GNU
    Readline) installed in a non-standard
    location, you have to use this option and probably also the
    corresponding `-Dextra_lib_dirs` option.

    Example: `-Dextra_include_dirs=/opt/gnu/include,/usr/sup/include`.
<a id="CONFIGURE-EXTRA-LIB-DIRS-MESON"></a>

`-Dextra_lib_dirs=DIRECTORIES` [#](#CONFIGURE-EXTRA-LIB-DIRS-MESON)
:   *`DIRECTORIES`* is a comma-separated list of
    directories to search for libraries. You will probably have to use
    this option (and the corresponding
    `-Dextra_include_dirs` option) if you have packages
    installed in non-standard locations.

    Example: `-Dextra_lib_dirs=/opt/gnu/lib,/usr/sup/lib`.
<a id="CONFIGURE-SYSTEM-TZDATA-MESON"></a>

`-Dsystem_tzdata=DIRECTORY` <a id="id-1.6.4.7.4.6.2.7.1.2"></a> [#](#CONFIGURE-SYSTEM-TZDATA-MESON)
:   PostgreSQL includes its own time zone
    database, which it requires for date and time operations. This time
    zone database is in fact compatible with the IANA time zone database
    provided by many operating systems such as FreeBSD, Linux, and
    Solaris, so it would be redundant to install it again. When this
    option is used, the system-supplied time zone database in
    *`DIRECTORY`* is used instead of the one
    included in the PostgreSQL source distribution.
    *`DIRECTORY`* must be specified as an absolute
    path. `/usr/share/zoneinfo` is a likely directory
    on some operating systems. Note that the installation routine will
    not detect mismatching or erroneous time zone data. If you use this
    option, you are advised to run the regression tests to verify that the
    time zone data you have pointed to works correctly with
    PostgreSQL.

    <a id="id-1.6.4.7.4.6.2.7.2.2"></a>

    This option is mainly aimed at binary package distributors who know
    their target operating system well. The main advantage of using this
    option is that the PostgreSQL package won't need to be upgraded
    whenever any of the many local daylight-saving time rules change.
    Another advantage is that PostgreSQL can be cross-compiled more
    straightforwardly if the time zone database files do not need to be
    built during the installation.
<a id="CONFIGURE-EXTRA-VERSION-MESON"></a>

`-Dextra_version=STRING` [#](#CONFIGURE-EXTRA-VERSION-MESON)
:   Append *`STRING`* to the PostgreSQL version
    number. You can use this, for example, to mark binaries built from
    unreleased Git snapshots or containing
    custom patches with an extra version string, such as a `git
    describe` identifier or a distribution package release
    number.
<a id="CONFIGURE-RPATH-MESON"></a>

`-Drpath={ true | false }` [#](#CONFIGURE-RPATH-MESON)
:   This option is set to true by default. If set to false,
    do not mark PostgreSQL's executables
    to indicate that they should search for shared libraries in the
    installation's library directory (see `--libdir`).
    On most platforms, this marking uses an absolute path to the
    library directory, so that it will be unhelpful if you relocate
    the installation later. However, you will then need to provide
    some other way for the executables to find the shared libraries.
    Typically this requires configuring the operating system's
    dynamic linker to search the library directory; see
    [Section 17.5.1](install-post.md#INSTALL-POST-SHLIBS) for more detail.
<a id="CONFIGURE-BINARY-NAME-MESON"></a>

`-DBINARY_NAME=PATH` [#](#CONFIGURE-BINARY-NAME-MESON)
:   If a program required to build PostgreSQL (with or without optional
    flags) is stored at a non-standard path, you can specify it manually
    to `meson configure`. The complete list of programs
    for which this is supported can be found by running `meson
    configure`. Example:

    ```
    meson configure -DBISON=PATH_TO_BISON
    ```

<a id="MESON-OPTIONS-DOCS"></a>

#### 17.4.3.5. Documentation [#](#MESON-OPTIONS-DOCS)

See [Section J.2](../../appendixes/docguide/docguide-toolsets.md) for the tools needed for building
the documentation.

<a id="CONFIGURE-DOCS-MESON"></a>

`-Ddocs={ auto | enabled | disabled }` [#](#CONFIGURE-DOCS-MESON)
:   Enables building the documentation in HTML and
    man format. It defaults to auto.
<a id="CONFIGURE-DOCS-PDF-MESON"></a>

`-Ddocs_pdf={ auto | enabled | disabled }` [#](#CONFIGURE-DOCS-PDF-MESON)
:   Enables building the documentation in PDF
    format. It defaults to auto.
<a id="CONFIGURE-DOCS-HTML-STYLE"></a>

`-Ddocs_html_style={ simple | website }` [#](#CONFIGURE-DOCS-HTML-STYLE)
:   Controls which CSS stylesheet is used. The default
    is `simple`. If set to `website`,
    the HTML documentation will reference the stylesheet for [postgresql.org](https://www.postgresql.org/docs/current/).

<a id="MESON-OPTIONS-MISC"></a>

#### 17.4.3.6. Miscellaneous [#](#MESON-OPTIONS-MISC)

<a id="CONFIGURE-PGPORT-MESON"></a>

`-Dpgport=NUMBER` [#](#CONFIGURE-PGPORT-MESON)
:   Set *`NUMBER`* as the default port number for
    server and clients. The default is 5432. The port can always
    be changed later on, but if you specify it here then both
    server and clients will have the same default compiled in,
    which can be very convenient. Usually the only good reason
    to select a non-default value is if you intend to run multiple
    PostgreSQL servers on the same machine.
<a id="CONFIGURE-KRB-SRVNAM-MESON"></a>

`-Dkrb_srvnam=NAME` [#](#CONFIGURE-KRB-SRVNAM-MESON)
:   The default name of the Kerberos service principal used
    by GSSAPI.
    `postgres` is the default. There's usually no
    reason to change this unless you are building for a Windows
    environment, in which case it must be set to upper case
    `POSTGRES`.
<a id="CONFIGURE-SEGSIZE-MESON"></a>

`-Dsegsize=SEGSIZE` [#](#CONFIGURE-SEGSIZE-MESON)
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
<a id="CONFIGURE-BLOCKSIZE-MESON"></a>

`-Dblocksize=BLOCKSIZE` [#](#CONFIGURE-BLOCKSIZE-MESON)
:   Set the *block size*, in kilobytes. This is the unit
    of storage and I/O within tables. The default, 8 kilobytes,
    is suitable for most situations; but other values may be useful
    in special cases.
    The value must be a power of 2 between 1 and 32 (kilobytes).
<a id="CONFIGURE-WAL-BLOCKSIZE-MESON"></a>

`-Dwal_blocksize=BLOCKSIZE` [#](#CONFIGURE-WAL-BLOCKSIZE-MESON)
:   Set the *WAL block size*, in kilobytes. This is the unit
    of storage and I/O within the WAL log. The default, 8 kilobytes,
    is suitable for most situations; but other values may be useful
    in special cases.
    The value must be a power of 2 between 1 and 64 (kilobytes).

<a id="MESON-OPTIONS-DEVEL"></a>

#### 17.4.3.7. Developer Options [#](#MESON-OPTIONS-DEVEL)

Most of the options in this section are only of interest for
developing or debugging PostgreSQL.
They are not recommended for production builds, except
for `--debug`, which can be useful to enable
detailed bug reports in the unlucky event that you encounter a bug.
On platforms supporting DTrace, `-Ddtrace`
may also be reasonable to use in production.

When building an installation that will be used to develop code inside
the server, it is recommended to use at least the `--buildtype=debug`
and `-Dcassert` options.

<a id="CONFIGURE-BUILDTYPE-MESON"></a>

`--buildtype=BUILDTYPE` [#](#CONFIGURE-BUILDTYPE-MESON)
:   This option can be used to specify the buildtype to use; defaults to
    `debugoptimized`. If you'd like finer control on the debug
    symbols and optimization levels than what this option provides, you
    can refer to the `--debug` and
    `--optimization` flags.

    The following build types are generally used: `plain`,
    `debug`, `debugoptimized` and
    `release`. More information about them can be found in
    the [Meson
    documentation](https://mesonbuild.com/Running-Meson.html#configuring-the-build-directory).
<a id="CONFIGURE-DEBUG-MESON"></a>

`--debug` [#](#CONFIGURE-DEBUG-MESON)
:   Compiles all programs and libraries with debugging symbols. This
    means that you can run the programs in a debugger to analyze
    problems. This enlarges the size of the installed executables
    considerably, and on non-GCC compilers it usually also disables
    compiler optimization, causing slowdowns. However, having the symbols
    available is extremely helpful for dealing with any problems that
    might arise. Currently, this option is recommended for production
    installations only if you use GCC. But you should always have it on
    if you are doing development work or running a beta version.
<a id="CONFIGURE-OPTIMIZATION-MESON"></a>

`--optimization`=*`LEVEL`* [#](#CONFIGURE-OPTIMIZATION-MESON)
:   Specify the optimization level. `LEVEL` can be set to any of {0,g,1,2,3,s}.
<a id="CONFIGURE-WERROR-MESON"></a>

`--werror` [#](#CONFIGURE-WERROR-MESON)
:   Setting this option asks the compiler to treat warnings as
    errors. This can be useful for code development.
<a id="CONFIGURE-CASSERT-MESON"></a>

`-Dcassert={ true | false }` [#](#CONFIGURE-CASSERT-MESON)
:   Enables *assertion* checks in the server, which
    test for many “cannot happen” conditions. This is
    invaluable for code development purposes, but the tests slow down the
    server significantly. Also, having the tests turned on won't
    necessarily enhance the stability of your server! The assertion
    checks are not categorized for severity, and so what might be a
    relatively harmless bug will still lead to server restarts if it
    triggers an assertion failure. This option is not recommended for
    production use, but you should have it on for development work or when
    running a beta version.
<a id="CONFIGURE-TAP-TESTS-MESON"></a>

`-Dtap_tests={ auto | enabled | disabled }` [#](#CONFIGURE-TAP-TESTS-MESON)
:   Enable tests using the Perl TAP tools. Defaults to auto and requires
    a Perl installation and the Perl module `IPC::Run`.
    See [Section 31.4](../regress/regress-tap.md) for more information.
<a id="CONFIGURE-PG-TEST-EXTRA-MESON"></a>

`-DPG_TEST_EXTRA=TEST_SUITES` [#](#CONFIGURE-PG-TEST-EXTRA-MESON)
:   Enable additional test suites, which are not run by default because
    they are not secure to run on a multiuser system, require special
    software to run, or are resource intensive. The argument is a
    whitespace-separated list of tests to enable. See
    [Section 31.1.3](../regress/regress-run.md#REGRESS-ADDITIONAL) for details. If the
    `PG_TEST_EXTRA` environment variable is set when the
    tests are run, it overrides this setup-time option.
<a id="CONFIGURE-B-COVERAGE-MESON"></a>

`-Db_coverage={ true | false }` [#](#CONFIGURE-B-COVERAGE-MESON)
:   If using GCC, all programs and libraries are compiled with
    code coverage testing instrumentation. When run, they
    generate files in the build directory with code coverage
    metrics.
    See [Section 31.5](../regress/regress-coverage.md)
    for more information. This option is for use only with GCC
    and when doing development work.
<a id="CONFIGURE-DTRACE-MESON"></a>

`-Ddtrace={ auto | enabled | disabled }` [#](#CONFIGURE-DTRACE-MESON)
:   <a id="id-1.6.4.7.4.9.4.9.2.1.1"></a>
    Enabling this compiles PostgreSQL with support for the
    dynamic tracing tool DTrace.
    See [Section 27.5](../monitoring/dynamic-trace.md) for more information.

    To point to the `dtrace` program, the
    `DTRACE` option can be set. This
    will often be necessary because `dtrace` is
    typically installed under `/usr/sbin`,
    which might not be in your `PATH`.
<a id="CONFIGURE-INJECTION-POINTS-MESON"></a>

`-Dinjection_points={ true | false }` [#](#CONFIGURE-INJECTION-POINTS-MESON)
:   Compiles PostgreSQL with support for
    injection points in the server. Injection points allow to run
    user-defined code from within the server in pre-defined code paths.
    This helps in testing and in the investigation of concurrency scenarios
    in a controlled fashion. This option is disabled by default. See
    [Section 36.10.14](../../server-programming/extend/xfunc-c.md#XFUNC-ADDIN-INJECTION-POINTS) for more details. This
    option is intended to be used only by developers for testing.
<a id="CONFIGURE-SEGSIZE-BLOCKS-MESON"></a>

`-Dsegsize_blocks=SEGSIZE_BLOCKS` [#](#CONFIGURE-SEGSIZE-BLOCKS-MESON)
:   Specify the relation segment size in blocks. If both
    `-Dsegsize` and this option are specified, this option
    wins.
    This option is only for developers, to test segment related code.

<a id="TARGETS-MESON"></a>

### 17.4.4. `meson` Build Targets [#](#TARGETS-MESON)

Individual build targets can be built using `ninja` *`target`*.
When no target is specified, everything except documentation is
built. Individual build products can be built using the path/filename as
*`target`*.

<a id="TARGETS-MESON-CODE"></a>

#### 17.4.4.1. Code Targets [#](#TARGETS-MESON-CODE)

<a id="MESON-TARGET-ALL"></a>

`all` [#](#MESON-TARGET-ALL)
:   Build everything other than documentation
<a id="MESON-TARGET-BACKEND"></a>

`backend` [#](#MESON-TARGET-BACKEND)
:   Build backend and related modules
<a id="MESON-TARGET-BIN"></a>

`bin` [#](#MESON-TARGET-BIN)
:   Build frontend binaries
<a id="MESON-TARGET-CONTRIB"></a>

`contrib` [#](#MESON-TARGET-CONTRIB)
:   Build contrib modules
<a id="MESON-TARGET-PL"></a>

`pl` [#](#MESON-TARGET-PL)
:   Build procedural languages

<a id="TARGETS-MESON-DEVELOPER"></a>

#### 17.4.4.2. Developer Targets [#](#TARGETS-MESON-DEVELOPER)

<a id="MESON-TARGET-REFORMAT-DAT-FILES"></a>

`reformat-dat-files` [#](#MESON-TARGET-REFORMAT-DAT-FILES)
:   Rewrite catalog data files into standard format
<a id="MESON-TARGET-EXPAND-DAT-FILES"></a>

`expand-dat-files` [#](#MESON-TARGET-EXPAND-DAT-FILES)
:   Expand all data files to include defaults
<a id="MESON-TARGET-UPDATE-UNICODE"></a>

`update-unicode` [#](#MESON-TARGET-UPDATE-UNICODE)
:   Update unicode data to new version

<a id="TARGETS-MESON-DOCUMENTATION"></a>

#### 17.4.4.3. Documentation Targets [#](#TARGETS-MESON-DOCUMENTATION)

<a id="MESON-TARGET-HTML"></a>

`html` [#](#MESON-TARGET-HTML)
:   Build documentation in multi-page HTML format
<a id="MESON-TARGET-MAN"></a>

`man` [#](#MESON-TARGET-MAN)
:   Build documentation in man page format
<a id="MESON-TARGET-DOCS"></a>

`docs` [#](#MESON-TARGET-DOCS)
:   Build documentation in multi-page HTML and man page format
<a id="MESON-TARGET-DOC-SRC-SGML-POSTGRES-A4.PDF"></a>

`doc/src/sgml/postgres-A4.pdf` [#](#MESON-TARGET-DOC-SRC-SGML-POSTGRES-A4.PDF)
:   Build documentation in PDF format, with A4 pages
<a id="MESON-TARGET-DOC-SRC-SGML-POSTGRES-US.PDF"></a>

`doc/src/sgml/postgres-US.pdf` [#](#MESON-TARGET-DOC-SRC-SGML-POSTGRES-US.PDF)
:   Build documentation in PDF format, with US letter pages
<a id="MESON-TARGET-DOC-SRC-SGML-POSTGRES.HTML"></a>

`doc/src/sgml/postgres.html` [#](#MESON-TARGET-DOC-SRC-SGML-POSTGRES.HTML)
:   Build documentation in single-page HTML format
<a id="MESON-TARGET-ALLDOCS"></a>

`alldocs` [#](#MESON-TARGET-ALLDOCS)
:   Build documentation in all supported formats

<a id="TARGETS-MESON-INSTALLATION"></a>

#### 17.4.4.4. Installation Targets [#](#TARGETS-MESON-INSTALLATION)

<a id="MESON-TARGET-INSTALL"></a>

`install` [#](#MESON-TARGET-INSTALL)
:   Install postgres, excluding documentation
<a id="MESON-TARGET-INSTALL-DOCS"></a>

`install-docs` [#](#MESON-TARGET-INSTALL-DOCS)
:   Install documentation in multi-page HTML and man page formats
<a id="MESON-TARGET-INSTALL-HTML"></a>

`install-html` [#](#MESON-TARGET-INSTALL-HTML)
:   Install documentation in multi-page HTML format
<a id="MESON-TARGET-INSTALL-MAN"></a>

`install-man` [#](#MESON-TARGET-INSTALL-MAN)
:   Install documentation in man page format
<a id="MESON-TARGET-INSTALL-QUIET"></a>

`install-quiet` [#](#MESON-TARGET-INSTALL-QUIET)
:   Like "install", but installed files are not displayed
<a id="MESON-TARGET-INSTALL-WORLD"></a>

`install-world` [#](#MESON-TARGET-INSTALL-WORLD)
:   Install postgres, including multi-page HTML and man page documentation
<a id="MESON-TARGET-UNINSTALL"></a>

`uninstall` [#](#MESON-TARGET-UNINSTALL)
:   Remove installed files

<a id="TARGETS-MESON-OTHER"></a>

#### 17.4.4.5. Other Targets [#](#TARGETS-MESON-OTHER)

<a id="MESON-TARGET-CLEAN"></a>

`clean` [#](#MESON-TARGET-CLEAN)
:   Remove all build products
<a id="MESON-TARGET-TEST"></a>

`test` [#](#MESON-TARGET-TEST)
:   Run all enabled tests (including contrib)
<a id="MESON-TARGET-WORLD"></a>

`world` [#](#MESON-TARGET-WORLD)
:   Build everything, including documentation
<a id="MESON-TARGET-HELP"></a>

`help` [#](#MESON-TARGET-HELP)
:   List important targets

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/install-meson.html)（英文原文，待翻譯）
