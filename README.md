# ai-commiter

A pre-commit hook that automatically generates semantic commit messages using AI.

## Quick Start

### 1. Set up your API credentials

Set your AI Committer credentials as environment variables:

```bash
export AI_COMMITER_API_KEY="your-openrouter-api-key"
export AI_COMMITER_BASE_URL="https://openrouter.ai/api/v1"
```

### 2. Configure pre-commit

Add the hook to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/techbend/ai-commiter
    rev: v1.0.0  # Use the latest release
    hooks:
      - id: ai-message
```

### 3. Install and start using

```bash
pre-commit install --hook-type commit-msg
git add .
git commit  # Your commit message will be generated automatically!
```

## Optional Configuration

You can customize the behavior with additional environment variables:

```bash
# Optional: Use a different AI model
export AI_COMMITER_MODEL="gpt-4"

# Optional: Customize prompts (advanced users)
export AI_COMMITER_SYSTEM_PROMPT="Your custom system prompt..."
export AI_COMMITER_USER_PROMPT="Your custom user prompt..."
```

## Configuration Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `AI_COMMITER_API_KEY` | ✅ | - | Your OpenRouter API key |
| `AI_COMMITER_BASE_URL` | ✅ | - | API endpoint URL |
| `AI_COMMITER_MODEL` | ❌ | `deepseek/deepseek-chat:free` | AI model to use |
| `AI_COMMITER_SYSTEM_PROMPT` | ❌ | Built-in default | Custom system prompt |
| `AI_COMMITER_USER_PROMPT` | ❌ | Built-in default | Custom user prompt |

## Security Note

**Never commit API keys to your repository!** Set environment variables in your shell profile or use a `.env` file (and add `.env` to your `.gitignore`).