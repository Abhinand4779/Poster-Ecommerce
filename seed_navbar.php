<?php
$host = '127.0.0.1';
$db   = 'klaiz_designs';
$user = 'root';
$pass = '';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$db", $user, $pass);
    
    $links = [
        ['label' => 'Best Sellers', 'url' => 'collection.html'],
        ['label' => 'New Arrivals', 'url' => 'collection-new.html'],
        ['label' => 'Design Your Own', 'url' => 'custom-builder.html'],
        ['label' => 'About', 'url' => 'about.html'],
        ['label' => 'Contact', 'url' => 'contact.html']
    ];
    
    $value = json_encode(['links' => $links]);
    
    // Check if navbar already exists
    $stmt = $pdo->prepare("SELECT COUNT(*) FROM site_settings WHERE `key` = 'navbar'");
    $stmt->execute();
    if ($stmt->fetchColumn() == 0) {
        $stmt = $pdo->prepare("INSERT INTO site_settings (`key`, `value`) VALUES ('navbar', ?)");
        $stmt->execute([$value]);
        echo "Success: Navbar pre-populated with current links!\n";
    } else {
        echo "Navbar already exists in database. No changes made.\n";
    }

} catch (PDOException $e) {
    echo "Error: " . $e->getMessage() . "\n";
}
