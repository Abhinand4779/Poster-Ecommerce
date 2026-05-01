import os

def main():
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]

    for file in html_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update the logo image path from klaiz_logo.png to black blue.png
        content = content.replace('klaiz_logo.png', 'black blue.png')

        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated Logo filename in {file}")

if __name__ == '__main__':
    main()
