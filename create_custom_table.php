<?php
$host = '127.0.0.1';
$db   = 'klaiz_designs';
$user = 'root';
$pass = '';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$db", $user, $pass);
    $sql = "CREATE TABLE IF NOT EXISTS custom_orders (
        id INT AUTO_INCREMENT PRIMARY KEY, 
        customer_name VARCHAR(255), 
        email VARCHAR(255), 
        size VARCHAR(50), 
        image_path VARCHAR(255), 
        price DECIMAL(10,2),
        status VARCHAR(50) DEFAULT 'pending', 
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )";
    $pdo->exec($sql);
    echo "Success: Custom Orders table is ready!\n";
} catch (PDOException $e) {
    echo "Error: " . $e->getMessage() . "\n";
}
