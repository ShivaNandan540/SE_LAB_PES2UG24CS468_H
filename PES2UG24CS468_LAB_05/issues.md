# Issue in Code

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Shell command execution | Security - High | 56 | User-controlled event input was included in a shell command, creating a potential command injection risk. | Removed the unused badge-printing function and subprocess dependency. |
| Unsafe pickle deserialization | Security - Medium | 51 | Loading untrusted pickle files can execute malicious code during deserialization. | Replaced pickle storage with JSON serialization and deserialization. |
| Mutable default argument | Code quality | 9 | The default empty list could be shared across function calls. | Used None as the default and created a new list inside the function. |
| Naming conventions | Style | Multiple | Function names and arguments did not follow the snake_case convention. | Renamed functions and arguments and updated their calls. |
| Missing docstrings | Maintainability | Multiple | The module and several functions lacked descriptive documentation. | Added module and function docstrings. |
| Unused argument | Code quality | 39 | The sorting argument was accepted but not used. | Implemented the requested sorting behavior. |
| Unnecessary else | Maintainability | 33 | An else block followed a branch that already returned. | Removed the redundant else block. |
| Formatting violations | Style | Multiple | Missing spaces, blank lines, and correct inline-comment spacing violated Python style guidelines. | Corrected formatting and verified the file using Flake8. |
| Weak random selection | Randomness | 72 | The standard random generator is unsuitable for security-sensitive selections. | Used a cryptographically stronger selection method where required. |
| Subprocess warnings | Security | 73 | Bandit reported subprocess usage and a partially specified executable path. | Removed the unused badge-printing function and its subprocess dependency. |

