import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

# Azure DevOps configuration
ORG_URL = "https://dev.azure.com/<your-organization>"  # Replace with your Azure DevOps org URL
PAT = os.getenv("AZURE_DEVOPS_PAT")  # Add your Personal Access Token as an environment variable

# Email configuration
SMTP_SERVER = "smtp.example.com"  # Replace with your SMTP server
SMTP_PORT = 587  # Update if needed
SMTP_USERNAME = "your_email@example.com"  # Replace with your email
SMTP_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Add your email password as an environment variable
DL_EMAIL = "audit-dl@example.com"  # Distribution list email address

def get_releases_for_date(target_date):
    """Fetch all releases from all projects in the organization for a specific date."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {PAT}"
    }

    # Get all projects
    projects_url = f"{ORG_URL}/_apis/projects?api-version=7.1-preview.4"
    response = requests.get(projects_url, headers=headers)
    response.raise_for_status()
    projects = response.json().get("value", [])

    release_data = []

    for project in projects:
        project_name = project["name"]

        # Get releases for the project
        releases_url = f"{ORG_URL}/{project_name}/_apis/release/releases?api-version=7.1-preview.4"
        releases_response = requests.get(releases_url, headers=headers)
        releases_response.raise_for_status()
        releases = releases_response.json().get("value", [])

        for release in releases:
            release_date = datetime.strptime(release["createdOn"], "%Y-%m-%dT%H:%M:%S.%fZ").date()
            if release_date == target_date:
                release_work_items = [
                    work_item
                    for work_item in release.get("artifacts", [])
                    if work_item.get("type", "").lower() == "release"
                ]

                for work_item in release_work_items:
                    release_data.append({
                        "project": project_name,
                        "release_name": release["name"],
                        "release_time": release["createdOn"],
                        "work_item_url": work_item.get("url")
                    })

    return release_data

def send_email(release_data, target_date):
    """Send an audit email with all releases for the given date."""
    if not release_data:
        print("No releases found for the specified date.")
        return

    # Prepare email content
    table_rows = ""
    for item in release_data:
        table_rows += f"""
        <tr>
            <td>{item['project']}</td>
            <td>{item['release_name']}</td>
            <td>{item['release_time']}</td>
            <td><a href="{item['work_item_url']}">Work Item Link</a></td>
        </tr>
        """

    html_content = f"""
    <html>
        <body>
            <h3>Release Audit for {target_date}</h3>
            <table border="1">
                <thead>
                    <tr>
                        <th>Project</th>
                        <th>Release Name</th>
                        <th>Release Time</th>
                        <th>Work Item Link</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </body>
    </html>
    """

    msg = MIMEMultipart()
    msg["From"] = SMTP_USERNAME
    msg["To"] = DL_EMAIL
    msg["Subject"] = f"Release Audit for {target_date}"
    msg.attach(MIMEText(html_content, "html"))

    # Send email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, DL_EMAIL, msg.as_string())

    print("Audit email sent successfully.")

def main():
    # Get target date from pipeline input (default to today for local testing)
    target_date_str = input("Enter the target date (YYYY-MM-DD): ")
    target_date = datetime.strptime(target_date_str, "%Y-%m-%d").date()

    # Get release data
    release_data = get_releases_for_date(target_date)

    # Send email with release data
    send_email(release_data, target_date)

if __name__ == "__main__":
    main()
