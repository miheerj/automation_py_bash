# Azure DevOps Release Audit Script 🚀

## 📋 Overview
This script helps you audit releases in Azure DevOps for a specific date by:
- Fetching all releases from all projects in your organization.
- Identifying `Release` work items associated with the releases.
- Sending a detailed audit email to a specified distribution list.

## ✨ Features
- Supports Azure DevOps multi-project organizations.
- Filters and processes releases by date.
- Automatically sends an audit email with a formatted table of release details.

---

## 📂 Repository Structure
```plaintext
audit-releases_ado/
├── src/
│   ├── audit_releases.py  # Main Python script
├── docs/
│   ├── setup_guide.md     # Detailed setup and configuration guide
│   ├── usage_examples.md  # Example usage scenarios
├── .gitignore             # Files to ignore
├── LICENSE                # License for this project
├── README.md              # Project description and usage
├── requirements.txt       # Python dependencies
