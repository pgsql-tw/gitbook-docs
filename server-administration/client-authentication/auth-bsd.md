## 20.14. BSD Authentication [#](#AUTH-BSD)

<a id="id-1.6.7.21.2"></a>

This authentication method operates similarly to
`password` except that it uses BSD Authentication
to verify the password. BSD Authentication is used only
to validate user name/password pairs. Therefore the user's role must
already exist in the database before BSD Authentication can be used
for authentication. The BSD Authentication framework is currently
only available on OpenBSD.

BSD Authentication in PostgreSQL uses
the `auth-postgresql` login type and authenticates with
the `postgresql` login class if that's defined
in `login.conf`. By default that login class does not
exist, and PostgreSQL will use the default login class.

### Note

To use BSD Authentication, the PostgreSQL user account (that is, the
operating system user running the server) must first be added to
the `auth` group. The `auth` group
exists by default on OpenBSD systems.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/auth-bsd.html)（英文原文，待翻譯）
