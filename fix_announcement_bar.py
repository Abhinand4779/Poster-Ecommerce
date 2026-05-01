import os
import re

def main():
    root_dir = '.'
    html_files = [f for f in os.listdir(root_dir) if f.lower().endswith('.html') and os.path.isfile(f)]

    new_announcement_bar = """<div class="announcement-bar">
        <div class="marquee-wrapper">
            <div class="marquee">
                <span>FREE SHIPPING on orders above ₹499 | COD Available | 10,000+ Happy Customers</span>
                <span>FREE SHIPPING on orders above ₹499 | COD Available | 10,000+ Happy Customers</span>
                <span>FREE SHIPPING on orders above ₹499 | COD Available | 10,000+ Happy Customers</span>
                <span>FREE SHIPPING on orders above ₹499 | COD Available | 10,000+ Happy Customers</span>
            </div>
            <div class="marquee" aria-hidden="true">
                <span>FREE SHIPPING on orders above ₹499 | COD Available | 10,000+ Happy Customers</span>
                <span>FREE SHIPPING on orders above ₹499 | COD Available | 10,000+ Happy Customers</span>
                <span>FREE SHIPPING on orders above ₹499 | COD Available | 10,000+ Happy Customers</span>
                <span>FREE SHIPPING on orders above ₹499 | COD Available | 10,000+ Happy Customers</span>
            </div>
        </div>
    </div>"""

    # We will match from <div class="announcement-bar"> up to <!-- 2. STICKY NAVBAR -->
    # so we don't accidentally leave dangling divs.
    pattern = re.compile(r'<div class="announcement-bar">.*?(?=<!--\s*2\.\s*STICKY NAVBAR\s*-->|<nav class="navbar)', re.DOTALL | re.IGNORECASE)

    for file in html_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if announcement-bar exists in file
        if '<div class="announcement-bar">' in content:
            new_content, count = pattern.subn(new_announcement_bar + '\n\n    ', content)
            
            if count > 0:
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Fixed announcement bar in {file}")

if __name__ == '__main__':
    main()
