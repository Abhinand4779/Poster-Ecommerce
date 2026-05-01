import os
import glob

def main():
    root_dir = '.'
    html_files = glob.glob(os.path.join(root_dir, '*.html'))

    replacements = {
        'support@klaizdesigns.com': 'support@klaizdesigns.in',
        'hello@klaizdesigns.com': 'support@klaizdesigns.in',
        '+91 98765 43210': '+91 7034219758',
        'href="https://instagram.com"': 'href="https://instagram.com/klaizdesigns.in"',
        # Also just in case they used single quotes or other variations:
        "href='https://instagram.com'": "href='https://instagram.com/klaizdesigns.in'",
    }

    for file in html_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content = content
        for old, new in replacements.items():
            new_content = new_content.replace(old, new)

        if content != new_content:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated contact info in {file}")

if __name__ == '__main__':
    main()
