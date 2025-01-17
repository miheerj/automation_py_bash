# Setup Guide for Azure DevOps Release Audit Script

## Prerequisites
1. **Python 3.8+**: Install Python from [python.org](https://www.python.org/).
2. **Azure DevOps PAT**:  
   - Go to Azure DevOps > Personal Access Tokens > New Token.
   - Select scopes: `Release`, `Project and Team`.
   - Copy and save the token securely.

3. **SMTP Server**: Ensure access to an SMTP server for email delivery.

---

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/miheerj/automation_py_bash.git
   cd audit-releases-ado
