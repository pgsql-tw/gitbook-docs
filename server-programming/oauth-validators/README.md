## Chapter 50. OAuth Validator Modules

**Table of Contents**

[50.1. Safely Designing a Validator Module](oauth-validator-design.md)
:   [50.1.1. Validator Responsibilities](oauth-validator-design.md#OAUTH-VALIDATOR-DESIGN-RESPONSIBILITIES)

    [50.1.2. General Coding Guidelines](oauth-validator-design.md#OAUTH-VALIDATOR-DESIGN-GUIDELINES)

    [50.1.3. Authorizing Users (Usermap Delegation)](oauth-validator-design.md#OAUTH-VALIDATOR-DESIGN-USERMAP-DELEGATION)

[50.2. Initialization Functions](oauth-validator-init.md)

[50.3. OAuth Validator Callbacks](oauth-validator-callbacks.md)
:   [50.3.1. Startup Callback](oauth-validator-callbacks.md#OAUTH-VALIDATOR-CALLBACK-STARTUP)

    [50.3.2. Validate Callback](oauth-validator-callbacks.md#OAUTH-VALIDATOR-CALLBACK-VALIDATE)

    [50.3.3. Shutdown Callback](oauth-validator-callbacks.md#OAUTH-VALIDATOR-CALLBACK-SHUTDOWN)

<a id="id-1.8.17.2"></a>

PostgreSQL provides infrastructure for creating
custom modules to perform server-side validation of OAuth bearer tokens.
Because OAuth implementations vary so wildly, and bearer token validation is
heavily dependent on the issuing party, the server cannot check the token
itself; validator modules provide the integration layer between the server
and the OAuth provider in use.

OAuth validator modules must at least consist of an initialization function
(see [Section 50.2](oauth-validator-init.md)) and the required callback for
performing validation (see [Section 50.3.2](oauth-validator-callbacks.md#OAUTH-VALIDATOR-CALLBACK-VALIDATE)).

### Warning

Since a misbehaving validator might let unauthorized users into the database,
correct implementation is crucial for server safety. See
[Section 50.1](oauth-validator-design.md) for design considerations.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/oauth-validators.html)（英文原文，待翻譯）
