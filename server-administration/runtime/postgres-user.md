## 18.1. The PostgreSQL User Account [#](#POSTGRES-USER)

<a id="id-1.6.5.4.2"></a>

As with any server daemon that is accessible to the outside world,
it is advisable to run PostgreSQL under a
separate user account. This user account should only own the data
that is managed by the server, and should not be shared with other
daemons. (For example, using the user `nobody` is a bad
idea.) In particular, it is advisable that this user account not own
the PostgreSQL executable files, to ensure
that a compromised server process could not modify those executables.

Pre-packaged versions of PostgreSQL will
typically create a suitable user account automatically during
package installation.

To add a Unix user account to your system, look for a command
`useradd` or `adduser`. The user
name postgres is often used, and is assumed
throughout this book, but you can use another name if you like.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/postgres-user.html)（英文原文，待翻譯）
