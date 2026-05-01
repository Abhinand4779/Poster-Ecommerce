import os

def main():
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]

    for file in html_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Add About and Contact to nav-links if not present
        search_str = '<li><a href="custom-builder.html">Design Your Own</a></li>'
        if '<li><a href="about.html">About</a></li>' not in content:
            new_links = '<li><a href="custom-builder.html">Design Your Own</a></li>\n                    <li><a href="about.html">About</a></li>\n                    <li><a href="contact.html">Contact</a></li>'
            
            # The previous script might have literally inserted \n
            content = content.replace(r'<li><a href="custom-builder.html">Design Your Own</a></li>\n                    <li><a href="about.html">About</a></li>\n                    <li><a href="contact.html">Contact</a></li>', search_str)
            
            content = content.replace(search_str, new_links)

        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated {file}")

if __name__ == '__main__':
    main()
