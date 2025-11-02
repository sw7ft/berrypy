import http.server
import socketserver
import subprocess
import os
import signal
import urllib.parse
import re
import urllib.request
import zipfile
import stat
import time
import threading
import socket
import json

PORT = 8001
BASE_DIR = os.path.dirname(__file__)
HTML_TEMPLATE_PATH = os.path.join(BASE_DIR, 'taskmgr.html')
AUTO_CONFIG_TEMPLATE_PATH = os.path.join(BASE_DIR, 'auto-config.html')

# New template paths
ABOUT_TEMPLATE_PATH = os.path.join(BASE_DIR, 'about.html')
ANDROID_TEMPLATE_PATH = os.path.join(BASE_DIR, 'android.html')

CLI_APPS_DIR = os.path.expanduser('~/usr/local/bin')  # CLI apps directory
WEB_APPS_DIR = os.path.expanduser('~/apps')           # Web apps directory
AVAILABLE_APPS_URL = 'http://berrystore.sw7ft.com/bins/'
WEB_APPS_URL = 'http://berrystore.sw7ft.com/apps/'
# New: APKs directory
APKS_URL = 'http://berrystore.sw7ft.com/apks/'

PROFILE_FILE = os.path.expanduser('~/.profile')
app_ports = {}  # Store mapping of PID to port

# Performance optimization: Caching
CACHE_DURATION = 300  # 5 minutes cache
REQUEST_TIMEOUT = 10  # 10 seconds timeout
APPS_CACHE_DURATION = 60  # 1 minute cache for installed apps
cache = {}
apps_cache = {}

def get_cached_or_fetch(url, cache_key):
    """Get data from cache or fetch from URL with timeout"""
    current_time = time.time()
    
    # Check if we have cached data that's still valid
    if cache_key in cache:
        cached_time, cached_data = cache[cache_key]
        if current_time - cached_time < CACHE_DURATION:
            return cached_data
    
    # Fetch new data with timeout
    try:
        request = urllib.request.Request(url)
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT) as response:
            if response.status != 200:
                print(f"Failed to fetch {url}: Status {response.status}")
                return None
            data = response.read().decode()
            # Cache the result
            cache[cache_key] = (current_time, data)
            return data
    except (urllib.error.URLError, socket.timeout) as e:
        print(f"Error fetching {url}: {e}")
        # Return stale cache if available
        if cache_key in cache:
            cached_time, cached_data = cache[cache_key]
            print(f"Using stale cache for {cache_key}")
            return cached_data
        return None

class TaskManagerHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)

        # Handle /action?...
        if self.path.startswith('/action'):
            params = urllib.parse.parse_qs(parsed_path.query)
            action = params.get('action', [''])[0]
            app_name = params.get('app_name', [''])[0]
            pid = params.get('pid', [''])[0]
            app_type = params.get('app_type', ['cli'])[0]

            if action == 'start' and app_name:
                self.start_app(app_name, app_type)
            elif action == 'stop' and pid:
                self.stop_app(pid)
            elif action == 'install' and app_name:
                self.install_app(app_name, app_type)
            elif action == 'delete' and app_name:
                self.delete_app(app_name, app_type)
            elif action == 'enable_auto_start' and app_name:
                self.enable_auto_start_app(app_name, app_type)
            elif action == 'disable_auto_start' and app_name:
                self.disable_auto_start_app(app_name)

            referer = self.headers.get('Referer', '/')
            self.send_response(303)
            self.send_header('Location', referer)
            self.end_headers()

        # Handle /auto-config page
        elif self.path.startswith('/auto-config'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = self.generate_auto_config_html()
            self.wfile.write(html.encode())

        # New: handle /about page
        elif self.path == '/about':
            self.serve_about_page()

        # New: handle /android page
        elif self.path == '/android':
            self.serve_android_page()

        # Handle lazy loading endpoints
        elif self.path == '/api/available-cli':
            self.serve_available_cli_json()
        elif self.path == '/api/available-web':
            self.serve_available_web_json()
        elif self.path.startswith('/api/app-details'):
            self.serve_app_details()
        elif self.path == '/news':
            self.serve_news_page()
        
        # Serve app icons
        elif self.path.startswith('/app-icons/'):
            self.serve_app_icon()

        # Otherwise serve the main page
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = self.generate_html()
            self.wfile.write(html.encode())

    def serve_available_cli_json(self):
        """Serve available CLI apps as JSON for lazy loading"""
        try:
            html = self.generate_available_cli_html()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())
        except Exception as e:
            print(f"Error serving available CLI apps: {e}")
            self.send_error(500, 'Error loading CLI apps')

    def serve_available_web_json(self):
        """Serve available web apps as JSON for lazy loading"""
        try:
            html = self.generate_available_web_apps_html()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())
        except Exception as e:
            print(f"Error serving available web apps: {e}")
            self.send_error(500, 'Error loading web apps')

    def serve_app_details(self):
        """Serve app details including overview.md content"""
        try:
            parsed_path = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed_path.query)
            app_name = params.get('app_name', [''])[0]
            app_type = params.get('app_type', ['cli'])[0]
            
            if not app_name:
                self.send_error(400, 'App name required')
                return
            
            # Get app description from overview.md
            description = self.get_app_description(app_name, app_type)
            
            # Create install URL
            app_encoded = urllib.parse.quote(app_name + '.zip')
            install_url = f'/action?action=install&app_name={app_encoded}&app_type={app_type}'
            
            # Return JSON response
            response = {
                'description': description,
                'install_url': install_url
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            print(f"Error serving app details: {e}")
            self.send_error(500, 'Error loading app details')

    def serve_app_icon(self):
        """Serve app icon images from app-icons directory"""
        try:
            # Extract icon filename from path
            icon_name = self.path.split('/app-icons/')[-1]
            icon_path = os.path.join(os.path.dirname(__file__), 'app-icons', icon_name)
            
            if os.path.exists(icon_path):
                # Determine content type based on file extension
                if icon_path.endswith('.png'):
                    content_type = 'image/png'
                elif icon_path.endswith('.jpg') or icon_path.endswith('.jpeg'):
                    content_type = 'image/jpeg'
                elif icon_path.endswith('.gif'):
                    content_type = 'image/gif'
                else:
                    content_type = 'application/octet-stream'
                
                with open(icon_path, 'rb') as f:
                    icon_data = f.read()
                
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.send_header('Content-Length', len(icon_data))
                self.end_headers()
                self.wfile.write(icon_data)
            else:
                self.send_error(404, 'Icon not found')
        except Exception as e:
            print(f"Error serving icon: {e}")
            self.send_error(500, 'Error loading icon')

    def get_app_description(self, app_name, app_type):
        """
        Fetch app description from catalog.json file on the server.
        Returns formatted HTML description or fallback text.
        """
        try:
            # Construct URL to fetch catalog.json from the appropriate server
            if app_type == 'cli':
                catalog_url = urllib.parse.urljoin(AVAILABLE_APPS_URL, 'catalog.json')
            else:  # web
                catalog_url = urllib.parse.urljoin(WEB_APPS_URL, 'catalog.json')
            
            # Fetch and cache the catalog
            catalog_data = get_cached_or_fetch(catalog_url, f'catalog_{app_type}')
            
            if catalog_data is None:
                return f'<p>No description available for {app_name}.</p>'
            
            # Parse JSON
            catalog = json.loads(catalog_data)
            
            # Get app info from catalog
            if 'apps' in catalog and app_name in catalog['apps']:
                app_info = catalog['apps'][app_name]
                
                # Build HTML description
                html = '<div class="app-description">'
                if 'name' in app_info:
                    html += f'<h3>{app_info["name"]}</h3>'
                if 'description' in app_info:
                    html += f'<p>{app_info["description"]}</p>'
                if 'version' in app_info:
                    html += f'<p><strong>Version:</strong> {app_info["version"]}</p>'
                if 'author' in app_info:
                    html += f'<p><strong>Author:</strong> {app_info["author"]}</p>'
                if 'category' in app_info:
                    html += f'<p><strong>Category:</strong> {app_info["category"]}</p>'
                if 'requirements' in app_info and app_info['requirements']:
                    html += '<div class="app-requirements">'
                    html += '<p><strong>Python Requirements:</strong></p>'
                    html += '<p style="font-size: 12px; color: #aaa;">Install with:</p>'
                    html += '<pre style="background: #1a1a1a; padding: 10px; border-radius: 4px; overflow-x: auto;">'
                    for req in app_info['requirements']:
                        html += f'python3 -m pip install {req}\n'
                    html += '</pre>'
                    html += '</div>'
                html += '</div>'
                
                return html
            else:
                return f'<p>No description available for {app_name}.</p>'
                    
        except (urllib.error.URLError, urllib.error.HTTPError, socket.timeout) as e:
            print(f"Error fetching catalog.json for {app_name}: {e}")
            return f'<p>No description available for {app_name}.</p>'
        except json.JSONDecodeError as e:
            print(f"Error parsing catalog.json: {e}")
            return f'<p>No description available for {app_name}.</p>'
        except Exception as e:
            print(f"Error processing catalog.json for {app_name}: {e}")
            return f'<p>No description available for {app_name}.</p>'

    def markdown_to_html(self, markdown_text):
        """
        Convert basic markdown to HTML for display in modal.
        Handles common markdown elements like headers, paragraphs, lists, and links.
        """
        try:
            lines = markdown_text.split('\n')
            html_lines = []
            in_list = False
            
            for line in lines:
                line = line.strip()
                if not line:
                    if in_list:
                        html_lines.append('</ul>')
                        in_list = False
                    html_lines.append('<br>')
                    continue
                
                # Headers
                if line.startswith('# '):
                    html_lines.append(f'<h2>{line[2:]}</h2>')
                elif line.startswith('## '):
                    html_lines.append(f'<h3>{line[3:]}</h3>')
                elif line.startswith('### '):
                    html_lines.append(f'<h4>{line[4:]}</h4>')
                
                # Lists
                elif line.startswith('- ') or line.startswith('* '):
                    if not in_list:
                        html_lines.append('<ul>')
                        in_list = True
                    html_lines.append(f'<li>{line[2:]}</li>')
                
                # Links
                elif '[' in line and '](' in line and ')' in line:
                    # Simple markdown link conversion
                    import re
                    line = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', line)
                    html_lines.append(f'<p>{line}</p>')
                
                # Bold and italic
                elif '**' in line:
                    line = line.replace('**', '<strong>', 1).replace('**', '</strong>', 1)
                    html_lines.append(f'<p>{line}</p>')
                elif '*' in line:
                    line = line.replace('*', '<em>', 1).replace('*', '</em>', 1)
                    html_lines.append(f'<p>{line}</p>')
                
                # Regular paragraphs
                else:
                    if in_list:
                        html_lines.append('</ul>')
                        in_list = False
                    html_lines.append(f'<p>{line}</p>')
            
            # Close any open list
            if in_list:
                html_lines.append('</ul>')
            
            return '\n'.join(html_lines)
            
        except Exception as e:
            print(f"Error converting markdown to HTML: {e}")
            return f'<p>{markdown_text}</p>'

    def serve_news_page(self):
        """Serve the news page with content from news.json"""
        try:
            # Load news from JSON file
            news_data = self.load_news_data()
            
            # Generate HTML content
            news_html = self.generate_news_html(news_data)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(news_html.encode())
            
        except Exception as e:
            print(f"Error serving news page: {e}")
            self.send_error(500, 'Error loading news')

    def load_news_data(self):
        """Load news data from news.json file"""
        try:
            news_file_path = os.path.join(BASE_DIR, 'news.json')
            if not os.path.exists(news_file_path):
                return {"news": [], "last_updated": ""}
            
            with open(news_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading news data: {e}")
            return {"news": [], "last_updated": ""}

    def generate_news_html(self, news_data):
        """Generate HTML for the news page"""
        try:
            # Start with the base HTML structure
            html = f'''<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="initial-scale=1, user-scalable=no">
    <title>BB10 News</title>
    <style>
        body {{
            background-color: #1e1e1e;
            color: white;
            font-family: "Slate Pro", Slate, "Myriad Pro", Helvetica, sans-serif;
            font-size: 14px;
            margin: 0;
            padding: 0;
        }}
        .header {{
            background-color: #2b2b2b;
            border-bottom: 2px solid #00769e;
            padding: 10px 20px;
            color: white;
            height: 60px;
            line-height: 40px;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        h1 {{
            font-size: 20px;
            flex-grow: 1;
            text-align: center;
            margin: 0;
        }}
        .hamburger {{
            cursor: pointer;
            width: 30px;
            height: 25px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        .hamburger div {{
            width: 100%;
            height: 4px;
            background-color: white;
            border-radius: 2px;
        }}
        .dropdown {{
            position: relative;
            display: inline-block;
        }}
        .dropdown-content {{
            display: none;
            position: absolute;
            right: 0;
            top: 35px;
            background-color: #2b2b2b;
            min-width: 160px;
            box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
            z-index: 1001;
            border: 1px solid #00769e;
            border-radius: 4px;
        }}
        .dropdown-content a {{
            color: white;
            padding: 12px 16px;
            text-decoration: none;
            display: block;
        }}
        .dropdown-content a:hover {{
            background-color: #00769e;
        }}
        .dropdown:hover .dropdown-content {{
            display: block;
        }}
        .content {{
            padding: 80px 20px 20px 20px;
        }}
        .news-item {{
            background-color: #2b2b2b;
            border: 1px solid #00769e;
            border-radius: 8px;
            margin-bottom: 20px;
            padding: 20px;
        }}
        .news-header {{
            border-bottom: 1px solid #00769e;
            padding-bottom: 10px;
            margin-bottom: 15px;
        }}
        .news-title {{
            font-size: 18px;
            font-weight: bold;
            color: #00769e;
            margin: 0 0 5px 0;
        }}
        .news-meta {{
            font-size: 12px;
            color: #888;
        }}
        .news-category {{
            display: inline-block;
            background-color: #00769e;
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 10px;
            margin-left: 10px;
        }}
        .news-content {{
            line-height: 1.6;
        }}
        .news-content p {{
            margin: 0 0 10px 0;
        }}
        .news-content ul {{
            margin: 10px 0;
            padding-left: 20px;
        }}
        .news-content li {{
            margin: 5px 0;
        }}
        .news-content strong {{
            color: #00769e;
        }}
        .no-news {{
            text-align: center;
            color: #888;
            font-style: italic;
            padding: 40px 20px;
        }}
        .last-updated {{
            text-align: center;
            color: #888;
            font-size: 12px;
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #333;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>BB10 News</h1>
        <div class="dropdown">
            <div class="hamburger">
                <div></div>
                <div></div>
                <div></div>
            </div>
            <div class="dropdown-content">
                <a href="/">Back to Task Manager</a>
                <a href="/auto-config">Auto Start Apps</a>
                <a href="/android">Android Apps</a>
                <a href="/about">About Sw7ft</a>
            </div>
        </div>
    </div>
    <div class="content">
        <h2>Latest Updates</h2>'''
            
            # Add news items
            if news_data.get('news'):
                for news_item in news_data['news']:
                    # Convert markdown content to HTML
                    content_html = self.markdown_to_html(news_item['content'])
                    
                    # Format date
                    date_str = news_item.get('date', 'Unknown')
                    author_str = news_item.get('author', 'Unknown')
                    category_str = news_item.get('category', 'general')
                    
                    html += f'''
        <div class="news-item">
            <div class="news-header">
                <div class="news-title">{news_item['title']}</div>
                <div class="news-meta">
                    {date_str} by {author_str}
                    <span class="news-category">{category_str}</span>
                </div>
            </div>
            <div class="news-content">
                {content_html}
            </div>
        </div>'''
            else:
                html += '''
        <div class="no-news">
            <p>No news available at the moment.</p>
            <p>Check back soon for updates!</p>
        </div>'''
            
            # Add last updated footer
            last_updated = news_data.get('last_updated', '')
            if last_updated:
                html += f'''
        <div class="last-updated">
            Last updated: {last_updated}
        </div>'''
            
            html += '''
    </div>
</body>
</html>'''
            
            return html
            
        except Exception as e:
            print(f"Error generating news HTML: {e}")
            return '''<html><body><h1>Error loading news</h1></body></html>'''

    # -------------------------------------------------------------------------
    # New methods for /about and /android
    # -------------------------------------------------------------------------
    def serve_about_page(self):
        """Serve the about.html page."""
        try:
            with open(ABOUT_TEMPLATE_PATH, 'r') as file:
                html = file.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())
        except Exception as e:
            print(f"Error loading about.html: {e}")
            self.send_error(500, 'Error loading about.html')

    def serve_android_page(self):
        """Serve the android.html page, after populating it with the list of .apk files."""
        try:
            # Fetch the list of .apk files
            apks = self.fetch_android_apks()

            with open(ANDROID_TEMPLATE_PATH, 'r') as file:
                html = file.read()

            # Build app cards similar to available apps section
            if not apks:
                apks_html = '<div class="no-apps">No APKs found.</div>'
            else:
                apks_html = '<div id="apkContainer" class="app-grid">'
                for apk in apks:
                    apk_name = os.path.splitext(apk)[0]  # Remove .apk extension
                    apk_link = urllib.parse.urljoin(APKS_URL, apk)
                    
                    # Determine category based on app name (you can enhance this logic)
                    category = self.determine_apk_category(apk_name)
                    
                    # Create app card - only download button is clickable
                    apks_html += f'''
                    <div class="app-card" data-category="{category}">
                        <div class="app-card-header">
                            <div class="app-icon">&#128241;</div>
                            <div class="app-info">
                                <div class="app-name">{apk_name}</div>
                                <div class="app-type">{category}</div>
                            </div>
                        </div>
                        <div class="app-actions">
                            <a href="{apk_link}" target="_blank" class="app-button">Download APK</a>
                        </div>
                    </div>'''
                apks_html += '</div>'

            # Replace a placeholder in android.html, e.g. <!-- apks_list -->, with our content
            html = html.replace('<!-- apks_list -->', apks_html)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())
        except Exception as e:
            print(f"Error serving android.html: {e}")
            self.send_error(500, 'Error serving android.html')

    def install_app(self, app_name, app_type='cli'):
        try:
            if app_type == 'cli':
                download_url = urllib.parse.urljoin(AVAILABLE_APPS_URL, app_name)
                install_dir = CLI_APPS_DIR
            elif app_type == 'web':
                download_url = urllib.parse.urljoin(WEB_APPS_URL, app_name)
                install_dir = WEB_APPS_DIR
            else:
                print(f"Unknown app type:{app_type}" )
                return

            print(f"Downloading {download_url}")
            request = urllib.request.Request(download_url)
            with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT) as response:
                if response.status != 200:
                    print(f"Failed to download {download_url}: Status {response.status}")
                    return
                zip_data = response.read()

            if not os.path.exists(install_dir):
                os.makedirs(install_dir)
                print(f"Created installation directory at: {install_dir}")

            zip_path = os.path.join(install_dir, app_name)
            with open(zip_path, 'wb') as f:
                f.write(zip_data)
            print(f"Downloaded {app_name} to {zip_path}")

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                if app_type == 'web':
                    app_folder = os.path.splitext(app_name)[0]
                    extract_path = os.path.join(install_dir, app_folder)
                    os.makedirs(extract_path, exist_ok=True)
                    zip_ref.extractall(extract_path)
                    print(f"Extracted {app_name} to {extract_path}")
                else:
                    # For CLI apps, handle lib/ directories specially
                    lib_dir = os.path.expanduser('~/usr/local/lib')
                    bin_dir = os.path.expanduser('~/usr/local/bin')
                    
                    for member in zip_ref.namelist():
                        if member.startswith('lib/'):
                            # Extract lib files to ~/usr/local/lib/
                            # Remove 'lib/' prefix and extract to lib directory
                            lib_file = member[4:]  # Remove 'lib/' prefix
                            if lib_file:  # Skip empty directory entries
                                target_path = os.path.join(lib_dir, lib_file)
                                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                                with zip_ref.open(member) as source, open(target_path, 'wb') as target:
                                    target.write(source.read())
                                print(f"Extracted library: {lib_file} to {lib_dir}")
                        elif member.startswith('bin/'):
                            # Extract bin files to ~/usr/local/bin/
                            bin_file = member[4:]  # Remove 'bin/' prefix
                            if bin_file:  # Skip empty directory entries
                                target_path = os.path.join(bin_dir, bin_file)
                                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                                with zip_ref.open(member) as source, open(target_path, 'wb') as target:
                                    target.write(source.read())
                                print(f"Extracted binary: {bin_file} to {bin_dir}")
                        else:
                            # For other files, extract to bin directory
                            if not member.endswith('/'):  # Skip directories
                                target_path = os.path.join(bin_dir, member)
                                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                                with zip_ref.open(member) as source, open(target_path, 'wb') as target:
                                    target.write(source.read())
                                print(f"Extracted file: {member} to {bin_dir}")

            # Make binaries executable
            if app_type == 'cli':
                self.ensure_cli_paths()
                extracted_files = zip_ref.namelist()
                for file in extracted_files:
                    if not file.endswith('/'):
                        if file.startswith('bin/'):
                            file_path = os.path.join(bin_dir, file[4:])
                        else:
                            file_path = os.path.join(bin_dir, file)
                        if os.path.exists(file_path):
                            os.chmod(file_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
                            print(f"Made {file_path} executable")

            os.remove(zip_path)
            print(f"Removed temporary zip file: {zip_path}")

        except Exception as e:
            print(f"Error installing app {app_name}: {e}")

    def ensure_cli_paths(self):
        """Ensure CLI paths exist"""
        for path in [CLI_APPS_DIR, os.path.expanduser('~/usr/local/lib')]:
            if not os.path.exists(path):
                os.makedirs(path)
                print(f"Created directory: {path}")

    def delete_app(self, app_name, app_type='cli'):
        try:
            if app_type == 'cli':
                app_path = os.path.join(CLI_APPS_DIR, app_name)
                if os.path.exists(app_path):
                    os.remove(app_path)
                    print(f"Deleted CLI app: {app_path}")
            elif app_type == 'web':
                app_path = os.path.join(WEB_APPS_DIR, app_name)
                if os.path.exists(app_path):
                    import shutil
                    shutil.rmtree(app_path)
                    print(f"Deleted web app: {app_path}")
        except Exception as e:
            print(f"Error deleting app {app_name}: {e}")

    def start_app(self, app_name, app_type='cli'):
        try:
            if app_type == 'web':
                app_path = os.path.join(WEB_APPS_DIR, app_name, 'app.py')
                if os.path.exists(app_path):
                    # First read the port from app.py - this is now our primary method
                    port = None
                    try:
                        with open(app_path, 'r') as f:
                            content = f.read()
                            # Look for PORT = XXXX pattern (most common in BB10 apps)
                            port_match = re.search(r'PORT\s*=\s*(\d+)', content)
                            if port_match:
                                port = int(port_match.group(1))
                                print(f"Found port {port} in {app_name}/app.py (PORT variable)")
                            else:
                                # Look for port in app.run() call: app.run(port=XXXX)
                                port_match = re.search(r'app\.run\([^)]*port\s*=\s*(\d+)', content)
                                if port_match:
                                    port = int(port_match.group(1))
                                    print(f"Found port {port} in {app_name}/app.py (app.run)")
                    except Exception as e:
                        print(f"Error reading port from app.py: {e}")
                        return
                    
                    if not port:
                        print(f"Could not find PORT in {app_name}/app.py")
                        return
                    
                    # Start the process
                    process = subprocess.Popen(['python3', app_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    print(f"Started web app: {app_name} with PID: {process.pid}")
                    
                    # Store the port immediately - we trust the PORT value in the file
                    app_ports[process.pid] = port
                    print(f"Using port {port} for {app_name}")
                    
                    # Give the app a moment to start
                    time.sleep(2)
                    
                    # Verify the app started successfully
                    if process.poll() is not None:
                        print(f"ERROR: Process {process.pid} failed to start!")
                        stdout, stderr = process.communicate()
                        print(f"Process output: {stdout.decode()}")
                        print(f"Process errors: {stderr.decode()}")
                else:
                    print(f"Web app not found: {app_path}")
            else:
                # Handle CLI apps
                app_path = os.path.join(CLI_APPS_DIR, app_name)
                if os.path.exists(app_path):
                    # Make sure the file is executable
                    os.chmod(app_path, os.stat(app_path).st_mode | stat.S_IXUSR)
                    
                    # Start the CLI app in background
                    process = subprocess.Popen([app_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    print(f"Started CLI app: {app_name} with PID: {process.pid}")
                else:
                    print(f"CLI app not found: {app_path}")
        except Exception as e:
            print(f"Error starting app {app_name}: {e}")

    def detect_app_port(self, pid, app_name):
        """
        Detect the actual port a web app is running on by checking netstat output
        """
        try:
            print(f"DEBUG: Detecting port for PID {pid}, app {app_name}")
            
            # Method 1: Parse the app.py file for port configuration FIRST
            # This is more reliable than network scanning
            app_path = os.path.join(WEB_APPS_DIR, app_name, 'app.py')
            if os.path.exists(app_path):
                try:
                    with open(app_path, 'r') as f:
                        content = f.read()
                        # Look for common port patterns
                        import re
                        
                        patterns = [
                            (r'PORT\s*=\s*(\d+)', 'PORT constant'),
                            (r'port\s*=\s*(\d+)', 'port variable'),
                            (r'server_address\s*=\s*\([^,]+,\s*(\d+)\)', 'server_address tuple'),
                            (r'HTTPServer\(\s*\([^,]+,\s*(\d+)\)', 'HTTPServer tuple'),
                            (r'app\.run\([^)]*port\s*=\s*(\d+)', 'app.run'),
                            (r'TCPServer\([^)]*(\d+)\)', 'TCPServer')
                        ]
                        
                        for pattern, desc in patterns:
                            port_match = re.search(pattern, content, re.IGNORECASE)
                            if port_match:
                                try:
                                    port = int(port_match.group(1))
                                    if 1024 <= port <= 65535:  # Valid user port range
                                        print(f"DEBUG: Found port {port} in app.py ({desc})")
                                        # Verify the port is actually in use
                                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                        sock.settimeout(0.1)
                                        result = sock.connect_ex(('127.0.0.1', port))
                                        sock.close()
                                        if result == 0:  # Port is open
                                            print(f"DEBUG: Verified port {port} is active")
                                            return port
                                except (ValueError, IndexError):
                                    continue
                except Exception as e:
                    print(f"Error parsing app.py for port: {e}")

            # Method 2: Try netstat (QNX style)
            try:
                output = subprocess.check_output(['netstat', '-an'], timeout=5, stderr=subprocess.DEVNULL).decode()
                lines = output.strip().split('\n')
                
                # First pass: Look for exact PID match
                for line in lines:
                    if str(pid) in line and 'LISTEN' in line:
                        parts = line.split()
                        for part in parts:
                            if ':' in part:
                                try:
                                    port = int(part.split(':')[-1])
                                    if 1024 <= port <= 65535:
                                        print(f"DEBUG: Found port {port} via netstat (PID match)")
                                        return port
                                except (ValueError, IndexError):
                                    continue
                
                # Second pass: Look for listening ports in common ranges
                web_ports = []
                for line in lines:
                    if 'LISTEN' in line:
                        parts = line.split()
                        for part in parts:
                            if ':' in part:
                                try:
                                    port = int(part.split(':')[-1])
                                    if 8000 <= port <= 9000:  # Common web app range
                                        web_ports.append(port)
                                except (ValueError, IndexError):
                                    continue
                
                if len(web_ports) == 1:
                    print(f"DEBUG: Found single listening web port: {web_ports[0]}")
                    return web_ports[0]
                elif web_ports:
                    print(f"DEBUG: Found multiple web ports: {web_ports}")
                    # Prefer port 8000 if available, as it's a common default
                    if 8000 in web_ports:
                        return 8000
                    # Otherwise return the lowest port number
                    return min(web_ports)
                    
            except Exception as e:
                print(f"DEBUG: netstat check failed: {e}")
            
            # Method 3: Direct socket check of common ports
            common_ports = [8000, 8080, 8001, 8002, 8003, 8004, 8005, 8006, 8007, 8008, 8009, 8010]
            listening_ports = []
            
            for port in common_ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.1)
                    result = sock.connect_ex(('127.0.0.1', port))
                    sock.close()
                    if result == 0:  # Port is open
                        listening_ports.append(port)
                except Exception:
                    continue
            
            if len(listening_ports) == 1:
                print(f"DEBUG: Found single listening port via socket check: {listening_ports[0]}")
                return listening_ports[0]
            elif listening_ports:
                print(f"DEBUG: Multiple ports found via socket check: {listening_ports}")
                # Prefer port 8000 if available
                if 8000 in listening_ports:
                    return 8000
                # Otherwise return the lowest port number
                return min(listening_ports)
            
            print(f"DEBUG: No port found for PID {pid}")
            return None
            
        except Exception as e:
            print(f"Error detecting port for PID {pid}: {e}")
            return None

    def stop_app(self, pid):
        try:
            os.kill(int(pid), signal.SIGTERM)
            print(f"Stopped app with PID: {pid}")
            # Remove from port mapping
            if int(pid) in app_ports:
                del app_ports[int(pid)]
        except Exception as e:
            print(f"Error stopping app {pid}: {e}")

    def generate_html(self):
        try:
            with open(HTML_TEMPLATE_PATH, 'r') as file:
                html = file.read()

            manage_apps_html = self.generate_manage_apps_html()
            installed_apps_html = self.generate_installed_apps_html()
            
            # For performance, load available apps with lazy loading placeholders
            available_cli_html = '<div id="available-cli-loading">Loading CLI apps...</div>'
            available_web_html = '<div id="available-web-loading">Loading web apps...</div>'

            manage_apps_html = manage_apps_html if manage_apps_html is not None else ''
            installed_apps_html = installed_apps_html if installed_apps_html is not None else ''

            html = html.replace('<!-- manage_apps -->', manage_apps_html)
            html = html.replace('<!-- installed_apps -->', installed_apps_html)
            html = html.replace('<!-- available_cli_apps -->', available_cli_html)
            html = html.replace('<!-- available_web_apps -->', available_web_html)

            # Add lazy loading JavaScript (ES5 compatible)
            lazy_script = '''
            <script>
            // ES5 compatible lazy loading
            function loadAvailableApps() {
                // Load CLI apps
                var cliContainer = document.getElementById('available-cli-loading');
                if (cliContainer) {
                    var xhr1 = new XMLHttpRequest();
                    xhr1.open('GET', '/api/available-cli', true);
                    xhr1.onreadystatechange = function() {
                        if (xhr1.readyState === 4) {
                            if (xhr1.status === 200) {
                                cliContainer.innerHTML = xhr1.responseText;
                            } else {
                                cliContainer.innerHTML = '<p>Error loading CLI apps</p>';
                            }
                        }
                    };
                    xhr1.send();
                }

                // Load web apps
                var webContainer = document.getElementById('available-web-loading');
                if (webContainer) {
                    var xhr2 = new XMLHttpRequest();
                    xhr2.open('GET', '/api/available-web', true);
                    xhr2.onreadystatechange = function() {
                        if (xhr2.readyState === 4) {
                            if (xhr2.status === 200) {
                                webContainer.innerHTML = xhr2.responseText;
                            } else {
                                webContainer.innerHTML = '<p>Error loading web apps</p>';
                            }
                        }
                    };
                    xhr2.send();
                }
            }

            // Load available apps after page loads
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', loadAvailableApps);
            } else {
                loadAvailableApps();
            }
            </script>
            '''
            html = html.replace('</body>', lazy_script + '</body>')

            return html
        except Exception as e:
            print(f'Error loading HTML template: {e}')
            return '<html><body><h1>Error loading HTML template</h1></body></html>'

    def extract_app_name_from_command(self, cmd):
        """
        Extract a user-friendly app name from a command string.
        Examples:
        - 'python3 /data/apps/myapp/app.py' -> 'myapp'
        - '/usr/local/bin/tool' -> 'tool'
        - 'python3 /data/apps/webserver/app.py' -> 'webserver'
        - 'myapp' -> 'myapp'
        """
        try:
            # Remove common prefixes and extract the app name
            if '/data/apps/' in cmd:
                # Web app pattern: /data/apps/appname/app.py
                parts = cmd.split('/data/apps/')
                if len(parts) > 1:
                    app_part = parts[1].split('/')[0]
                    return app_part
            elif '/usr/local/bin/' in cmd:
                # CLI app pattern: /usr/local/bin/toolname
                parts = cmd.split('/usr/local/bin/')
                if len(parts) > 1:
                    app_part = parts[1].split()[0]  # Take first part before any args
                    return app_part
            elif 'app.py' in cmd:
                # Generic app.py pattern
                if '/apps/' in cmd:
                    parts = cmd.split('/apps/')
                    if len(parts) > 1:
                        app_part = parts[1].split('/')[0]
                        return app_part
                elif '/data/' in cmd:
                    parts = cmd.split('/data/')
                    if len(parts) > 1:
                        app_part = parts[1].split('/')[0]
                        return app_part
            
            # Handle direct executable names (CLI apps)
            if not '/' in cmd and not 'python' in cmd.lower():
                # This might be a direct executable name
                app_name = cmd.split()[0]  # Take first part before any args
                return app_name
            
            # Fallback: try to extract from the end of the path
            if cmd.endswith('app.py'):
                # Remove 'app.py' and get the directory name
                clean_cmd = cmd.replace('app.py', '').rstrip('/')
                app_name = os.path.basename(clean_cmd)
                if app_name:
                    return app_name
            
            # Last resort: return a cleaned version of the command
            return os.path.basename(cmd.split()[0]) if cmd.split() else 'Unknown App'
            
        except Exception as e:
            print(f"Error extracting app name from command '{cmd}': {e}")
            return 'Unknown App'

    def generate_processes_html(self):
        try:
            processes = self.get_python_processes()
            print(f"DEBUG: Found {len(processes)} processes")
            
            if not processes:
                return '<div class="no-apps">No running apps detected. Try refreshing the page.</div>'
            
            cards_html = ''
            for pid, cmd in processes:
                # Extract user-friendly app name instead of showing full command
                app_name = self.extract_app_name_from_command(cmd)
                
                # Check if we already have a port for this PID
                pid_int = int(pid)
                port = None
                if pid_int in app_ports:
                    port = app_ports[pid_int]
                elif 'app.py' in cmd or '/data/apps/' in cmd:
                    detected_port = self.detect_app_port(pid_int, app_name)
                    if detected_port:
                        app_ports[pid_int] = detected_port
                        port = detected_port
                        print(f"Detected port {detected_port} for existing process {pid} ({app_name})")
                
                # Create app card - slim horizontal layout
                address_info = f'<div class="app-address">127.0.0.1:{port}</div>' if port else '<div class="app-address" style="opacity: 0.3;">—</div>'
                cards_html += f'''
                <div class="app-card">
                    <div class="app-icon">{app_name[0].upper()}</div>
                    <div class="app-info">
                        <div class="app-name">{app_name}</div>
                        {address_info}
                    </div>
                    <div class="app-actions">'''
                
                if port:
                    cards_html += f'''
                        <a href="http://127.0.0.1:{port}" target="_blank" class="launch-btn">LAUNCH</a>'''
                
                cards_html += f'''
                        <a href="/action?action=stop&pid={pid}" class="stop-btn">STOP</a>
                    </div>
                </div>'''
            
            return cards_html
        except Exception as e:
            print(f'Error generating processes HTML: {e}')
            return '<div class="error-message">Error loading processes</div>'

    def generate_manage_apps_html(self):
        """
        Generate HTML for the Manage Apps section showing all web apps with start/stop toggle buttons.
        Shows both running and stopped web apps with appropriate buttons.
        """
        try:
            # Get all installed web apps
            web_apps = self.scan_apps_directory(WEB_APPS_DIR, 'web')
            
            # Get currently running processes to determine app status
            running_processes = self.get_python_processes()
            running_app_names = set()
            running_app_pids = {}
            
            for pid, cmd in running_processes:
                app_name = self.extract_app_name_from_command(cmd)
                if 'app.py' in cmd or '/data/apps/' in cmd:
                    running_app_names.add(app_name)
                    running_app_pids[app_name] = pid
            
            # Add taskapp itself if it's running (special case)
            taskapp_running = False
            taskapp_pid = None
            taskapp_port = PORT  # Use the defined PORT constant
            
            for pid, cmd in running_processes:
                if 'taskapp.py' in cmd:
                    taskapp_running = True
                    taskapp_pid = pid
                    running_app_names.add('taskapp')
                    running_app_pids['taskapp'] = pid
                    app_ports[int(pid)] = taskapp_port
                    break
            
            # Create a combined list of all web apps (installed + taskapp)
            all_web_apps = list(web_apps)
            if taskapp_running:
                all_web_apps.append(('taskapp', 'web'))
            
            if not all_web_apps:
                return '<div class="no-apps">No web apps installed. Install web apps from the Available Apps section.</div>'
            
            # Sort apps: running first, then stopped, each group alphabetically
            all_web_apps.sort(key=lambda x: (x[0] not in running_app_names, x[0].lower()))
            
            cards_html = ''
            for app, app_type in all_web_apps:
                if app_type != 'web':
                    continue
                    
                app_encoded = urllib.parse.quote(app)
                is_running = app in running_app_names
                
                # Get port information if running
                port = None
                pid = None
                if is_running:
                    pid = running_app_pids.get(app)
                    if pid and int(pid) in app_ports:
                        port = app_ports[int(pid)]
                    elif pid:
                        # Try to detect port
                        detected_port = self.detect_app_port(int(pid), app)
                        if detected_port:
                            app_ports[int(pid)] = detected_port
                            port = detected_port
                
                # Create app card with toggle functionality
                status_class = 'running' if is_running else 'stopped'
                status_text = 'Running' if is_running else 'Stopped'
                address_info = f'<div class="app-address">{port}</div>' if port else ''
                
                cards_html += f'''
                <div class="app-card app-{status_class}" data-app-name="{app}" data-app-type="web">
                    <div class="app-info">
                        <div class="app-name">{app}</div>
                        {address_info}
                        <div class="app-status">{status_text}</div>
                    </div>
                    <div class="app-actions">'''
                
                if is_running:
                    # Show Launch and Stop buttons
                    if port:
                        cards_html += f'''
                        <a href="http://127.0.0.1:{port}" target="_blank" class="launch-btn">LAUNCH</a>'''
                    
                    # Add stop button for all apps including taskapp
                    cards_html += f'''
                        <button class="stop-btn" onclick="toggleApp('{app}', 'stop', '{pid}')">STOP</button>'''
                else:
                    # Show Start button for stopped apps
                    cards_html += f'''
                        <button class="start-btn" onclick="toggleApp('{app}', 'start', '')">START</button>'''
                
                cards_html += '''
                    </div>
                </div>'''
            
            return cards_html
        except Exception as e:
            print(f'Error generating manage apps HTML: {e}')
            return '<div class="error-message">Error loading manage apps</div>'

    def generate_installed_apps_html(self):
        try:
            # Check cache first
            current_time = time.time()
            cache_key = 'installed_apps'
            
            if cache_key in apps_cache:
                cached_time, cached_apps = apps_cache[cache_key]
                if current_time - cached_time < APPS_CACHE_DURATION:
                    all_apps = cached_apps
                else:
                    # Cache expired, rescan
                    cli_apps = self.scan_apps_directory(CLI_APPS_DIR, 'cli')
                    web_apps = self.scan_apps_directory(WEB_APPS_DIR, 'web')
                    all_apps = cli_apps + web_apps
                    apps_cache[cache_key] = (current_time, all_apps)
            else:
                # No cache, scan and cache
                cli_apps = self.scan_apps_directory(CLI_APPS_DIR, 'cli')
                web_apps = self.scan_apps_directory(WEB_APPS_DIR, 'web')
                all_apps = cli_apps + web_apps
                apps_cache[cache_key] = (current_time, all_apps)

            if not all_apps:
                return '<div class="no-apps">No installed apps found.</div>'

            # Generate list-style HTML similar to running apps - optimized
            html_parts = []
            for app, app_type in all_apps:
                app_encoded = urllib.parse.quote(app)
                display_type = 'Web App' if app_type == 'web' else 'CLI App'
                
                # Build complete card HTML without action buttons
                card_html = f'''<div class="app-card" data-app-name="{app}" data-app-type="{app_type}">
                    <input type="checkbox" class="app-checkbox" value="{app}|{app_type}">
                    <div class="app-info">
                        <div class="app-name">{app}</div>
                        <div class="app-type">{display_type}</div>
                    </div>
                </div>'''
                
                html_parts.append(card_html)
            
            return ''.join(html_parts)
        except Exception as e:
            print(f'Error generating installed apps HTML: {e}')
            return '<div class="error-message">Error loading installed apps</div>'

    def enable_auto_start_app(self, app_name, app_type='cli'):
        try:
            if app_type == 'web':
                app_command = f'python3 "{os.path.join(WEB_APPS_DIR, app_name, "app.py")}" &\n'
            else:
                app_command = f'python3 "{os.path.join(CLI_APPS_DIR, app_name)}" &\n'

            with open(PROFILE_FILE, 'r') as f:
                profile_contents = f.readlines()

            AUTO_START_MARKER_START = f'# <<< Auto-Start for {app_name} >>>'
            AUTO_START_MARKER_END = f'# <<< End Auto-Start for {app_name} >>>'

            if any(app_command.strip() in line.strip() for line in profile_contents):
                print(f"Auto-start for {app_name} is already enabled.")
                return

            with open(PROFILE_FILE, 'a') as f:
                f.write(f'\n{AUTO_START_MARKER_START}\n')
                f.write(app_command)
                f.write(f'{AUTO_START_MARKER_END}\n')

            print(f"Enabled auto-start for {app_name}.")
        except Exception as e:
            print(f"Error enabling auto start for {app_name}: {e}")

    def disable_auto_start_app(self, app_name):
        try:
            if not os.path.exists(PROFILE_FILE):
                print(f"{PROFILE_FILE} does not exist.")
                return

            AUTO_START_MARKER_START = f'# <<< Auto-Start for {app_name} >>>'
            AUTO_START_MARKER_END = f'# <<< End Auto-Start for {app_name} >>>'

            with open(PROFILE_FILE, 'r') as f:
                profile_lines = f.readlines()

            updated_lines = []
            skip = False
            for line in profile_lines:
                if line.strip() == AUTO_START_MARKER_START:
                    skip = True
                    continue
                if line.strip() == AUTO_START_MARKER_END:
                    skip = False
                    continue
                if not skip:
                    updated_lines.append(line)

            with open(PROFILE_FILE, 'w') as f:
                f.writelines(updated_lines)

            print(f"Disabled auto-start for {app_name}.")
        except Exception as e:
            print(f"Error disabling auto start for {app_name}: {e}")

    def generate_available_cli_html(self):
        try:
            available_zips = self.fetch_available_zips()
            if available_zips is None:
                return '<p>Error loading Command Line Utilities.</p>'
                
            installed_cli_apps = set(app for app, _ in self.scan_apps_directory(CLI_APPS_DIR, 'cli'))
            # Exclude installed apps and hide taskapp from available list
            available_zips = [z for z in available_zips if os.path.splitext(z)[0] not in installed_cli_apps and os.path.splitext(z)[0] != 'taskapp']

            if not available_zips:
                return '<p>No Command Line Utilities available.</p>'

            # Fetch catalog to get icon information
            catalog_url = urllib.parse.urljoin(AVAILABLE_APPS_URL, 'catalog.json')
            catalog_data = get_cached_or_fetch(catalog_url, 'catalog_cli')
            catalog = {}
            if catalog_data:
                try:
                    catalog = json.loads(catalog_data).get('apps', {})
                except:
                    pass

            apps_html = '<div class="apps-container">'
            for zip_file in available_zips:
                app_name = os.path.splitext(zip_file)[0]
                
                # Get icon from catalog or use fallback
                icon_html = f'<div class="app-icon-text">{app_name[0].upper()}</div>'
                if app_name in catalog and 'icon' in catalog[app_name]:
                    icon_file = catalog[app_name]['icon']
                    icon_html = f'<img src="/app-icons/{icon_file}" width="48" height="48" alt="{app_name}" onerror="this.outerHTML=\'<div class=&quot;app-icon-text&quot;>{app_name[0].upper()}</div>\'">'
                
                apps_html += f'''
                <div class="app-item" onclick="openModal('{app_name}', 'cli')" style="cursor: pointer;">
                    <div class="app-icon">{icon_html}</div>
                    <div class="app-name">{app_name}</div>
                    <div class="app-click-hint">Click for details</div>
                </div>
                '''
            apps_html += '</div>'
            return apps_html
        except Exception as e:
            print(f"Error generating available CLI apps HTML: {e}")
            return '<p>Error loading Command Line Utilities.</p>'

    def generate_available_web_apps_html(self):
        try:
            available_zips = self.fetch_web_apps()
            if available_zips is None:
                return '<p>Error loading Web Apps.</p>'
                
            installed_web_apps = set(app for app, _ in self.scan_apps_directory(WEB_APPS_DIR, 'web'))
            # Exclude installed apps and hide taskapp from available list
            available_zips = [z for z in available_zips if os.path.splitext(z)[0] not in installed_web_apps and os.path.splitext(z)[0] != 'taskapp']

            if not available_zips:
                return '<p>No Web Apps available.</p>'

            # Fetch catalog to get icon information
            catalog_url = urllib.parse.urljoin(WEB_APPS_URL, 'catalog.json')
            catalog_data = get_cached_or_fetch(catalog_url, 'catalog_web')
            catalog = {}
            if catalog_data:
                try:
                    catalog = json.loads(catalog_data).get('apps', {})
                except:
                    pass

            apps_html = '<div class="apps-container">'
            for zip_file in available_zips:
                app_name = os.path.splitext(zip_file)[0]
                
                # Get icon from catalog or use fallback
                icon_html = f'<div class="app-icon-text">{app_name[0].upper()}</div>'
                if app_name in catalog and 'icon' in catalog[app_name]:
                    icon_file = catalog[app_name]['icon']
                    icon_html = f'<img src="/app-icons/{icon_file}" width="48" height="48" alt="{app_name}" onerror="this.outerHTML=\'<div class=&quot;app-icon-text&quot;>{app_name[0].upper()}</div>\'">'
                
                apps_html += f'''
                <div class="app-item" onclick="openModal('{app_name}', 'web')" style="cursor: pointer;">
                    <div class="app-icon">{icon_html}</div>
                    <div class="app-name">{app_name}</div>
                    <div class="app-click-hint">Click for details</div>
                </div>
                '''
            apps_html += '</div>'
            return apps_html
        except Exception as e:
            print(f"Error generating available Web Apps HTML: {e}")
            return '<p>Error loading Web Apps.</p>'

    def determine_apk_category(self, apk_name):
        """
        Determine the category of an APK based on its name.
        This is a simple categorization - you can enhance this logic.
        """
        apk_lower = apk_name.lower()
        
        # Define category keywords
        categories = {
            'Utility': ['util', 'tool', 'manager', 'cleaner', 'optimizer', 'battery', 'file', 'system'],
            'Emulator': ['emulator', 'emu', 'retro', 'arcade', 'console', 'nintendo', 'sega', 'playstation'],
            'Launcher': ['launcher', 'home', 'desktop', 'theme', 'icon'],
            'Browser': ['browser', 'web', 'chrome', 'firefox', 'opera', 'internet'],
            'Productivity': ['office', 'document', 'pdf', 'note', 'calendar', 'task', 'todo', 'editor'],
            'Communications': ['chat', 'message', 'mail', 'email', 'social', 'whatsapp', 'telegram', 'discord'],
            'Coding': ['code', 'editor', 'ide', 'git', 'terminal', 'ssh', 'ftp', 'developer'],
            'Game': ['game', 'play', 'puzzle', 'action', 'adventure', 'strategy', 'rpg', 'racing']
        }
        
        # Check each category
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in apk_lower:
                    return category
        
        # Default category if no match found
        return 'Utility'

    # New: Fetch .apk files from the berrystore directory
    def fetch_android_apks(self):
        """
        Fetch and parse the listing of .apk files from APKS_URL.
        Returns a list of filenames (e.g. ['myapp.apk', 'anotherapp.apk', ...]).
        """
        html_content = get_cached_or_fetch(APKS_URL, 'android_apks')
        if html_content is None:
            return []

        try:
            # Look for all anchors linking to something ending in .apk
            apk_files = re.findall(r'href=["\']([^"\']+\.apk)["\']', html_content)
            # Just keep the base filenames
            apk_files = [os.path.basename(a) for a in apk_files]
            return apk_files
        except Exception as e:
            print(f"Error parsing Android APKs: {e}")
            return []

    def fetch_available_zips(self):
        html_content = get_cached_or_fetch(AVAILABLE_APPS_URL, 'available_cli_zips')
        if html_content is None:
            return None

        try:
            zip_files = re.findall(r'href=["\']([^"\']+\.zip)["\']', html_content)
            zip_files = [os.path.basename(z) for z in zip_files]
            return zip_files
        except Exception as e:
            print(f"Error parsing available CLI zips: {e}")
            return None

    def fetch_web_apps(self):
        html_content = get_cached_or_fetch(WEB_APPS_URL, 'available_web_apps')
        if html_content is None:
            return None

        try:
            zip_files = re.findall(r'href=["\']([^"\']+\.zip)["\']', html_content)
            zip_files = [os.path.basename(z) for z in zip_files]
            return zip_files
        except Exception as e:
            print(f"Error parsing web apps: {e}")
            return None

    def get_python_processes(self):
        """
        IMPROVED: Better process detection for QNX - looks for all relevant processes
        """
        processes = []
        try:
            # Use pidin ar to get all processes, then filter for relevant ones
            output = subprocess.check_output(['pidin', 'ar'], timeout=5, stderr=subprocess.DEVNULL).decode()
            lines = output.strip().split('\n')
            
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        pid = parts[0]
                        cmd = ' '.join(parts[1:])
                        
                        # Look for various types of running apps:
                        # 1. Python processes (web apps, CLI tools)
                        # 2. Processes in /data/apps/ directory
                        # 3. Processes in /usr/local/bin/ directory
                        # 4. Any process that looks like an app
                        is_relevant = (
                            'python' in cmd.lower() or
                            '/data/apps/' in cmd or
                            '/usr/local/bin/' in cmd or
                            'app.py' in cmd or
                            (cmd.endswith('.py') and not 'taskapp.py' in cmd)  # Exclude taskapp itself
                        )
                        
                        if is_relevant:
                            # Clean up command path for display
                            if '/data/' in cmd:
                                index = cmd.find('/data/') + len('/data/')
                                cmd = cmd[index:]
                            elif '/usr/local/bin/' in cmd:
                                index = cmd.find('/usr/local/bin/') + len('/usr/local/bin/')
                                cmd = cmd[index:]
                            
                            processes.append((pid, cmd))
                            
        except subprocess.CalledProcessError:
            # Fallback: try with different pidin options
            try:
                output = subprocess.check_output(['pidin', '-f', '%a %A %n %p'], timeout=5, stderr=subprocess.DEVNULL).decode()
                lines = output.strip().split('\n')
                
                for line in lines:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 2:
                            pid = parts[0]
                            cmd = ' '.join(parts[1:])
                            
                            is_relevant = (
                                'python' in cmd.lower() or
                                '/data/apps/' in cmd or
                                '/usr/local/bin/' in cmd or
                                'app.py' in cmd or
                                (cmd.endswith('.py') and not 'taskapp.py' in cmd)
                            )
                            
                            if is_relevant:
                                if '/data/' in cmd:
                                    index = cmd.find('/data/') + len('/data/')
                                    cmd = cmd[index:]
                                elif '/usr/local/bin/' in cmd:
                                    index = cmd.find('/usr/local/bin/') + len('/usr/local/bin/')
                                    cmd = cmd[index:]
                                
                                processes.append((pid, cmd))
                                
            except Exception as e:
                print(f'Error getting processes (fallback): {e}')
        except Exception as e:
            print(f'Error getting processes: {e}')
        
        return processes

    def scan_apps_directory(self, directory, app_type):
        apps = []
        try:
            if not os.path.exists(directory):
                return apps
            
            # Optimized scanning - avoid deep recursion for better performance
            if app_type == 'web':
                # For web apps, only scan first level directories for app.py
                try:
                    for item in os.listdir(directory):
                        item_path = os.path.join(directory, item)
                        if os.path.isdir(item_path):
                            app_py_path = os.path.join(item_path, 'app.py')
                            if os.path.exists(app_py_path):
                                apps.append((item, 'web'))
                except OSError:
                    pass
            else:
                # For CLI apps, scan only the bin directory itself
                try:
                    for file in os.listdir(directory):
                        file_path = os.path.join(directory, file)
                        if os.path.isfile(file_path) and not file.endswith('.py') and not file.startswith('.'):
                            # Check if file is executable
                            if os.access(file_path, os.X_OK):
                                apps.append((file, 'cli'))
                except OSError:
                    pass
        except Exception as e:
            print(f'Error scanning apps directory: {e}')
        return apps

    def generate_auto_config_html(self):
        """
        Generate the HTML for the auto-config page, showing web apps
        with options to enable or disable auto start.
        """
        try:
            with open(AUTO_CONFIG_TEMPLATE_PATH, 'r') as file:
                html = file.read()

            all_apps = self.get_all_installed_apps()

            if not all_apps:
                apps_html = '<p>No installed web apps found.</p>'
            else:
                apps_html = '<table>'
                apps_html += '<tr><th>App Name</th><th>Type</th><th>Auto Start</th></tr>'
                for app, app_type in all_apps:
                    if app_type == 'web':  # Only include web apps
                        app_encoded = urllib.parse.quote(app)
                        if self.is_auto_start_enabled(app):
                            # Show Disable Auto Start link if enabled
                            apps_html += f'<tr><td>{app}</td><td>{app_type.upper()}</td><td><a href="/action?action=disable_auto_start&app_name={app_encoded}&app_type={app_type}">Disable Auto Start</a></td></tr>'
                        else:
                            # Show Enable Auto Start link if not enabled
                            apps_html += f'<tr><td>{app}</td><td>{app_type.upper()}</td><td><a href="/action?action=enable_auto_start&app_name={app_encoded}&app_type={app_type}">Enable Auto Start</a></td></tr>'
                apps_html += '</table>'

            html = html.replace('<!-- installed_apps_auto -->', apps_html)
            return html
        except Exception as e:
            print(f'Error loading auto-config HTML template: {e}')
            return '<html><body><h1>Error loading auto-config template</h1></body></html>'

    def get_all_installed_apps(self):
        cli_apps = self.scan_apps_directory(CLI_APPS_DIR, 'cli')
        web_apps = self.scan_apps_directory(WEB_APPS_DIR, 'web')
        return cli_apps + web_apps

    def is_auto_start_enabled(self, app_name):
        """
        Check if auto-start is enabled for the given app by inspecting ~/.profile.
        """
        try:
            if not os.path.exists(PROFILE_FILE):
                return False

            with open(PROFILE_FILE, 'r') as f:
                profile_lines = f.readlines()

            for line in profile_lines:
                if f'python3 "{os.path.join(WEB_APPS_DIR, app_name, "app.py")}" &' in line:
                    return True

            return False
        except Exception as e:
            print(f"Error checking auto-start for {app_name}: {e}")
            return False


def check_path():
    current_path = os.environ.get('PATH', '')
    paths = current_path.split(os.pathsep)
    if CLI_APPS_DIR not in paths:
        print(f"Warning: {CLI_APPS_DIR} is not in your PATH.")
        print("Add to ~/.profile:")
        print(f'export PATH="{CLI_APPS_DIR}:$PATH"')

    if WEB_APPS_DIR not in paths:
        print(f"Note: {WEB_APPS_DIR} is not in your PATH.")
        print("If you want to run web apps from command line, consider adding:")
        print(f'export PATH="{WEB_APPS_DIR}:$PATH"')

if __name__ == '__main__':
    check_path()
    print("Starting optimized Task Manager...")
    print("Performance improvements:")
    print("- Caching network requests (5min TTL)")
    print("- Timeout handling (10s timeout)")
    print("- Optimized pidin usage")
    print("- Lazy loading for available apps")
    
    with socketserver.TCPServer(("", PORT), TaskManagerHandler) as httpd:
        print(f"Serving on port {PORT}")
        httpd.serve_forever() 