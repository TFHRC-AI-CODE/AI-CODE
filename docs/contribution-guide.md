---

### `docs/contribution-guide.md`

```markdown
# How to Submit a Case Study to CODE

We encourage transportation agencies, state DOTs, academic researchers, and industry developers to share their practical AI applications, code, and datasets[cite: 1].

---

## Submission Process

### Step 1: Fork the Repository
Fork the main **CODE** repository to your GitHub account.

### Step 2: Create Your Case Study Page
1. Navigate to `docs/templates/case-study-template.md`.
2. Copy the template file into the appropriate domain directory under `docs/case-studies/`:
   * `docs/case-studies/infrastructure/`[cite: 1]
   * `docs/case-studies/safety/`[cite: 1]
   * `docs/case-studies/traffic/`[cite: 1]
   * `docs/case-studies/asset-management/`[cite: 1]
3. Rename the file using lower-case hyphenated words (e.g., `pavement-cracking-detection.md`).

### Step 3: Fill Out the Details
Populate all required sections including dataset links, model parameters, setup commands, and lessons learned[cite: 1].

### Step 4: Register in `mkdocs.yml`
Open `mkdocs.yml` in the root directory and add your new page under the `Case Study Catalog` section:

```yaml
nav:
  - Case Studies:
      - Infrastructure & NDE:
          - Your Case Study Title: case-studies/infrastructure/your-file-name.md
