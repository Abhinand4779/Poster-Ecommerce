import os
import re

def main():
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]

    logo_text = r'POSTER<span>IZED</span>'
    logo_img = r'<img src="klaiz_logo.png" alt="Klaiz Designs" class="nav-logo-img">'
    
    for file in html_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace Navbar / Footer Logo
        content = re.sub(logo_text, logo_img, content, flags=re.IGNORECASE)
        
        # Replace Footer copyright / Meta tags
        content = content.replace('POSTERIZED', 'Klaiz Designs')
        content = content.replace('posterized.in', 'klaizdesigns.com')

        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated Logo in {file}")

if __name__ == '__main__':
    main()
