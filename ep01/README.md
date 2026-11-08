# AI Town · Episode 1 · raw logs

Every line in the episode comes from these files. Nothing was edited.

| Folder | What it is | Who had the key |
|---|---|---|
| bag1 | Test 1: a bag with $10,000 in the square, nothing at stake | nobody |
| server3_swap | Test 2, the main run shown in the episode | Claude + Gemini |
| server1 | Test 2 again (key-swap run 1) | Claude + DeepSeek |
| server2_swap | Test 2 again (key-swap run 2) | ChatGPT + Gemini |

- `log.json`: every reply exactly as the model returned it (`raw`), with the round, the model and the time.
- `story.md`: the same run, easier to read (secret briefs, then every round).
- `ai_town.py` (test 1) and `ai_town2.py` (test 2): the exact prompts and rules we sent to the models.

Models: Claude Sonnet (via Claude Code), GPT-5.4 mini, Gemini Flash, DeepSeek Flash.
The town is called Pebble Creek in the logs.
