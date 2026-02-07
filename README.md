# Theater Checker

A console application to monitor Teatr im. Wandy Siemaszkowej (https://teatr-rzeszow.pl/) for new plays and tickets.

## Setup

1. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Configure environment variables (optional but recommended for notifications):
   ```bash
   export RECIPIENT_EMAIL="TBD_1@gmail.com;TBD_2@gmail.com" # Multiple emails supported with ;
   export SENDER_EMAIL="TBD@gmail.com"
   export SENDER_PASSWORD="TBD"
   # To test without sending actual emails:
   export MOCK_EMAIL="true"
   # If you encounter SSL certificate errors (common on macOS):
   export VERIFY_SSL="false"
   ```
3. Run the application:
    ```bash
    export PYTHONPATH=$PYTHONPATH:$(pwd)/src
    python3 src/main.py
   ```

4. Run tests:
   ```bash
   export PYTHONPATH=$PYTHONPATH:$(pwd)/src
   pytest
   ```

## Scheduling (Cron)

To run this script every day at 9 AM, add the following to your `crontab -e`:

```bash
0 9 * * * cd /path/to/theater-checker && export PYTHONPATH=$PYTHONPATH:$(pwd)/src && .venv/bin/python3 src/main.py >> log.txt 2>&1
```

Note: Ensure you set the necessary environment variables in your shell or within the crontab.