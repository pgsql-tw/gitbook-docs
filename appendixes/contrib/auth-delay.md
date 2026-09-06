## F.2. auth_delay — pause on authentication failure [#](#AUTH-DELAY)

[F.2.1. Configuration Parameters](auth-delay.md#AUTH-DELAY-CONFIGURATION-PARAMETERS)

[F.2.2. Author](auth-delay.md#AUTH-DELAY-AUTHOR)

<a id="id-1.11.7.12.2"></a>

`auth_delay` causes the server to pause briefly before
reporting authentication failure, to make brute-force attacks on database
passwords more difficult. Note that it does nothing to prevent
denial-of-service attacks, and may even exacerbate them, since processes
that are waiting before reporting authentication failure will still consume
connection slots.

In order to function, this module must be loaded via
[shared_preload_libraries](../../server-administration/runtime-config/runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES) in `postgresql.conf`.

<a id="AUTH-DELAY-CONFIGURATION-PARAMETERS"></a>

### F.2.1. Configuration Parameters [#](#AUTH-DELAY-CONFIGURATION-PARAMETERS)

`auth_delay.milliseconds` (`integer`) <a id="id-1.11.7.12.5.2.1.1.3"></a>
:   The number of milliseconds to wait before reporting an authentication
    failure. The default is 0.

These parameters must be set in `postgresql.conf`.
Typical usage might be:

```

# postgresql.conf
shared_preload_libraries = 'auth_delay'

auth_delay.milliseconds = '500'
```

<a id="AUTH-DELAY-AUTHOR"></a>

### F.2.2. Author [#](#AUTH-DELAY-AUTHOR)

KaiGai Kohei `<kaigai@ak.jp.nec.com>`

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/auth-delay.html)（英文原文，待翻譯）
