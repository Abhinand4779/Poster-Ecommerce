import os
import re

def main():
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]

    for file in html_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update the logo image path from black blue.png to white blue.png
        content = content.replace('black blue.png', 'white blue.png')

        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated Logo filename in {file}")

if __name__ == '__main__':
    main()
