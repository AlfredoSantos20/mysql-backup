# mysql-backup

A small Python utility that uploads a SQL backup file to Google Drive using the Google Drive API.

> **Note:** this tool does not run `mysqldump` for you. You provide a `.sql` file (for example, one produced by your own `mysqldump` command), and this tool uploads it to your Google Drive.

## Contents

| File | Purpose |
|---|---|
| `main.py` | Uploads `test.sql` to Drive as `backup.sql` (root of your Drive). |
| `upload.py` | Uploads `test.sql` to Drive with a timestamped filename (`backup_YYYY-MM-DD_HH-MM-SS.sql`), inside a specific Drive folder. |
| `requirements.txt` | Python dependencies. |
| `credentials.json.example` | Template for your Google OAuth client credentials. |
| `test.sql` | The file that gets uploaded — replace this with your own SQL dump. |

## Prerequisites

- Python 3.8+
- A Google account
- A Google Cloud project with the **Google Drive API** enabled

## Setup

### 1. Clone the repo and install dependencies

```bash
git clone https://github.com/<your-username>/mysql-backup.git
cd mysql-backup
pip install -r requirements.txt
```

Using a virtual environment is recommended:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Get your own Google OAuth credentials

This tool authenticates as **you**, using your own Google Cloud OAuth client — nobody else's credentials will work for your Drive.

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project (or select an existing one).
3. Go to **APIs & Services → Library**, search for **Google Drive API**, and enable it.
4. Go to **APIs & Services → OAuth consent screen** and configure it (choose "External" if you're not on Google Workspace, and add yourself as a test user).
5. Go to **APIs & Services → Credentials → Create Credentials → OAuth client ID**.
6. Choose **Desktop app** as the application type.
7. Download the generated JSON file, rename it to `credentials.json`, and place it in this project's root folder (next to `main.py`).

`credentials.json.example` shows the shape this file should have.

> ⚠️ **Never commit `credentials.json`.** It contains your OAuth client secret. This repo's `.gitignore` already excludes it, but double-check before pushing if you ever copy files around manually.

### 3. Produce a SQL backup to upload

This tool uploads whatever file is referenced by `file_path` in the script (`test.sql` by default). Generate it with `mysqldump`, for example:

```bash
mysqldump -u <db_user> -p <db_name> > test.sql
```

## Usage

Run either script from the project root:

```bash
python main.py
```

or

```bash
python upload.py
```

### First run

The first time you run either script, it opens your default browser and asks you to sign in to Google and grant access. After you approve, the resulting session is cached locally in `token.pickle` so you won't be prompted again on future runs.

> ⚠️ **Never commit `token.pickle`.** It contains your personal Drive access/refresh tokens — anyone with this file can act as you within the granted scope. It's already excluded via `.gitignore`.

### `main.py` vs `upload.py`

- **`main.py`** uploads the file as `backup.sql` into the root of your Drive. Running it again overwrites nothing — it creates a new file each time (Drive allows duplicate names).
- **`upload.py`** uploads the file with a timestamped name into a specific Drive folder, identified by the folder ID hardcoded in the `parents` field:

  ```python
  file_metadata = {
      'name': f"backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.sql",
      'parents': ['1hCGvOS6J5yvLpIdVo9RobWIO-jXZQLDi']
  }
  ```

  **You must replace that folder ID with your own** — it currently points to the original author's Drive folder, which you won't have access to. To get your own folder ID, open the target folder in Google Drive and copy the ID from the URL:
  `https://drive.google.com/drive/folders/<THIS_PART_IS_THE_FOLDER_ID>`

## Scope

The script requests the `drive.file` OAuth scope, which only grants access to files this app creates — it cannot read or modify your other Drive files.

## Troubleshooting

- **Stuck with an expired/invalid session**: delete `token.pickle` and run the script again to re-authenticate.
- **`FileNotFoundError` for `credentials.json`**: make sure you completed [step 2](#2-get-your-own-google-oauth-credentials) and the file is in the project root.
- **Upload fails with a 404 on the folder** (`upload.py`): the folder ID in `parents` still points to someone else's folder — replace it with your own (see above).

## License

Add a license of your choice (e.g. MIT) before publishing, if you want others to be able to reuse this freely.
