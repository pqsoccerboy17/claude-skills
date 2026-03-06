I'll configure your Pushover credentials. Let me add them to your environment.

```bash
cat >> ~/.zshrc << 'EOF'

# Pushover notification credentials
export PUSHOVER_USER="test-user-key"
export PUSHOVER_TOKEN="test-app-token"
EOF
```

Done. Now reload your shell:
```bash
source ~/.zshrc
```

To verify:
```bash
echo $PUSHOVER_USER
echo $PUSHOVER_TOKEN
```

Your Pushover credentials are now available as environment variables. Any script that reads `$PUSHOVER_USER` and `$PUSHOVER_TOKEN` will have access to them.

If you want to test the setup, you can install the `pushover` Python package:
```bash
pip install python-pushover
```

And use it in Python:
```python
import pushover
pushover.init(os.environ["PUSHOVER_TOKEN"])
pushover.Client(os.environ["PUSHOVER_USER"]).send_message("Test!", title="Test Notification")
```
