import os

def main():
    template = 'collection.html'
    
    # Format: slug: (Breadcrumb, Title, Subtitle, AdminCategory)
    categories = {
        'superhero': ('Superhero', 'Superhero Posters', 'Action-packed prints', 'Superhero'),
        'cars': ('Cars & Bikes', 'Car Posters', 'High-speed wall art', 'Cars'),
        'movies': ('Movies', 'Movie Posters', 'Cinematic masterpieces', 'Movies'),
        'tvseries': ('TV Series', 'TV Series Posters', 'Your favorite shows', 'TV Series'),
        'music': ('Music', 'Music Posters', 'Melody for your walls', 'Music'),
        'games': ('Games', 'Gaming Posters', 'Level up your room', 'Gaming'),
        'motivational': ('Motivational', 'Motivational Posters', 'Stay inspired', 'Motivational'),
        'cricket': ('Sports', 'Cricket Posters', 'Field of dreams', 'Sports'),
        'football': ('Sports', 'Football Posters', 'Pitch perfect art', 'Sports'),
        'f1': ('Sports', 'Formula 1 Posters', 'Fast & Furious', 'Sports')
    }

    if not os.path.exists(template):
        print(f"Error: {template} not found.")
        return

    with open(template, 'r', encoding='utf-8') as f:
        content = f.read()

    for slug, (breadcrumb, title, count, admin_cat) in categories.items():
        new_file = f'collection-{slug}.html'
        
        # 1. Inject Breadcrumb, Title, and Count placeholders
        new_content = content.replace('{BREADCRUMB}', breadcrumb)
        new_content = new_content.replace('{PAGE_TITLE}', title)
        new_content = new_content.replace('{PRODUCT_COUNT}', count)
        
        # 2. IMPORTANT: Update the data-category on the body tag
        # This is what connects the page to the specific Admin category!
        new_content = new_content.replace('data-category="all"', f'data-category="{admin_cat}"')
        
        # 3. Update the page <title>
        new_content = new_content.replace('<title>Car Posters | Klaiz Designs</title>', f'<title>{title} | Klaiz Designs</title>')

        with open(new_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Successfully generated {new_file} (Category: {admin_cat})")

if __name__ == '__main__':
    main()
