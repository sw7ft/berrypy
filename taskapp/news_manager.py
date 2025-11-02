#!/usr/bin/env python3
"""
News Manager for BB10 Task Manager
Simple script to add, edit, and manage news posts in news.json
"""

import json
import os
import datetime
from pathlib import Path

NEWS_FILE = 'news.json'

def load_news():
    """Load existing news data"""
    if os.path.exists(NEWS_FILE):
        with open(NEWS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"news": [], "last_updated": ""}

def save_news(news_data):
    """Save news data to file"""
    news_data['last_updated'] = datetime.datetime.now().isoformat()
    with open(NEWS_FILE, 'w', encoding='utf-8') as f:
        json.dump(news_data, f, indent=2, ensure_ascii=False)
    print(f"News saved to {NEWS_FILE}")

def add_news_post():
    """Add a new news post"""
    print("\n=== Add New News Post ===\n")
    
    title = input("Title: ").strip()
    if not title:
        print("Title is required!")
        return
    
    content = input("Content (markdown format): ").strip()
    if not content:
        print("Content is required!")
        return
    
    author = input("Author (default: Sw7ft): ").strip() or "Sw7ft"
    category = input("Category (update/new-app/android/guide, default: update): ").strip() or "update"
    priority = input("Priority (high/medium/low, default: medium): ").strip() or "medium"
    
    # Load existing news
    news_data = load_news()
    
    # Generate new ID
    new_id = max([item.get('id', 0) for item in news_data.get('news', [])], default=0) + 1
    
    # Create new post
    new_post = {
        "id": new_id,
        "title": title,
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "author": author,
        "content": content,
        "category": category,
        "priority": priority
    }
    
    # Add to news list (at the beginning for newest first)
    news_data['news'].insert(0, new_post)
    
    # Save
    save_news(news_data)
    print(f"\n✅ News post '{title}' added successfully!")

def list_news_posts():
    """List all news posts"""
    news_data = load_news()
    news_list = news_data.get('news', [])
    
    if not news_list:
        print("No news posts found.")
        return
    
    print(f"\n=== News Posts ({len(news_list)} total) ===\n")
    
    for i, post in enumerate(news_list, 1):
        print(f"{i}. [{post.get('category', 'general')}] {post['title']}")
        print(f"   Date: {post.get('date', 'Unknown')} | Author: {post.get('author', 'Unknown')}")
        print(f"   Priority: {post.get('priority', 'medium')}")
        print()

def delete_news_post():
    """Delete a news post by ID"""
    news_data = load_news()
    news_list = news_data.get('news', [])
    
    if not news_list:
        print("No news posts to delete.")
        return
    
    print("\n=== Delete News Post ===\n")
    list_news_posts()
    
    try:
        choice = int(input("Enter the number of the post to delete: ")) - 1
        if 0 <= choice < len(news_list):
            post = news_list[choice]
            confirm = input(f"Are you sure you want to delete '{post['title']}'? (y/N): ").strip().lower()
            
            if confirm == 'y':
                deleted_post = news_list.pop(choice)
                save_news(news_data)
                print(f"✅ Deleted: {deleted_post['title']}")
            else:
                print("Deletion cancelled.")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")

def edit_news_post():
    """Edit an existing news post"""
    news_data = load_news()
    news_list = news_data.get('news', [])
    
    if not news_list:
        print("No news posts to edit.")
        return
    
    print("\n=== Edit News Post ===\n")
    list_news_posts()
    
    try:
        choice = int(input("Enter the number of the post to edit: ")) - 1
        if 0 <= choice < len(news_list):
            post = news_list[choice]
            print(f"\nEditing: {post['title']}\n")
            
            # Edit fields
            new_title = input(f"Title ({post['title']}): ").strip()
            if new_title:
                post['title'] = new_title
            
            new_content = input(f"Content (press Enter to keep current): ").strip()
            if new_content:
                post['content'] = new_content
            
            new_author = input(f"Author ({post.get('author', 'Unknown')}): ").strip()
            if new_author:
                post['author'] = new_author
            
            new_category = input(f"Category ({post.get('category', 'update')}): ").strip()
            if new_category:
                post['category'] = new_category
            
            new_priority = input(f"Priority ({post.get('priority', 'medium')}): ").strip()
            if new_priority:
                post['priority'] = new_priority
            
            # Update date
            post['date'] = datetime.datetime.now().strftime("%Y-%m-%d")
            
            save_news(news_data)
            print(f"✅ Updated: {post['title']}")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")

def main():
    """Main menu"""
    while True:
        print("\n" + "="*50)
        print("BB10 News Manager")
        print("="*50)
        print("1. Add new news post")
        print("2. List all news posts")
        print("3. Edit news post")
        print("4. Delete news post")
        print("5. Exit")
        print("-"*50)
        
        choice = input("Select an option (1-5): ").strip()
        
        if choice == '1':
            add_news_post()
        elif choice == '2':
            list_news_posts()
        elif choice == '3':
            edit_news_post()
        elif choice == '4':
            delete_news_post()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-5.")

if __name__ == '__main__':
    main() 