import os

def main():
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]

    for file in html_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Fix the navbar inner class mistake
        content = content.replace('navbar scrolled-inner', 'navbar-inner')
        content = content.replace('navbar scrolled scrolled', 'navbar scrolled')

        # Double check if any duplicate STICKY NAVBAR comments
        content = content.replace('<!-- 2. STICKY NAVBAR -->\n    <!-- 2. STICKY NAVBAR -->', '<!-- 2. STICKY NAVBAR -->')

        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed {file}")

if __name__ == '__main__':
    main()
