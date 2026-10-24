# 🛡️ PT Web Lab — Web Application Security

### Build • Secure • Test • Document

A hands-on cybersecurity project by **Itay Bechor**, combining web development, network security, application hardening, and penetration testing in a personal virtual lab.

![PT Web Lab — Project Cover](images/slides/slide-01.png)

---

## 🎯 Project Overview

What does it take to protect a web application beyond simply adding a login page?

In this project, I built a registration and authentication application, placed it behind a firewall, implemented security controls, and tested how those controls behaved under different conditions.

The goal was to understand the entire path of a request: from the testing workstation, through the firewall and web server, to the application and database.

All security testing was performed within my own lab environment.

## 🧰 Technology Stack

| Component | Technology |
|---|---|
| Application | Python and Flask |
| Database | SQLite |
| Password hashing | scrypt |
| Web server and HTTPS | Nginx |
| Application server | Gunicorn |
| Firewall and network segmentation | OPNsense |
| Application host | Kali Linux |
| Testing workstation | Windows |
| Virtualization | VMware |
| Testing tools | Nmap, curl, browser tools, and PowerShell |

## 🌐 Lab Architecture

The Windows testing workstation accesses the application through the OPNsense WAN interface.

An HTTPS forwarding rule directs authorized traffic to Nginx on the internal Kali server. Nginx then forwards application requests to Gunicorn, which listens on localhost.

Access to the application is restricted by firewall rules.

## 🔐 Security Controls

- Password hashing with scrypt.
- Parameterized SQL queries.
- Server-side sessions with hashed session tokens.
- Session expiration and invalidation after logout.
- Secure, HttpOnly, and SameSite cookie attributes.
- Origin validation for POST requests.
- CSRF token validation for authenticated logout.
- IP-based rate limiting for authentication and registration.
- Input validation and template output escaping.
- HTTPS and restricted TLS cipher configuration.
- Firewall filtering and network segmentation.
- Application and firewall logs for troubleshooting and evidence.

## 📚 Project Documents

- [30-slide project presentation — PDF](docs/PT-Web-Lab-30-Slides.pdf)
- [Editable presentation — PowerPoint](docs/PT-Web-Lab-30-Slides.pptx)
- [Information Security Guidelines — Hebrew PDF](docs/Security-Guidelines-HE.pdf)
- [Architecture notes](docs/ARCHITECTURE.md)
- [Testing notes and limitations](docs/TESTING.md)

The security guidelines describe a proposed policy for an example organization. They cover a broader scope than the controls implemented in this lab.

---

## 📸 Project Walkthrough

The following 30 slides document the lab, configuration, testing, remediation, and backup process.

### 01 — Project Introduction

A personal lab connecting application development, defensive configuration, and practical security testing.

![Project introduction](images/slides/slide-01.png)

### 02 — Building the Web Application

A registration and login application built with Python, Flask, and SQLite.

![Web application](images/slides/slide-02.png)

### 03 — Password Storage

Database inspection confirmed the use of scrypt password hashes rather than plaintext passwords.

![Password hashing](images/slides/slide-03.png)

### 04 — Network Segmentation

OPNsense separates the testing network from the internal application network using WAN and LAN interfaces.

![Network segmentation](images/slides/slide-04.png)

### 05 — Application Services

The application and Nginx were configured to run as services and start automatically.

![Application services](images/slides/slide-05.png)

### 06 — Stable Server Addressing

A DHCP reservation keeps the application server address consistent with the firewall forwarding rule.

![Server addressing](images/slides/slide-06.png)

### 07 — Restricting the Allowed Source

The HTTPS access rule permits the designated testing workstation rather than the entire network.

![Source restriction](images/slides/slide-07.png)

### 08 — HTTPS Port Forwarding

The NAT rule forwards authorized HTTPS traffic to the internal application server on port 443.

![HTTPS forwarding](images/slides/slide-08.png)

### 09 — Authorized Connectivity Test

A successful TCP connection confirmed that the permitted workstation could reach the configured HTTPS endpoint.

![Authorized connection](images/slides/slide-09.png)

### 10 — Unauthorized Source Test

A connection attempt from a source address outside the allow rule failed.

![Unauthorized source test](images/slides/slide-10.png)

### 11 — Firewall Log Evidence

Firewall logs were checked alongside the connection result to confirm that the tested traffic was blocked.

![Firewall logs](images/slides/slide-11.png)

### 12 — Successful Authentication Baseline

A test account successfully logged in and accessed the dashboard, establishing a baseline for subsequent checks.

![Authentication baseline](images/slides/slide-12.png)

### 13 — Registration Input Validation

A username containing a script tag was rejected with HTTP 400. This result applies to the specific input tested.

![Input validation](images/slides/slide-13.png)

