# 16.2. Requirements

In general, a modern Unix-compatible platform should be able to run PostgreSQL. The platforms that had received specific testing at the time of release are listed in [Section 16.6](https://www.postgresql.org/docs/10/static/supported-platforms.html) below. In the `doc` subdirectory of the distribution there are several platform-specific FAQ documents you might wish to consult if you are having trouble.

The following software packages are required for building PostgreSQL:

* GNU make version 3.80 or newer is required; other make programs or older GNU make versions will _not_ work. \(GNU make is sometimes installed under the name `gmake`.\) To test for GNU make enter:

  ```text
  make --version
  ```

* You need an ISO/ANSI C compiler \(at least C89-compliant\). Recent versions of GCC are recommended, but PostgreSQL is known to build using a wide variety of compilers from different vendors.
* tar is required to unpack the source distribution, in addition to either gzip or bzip2.
* The GNU Readline library is used by default. It allows psql \(the PostgreSQL command line SQL interpreter\) to remember each command you type, and allows you to use arrow keys to recall and edit previous commands. This is very helpful and is strongly recommended. If you don't want to use it then you must specify the `--without-readline` option to `configure`. As an alternative, you can often use the BSD-licensed `libedit` library, originally developed on NetBSD. The `libedit` library is GNU Readline-compatible and is used if `libreadline` is not found, or if `--with-libedit-preferred` is used as an option to `configure`. If you are using a package-based Linux distribution, be aware that you need both the `readline` and `readline-devel` packages, if those are separate in your distribution.
* The zlib compression library is used by default. If you don't want to use it then you must specify the `--without-zlib` option to `configure`. Using this option disables support for compressed archives in pg\_dump andpg\_restore.

The following packages are optional. They are not required in the default configuration, but they are needed when certain build options are enabled, as explained below:

* To build the server programming language PL/Perl you need a full Perl installation, including the `libperl` library and the header files. The minimum required version is Perl 5.8.3. Since PL/Perl will be a shared library, the `libperl` library must be a shared library also on most platforms. This appears to be the default in recent Perl versions, but it was not in earlier versions, and in any case it is the choice of whomever installed Perl at your site. `configure` will fail if building PL/Perl is selected but it cannot find a shared `libperl`. In that case, you will have to rebuild and install Perl manually to be able to build PL/Perl. During the configuration process for Perl, request a shared library.

  If you intend to make more than incidental use of PL/Perl, you should ensure that the Perl installation was built with the `usemultiplicity` option enabled \(`perl -V` will show whether this is the case\).

* To build the PL/Python server programming language, you need a Python installation with the header files and the distutils module. The minimum required version is Python 2.4. Python 3 is supported if it's version 3.1 or later; but see [Section 45.1](https://www.postgresql.org/docs/10/static/plpython-python23.html) when using Python 3.

  Since PL/Python will be a shared library, the `libpython` library must be a shared library also on most platforms. This is not the case in a default Python installation built from source, but a shared library is available in many operating system distributions. `configure` will fail if building PL/Python is selected but it cannot find a shared `libpython`. That might mean that you either have to install additional packages or rebuild \(part of\) your Python installation to provide this shared library. When building from source, run Python's configure with the `--enable-shared` flag.

* To build the PL/Tcl procedural language, you of course need a Tcl installation. The minimum required version is Tcl 8.4.
* To enable Native Language Support \(NLS\), that is, the ability to display a program's messages in a language other than English, you need an implementation of the Gettext API. Some operating systems have this built-in \(e.g., Linux, NetBSD, Solaris\), for other systems you can download an add-on package from [http://www.gnu.org/software/gettext/](http://www.gnu.org/software/gettext/). If you are using the Gettext implementation in the GNU C library then you will additionally need the GNU Gettext package for some utility programs. For any of the other implementations you will not need it.
* You need OpenSSL, if you want to support encrypted client connections. The minimum required version is 0.9.8.
* You need Kerberos, OpenLDAP, and/or PAM, if you want to support authentication using those services.
* To build the PostgreSQL documentation, there is a separate set of requirements; see [Section J.2](https://www.postgresql.org/docs/10/static/docguide-toolsets.html).

If you are building from a Git tree instead of using a released source package, or if you want to do server development, you also need the following packages:

* GNU Flex and Bison are needed to build from a Git checkout, or if you changed the actual scanner and parser definition files. If you need them, be sure to get Flex 2.5.31 or later and Bison 1.875 or later. Other lexand yacc programs cannot be used.
* Perl 5.8.3 or later is needed to build from a Git checkout, or if you changed the input files for any of the build steps that use Perl scripts. If building on Windows you will need Perl in any case. Perl is also required to run some test suites.

If you need to get a GNU package, you can find it at your local GNU mirror site \(see [http://www.gnu.org/order/ftp.html](http://www.gnu.org/order/ftp.html) for a list\) or at [ftp://ftp.gnu.org/gnu/](ftp://ftp.gnu.org/gnu/).

Also check that you have sufficient disk space. You will need about 100 MB for the source tree during compilation and about 20 MB for the installation directory. An empty database cluster takes about 35 MB; databases take about five times the amount of space that a flat text file with the same data would take. If you are going to run the regression tests you will temporarily need up to an extra 150 MB. Use the `df` command to check free disk space.  


