# J.2. Tool Sets

The following tools are used to process the documentation. Some might be optional, as noted.

[DocBook DTD](https://www.oasis-open.org/docbook/)

This is the definition of DocBook itself. We currently use version 4.5; you cannot use later or earlier versions. You need the XML variant of the DocBook DTD, not the SGML variant.

[DocBook XSL Stylesheets](https://github.com/docbook/wiki/wiki/DocBookXslStylesheets)

These contain the processing instructions for converting the DocBook sources to other formats, such as HTML.

The minimum required version is currently 1.77.0, but it is recommended to use the latest available version for best results.

[Libxml2](http://xmlsoft.org/) for `xmllint`

This library and the `xmllint` tool it contains are used for processing XML. Many developers will already have Libxml2 installed, because it is also used when building the PostgreSQL code. Note, however, that `xmllint` might need to be installed from a separate subpackage.

[Libxslt](http://xmlsoft.org/XSLT/) for `xsltproc`

`xsltproc` is an XSLT processor, that is, a program to convert XML to other formats using XSLT stylesheets.

[FOP](https://xmlgraphics.apache.org/fop/)

This is a program for converting, among other things, XML to PDF.

We have documented experience with several installation methods for the various tools that are needed to process the documentation. These will be described below. There might be some other packaged distributions for these tools. Please report package status to the documentation mailing list, and we will include that information here.

You can get away with not installing DocBook XML and the DocBook XSLT stylesheets locally, because the required files will be downloaded from the Internet and cached locally. This may in fact be the preferred solution if your operating system packages provide only an old version of these files, or if no packages are available at all. If you want to prevent any attempt to access the Internet while building the documentation, you need to pass the `--nonet` option to `xmllint` and `xsltproc`; see below for an example.

## J.2.1. Installation on Fedora, RHEL, and Derivatives

To install the required packages, use:

```
yum install docbook-dtds docbook-style-xsl fop libxslt
```

## J.2.2. Installation on FreeBSD

To install the required packages with `pkg`, use:

```
pkg install docbook-xml docbook-xsl fop libxslt
```

When building the documentation from the `doc` directory you'll need to use `gmake`, because the makefile provided is not suitable for FreeBSD's `make`.

## J.2.3. Debian Packages

There is a full set of packages of the documentation tools available for Debian GNU/Linux. To install, simply use:

```
apt-get install docbook-xml docbook-xsl fop libxml2-utils xsltproc
```

## J.2.4. macOS

On macOS, you can build the HTML and man documentation without installing anything extra. If you want to build PDFs or want to install a local copy of DocBook, you can get those from your preferred package manager.

If you use MacPorts, the following will get you set up:

```
sudo port install docbook-xml-4.5 docbook-xsl fop
```

If you use Homebrew, use this:

```
brew install docbook docbook-xsl fop
```

## J.2.5. Detection by `configure`

Before you can build the documentation you need to run the `configure` script, as you would when building the PostgreSQL programs themselves. Check the output near the end of the run; it should look something like this:

```
checking for xmllint... xmllint
checking for xsltproc... xsltproc
checking for fop... fop
checking for dbtoepub... dbtoepub
```

If `xmllint` or `xsltproc` is not found, you will not be able to build any of the documentation. `fop` is only needed to build the documentation in PDF format. `dbtoepub` is only needed to build the documentation in EPUB format.

If necessary, you can tell `configure` where to find these programs, for example

```
./configure ... XMLLINT=/opt/local/bin/xmllint ...
```

Also, if you want to ensure that `xmllint` and `xsltproc` will not perform any network access, you can do something like

```
./configure ... XMLLINT="xmllint --nonet" XSLTPROC="xsltproc --nonet" ...
```
