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

## Usage

```bash
# Run the main script
python main.py
```

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


