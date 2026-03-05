# Pushover Notification Credentials

Setting up your Pushover keys for notifications.

## Configuration

Add the credentials to your environment:

```bash
# Add to your shell config
echo 'export PUSHOVER_USER="test-user-key"' >> ~/.zshrc
echo 'export PUSHOVER_TOKEN="test-app-token"' >> ~/.zshrc
```

Then reload:
```bash
source ~/.zshrc
```

## Alternative: .env file

If you're using this with a specific project:

```bash
# Create .env in project directory
cat > .env << EOF
PUSHOVER_USER=test-user-key
PUSHOVER_TOKEN=test-app-token
EOF
```

## Verify

```bash
echo $PUSHOVER_USER
echo $PUSHOVER_TOKEN
```

## Test It

```bash
curl -s \
  -F "token=$PUSHOVER_TOKEN" \
  -F "user=$PUSHOVER_USER" \
  -F "message=Hello from setup" \
  https://api.pushover.net/1/messages.json
```

You should get a success response from the Pushover API.
