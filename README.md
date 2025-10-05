# Python Test Project

Purpose
- This repository provides simple, concrete examples of Python package structures and serves as a sandbox for proof-of-concept (PoC) work. It is intentionally lightweight to make it easy to explore layout, imports, and basic packaging patterns.

What’s included
- A minimal package: `python_test_project/`
  - `kvstore/`: a toy key–value store demonstrating package structure, modular design, and interchangeable backends
    - Backends: in-memory and filesystem
    - Supporting modules: API, base classes, factory, config, and error types
  - Example scripts:
    - `kvstore_example.py`: shows how to use the kvstore API
    - `main.py`: entry-point style script you can run directly

Quick start
1) Ensure you have Python 3.11+ installed.
2) From the project root, you can run the examples:
   - Run the main script:
     - `python -m python_test_project.main`
   - Run the kvstore example:
     - `python -m python_test_project.kvstore_example`

Repository goals
- Demonstrate clean, readable package organization
- Provide a safe place to try PoC ideas without production constraints
- Offer small, testable components you can extend or replace

Notes
- Requires Python 3.11+; examples may use 3.11 features (e.g., typing improvements and stdlib additions).
- This project is not intended for production use; it is for learning and experimentation.
- Feel free to copy patterns you find useful into your own projects.