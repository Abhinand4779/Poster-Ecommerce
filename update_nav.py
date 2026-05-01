import os
import re

def extract_block(content, start_tag, end_tag, include_tags=True):
    pattern = re.compile(rf'({re.escape(start_tag)}.*?{re.escape(end_tag)})', re.DOTALL | re.IGNORECASE)
    match = pattern.search(content)
    if match:
        return match.group(1)
    return None

def main():
    # Read index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        index_content = f.read()

    # Extract standard blocks
    drawer_pattern = re.compile(r'(<!-- 1\. MOBILE MENU DRAWER -->.*?</div>\s*<!-- 2\. BOTTOM NAVIGATION BAR -->)', re.DOTALL)
    drawer_match = drawer_pattern.search(index_content)
    drawer_block = drawer_match.group(1).replace('<!-- 2. BOTTOM NAVIGATION BAR -->', '').strip() if drawer_match else ""

    bottom_nav_pattern = re.compile(r'(<!-- 2\. BOTTOM NAVIGATION BAR -->.*?</nav>)', re.DOTALL)
    bottom_nav_match = bottom_nav_pattern.search(index_content)
    bottom_nav_block = bottom_nav_match.group(1).strip() if bottom_nav_match else ""

    overlay_pattern = re.compile(r'(<!-- 3\. BOTTOM SHEET OVERLAY -->.*?</div>)', re.DOTALL)
    overlay_match = overlay_pattern.search(index_content)
    overlay_block = overlay_match.group(1).strip() if overlay_match else ""

    navbar_pattern = re.compile(r'(<!-- 2\. STICKY NAVBAR -->.*?</nav>)', re.DOTALL)
    navbar_match = navbar_pattern.search(index_content)
    navbar_block = navbar_match.group(1).strip() if navbar_match else ""
    
    if not navbar_block:
        navbar_pattern = re.compile(r'(<nav class="navbar[^>]*id="main-nav">.*?</nav>)', re.DOTALL)
        navbar_match = navbar_pattern.search(index_content)
        navbar_block = navbar_match.group(1).strip() if navbar_match else ""

    footer_pattern = re.compile(r'(<footer class="footer">.*?</footer>)', re.DOTALL)
    footer_match = footer_pattern.search(index_content)
    footer_block = footer_match.group(1).strip() if footer_match else ""

    mobile_stuff = f"{drawer_block}\n\n    {bottom_nav_block}\n\n    {overlay_block}\n"

    # Files to process
    html_files = [f for f in os.listdir('.') if f.endswith('.html') and f != 'index.html']

    for file in html_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove old mobile drawer if exists
        content = re.sub(r'<!-- Mobile Drawer -->.*?</div>\s*</div>', '', content, flags=re.DOTALL)
        content = re.sub(r'<div class="mobile-drawer"[^>]*>.*?</div>\s*(<main|<div class="drawer-footer">)', r'\1', content, flags=re.DOTALL)
        content = re.sub(r'<div class="mobile-drawer"[^>]*>.*?</div>\s*</div>', '', content, flags=re.DOTALL)

        # Remove old bottom nav / overlay if exists
        content = re.sub(r'<nav class="bottom-nav">.*?</nav>', '', content, flags=re.DOTALL)
        content = re.sub(r'<div class="sheet-overlay"[^>]*></div>', '', content, flags=re.DOTALL)

        # Replace navbar
        content = re.sub(r'<nav class="navbar[^>]*>.*?</nav>', navbar_block.replace('navbar', 'navbar scrolled'), content, count=1, flags=re.DOTALL)
        
        # Replace footer
        content = re.sub(r'<footer class="footer">.*?</footer>', footer_block, content, flags=re.DOTALL)

        # Inject mobile stuff right after <body...>
        if "MOBILE MENU DRAWER" not in content:
            content = re.sub(r'(<body[^>]*>)', r'\1\n\n    ' + mobile_stuff.replace('\\', '\\\\'), content, count=1)

        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated {file}")

if __name__ == '__main__':
    main()
