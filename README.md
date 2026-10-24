# 🛡️ PT Web Lab — Web Application Security

**By Itay Bechor | Build • Secure • Test • Document**

A personal cybersecurity lab combining web application development, firewall configuration, security testing, remediation, and documentation.

![PT Web Lab cover](./slide-01.png)

---

## 🎯 About the Project

I built a registration and login application, deployed it behind an OPNsense firewall, and tested its security controls in a controlled virtual environment.

The project follows a request from the testing workstation through the firewall and web server to the application and database.

The goal was to develop practical skills in secure development, network defense, troubleshooting, and evidence-based security testing.

## 🧰 Technologies

| Area | Tools |
|---|---|
| Application | Python, Flask |
| Database | SQLite |
| Password hashing | scrypt |
| Web server | Nginx |
| Application server | Gunicorn |
| Firewall | OPNsense |
| Virtualization | VMware |
| Operating systems | Kali Linux, Windows |
| Testing | Nmap, curl, PowerShell, browser tools |

## 🌐 Architecture

The Windows testing workstation connects to the OPNsense WAN interface over HTTPS.

OPNsense forwards permitted traffic to the internal Kali server. Nginx handles HTTPS and forwards application requests to Gunicorn on localhost.

The application stores account and session data in SQLite.

## 🔐 Security Controls

- Password hashing with scrypt.
- Parameterized SQL queries.
- Server-side sessions with hashed session tokens.
- Session expiration and logout invalidation.
- Secure, HttpOnly, and SameSite cookie attributes.
- POST request Origin validation.
- CSRF token validation for authenticated logout.
- IP-based login and registration rate limiting.
- Input validation and HTML output escaping.
- HTTPS and TLS configuration hardening.
- Firewall source restrictions and network segmentation.
- Application and firewall logging.

---

## 📸 Project Walkthrough — 30 Slides

The presentation images contain Hebrew annotations. English explanations accompany each slide below.

### 01 — Project Introduction

The cover above introduces the lab: application development, defensive configuration, and practical security testing.

### 02 — Building the Application

A registration and login application built with Python, Flask, and SQLite.

![Web application](./slide-02.png)

### 03 — Password Hashing

Database inspection confirmed that passwords were stored as scrypt hashes rather than plaintext.

![Password hashing](./slide-03.png)

### 04 — Network Segmentation

OPNsense separates the testing network from the internal application network through WAN and LAN interfaces.

![Network segmentation](./slide-04.png)

### 05 — Automatic Service Startup

The application and Nginx were configured to run as services and start automatically.

![Application services](./slide-05.png)

### 06 — Stable Server Addressing

A DHCP reservation maintains a consistent internal server address for the forwarding configuration.

![Server addressing](./slide-06.png)

### 07 — Restricting Access by Source

The HTTPS rule permits the designated testing workstation instead of allowing the entire network.

![Source restriction](./slide-07.png)

### 08 — HTTPS Port Forwarding

The NAT configuration forwards permitted WAN traffic on port 443 to the internal application's HTTPS endpoint.

![HTTPS forwarding](./slide-08.png)

### 09 — Authorized Connection Test

A successful TCP test confirmed that the permitted workstation could reach the configured HTTPS endpoint.

![Authorized connection test](./slide-09.png)

### 10 — Unauthorized Source Test

A connection attempt from a source address outside the allow rule failed.

![Unauthorized source test](./slide-10.png)

### 11 — Firewall Log Verification

Firewall logs were correlated with the test source and connection result to verify blocking.

![Firewall log evidence](./slide-11.png)

### 12 — Authentication Baseline

A test account successfully logged in and accessed the dashboard, establishing a baseline for further checks.

![Authentication baseline](./slide-12.png)

### 13 — Registration Input Validation

A username containing a script tag was rejected with HTTP 400. This result applies to the specific input tested.

![Registration input validation](./slide-13.png)

### 14 — Output Escaping

The inspected HTML response contained escaped characters rather than an active script tag.

![HTML output escaping](./slide-14.png)

### 15 — Login Rate Limiting

Five failed login requests returned HTTP 401. The sixth returned HTTP 429.

The lab implementation uses IP-based, in-memory rate limiting.

![Login rate limiting](./slide-15.png)

