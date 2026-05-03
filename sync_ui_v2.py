import os
import re

# Source of truth
source_file = r"c:\Users\HP\posterrr\index.html"

with open(source_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract sections
def extract_section(tag_id, full_block_regex):
    match = re.search(full_block_regex, content, re.DOTALL)
    if match:
        return match.group(0)
    return None

# Simplified extraction for Mobile Drawer, Bottom Nav, Announcement Bar, Navbar, and Footer
mobile_drawer = re.search(r'<!-- 1\. MOBILE MENU DRAWER -->.*?<div class="mobile-drawer".*?</div>', content, re.DOTALL).group(0)
bottom_nav = re.search(r'<!-- 2\. BOTTOM NAVIGATION BAR.*?<nav class="bottom-nav">.*?</nav>', content, re.DOTALL).group(0)
announcement_bar = re.search(r'<!-- 1\. ANNOUNCEMENT BAR -->.*?<div class="announcement-bar">.*?</div>\s*</div>\s*</div>', content, re.DOTALL)
# Announcement bar structure might be slightly different, let's just grab the whole block
announcement_bar = re.search(r'<!-- 1\. ANNOUNCEMENT BAR -->.*?<div class="announcement-bar">.*?</div>\s*</div>', content, re.DOTALL).group(0)
navbar = re.search(r'<!-- 2\. STICKY NAVBAR -->.*?<nav class="navbar".*?</nav>', content, re.DOTALL).group(0)
footer = re.search(r'<footer class="footer">.*?</footer>', content, re.DOTALL).group(0)

# Also check for overlay
overlay = '<div class="sheet-overlay" id="sheet-overlay"></div>'

sections = {
    'drawer': mobile_drawer,
    'bottom_nav': bottom_nav,
    'announcement': announcement_bar,
    'navbar': navbar,
    'footer': footer
}

target_dir = r"c:\Users\HP\posterrr"
html_files = [f for f in os.listdir(target_dir) if f.endswith('.html') and f != 'index.html']

for filename in html_files:
    filepath = os.path.join(target_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        file_content = f.read()

    # 1. Update Mobile Drawer
    file_content = re.sub(r'<!-- 1\. MOBILE MENU DRAWER -->.*?<div class="mobile-drawer".*?</div>', mobile_drawer, file_content, flags=re.DOTALL)
    
    # 2. Update Bottom Nav
    file_content = re.sub(r'<!-- 2\. BOTTOM NAVIGATION BAR.*?<nav class="bottom-nav">.*?</nav>', bottom_nav, file_content, flags=re.DOTALL)
    
    # 3. Update Announcement Bar
    file_content = re.sub(r'<!-- 1\. ANNOUNCEMENT BAR -->.*?<div class="announcement-bar">.*?</div>\s*</div>', announcement_bar, file_content, flags=re.DOTALL)
    
    # 4. Update Navbar
    file_content = re.sub(r'<!-- 2\. STICKY NAVBAR -->.*?<nav class="navbar".*?</nav>', navbar, file_content, flags=re.DOTALL)
    
    # 5. Update Footer
    file_content = re.sub(r'<footer class="footer">.*?</footer>', footer, file_content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(file_content)

print(f"Synced {len(html_files)} files.")
