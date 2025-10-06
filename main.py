"""Main entry point for action-items CLI."""

from datetime import datetime

import click

from src.email import fetch_emails
from src.utils import get_last_run, reset_last_run, save_last_run


@click.group()
def cli():
    """Action Items - Email management automation tool."""
    pass


@cli.command()
@click.option(
    "--days",
    type=int,
    help="Fetch emails from last N days (overrides incremental mode)",
)
@click.option(
    "--since",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="Fetch emails since specific date (YYYY-MM-DD)",
)
@click.option(
    "--unread-only/--all",
    default=True,
    help="Fetch only unread emails (default: unread only)",
)
@click.option(
    "--max",
    "max_results",
    type=int,
    default=100,
    help="Maximum number of emails to fetch (default: 100)",
)
@click.option(
    "--interactive/--no-interactive",
    default=True,
    help="Use interactive mode for missing options",
)
def fetch(days, since, unread_only, max_results, interactive):
    """Fetch emails from Gmail.

    By default, uses incremental mode (fetches since last run).
    Use --days or --since to override.
    """
    print("=" * 70)
    print("📬 Action Items - Email Fetcher")
    print("=" * 70)

    try:
        # Track if we should save state (for incremental mode)
        save_state = False

        # Interactive mode if no arguments provided
        if interactive and not days and not since:
            print("\n🔧 Interactive Mode")
            print("-" * 70)

            last_run = get_last_run()
            if last_run:
                print(f"\n⏱️  Last run: {last_run.strftime('%Y-%m-%d %H:%M:%S')}")
                choice = click.prompt(
                    "\nHow would you like to fetch emails?"
                    + "\n1) Since last run (incremental)"
                    + "\n2) From last N days"
                    + "\n3) Since specific date"
                    + "\nEnter choice",
                    type=click.Choice(["1", "2", "3"], case_sensitive=False),
                    default="1",
                    show_choices=True,
                    show_default=True,
                )

                if choice == "1":
                    print("\n📅 Fetching emails since last run...")
                    since = last_run
                    save_state = True
                elif choice == "2":
                    days = click.prompt("How many days back?", type=int, default=7)
                else:
                    date_str = click.prompt(
                        "Enter start date (YYYY-MM-DD)",
                        type=str,
                    )
                    since = datetime.strptime(date_str, "%Y-%m-%d")
            else:
                print("\n🆕 First run detected!")
                days = click.prompt(
                    "How many days of emails to fetch?",
                    type=int,
                    default=7,
                )
                save_state = True  # Save state on first run

            unread_filter = click.confirm(
                "\nFetch unread emails only?",
                default=True,
            )
            unread_only = unread_filter
        else:
            # Non-interactive mode with no date args = incremental
            if not days and not since:
                save_state = True

        # Determine fetch strategy
        current_run = datetime.now()

        if days:
            print(f"\n📅 Fetching emails from last {days} days...\n")
            emails = fetch_emails(
                days=days, unread_only=unread_only, max_results=max_results
            )
        elif since:
            print(f"\n📅 Fetching emails since {since.strftime('%Y-%m-%d')}...\n")
            emails = fetch_emails(
                after=since, unread_only=unread_only, max_results=max_results
            )
        else:
            # Incremental mode
            last_run = get_last_run()
            if last_run:
                print(f"\n⏱️  Last run: {last_run.strftime('%Y-%m-%d %H:%M:%S')}")
                print("📅 Fetching emails since last run...\n")
                emails = fetch_emails(
                    after=last_run, unread_only=unread_only, max_results=max_results
                )
            else:
                print("\n🆕 First run - fetching last 7 days...\n")
                emails = fetch_emails(
                    days=7, unread_only=unread_only, max_results=max_results
                )

        # Display results
        if not emails:
            print("✓ No emails found!")
        else:
            print(f"\n✓ Found {len(emails)} email(s)")
            print("-" * 70)

            for i, email in enumerate(emails, 1):
                print(f"\n[{i}] {email.subject}")
                print(f"    From: {email.sender} <{email.sender_email}>")
                print(f"    Date: {email.date.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"    Preview: {email.snippet[:100]}...")

            print("\n" + "-" * 70)

        # Save timestamp if in incremental mode
        if save_state:
            print()
            save_last_run(current_run)

    except FileNotFoundError as e:
        click.echo(f"\n✗ Error: {e}", err=True)
        click.echo(
            "\nPlease ensure your OAuth2 credentials file is in the project root.",
            err=True,
        )
        click.echo("See SETUP.md for instructions.", err=True)
    except Exception as e:
        click.echo(f"\n✗ Failed to fetch emails: {e}", err=True)
        import traceback

        traceback.print_exc()


@cli.command()
def reset():
    """Reset the last run timestamp.

    This will cause the next fetch to get emails from the last 7 days
    instead of incremental fetch.
    """
    if click.confirm("Are you sure you want to reset the last run timestamp?"):
        reset_last_run()
        click.echo("\n✓ Last run timestamp has been reset")
        click.echo("Next fetch will retrieve emails from the last 7 days")
    else:
        click.echo("Reset cancelled")


@cli.command()
def status():
    """Show current status and last run information."""
    print("=" * 70)
    print("📊 Status")
    print("=" * 70)

    last_run = get_last_run()

    if last_run:
        print(f"\n⏱️  Last run: {last_run.strftime('%Y-%m-%d %H:%M:%S')}")

        # Calculate time since last run
        time_diff = datetime.now() - last_run
        hours = int(time_diff.total_seconds() // 3600)
        minutes = int((time_diff.total_seconds() % 3600) // 60)

        print(f"📅 Time since last run: {hours}h {minutes}m ago")
    else:
        print("\n🆕 Never run before")
        print("📅 Next fetch will retrieve emails from the last 7 days")


if __name__ == "__main__":
    cli()
