import os
import shutil
import re

def main():
    root_dir = '.'
    photos_dir = 'photos'
    
    # Create photos directory if it doesn't exist
    if not os.path.exists(photos_dir):
        os.makedirs(photos_dir)

    # Find all image files
    image_files = [f for f in os.listdir(root_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg')) and os.path.isfile(f)]
    
    # Files to update
    code_files = [f for f in os.listdir(root_dir) if f.lower().endswith(('.html', '.css', '.js')) and os.path.isfile(f)]

    for code_file in code_files:
        with open(code_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update references for each image
        for img in image_files:
            # We want to replace exactly `img` with `photos/img`.
            # A simple string replacement could work but might be risky if `img` is part of another word.
            # But since they are filenames like `adhil.png`, `white blue.png`, etc., it's usually safe in HTML/CSS/JS.
            
            # Using regex to ensure we only replace it if it's not already prefixed with `photos/`
            # and to handle cases safely. We'll just do a standard replace for simplicity,
            # but ensure we don't do `photos/photos/img.png` if it was run twice.
            # We'll just do simple string replacement, assuming it's not prefixed yet.
            
            # Example: src="white blue.png" -> src="photos/white blue.png"
            # It could also be in data-full="product_poster_1_1777291679013.png"
            
            pattern = re.compile(rf'(?<!photos/)(?<!/)\b{re.escape(img)}\b', re.IGNORECASE)
            
            # Since 'white blue.png' contains a space, \b might not match perfectly at the boundary if we use it around the whole thing,
            # Wait, `img` has an extension. Let's just use string replacement, it's safer for these specific cases.
            # If the file hasn't been moved yet, it's definitely just `img` or `"img"`
            content = content.replace(f'"{img}"', f'"photos/{img}"')
            content = content.replace(f"'{img}'", f"'photos/{img}'")
            # For CSS background-image: url(img)
            content = content.replace(f'({img})', f'(photos/{img})')
            # If there's a space, they might just have `white blue.png` without quotes in some weird place? Not usually in HTML src
            
        with open(code_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated image paths in {code_file}")

    # Move images to photos directory
    for img in image_files:
        src_path = os.path.join(root_dir, img)
        dst_path = os.path.join(photos_dir, img)
        if os.path.exists(dst_path):
            os.remove(dst_path) # overwrite if exists
        shutil.move(src_path, dst_path)
        print(f"Moved {img} to photos/")

if __name__ == '__main__':
    main()
