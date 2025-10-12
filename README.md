# Amikom Students Enumerator

# Bug Fixed, this tool doesn't work anymore
---
![image](https://github.com/user-attachments/assets/fc9df9a4-f0b8-42ad-ba31-f9365256faa6)
---
this tools is used for get all picture of students in amikom.ac.id

this tools always work before the bug is updated/fixed



disclaimer : this tools is build for educational purpose


---
# Important Information: Student Photo System Vulnerabilities

## 1. Data Leakage (Mass Enumeration & IDOR)

The student photo system uses a predictable URL pattern without proper authentication or authorization.

Impact:
- Mass download of all student photos is possible.
- Risks include identity theft, phishing, and social engineering attacks.

## 2. Potential Overload (Denial of Service)

Using a multi-threaded downloader can send thousands of simultaneous requests.

Impact:
- The server may become slow or temporarily unavailable.
- Other services on the same server may also be affected.

## Summary of Issues

| Issue | Impact |
|--------|--------|
| Predictable URL access | Personal data leakage (student photos) |
| Excessive concurrent requests | Potential server overload and instability |
