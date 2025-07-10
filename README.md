# Valkey Tests 🧪

A test suite for validating Valkey client interactions, including publishing, subscribing, and connection handling.

## Table of Contents

- [Overview](#Overview)
- [Features](#Features)
- [Requirements](#Requirements)
- [Installation](#Installation)
- [Configuration](#Configuration)
- [Usage](#Usage)
- [Contributing](#Contributing)
- [License](#License)

---

## 📦 Overview

This repository provides a suite of tests to validate the functionality of the Valkey client. It includes:

- API connectivity checks
- Message publishing and subscription tests
- SSL/TLS validation and certificate handling
- Edge case and error handling scenarios

---

## 🧰 Requirements

- Python 3.8+
- `valkey` library (Python client)
- `PyYaml`

---

## ⚙️ Installation

1. Clone this repo:
   ```bash
   git clone https://github.com/iospap/valkey_tests.git
   cd valkey_tests

2. Create environment:
   ```bash
   python3 -m venv .env

3. Install requirements
   ```bash
   .env/bin/python -m pip install -r requirements.txt



## 🛠️ Configuration

Edit config.yaml (or .env) to set your connection details:

```yaml
connection:
  host: your.valkey.host
  port: 6379
  user: your.user
  password: your.password

publish:
  channel: 'test-channel'
  message:
    key1: value1
    key2: value2

subscribe:
  pattern: 'test*' 
  channels: ['test-channel']

```


## 🚀 Usage

Publish
  Run:

  ```bash
    python publish.py
  ```

Subscribe
  Run:

  ```bash
    python subscribe.py
  ```

## 🤝 Contributing
Contributions are welcome! To contribute:

Fork the repository

Create a feature branch

Write tests or improve existing ones

Submit a pull request for review


## 📄 License
This project is distributed under the GNU General Public License v3.0