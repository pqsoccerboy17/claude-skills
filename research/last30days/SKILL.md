---
name: last30days
description: Search Reddit and X/Twitter for any topic from the last 30 days, return structured findings with links and sentiment
---

# Social Listening Skill — Last 30 Days

Search Reddit, X/Twitter, and the web for recent discussion on any topic. Returns structured findings with links, sentiment, and confidence ratings.

## Usage

```
/last30days "AI consulting trends"
/last30days "Claude Code vs Cursor"
/last30days "real estate market Austin TX"
```

The skill accepts a single topic argument (quoted string).

## Instructions

When this skill is invoked with a topic, follow these steps exactly:

### Step 1: Search Reddit

Use `brave_web_search` (from brave-search MCP) to search:
```
site:reddit.com {topic} after:YYYY-MM-DD
```
Where the date is 30 days before today. Collect the top 5-10 results. Note the subreddit, upvote signals (if visible in snippets), and overall sentiment of each thread.

### Step 2: Search X/Twitter

Use `brave_web_search` to search:
```
(site:x.com OR site:twitter.com) {topic} after:YYYY-MM-DD
```
Collect the top 5-10 results. Note the author, engagement signals, and tone.

### Step 3: Search General Web

Use `brave_web_search` to search:
```
{topic} after:YYYY-MM-DD
```
Exclude Reddit and Twitter results mentally. Focus on news articles, blog posts, and industry publications from the last 30 days.

### Step 4: Organize Findings

Present results in the following structured format:

---

## {Topic} — Social Listening Report

**Date range:** {30 days ago} to {today}
**Sources searched:** Reddit, X/Twitter, Web

### Overview & Sentiment

A 2-3 sentence summary of the overall sentiment and volume of discussion. Rate overall sentiment as: Positive / Mixed / Negative / Neutral.

### Key Voices

List 3-5 notable accounts, authors, or community members driving the conversation. Include their platform and a one-line summary of their position.

| Who | Platform | Position | Confidence |
|-----|----------|----------|------------|
| u/example | Reddit | Bullish on topic, citing X | High |
| @example | X/Twitter | Critical of Y approach | Medium |

### Trending Themes

Bullet list of 3-5 recurring themes across all sources. For each theme, note which platforms it appears on and a confidence rating (High/Medium/Low).

### Top Reddit Threads

| Thread | Subreddit | Key Takeaway | Confidence |
|--------|-----------|--------------|------------|
| [Title](url) | r/subreddit | Summary | High/Med/Low |

List up to 5 threads, sorted by relevance.

### Top X/Twitter Posts

| Post | Author | Key Takeaway | Confidence |
|------|--------|--------------|------------|
| [Excerpt](url) | @handle | Summary | High/Med/Low |

List up to 5 posts, sorted by relevance.

### Recent Articles

| Article | Source | Key Takeaway | Confidence |
|---------|--------|--------------|------------|
| [Title](url) | Publication | Summary | High/Med/Low |

List up to 5 articles, sorted by relevance and recency.

### Conflicting Viewpoints

Flag any significant disagreements or contradictions found across sources. For each conflict:
- **Claim A:** (source, position)
- **Claim B:** (source, position)
- **Assessment:** Which has more supporting evidence

If no conflicts found, state "No significant conflicting viewpoints identified."

### Source Links

A flat list of all URLs referenced in the report for easy access.

---

## Confidence Rating Guide

- **High** — Multiple corroborating sources, direct quotes or data, recent (within 7 days)
- **Medium** — 1-2 sources, indirect evidence, or slightly older (7-21 days)
- **Low** — Single source, anecdotal, speculative, or near the 30-day boundary

## Notes

- This skill uses `brave_web_search` from the brave-search MCP server (configured globally)
- Search quality depends on Brave Search index coverage — some recent posts may not be indexed yet
- X/Twitter results may be limited due to platform indexing restrictions
- Always include the date range so the user knows exactly what window was searched
