# Contributing to Smart Resume AI

We welcome contributions to improve Smart Resume AI! To ensure a smooth collaboration, please follow these guidelines:

---

## 1. Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md) at all times.

---

## 2. How Can I Contribute?

### 2.1 Reporting Bugs
* Search the existing issues to ensure the bug has not been reported.
* Open a new issue with a clear title, description, and steps to reproduce (including logs and stack traces).

### 2.2 Suggesting Features
* Open an issue describing the proposed feature, target audience, and why it is valuable to the platform.

### 2.3 Pull Requests
1. Fork the repository and create a branch from `main`:
   ```bash
   git checkout -b feature/amazing-feature
   ```
2. Implement your changes, ensuring code is formatted and variables are clean.
3. Write automated unit tests under the `tests/` directory to cover new logic.
4. Run the test suite:
   ```bash
   python -m pytest tests/
   ```
5. Commit your changes with descriptive messages:
   ```bash
   git commit -m "feat: add amazing new feature"
   ```
6. Push to your branch and open a Pull Request against `main`.

---

## 3. Style Guidelines

* **Python**: Adhere to PEP 8 naming conventions and structure guidelines. Use black for formatting.
* **Streamlit**: Keep components modular, avoiding mixing rendering code directly with business logic (use the `services/` layer).
* **Database**: Always use parameterized queries for SQLite operations.
