import os
import re

def main():
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]

    for file in html_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Fix logo link
        content = re.sub(r'<a href="#" class="logo">POSTER<span>IZED</span></a>', 
                         r'<a href="index.html" class="logo">POSTER<span>IZED</span></a>', 
                         content)

        # Fix cart button closing tag mismatch
        content = re.sub(r'(<a href="cart\.html" class="nav-icon-btn cart-btn">.*?<span class="cart-count">0</span>\s*)</button>', 
                         r'\1</a>', 
                         content, flags=re.DOTALL)

        # Add About and Contact to nav-links if not present
        if 'href="about.html">About</a>' not in content and 'href="contact.html">Contact</a>' not in content:
            new_links = r'<li><a href="custom-builder.html">Design Your Own</a></li>\n                    <li><a href="about.html">About</a></li>\n                    <li><a href="contact.html">Contact</a></li>'
            content = content.replace('<li><a href="custom-builder.html">Design Your Own</a></li>', new_links)

        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated {file}")

if __name__ == '__main__':
    main()
