# 23.1. 語系支援

_Locale_ support refers to an application respecting cultural preferences regarding alphabets, sorting, number formatting, etc. PostgreSQL uses the standard ISO C and POSIX locale facilities provided by the server operating system. For additional information refer to the documentation of your system.

#### 23.1.1. Overview

Locale support is automatically initialized when a database cluster is created using `initdb`. `initdb` will initialize the database cluster with the locale setting of its execution environment by default, so if your system is already set to use the locale that you want in your database cluster then there is nothing else you need to do. If you want to use a different locale \(or you are not sure which locale your system is set to\), you can instruct `initdb` exactly which locale to use by specifying the `--locale` option. For example:

```text
initdb --locale=sv_SE
```

This example for Unix systems sets the locale to Swedish \(`sv`\) as spoken in Sweden \(`SE`\). Other possibilities might include `en_US` \(U.S. English\) and `fr_CA` \(French Canadian\). If more than one character set can be used for a locale then the specifications can take the form _`language_territory.codeset`_. For example, `fr_BE.UTF-8` represents the French language \(fr\) as spoken in Belgium \(BE\), with a UTF-8 character set encoding.

What locales are available on your system under what names depends on what was provided by the operating system vendor and what was installed. On most Unix systems, the command `locale -a` will provide a list of available locales. Windows uses more verbose locale names, such as `German_Germany` or `Swedish_Sweden.1252`, but the principles are the same.

Occasionally it is useful to mix rules from several locales, e.g., use English collation rules but Spanish messages. To support that, a set of locale subcategories exist that control only certain aspects of the localization rules:

| `LC_COLLATE` | String sort order |
| --- | --- | --- | --- | --- | --- |
| `LC_CTYPE` | Character classification \(What is a letter? Its upper-case equivalent?\) |
| `LC_MESSAGES` | Language of messages |
| `LC_MONETARY` | Formatting of currency amounts |
| `LC_NUMERIC` | Formatting of numbers |
| `LC_TIME` | Formatting of dates and times |

The category names translate into names of `initdb` options to override the locale choice for a specific category. For instance, to set the locale to French Canadian, but use U.S. rules for formatting currency, use `initdb --locale=fr_CA --lc-monetary=en_US`.

If you want the system to behave as if it had no locale support, use the special locale name `C`, or equivalently `POSIX`.

Some locale categories must have their values fixed when the database is created. You can use different settings for different databases, but once a database is created, you cannot change them for that database anymore. `LC_COLLATE` and `LC_CTYPE` are these categories. They affect the sort order of indexes, so they must be kept fixed, or indexes on text columns would become corrupt. \(But you can alleviate this restriction using collations, as discussed in [Section 23.2](https://www.postgresql.org/docs/10/static/collation.html).\) The default values for these categories are determined when `initdb` is run, and those values are used when new databases are created, unless specified otherwise in the `CREATE DATABASE` command.

The other locale categories can be changed whenever desired by setting the server configuration parameters that have the same name as the locale categories \(see [Section 19.11.2](https://www.postgresql.org/docs/10/static/runtime-config-client.html#RUNTIME-CONFIG-CLIENT-FORMAT) for details\). The values that are chosen by `initdb` are actually only written into the configuration file `postgresql.conf` to serve as defaults when the server is started. If you remove these assignments from `postgresql.conf` then the server will inherit the settings from its execution environment.

Note that the locale behavior of the server is determined by the environment variables seen by the server, not by the environment of any client. Therefore, be careful to configure the correct locale settings before starting the server. A consequence of this is that if client and server are set up in different locales, messages might appear in different languages depending on where they originated.

#### Note

When we speak of inheriting the locale from the execution environment, this means the following on most operating systems: For a given locale category, say the collation, the following environment variables are consulted in this order until one is found to be set: `LC_ALL`, `LC_COLLATE` \(or the variable corresponding to the respective category\), `LANG`. If none of these environment variables are set then the locale defaults to `C`.

Some message localization libraries also look at the environment variable `LANGUAGE` which overrides all other locale settings for the purpose of setting the language of messages. If in doubt, please refer to the documentation of your operating system, in particular the documentation about gettext.

To enable messages to be translated to the user's preferred language, NLS must have been selected at build time \(`configure --enable-nls`\). All other locale support is built in automatically.

#### 23.1.2. Behavior

The locale settings influence the following SQL features:

* Sort order in queries using `ORDER BY` or the standard comparison operators on textual data
* The `upper`, `lower`, and `initcap` functions
* Pattern matching operators \(`LIKE`, `SIMILAR TO`, and POSIX-style regular expressions\); locales affect both case insensitive matching and the classification of characters by character-class regular expressions
* The `to_char` family of functions
* The ability to use indexes with `LIKE` clauses

The drawback of using locales other than `C` or `POSIX` in PostgreSQL is its performance impact. It slows character handling and prevents ordinary indexes from being used by `LIKE`. For this reason use locales only if you actually need them.

As a workaround to allow PostgreSQL to use indexes with `LIKE` clauses under a non-C locale, several custom operator classes exist. These allow the creation of an index that performs a strict character-by-character comparison, ignoring locale comparison rules. Refer to [Section 11.9](https://www.postgresql.org/docs/10/static/indexes-opclass.html) for more information. Another approach is to create indexes using the `C` collation, as discussed in [Section 23.2](https://www.postgresql.org/docs/10/static/collation.html).

#### 23.1.3. Problems

If locale support doesn't work according to the explanation above, check that the locale support in your operating system is correctly configured. To check what locales are installed on your system, you can use the command `locale -a` if your operating system provides it.

Check that PostgreSQL is actually using the locale that you think it is. The `LC_COLLATE` and `LC_CTYPE` settings are determined when a database is created, and cannot be changed except by creating a new database. Other locale settings including `LC_MESSAGES` and `LC_MONETARY` are initially determined by the environment the server is started in, but can be changed on-the-fly. You can check the active locale settings using the `SHOW` command.

The directory `src/test/locale` in the source distribution contains a test suite for PostgreSQL's locale support.

Client applications that handle server-side errors by parsing the text of the error message will obviously have problems when the server's messages are in a different language. Authors of such applications are advised to make use of the error code scheme instead.

Maintaining catalogs of message translations requires the on-going efforts of many volunteers that want to see PostgreSQL speak their preferred language well. If messages in your language are currently not available or not fully translated, your assistance would be appreciated. If you want to help, refer to [Chapter 54](https://www.postgresql.org/docs/10/static/nls.html) or write to the developers' mailing list.

