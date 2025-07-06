# Assignment 1: Securing and Monitoring an Authenticated Flask App

Youtube Demo : https://youtu.be/55-etRc_vak 

# 🔐 CST8919 – Assignment 1: Securing & Monitoring an Authenticated Flask App

## 🧭 Objective

This assignment demonstrates the integration of **authentication**, **logging**, and **monitoring** in a secure Flask application. The goal is to simulate a real-world **DevSecOps scenario** by combining:

- **Authentication (SSO via Auth0)**  
- **Deployment to Azure App Service**  
- **Structured logging of user events**  
- **Observability through Azure Monitor and KQL-based alerting**

---

## 🛠️ Tools & Technologies

| Category           | Tools Used                           |
|-------------------|--------------------------------------|
| **Web Framework** | Flask (Python)                       |
| **Authentication**| Auth0 (OAuth 2.0 / OpenID Connect)   |
| **Cloud Hosting** | Azure App Service                    |
| **Logging**        | `app.logger` + Azure Monitor         |
| **Monitoring**     | Azure Log Analytics (KQL queries)    |
| **Alerting**       | Azure Alerts + Action Group (Email)  |
| **Dev Tools**      | VS Code, GitHub, Postman / .http     |

---

## 🔄 Workflow Overview

### 1. **Authentication Integration**
- Auth0 is configured to provide secure Single Sign-On (SSO).
- Successful and failed logins are logged with structured metadata.

### 2. **Logging Critical Events**
- Custom logs are emitted for:
  - ✅ Successful and failed logins
  - ✅ Access to protected endpoints
  - ❌ Unauthorized access attempts
- Logs include: username, timestamp, route, and message.

### 3. **Deployment to Azure**
- The Flask app is deployed to **Azure App Service** using CLI.
- Azure App Configuration is used to securely store secrets (e.g., Flask session key).
- Diagnostic logging is enabled and routed to **Log Analytics Workspace**.

### 4. **Monitoring via Azure Monitor + KQL**
- All structured logs are queryable via **Kusto Query Language (KQL)**.
- Example monitoring query identifies abnormal access patterns:

```kql
AppServiceConsoleLogs
| where TimeGenerated > ago(15m)
| where ResultDescription has "PROTECTED_ACCESS"
| parse ResultDescription with "PROTECTED_ACCESS: username=" username ", timestamp=" timestamp ", path=" path ", message=" message"
| summarize access_count = count() by username, bin(TimeGenerated, 5m)
| where access_count > 10
```

### 5. **Automated Alerting**

- An Azure alert rule is created to trigger when a user accesses /protected more than 10 times in 15 minutes.
- An email notification is sent via Action Group when the threshold is breached.

### 6.📈 **Outcome**

This lab successfully demonstrated:

✅ Secure integration of identity provider (Auth0)
✅ Real-time observability using Azure Monitor
✅ Automated detection of suspicious activity with KQL
✅ Actionable alerts through Azure native tools
