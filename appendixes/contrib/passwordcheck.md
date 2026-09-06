## F.24. passwordcheck — verify password strength [#](#PASSWORDCHECK)

[F.24.1. Configuration Parameters](passwordcheck.md#PASSWORDCHECK-CONFIGURATION-PARAMETERS)

<a id="id-1.11.7.34.2"></a>

The `passwordcheck` module checks users' passwords
whenever they are set with
[CREATE ROLE](../../reference/sql-commands/sql-createrole.md) or
[ALTER ROLE](../../reference/sql-commands/sql-alterrole.md).
If a password is considered too weak, it will be rejected and
the command will terminate with an error.

To enable this module, add `'$libdir/passwordcheck'`
to [shared_preload_libraries](../../server-administration/runtime-config/runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES) in
`postgresql.conf`, then restart the server.

You can adapt this module to your needs by changing the source code.
For example, you can use
[CrackLib](https://github.com/cracklib/cracklib)
to check passwords — this only requires uncommenting
two lines in the `Makefile` and rebuilding the
module. (We cannot include CrackLib
by default for license reasons.)
Without CrackLib, the module enforces a few
simple rules for password strength, which you can modify or extend
as you see fit.

### Caution

To prevent unencrypted passwords from being sent across the network,
written to the server log or otherwise stolen by a database administrator,
PostgreSQL allows the user to supply
pre-encrypted passwords. Many client programs make use of this
functionality and encrypt the password before sending it to the server.

This limits the usefulness of the `passwordcheck`
module, because in that case it can only try to guess the password.
For this reason, `passwordcheck` is not
recommended if your security requirements are high.
It is more secure to use an external authentication method such as GSSAPI
(see [Chapter 20](../../server-administration/client-authentication/README.md)) than to rely on
passwords within the database.

Alternatively, you could modify `passwordcheck`
to reject pre-encrypted passwords, but forcing users to set their
passwords in clear text carries its own security risks.

<a id="PASSWORDCHECK-CONFIGURATION-PARAMETERS"></a>

### F.24.1. Configuration Parameters [#](#PASSWORDCHECK-CONFIGURATION-PARAMETERS)

`passwordcheck.min_password_length` (`integer`) <a id="id-1.11.7.34.7.2.1.1.3"></a>
:   The minimum acceptable password length in bytes. The default is 8. Only
    superusers can change this setting.

    ### Note

    This parameter has no effect if a user supplies a pre-encrypted
    password.

In ordinary usage, this parameter is set in
`postgresql.conf`, but superusers can alter it on-the-fly
within their own sessions. Typical usage might be:

```

# postgresql.conf
passwordcheck.min_password_length = 12
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/passwordcheck.html)（英文原文，待翻譯）
