# Reflection

## 1. What issues did the static analysis tools identify?

Pylint identified code-quality issues such as wrong naming, missing docstrings, a mutable default argument, and an unused parameter. Flake8 identified formatting errors, including missing whitespaces and blank-line problems. Bandit identified potentially unsafe shell execution, pickle deserialization, and use of a standard random generator.

## 2. Which issue was the most serious, and why?

The shell-command construction was potentially the most serious because untrusted input could influence a command executed by the operating system. Loading untrusted pickle files was also risky because deserialization can execute malicious code. Both issues required careful review rather than simply suppressing tool warnings.

## 3. How did you fix and verify the issues?

I improved function names, added docstrings, removed the mutable default argument, implemented sorting, and corrected formatting. I replaced pickle storage with JSON and addressed the subprocess-related findings. After making the changes, I reran Pylint, Flake8, and Bandit to check the results and ran the program to verify its behavior.

## 4. What did you learn from this exercise?

I learned that static-analysis tools identify different categories of problems and that no single tool catches every bug. A program can run successfully while still containing maintainability or security risks. I also learned to review each warning, apply an appropriate fix, and rerun tests after changing code.
