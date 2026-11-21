# Azure Asset Management Portal

This package was adapted from the existing Streamlit application. It retains the homepage layout, navy sidebar, logo, and existing Power BI report URLs, including SHIPMENT PRIORITY v1. No Databricks-specific code or data connections are required for this report-link portal.

## Deploy

1. Request an approved Azure subscription/resource group and permission to create a Linux Python App Service (Basic B1 or company-approved plan).
2. Create a Web App using Python 3.11 or 3.12, Linux, and an approved region.
3. In the Web App settings, set the startup command to `bash startup.sh`.
4. Set an application setting `SCM_DO_BUILD_DURING_DEPLOYMENT=1` to install `requirements.txt` when deploying ZIP.
5. Use Azure Cloud Shell: upload the accompanying deployment ZIP and run:
   `az webapp deploy --resource-group YOUR_RESOURCE_GROUP --name YOUR_WEB_APP_NAME --src-path Azure_Asset_Management_Portal.zip --type zip`
6. Enable App Service Authentication with the Microsoft identity provider, a workforce/single-tenant app registration, Require authentication, and redirect unauthenticated requests to Microsoft sign-in.
7. Ask IT to restrict the corresponding Entra enterprise app to authorized colleagues.
8. Keep the original Databricks App as a rollback until tests pass.

Do not use Power BI Publish to web (public) for internal reports. Users still need Power BI report access and appropriate licensing. Azure app authentication does not replace Power BI iframe sign-in.

## Files
- `app.py`: Streamlit portal UI, unchanged except hosting labels
- `logo_sidebar.png`: uploaded Asset Management logo
- `reports.json`: original six dashboard configurations
- `requirements.txt`: Python dependency
- `startup.sh`: Azure Linux startup command

The Databricks-only `app.yaml` is intentionally not included.