### 16 — Session Cookie Attributes

The authentication cookie was checked for Secure, HttpOnly, and SameSite=Lax attributes.

The session token value is excluded from the evidence image.

![Session cookie attributes](./slide-16.png)

### 17 — Session Invalidation After Logout

Reusing the previous session after logout resulted in a redirect to the login page.

![Logout session invalidation](./slide-17.png)

### 18 — Request Origin Validation

An allowed HTTPS Origin reached authentication processing. A foreign Origin and a missing Origin returned HTTP 403.

![Request Origin validation](./slide-18.png)

### 19 — Logout CSRF Protection

An authenticated logout request without the required CSRF token returned HTTP 403.

Dashboard checks before and after the request confirmed that the rejected request had not logged the user out.

![Logout CSRF protection](./slide-19.png)

### 20 — Password Length Boundaries

Registration was tested with passwords of 0, 14, 15, 128, and 129 characters to verify the configured 15–128 character policy.

![Password length boundary tests](./slide-20.png)

### 21 — Full Password Verification

A 128-character password authenticated successfully. Changing its final character or shortening it caused authentication to fail for the test account.

![Full password verification](./slide-21.png)

### 22 — Reverse Proxy Configuration

Nginx handles HTTPS and forwards application requests to Gunicorn at 127.0.0.1:8000.

![Reverse proxy configuration](./slide-22.png)

### 23 — TLS Hardening and Retesting

After configuration changes, the Nmap scan showed TLS 1.2 with ECDHE and GCM or ChaCha20 cipher suites, alongside TLS 1.3.

![TLS hardening results](./slide-23.png)

### 24 — Listening Port Verification

Nginx listens for HTTPS on the server interface. Gunicorn listens on loopback rather than exposing port 8000 directly on the network interface.

![Listening port verification](./slide-24.png)

### 25 — Expired Session Rejection

A check approximately 52 minutes after session creation redirected to login.

The configured session lifetime is 30 minutes; the exact expiration boundary was not measured.

![Session expiration test](./slide-25.png)

### 26 — Sensitive File Exposure Checks

Tested paths for database files, Python source files, and backups returned HTTP 404.

The login page returned HTTP 200 as a control.

![Sensitive file exposure checks](./slide-26.png)

### 27 — Database Initialization Fix

Database initialization was updated to create the sessions table.

Follow-up checks covered initialization, service operation, login, and logout.

![Database initialization fix](./slide-27.png)

### 28 — Creating a Backup

A backup package was created for the application, database, and service configuration.

The application returned to an active state afterward.

![Backup creation](./slide-28.png)

### 29 — Copying the Backup to the Host

The backup package was copied to the Windows host.

A complete restore exercise remains to be verified. Backup archives containing private configuration or credentials are excluded from the public project materials.

![Backup copied to the host](./slide-29.png)

### 30 — Project Summary

The project documents a practical cycle of building, configuring, testing, fixing, and retesting.

![Project summary](./slide-30.png)

---

## 📋 Information Security Guidelines

A separate Hebrew policy document was prepared for an example IT services organization.

It addresses asset inventory, access management, endpoint protection, network security, secure development, logging, backups, and incident response.

These are proposed organizational guidelines. Their scope is broader than the controls implemented in this lab.

## 🔎 Scope and Limitations

This repository presents a personal learning project and its documented security checks.

- Testing was limited to my own lab environment.
- Results apply to the requests and configurations tested.
- The lab uses a self-signed TLS certificate.
- Rate limiting uses process-local memory.
- A copied backup does not prove that a complete restoration will succeed.
- The documented checks do not constitute exhaustive penetration testing or a guarantee of security.

The decorative cover artwork was AI-generated. Application and testing screenshots document the lab.

## 💡 Key Takeaways

- Verify both permitted and denied access.
- Correlate test results with logs.
- Retest after changing a security configuration.
- Distinguish observed evidence from assumptions.
- Document limitations and remaining verification work.
- Treat backup creation and restoration testing as separate tasks.

## 💻 Source Code Status

The published materials currently focus on project documentation and screenshots.

The final runnable application source is not included in this documentation upload.

## 👤 Author

**Itay Bechor**

Personal cybersecurity project focused on web application security, network defense, and practical security testing.
