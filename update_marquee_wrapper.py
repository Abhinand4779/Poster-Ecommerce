import os
import re

def main():
    root_dir = '.'
    html_files = [f for f in os.listdir(root_dir) if f.lower().endswith('.html') and os.path.isfile(f)]

    new_marquee = """<div class="marquee-wrapper">
            <div class="marquee">
                <span>FREE SHIPPING on orders above ₹499 | COD Available | 10,000+ Happy Customers</span>
                <span>FREE SHIPPING on orders above ₹499 | COD Available | 10,000+ Happy Customers</span>
            </div>
            <div class="marquee" aria-hidden="true">
                <span>FREE SHIPPING on orders above ₹499 | COD Available | 10,000+ Happy Customers</span>
                <span>FREE SHIPPING on orders above ₹499 | COD Available | 10,000+ Happy Customers</span>
            </div>
        </div>"""

    # Regex to match the entire announcement-content div OR the newly created marquee
    pattern = re.compile(r'<div class="announcement-content marquee">.*?</div>', re.DOTALL)
    
    # We might also need to match the previous structure if it's different.
    # The previous script replaced it with `<div class="announcement-content marquee">...</div>`
    for file in html_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content, count = pattern.subn(new_marquee, content)

        if count > 0:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated marquee in {file}")

if __name__ == '__main__':
    main()
