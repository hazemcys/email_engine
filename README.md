# Supercharged Email Engine (v2.0)

Hey! Welcome to my custom-built Email Engine. 

I designed this system to chew through massive **MBOX** email files insanely fast. It extracts Kuwaiti phone numbers, spots sensitive legal keywords, parses structured reports, and even hooks into **Gemini 2.0 AI** to classify emails automatically. No more manual sorting — the code does all the heavy lifting!

---

## How Things Are Organized
Every time you run the engine, it neatly organizes all the results into three awesome subfolders:

```text
output/
├── Excel_Reports/          # Beautifully styled spreadsheets!
│   ├── all_emails.xlsx         ← The master file (everything we parsed + AI stuff)
│   ├── most_occurred.xlsx      ← Stage 1: The spammy frequent numbers
│   ├── legal_keywords.xlsx     ← Stage 2: Caught emails with legal/sensitive words
│   ├── report_entries.xlsx     ← Stage 3: Found structured reports (Name : Phone)
│   ├── detected_phones.xlsx    ← Stage 4: Everything else that has a phone number
│   └── unprocessed.xlsx        ← Stage 5: No phone numbers, Needs human eyes!
│
├── SQL_Scripts/            # Database queries ready to fire
│   ├── most_occurred_block.sql     ← INSERT IGNORE: block those frequent spammers
│   ├── report_entries_delete.sql   ← DELETE: clean up the fullNames table
│   └── detected_phones_block.sql   ← INSERT IGNORE: block the leftover numbers
│
└── Summary_Logs/           # Quick stats and sender lists
    ├── summary.txt                 ← Quick rundown of the run
    ├── most_occurred_senders.txt
    ├── legal_keywords_senders.txt
    ├── report_entries_senders.txt
    └── detected_phones_senders.txt
```

---

## What's under the hood?

I picked the best tools for the job to keep things ridiculously efficient:

| Piece of the Puzzle | Tech I Used                         |
|---------------------|-------------------------------------|
| Core Logic          | Python 3.10                         |
| Environment         | Docker (Runs anywhere, amd64/arm64) |
| AI Brain            | Gemini 2.0 Flash (`google-genai`)   |
| Spreadsheets        | openpyxl (Because ugly excels suck) |
| Data Crunching      | Pandas + Custom Regex Magic         |

---

## Let's Run It!

### 1. Build the Docker Image
```bash
docker build -t email-engine-app .
```

### 2. Run Normally (Fast)
```bash
docker run -v $(pwd):/app email-engine-app python engine.py mbox
```

### 3. Run with AI Magic
```bash
docker run -v $(pwd):/app email-engine-app python engine.py mbox --classify
```

### 4. Tweak the Settings
```bash
python engine.py <input.mbox> \
  --output-dir ./results \
  --spam-threshold 5 \
  --classify
```

| Flag                | Default      | What it does                                  |
|---------------------|--------------|-----------------------------------------------|
| `input`             | *(required)* | Path to your `.mbox` file                     |
| `--output-dir`      | `./output`   | Where I should save all the cool files        |
| `--spam-threshold`  | `5`          | Stage 1 trigger for frequent phone numbers    |
| `--classify`        | off          | Turn on the Gemini AI brain                   |

---

## How the Pipeline Works

I built a strict 5-stage filtering pipeline to make sure no data slips through the cracks:

```text
MBOX File
    │
    ▼
Parse Emails  →  Translate Arabic Numbers  →  Hunt for Phones!
    │
    ├── Stage 1: Frequent Numbers (Are they spamming us?)
    │             → most_occurred.xlsx  |  most_occurred_block.sql
    │
    ├── Stage 2: Legal Check (Looking for courts, police, officials)
    │             → legal_keywords.xlsx
    │
    ├── Stage 3: Report Pattern ("Report [Name] : [Phone]")
    │             → report_entries.xlsx  |  report_entries_delete.sql
    │
    ├── Stage 4: Catch-all for remaining emails with phones
    │             → detected_phones.xlsx  |  detected_phones_block.sql
    │
    └── Stage 5: No phones detected? Save for a human to review
                  → unprocessed.xlsx
```

---

## AI Classification (Optional but Awesome)

If you use `--classify`, the AI goes through every email and tags it as one of these:

| Tag               | Meaning                            |
|-------------------|------------------------------------|
| `real_user`       | An actual human message            |
| `ad`              | Marketing and promos               |
| `undelivered`     | Bounced email / server error       |
| `invoice`         | Money stuff (payments, bills)      |
| `subscription`    | Just a newsletter                  |
| `company_support` | Replies from support desks         |
| `spam`            | Junk. Trash it.                    |
| `system`          | Automated system ping              |

*Note: Make sure to set your `GEMINI_API_KEY` environment variable first!*

---

## Why this is an Impressive Achievement
- Built a custom **MBOX parser** that handles massive 50K+ email files effortlessly.
- **Smart Arabic numeral translation** baked right into the regex logic.
- Built a cascading **5-stage data pipeline** exactly to spec.
- Super clean code with zero messy dependencies.
- **AI integration** that actually works in production!
