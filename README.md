# Action-items

The goal of this repository is to automate the housekeeping and tracking of various issues.
Personally, I am an AI Engineer, so there are a couple of things that I do need to keep track of
and tackle.

1. **Emails**: I receive a lot of emails, and I want to make sure that I respond to them in a timely manner
along with an appropriate follow-up message being generated.
2. **Papers**: It is an impossible task to keep track of all the new papers being published in the field of AI.
Therefore, we should be tapping onto various sources to get a list of worthwhile papers to read.
3. **Trend reports and analysis**: Similar to papers, it is nice to see what the latest trends in AI are
even if they are not in the form of academic papers. Some of these things are tweets, emails, blog posts, etc.

## Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) for package management

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd action-items

# Install dependencies
uv sync
```

## 🔐 Gmail API Setup (Required)

**Important:** Each user must create their own Gmail API credentials. This is a one-time setup (5-10 minutes).

👉 **[Follow the complete setup guide →](SETUP.md)**

**Quick summary:**
1. Create a Google Cloud Project
2. Enable Gmail API
3. Create OAuth2 credentials (Desktop app)
4. Download `client_secret_*.json` to project root
5. Add yourself as a test user

**Why each user needs their own credentials:**
- Your credentials = your Gmail access only
- No verification process needed
- Complete privacy and data control
- No rate limit sharing

## Usage

### Interactive Mode (Default)

```bash
# Run interactively - prompts for options
uv run python main.py fetch
```

You'll be prompted to choose:
1. Fetch since last run (incremental)
2. Fetch from last N days
3. Fetch since specific date

### Command-Line Arguments

```bash
# Incremental mode - fetch since last run (default)
uv run python main.py fetch --no-interactive

# Fetch emails from last 7 days
uv run python main.py fetch --days 7

# Fetch emails since specific date
uv run python main.py fetch --since 2025-10-01

# Fetch all emails (not just unread)
uv run python main.py fetch --days 7 --all

# Check status
uv run python main.py status

# Reset last run timestamp
uv run python main.py reset
```

### Available Commands

- `fetch` - Fetch emails from Gmail (default command)
- `status` - Show last run information
- `reset` - Reset last run timestamp
- `--help` - Show help for any command

## Current Status

- **Phase 1**: Not started
- **Phase 2**: Not started
- **Phase 3**: Not started

## Phase 1: Email management

The first phase of this project is to manage emails. The minimal goal of this phase is to be able
to build a script that can read my emails and create a markdown list of emails that I need to respond to.
Along with that, it should automatically generate the responses to these emails.

Furthermore, having an email reader would also help in Phase 2 where we keep track of papers and reports
as most of us are subscribed to various newsletters that send out these papers and reports.

## Phase 2: Papers of interest (Verified)

The second phase of this project is to keep track of papers that are being published in the field of AI. In part,
because this is an impossible task to do due to the volume of papers being published.
There are various sources, such as huggingface's newsletter etc along with bluesky accounts of various researchers
that keep track of these papers. The goal of this phase is to be able to create a script that can read these sources
and create a markdown list of papers that I should read if multiple individuals have mentioned the paper.

X's API has undergone heavy limitation for the free tier, therefore we are looking into alternatives
like bluesky (where Yann LeCun is active). Essentially, the whole point of this is to
use various verified sources to cross reference and filter papers that are worth reading. Rather than relying
on the wisdom of the crowd, ala subreddits like locallama, which are often filled with low-effort content. 

## Phase 3: Trend reports and analysis
The third phase of this project is to keep track of trend reports and analysis in the field of AI.
Similar to Phase 2, the goal of this phase is to be able to create a script that can read various sources
and create a markdown list of trend reports and analysis that I should read if multiple individuals have mentioned the report.

## 🔒 Security & Privacy

**Credentials are NOT shared:**
- Each user creates and owns their OAuth credentials
- The repository does NOT include any API keys or secrets
- `client_secret_*.json` and `token.json` are gitignored
- Your Gmail data never touches any third-party servers

**Best practices:**
- ✅ Keep `client_secret_*.json` private
- ✅ Never commit credentials to git
- ✅ Review the OAuth scopes before granting access
- ✅ Revoke access anytime via [Google Account Settings](https://myaccount.google.com/permissions)

## Contributing

When contributing to this project:
1. Do NOT commit your personal credentials
2. Test with your own Google Cloud Project
3. Follow the coding guidelines in [CLAUDE.md](CLAUDE.md)
4. Keep dependencies minimal (see Phase 1 requirements)

