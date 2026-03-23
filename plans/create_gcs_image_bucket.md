# Plan: Create GCS Image Bucket

This plan outlines the steps to add a Google Cloud Storage (GCS) bucket named
`biocirv_bucket` to the BioCirV infrastructure using Pulumi.

## 1. Configuration & APIs

### 1.1 Update `apis.py`

- Add `storage.googleapis.com` to the `REQUIRED_APIS` list in
  [`deployment/cloud/gcp/infrastructure/apis.py`](deployment/cloud/gcp/infrastructure/apis.py).

### 1.2 Update `config.py`

- Add `IMAGE_BUCKET_NAME = "biocirv_bucket"` to
  [`deployment/cloud/gcp/infrastructure/config.py`](deployment/cloud/gcp/infrastructure/config.py).

## 2. Infrastructure Definition

### 2.1 Create `storage.py`

- Create a new file `deployment/cloud/gcp/infrastructure/storage.py`.
- Define a `StorageResources` dataclass.
- Implement `create_storage_resources(depends_on)` which:
  - Creates a `gcp.storage.Bucket` resource.
  - Configures it with `uniform_bucket_level_access=True`.
  - Sets the location based on `GCP_REGION`.
  - **Public Access**: Grants `roles/storage.objectViewer` to `allUsers`. This
    allows the data portal to host images via direct public URLs (e.g.,
    `https://storage.googleapis.com/biocirv_bucket/image.jpg`).

### 2.2 Update `iam.py`

- Update `SA_DEFINITIONS` in
  [`deployment/cloud/gcp/infrastructure/iam.py`](deployment/cloud/gcp/infrastructure/iam.py)
  to grant storage access to relevant service accounts:
  - `webservice`: `roles/storage.objectAdmin` (to manage/delete images).
  - `prefect-worker`: `roles/storage.objectAdmin` (to upload images during ETL).

### 2.3 Access & Security

#### Public Access (allUsers)

- The bucket will allow anyone with the URL to view objects.
- **Risk**: Do not upload sensitive data (PII, private spreadsheets) to this
  specific bucket.
- **Benefit**: Simplest integration for the data portal frontend.

#### Contractor & Local Access

- **Contractors**: Grant their Google IDs `roles/storage.objectAdmin`
  **specifically on this bucket** via the GCP Console. This follows the
  principle of least privilege.
- **Local Developer**: Use `gcloud auth application-default login`. Project
  owners/editors have access by default.

### 2.4 Update `deploy.py`

- Import `create_storage_resources` in
  [`deployment/cloud/gcp/infrastructure/deploy.py`](deployment/cloud/gcp/infrastructure/deploy.py).
- Call it within `pulumi_program()` and ensure it depends on the storage API.
- Export the bucket name using
  `pulumi.export("image_bucket_name", storage.bucket.name)`.

## 3. Verification (No Deployment)

- Run `pixi run -e deployment cloud-plan` to verify the Pulumi plan.
- **DO NOT** run `cloud-deploy`.
