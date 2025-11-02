# BB10 News System

The BB10 Task Manager now includes a built-in news system that allows you to keep users informed about updates, new apps, and important announcements.

## Features

- **News Page**: Accessible via `/news` endpoint
- **Markdown Support**: Rich text formatting in news posts
- **Categories**: Organize posts by type (update, new-app, android, guide)
- **Priority Levels**: Mark posts as high, medium, or low priority
- **Easy Management**: Simple script to add, edit, and delete posts

## How to Use

### 1. Accessing News
Users can access the news page by:
- Clicking "News" in the hamburger menu on any page
- Going directly to `http://your-device:8001/news`

### 2. Managing News Posts

#### Using the News Manager Script
```bash
python3 news_manager.py
```

This will show a menu with options:
- **Add new news post** - Create a new announcement
- **List all news posts** - View existing posts
- **Edit news post** - Modify existing posts
- **Delete news post** - Remove posts
- **Exit** - Close the manager

#### Manual JSON Editing
You can also edit `news.json` directly:

```json
{
  "news": [
    {
      "id": 1,
      "title": "Your News Title",
      "date": "2024-07-09",
      "author": "Sw7ft",
      "content": "Your news content with **markdown** support",
      "category": "update",
      "priority": "high"
    }
  ],
  "last_updated": "2024-07-09T15:30:00Z"
}
```

### 3. News Post Fields

| Field | Description | Required |
|-------|-------------|----------|
| `id` | Unique identifier | Auto-generated |
| `title` | News post title | Yes |
| `date` | Publication date (YYYY-MM-DD) | Auto-generated |
| `author` | Author name | Yes |
| `content` | News content (markdown supported) | Yes |
| `category` | Post category | Yes |
| `priority` | Priority level | Yes |

### 4. Categories

- **update** - System updates and improvements
- **new-app** - New applications available
- **android** - Android APK updates
- **guide** - How-to guides and tutorials

### 5. Priority Levels

- **high** - Important announcements (shown prominently)
- **medium** - Regular updates
- **low** - Minor updates and tips

## Markdown Support

News posts support basic markdown formatting:

```markdown
# Main Title
## Subtitle

**Bold text** and *italic text*

- Bullet points
- Multiple items

1. Numbered lists
2. Second item

[Link text](https://example.com)
```

## File Structure

```
taskapp/
├── taskapp.py          # Main application (includes news system)
├── news.json           # News data file
├── news_manager.py     # News management script
├── taskmgr.html        # Main interface (includes news link)
└── other files...
```

## Adding News Posts

### Quick Example
```bash
python3 news_manager.py
# Select option 1: Add new news post
# Title: New App Available
# Content: We've added a new file manager app!
# Author: Sw7ft
# Category: new-app
# Priority: medium
```

### Content Tips
- Keep titles clear and descriptive
- Use markdown for formatting
- Include relevant details
- Keep content concise but informative
- Use appropriate categories and priorities

## Technical Details

- News is stored in `news.json` in the same directory as `taskapp.py`
- Posts are displayed newest first
- The system automatically updates the `last_updated` timestamp
- News page uses the same BB10 theme as other pages
- All news content is converted from markdown to HTML for display

## Troubleshooting

### News page shows "No news available"
- Check that `news.json` exists in the same directory as `taskapp.py`
- Verify the JSON format is valid
- Ensure the file has proper read permissions

### News manager script errors
- Make sure you're running it from the same directory as `news.json`
- Check that Python 3 is available
- Verify file permissions

### News not appearing
- Restart the taskapp after making changes to `news.json`
- Check the browser cache (try hard refresh)
- Verify the news.json format is correct

## Future Enhancements

Potential improvements for the news system:
- News notifications
- RSS feed support
- News search functionality
- News categories filtering
- News archive
- News scheduling 