import os
import re

# Read index.html to extract the exact navbar and footer
with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

# Extract Navbar section
nav_match = re.search(r'(<!-- 1\. MOBILE MENU DRAWER -->.*?</nav>)', index_content, re.DOTALL)
navbar_content = nav_match.group(1) if nav_match else None

if not navbar_content:
    print("Could not find navbar in index.html")

# Extract Footer section
footer_match = re.search(r'(<footer class="footer">.*?</footer>)', index_content, re.DOTALL)
footer_content = footer_match.group(1) if footer_match else None

if not footer_content:
    print("Could not find footer in index.html")

pages = [
    'collection.html', 'product.html', 'cart.html', 'checkout.html', 
    'custom-builder.html', 'policies.html', 'contact.html', 'about.html',
    'search.html', 'login.html', 'signup.html', 'collection-new.html', 'faq.html'
]

for page in pages:
    if os.path.exists(page):
        with open(page, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated = False
        
        # Replace Navbar
        if navbar_content:
            if re.search(r'<!-- 1\. MOBILE MENU DRAWER -->.*?</nav>', content, re.DOTALL):
                content = re.sub(r'<!-- 1\. MOBILE MENU DRAWER -->.*?</nav>', navbar_content, content, flags=re.DOTALL)
                updated = True
            elif re.search(r'<nav class="navbar".*?</nav>', content, re.DOTALL):
                content = re.sub(r'<nav class="navbar".*?</nav>', navbar_content, content, flags=re.DOTALL)
                updated = True

        # Replace Footer
        if footer_content:
            if re.search(r'<footer class="footer">.*?</footer>', content, re.DOTALL):
                content = re.sub(r'<footer class="footer">.*?</footer>', footer_content, content, flags=re.DOTALL)
                updated = True
            
        if updated:
            with open(page, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Successfully updated {page}')
        else:
            print(f'Could not find sections to update in {page}')