### 14 — HTML Output Escaping

The returned HTML showed escaped characters rather than an active script tag in the inspected response.

![Output escaping](images/slides/slide-14.png)

### 15 — Login Rate Limiting

Five failed login attempts returned HTTP 401. The sixth returned HTTP 429.

The lab implementation uses IP-based, in-memory rate limiting.

![Rate limiting](images/slides/slide-15.png)

### 16 — Session Cookie Attributes

The authentication cookie was checked for Secure, HttpOnly, and SameSite=Lax attributes.

The session token value is excluded from this evidence image.

![Cookie attributes](images/slides/slide-16.png)

### 17 — Logout Invalidation

Reusing the previous session after logout resulted in a redirect to the login page.

![Logout invalidation](images/slides/slide-17.png)

### 18 — Request Origin Validation

Requests with an allowed HTTPS Origin reached authentication processing. Requests with a foreign or missing Origin returned HTTP 403.

![Origin validation](images/slides/slide-18.png)

### 19 — Logout CSRF Protection

A logout request without the required CSRF token returned HTTP 403. Dashboard checks confirmed that the rejected request had not logged the user out.

![Logout CSRF protection](images/slides/slide-19.png)

### 20 — Password Length Boundaries

Registration was tested with password lengths of 0, 14, 15, 128, and 129 characters to verify the configured 15–128 character policy.

![Password length boundaries](images/slides/slide-20.png)

### 21 — Full Password Verification

A 128-character password authenticated successfully. Changing its final character or shortening it caused authentication to fail for the test account.

![Full password verification](images/slides/slide-21.png)

### 22 — Reverse Proxy Configuration

Nginx handles HTTPS and forwards requests to Gunicorn at 127.0.0.1:8000.

![Reverse proxy configuration](images/slides/slide-22.png)

### 23 — TLS Hardening and Retesting

After configuration changes, the Nmap scan showed TLS 1.2 with ECDHE and GCM or ChaCha20 cipher suites, alongside TLS 1.3.

![TLS hardening](images/slides/slide-23.png)

### 24 — Listening Port Verification

Nginx listens for HTTPS on the server interface. Gunicorn listens on loopback rather than exposing port 8000 directly on the network interface.

![Listening ports](images/slides/slide-24.png)

### 25 — Expired Session Rejection

A later check, approximately 52 minutes after session creation, redirected to login.

The configured lifetime is 30 minutes; the exact expiration boundary was not measured.

![Session expiration](images/slides/slide-25.png)

### 26 — Sensitive File Exposure Checks

Tested paths for database files, Python source files, and backups returned HTTP 404. The login page returned HTTP 200 as a control.

![Sensitive file checks](images/slides/slide-26.png)

### 27 — Database Initialization Fix

Database initialization was updated to create the sessions table. Follow-up checks covered initialization, service operation, login, and logout.

![Database initialization fix](images/slides/slide-27.png)

### 28 — Creating a Backup

A backup package was created for the application, database, and service configuration. The application returned to an active state afterward.

![Backup creation](images/slides/slide-28.png)

### 29 — Copying the Backup to the Host

The backup package was copied to the Windows host. A complete restore exercise remains to be verified.

Backup archives and private configuration files are not included in this public repository.

![Backup copy](images/slides/slide-29.png)

### 30 — Project Summary

The lab demonstrates a documented cycle of building, configuring, testing, fixing, and retesting.

![Project summary](images/slides/slide-30.png)

---

## 🔎 Scope and Limitations

This is a learning project with a defined set of documented checks, not a claim of complete security or exhaustive penetration testing.

- Test results apply to the requests, configurations, and conditions shown.
- The lab uses a self-signed TLS certificate.
- Rate limiting uses process-local memory and is not a distributed deployment design.
- Copying a backup does not verify that a full restoration will succeed.
- The security policy includes proposed organizational controls beyond the lab implementation.
- The decorative cover artwork was AI-generated; the application and testing screenshots document the lab.

## 📁 Repository Contents

| Path | Contents |
|---|---|
| `docs/` | Presentations, security guidelines, architecture, and testing notes |
| `images/slides/` | All 30 presentation slides |
| `images/evidence/` | Selected evidence screenshots |
| `tools/` | Source collection utility |
| `src/` | Notes about the application source |

**Source status:** This documentation package does not yet include the final runnable application source. The collection utility is a supporting tool, not the application itself.

## 💡 What I Learned

This project helped me connect application behavior with network configuration and security evidence.

It reinforced the importance of testing both allowed and denied actions, correlating results with logs, verifying changes after remediation, and clearly distinguishing what was tested from what remains unverified.

## 👤 Author

**Itay Bechor**

Personal cybersecurity lab focused on web application security, network defense, and practical security testing.
