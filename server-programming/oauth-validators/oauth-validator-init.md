## 50.2. Initialization Functions [#](#OAUTH-VALIDATOR-INIT)

<a id="id-1.8.17.7.2"></a>

OAuth validator modules are dynamically loaded from the shared
libraries listed in [oauth_validator_libraries](../../server-administration/runtime-config/runtime-config-connection.md#GUC-OAUTH-VALIDATOR-LIBRARIES).
Modules are loaded on demand when requested from a login in progress.
The normal library search path is used to locate the library. To
provide the validator callbacks and to indicate that the library is an OAuth
validator module a function named
`_PG_oauth_validator_module_init` must be provided. The
return value of the function must be a pointer to a struct of type
`OAuthValidatorCallbacks`, which contains a magic
number and pointers to the module's token validation functions. The returned
pointer must be of server lifetime, which is typically achieved by defining
it as a `static const` variable in global scope.

```

typedef struct OAuthValidatorCallbacks
{
    uint32        magic;            /* must be set to PG_OAUTH_VALIDATOR_MAGIC */

    ValidatorStartupCB startup_cb;
    ValidatorShutdownCB shutdown_cb;
    ValidatorValidateCB validate_cb;
} OAuthValidatorCallbacks;

typedef const OAuthValidatorCallbacks *(*OAuthValidatorModuleInit) (void);
```

Only the `validate_cb` callback is required, the others
are optional.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/oauth-validator-init.html)（英文原文，待翻譯）
