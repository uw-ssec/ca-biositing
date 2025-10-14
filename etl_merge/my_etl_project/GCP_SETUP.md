# Google Cloud Platform (GCP) Setup for Gspread

This guide explains how to set up a Google Cloud Platform project, create a service account, and generate the `credentials.json` file required to access the Google Sheets which contain the data which will be manipulated by the ETL pipeline.

---

### Overview

To allow our application to read data from a Google Sheet programmatically, we need to:
1.  Select or create a **Google Cloud Platform (GCP) project** which will house the operations of your service account.
2.  Create a **Service Account** in your GCP project. A service account is a special type of non-human user account used to access data programmatically.
3.  Enable the necessary APIs (Google Sheets and Google Drive) for your service account.
4.  Generate a JSON key (credentials.json) that the ETL pipeline application can use to authenticate as the service account.
5.  Share the target Google Sheet with the service account's email address.

---

### Step-by-Step Guide

**Step 1: Create or Select a GCP Project**

1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  If you don't have a project that can host a service agent, create one. If you do, select the project you want to use from the project dropdown at the top of the page.
    **NOTE FOR ORGANIZATION USERS** If you have an organization account (e.g. @LBL.gov) you may need to make a project within your organization's GCP folders structure. For LBL organization accounts, ask for editing permisions of the existing "BioCirV" project by selecting this project and then hitting "Request permissions" wherever you see notification of restricted permissions. If you do not request and recieve access, you will not be able to complete Step 2 or 3 of this guide.

**Step 2: Enable the Required APIs**

You need to enable the Google Sheets API and the Google Drive API for your project.

1.  Navigate to the [API Library](https://console.cloud.google.com/apis/library).
2.  Search for "Google Sheets API" and click **Enable**.
3.  Search for "Google Drive API" and click **Enable**.

**Step 3: Create a Service Account**

1.  Navigate to the [Service Accounts page](https://console.cloud.google.com/iam-admin/serviceaccounts) in the IAM & Admin section.
2.  Click **+ CREATE SERVICE ACCOUNT**.
3.  Give the service account a name (e.g., `g-sheets-etl-runner`) and a description. The Service account ID will be generated automatically. Click **CREATE AND CONTINUE**.
4.  **Grant access (Optional but recommended):** In the "Grant this service account access to project" step, grant the "Viewer" role. This is not strictly necessary for Gsheets access but is a good practice. Click **CONTINUE**.
5.  **Grant user access (Optional):** You can skip this step. Click **DONE**.

**Step 4: Generate a JSON Key**

1.  You should now be back on the Service Accounts page. Find the service account you just created and click on its email address in the "Email" column.
2.  Go to the **KEYS** tab.
3.  Click **ADD KEY** -> **Create new key**.
4.  Select **JSON** as the key type and click **CREATE**.
5.  A JSON file will be automatically downloaded to your computer. **This is your `credentials.json` file.**

**Step 5: Place the Credentials File**

1.  Rename the downloaded file to `credentials.json`.
2.  Move this file into the `my_etl_project/` directory. This file is listed in `.gitignore`, so it will not be committed to your repository.

**Step 6: Share the Google Sheet**

This is the final and most important step.

1.  Open the Google Sheet that you want the application to read.
2.  Find the service account's email address. You can either copy it from the "Email" column on the [Service Accounts page](https://console.cloud.google.com/iam-admin/serviceaccounts) or find it inside your `credentials.json` file under the `"client_email"` key.
3.  In your Google Sheet, click the **Share** button in the top right corner.
4.  Paste the service account's email address into the "Add people and groups" field.
5.  Ensure the service account has at least **Viewer** permissions.
6.  Click **Send**.

Your setup is now complete. The application will be able to use the `credentials.json` file to authenticate as the service account and read the data from the shared Google Sheet.
