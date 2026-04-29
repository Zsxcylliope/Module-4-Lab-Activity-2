# Module 4 Lab Activity 2: Secure API

## Overview
This repository contains the completed **Lab Activity 2: API Security, Encryption, and Security Best Practices**. It is a Secure Payment API built with Django that securely handles sensitive user information by implementing multiple layers of protection.

## Security Features Implemented

1. **Password Hashing (Argon2)**
   - Replaced default Django password hashing with the highly secure **Argon2** algorithm (`argon2-cffi`) to protect user credentials.

2. **Data Encryption (Fernet AES)**
   - Sensitive fields, such as credit card numbers, are **encrypted** using the `cryptography` library before being stored in the SQLite database as binary data.

3. **API Rate Limiting**
   - Protected the `/api/login/` endpoint against brute-force and credential-stuffing attacks by using `django-ratelimit`.
   - Limits users to **5 requests per minute** per IP address. Exceeding this limit automatically blocks the user with a `429 Too Many Requests` error.

4. **Secure Logging**
   - Implemented Django's `logging` module to track and monitor security-related events.
   - Specifically logs warnings (e.g., *"Multiple failed login attempts detected"*) to a dedicated `security.log` file for auditing purposes.

## Testing Documentation
Screenshots verifying the security testing requirements have been uploaded to the `Module 4 Lab 2_Screenshot` folder. They demonstrate the following scenarios:
* **Access without authentication:** `401 Unauthorized` responses.
* **Excessive API requests:** `429 Too Many Requests` responses triggered by rate limiting.
* **Invalid encrypted payloads / Encryption working:** Validating the data stored securely.
* **Admin Login Attempt:** Logging mechanisms in action.

## Technologies Used
* **Python / Django** (Backend Framework)
* **argon2-cffi** (Password Hashing)
* **cryptography** (Fernet Encryption)
* **django-ratelimit** (API Security)
