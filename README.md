# Translation Slack Command

A slash command for Slack that translates text using [Google Cloud Translation](https://cloud.google.com/translate/docs/overview) and announces it in a channel.

---

## Available Commands

- /to_french
- /to_spanish
- /to_english

## Deploying to GCP Cloud Functions

In this example, the French translation function is deployed. Change the name and entry pont to support other languages.

```
gcloud functions deploy translation_function_french \
--gen2 \
--runtime=python310 \
--region=REGION \
--source=. \
--entry-point=to_french \
--trigger-http \
--set-env-vars "SLACK_SECRET=YOUR_SLACK_SIGNING_SECRET" \
--allow-unauthenticated
```