---
name: Notion to docx
description: This skill can be used when users need to convert Notion pages to Microsoft Word (.docx) files. This skill preserves formatting, colors, and tables, and converts LaTeX formulas to editable OMML Word formulas.
---

# Notion to DOCX Conversion Guide

### Step 1: Obtain the Notion Page/Repository ID

- **If the user did not provide an ID (32-bit string)**: Search for the ID using the `uv` command:

```powershell
cd scripts
uv run --with-requirements requirements.txt python -B -c "from components.notion_api import search_notion_targets; targets = search_notion_targets(); print([(v['id'], v['title']) for v in targets.values()])"
```

Find the ID matching the title provided by the user from the output.

### Step 2: Perform the Transformation

Automatically process dependencies and execute the main script using the `uv` command. The script will automatically fetch the Notion page title and use it as the filename.

```powershell
uv run --with-requirements requirements.txt python -B main.py <page_id_or_database_id> -o "<output_directory>"
```

> [!Prompt]

> **Output path rules:**

> If not provided, be sure to ask the user for the exact output path (e.g., "C:\Users\<username>\Documents\output_notion_to_docx").

**Example:**

```bash
cd scripts
uv run --with-requirements requirements.txt python -B main.py 31ea7038c2628087b1dbf4611ea85018 -o "C:/Users/ken.liu/Documents/output_notion_to_docx"
```

This script will automatically perform the following operations:

1. Search for the Notion title to use as the output filename.

2. Determine whether the ID is a database or a page.

3. Retrieve Notion content and generate HTML.

4. Convert HTML to DOCX via Microsoft Word COM.

5. Inject natively editable mathematical formulas (MathML → OMML).

### Step 3: Report Output

- **Success 🎉**: Inform the user of the final file path:

`<output directory>/<clean_id>/<notion_title>.docx`

- **Failure ❌**: Report any errors (e.g., `404 Not Found` or missing API key).

## Quick Reference

| Parameters            | Required | Description                                         |
| --------------------- | -------- | --------------------------------------------------- |
| `id`                  | ✅       | Notion page/database ID (32-bit hexadecimal string) |
| `-o` / `--output-dir` | ✅       | Output directory path.                              |
