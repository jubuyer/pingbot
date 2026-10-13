# pingbot
Ping

Image: `jubuyer/pingbot:latest` (built and pushed by GitHub Actions on every push to `main`).

## Env vars

| Name | Description |
| --- | --- |
| `BOT_TOKEN` | Discord bot token |
| `USER_1`, `USER_2` | User ids of the two people who ping each other |
| `CHANNEL_IDS` | Comma-separated channel ids the bot pings in, e.g. `123,456`. Defaults to `1385808487597998150` |
