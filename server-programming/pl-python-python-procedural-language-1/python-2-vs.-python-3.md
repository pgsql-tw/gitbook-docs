# 45.1. Python 2 vs. Python 3

PL/Python supports both the Python 2 and Python 3 language variants. (The PostgreSQL installation instructions might contain more precise information about the exact supported minor versions of Python.) Because the Python 2 and Python 3 language variants are incompatible in some important aspects, the following naming and transitioning scheme is used by PL/Python to avoid mixing them:

* The PostgreSQL language named `plpython2u` implements PL/Python based on the Python 2 language variant.
* The PostgreSQL language named `plpython3u` implements PL/Python based on the Python 3 language variant.
* The language named `plpythonu` implements PL/Python based on the default Python language variant, which is currently Python 2. (This default is independent of what any local Python installations might consider to be their “default”, for example, what `/usr/bin/python` might be.) The default will probably be changed to Python 3 in a distant future release of PostgreSQL, depending on the progress of the migration to Python 3 in the Python community.

This scheme is analogous to the recommendations in [PEP 394](https://www.python.org/dev/peps/pep-0394/) regarding the naming and transitioning of the `python` command.

It depends on the build configuration or the installed packages whether PL/Python for Python 2 or Python 3 or both are available.

#### Tip

The built variant depends on which Python version was found during the installation or which version was explicitly set using the `PYTHON` environment variable; see [Section 16.4](https://www.postgresql.org/docs/12/install-procedure.html). To make both variants of PL/Python available in one installation, the source tree has to be configured and built twice.

This results in the following usage and migration strategy:

*   Existing users and users who are currently not interested in Python 3 use the language name `plpythonu` and don't have to change anything for the foreseeable future. It is recommended to gradually “future-proof” the code via migration to Python 2.6/2.7 to simplify the eventual migration to Python 3.

    In practice, many PL/Python functions will migrate to Python 3 with few or no changes.
* Users who know that they have heavily Python 2 dependent code and don't plan to ever change it can make use of the `plpython2u` language name. This will continue to work into the very distant future, until Python 2 support might be completely dropped by PostgreSQL.
* Users who want to dive into Python 3 can use the `plpython3u` language name, which will keep working forever by today's standards. In the distant future, when Python 3 might become the default, they might like to remove the “3” for aesthetic reasons.
* Daredevils, who want to build a Python-3-only operating system environment, can change the contents of [`pg_pltemplate`](https://www.postgresql.org/docs/12/catalog-pg-pltemplate.html) to make `plpythonu` be equivalent to `plpython3u`, keeping in mind that this would make their installation incompatible with most of the rest of the world.

See also the document [What's New In Python 3.0](https://docs.python.org/3/whatsnew/3.0.html) for more information about porting to Python 3.

It is not allowed to use PL/Python based on Python 2 and PL/Python based on Python 3 in the same session, because the symbols in the dynamic modules would clash, which could result in crashes of the PostgreSQL server process. There is a check that prevents mixing Python major versions in a session, which will abort the session if a mismatch is detected. It is possible, however, to use both PL/Python variants in the same database, from separate sessions.
