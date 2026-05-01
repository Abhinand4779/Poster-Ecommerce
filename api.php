<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");
header("Content-Type: application/json");

// Database Connection
$host = '127.0.0.1';
$db   = 'klaiz_designs';
$user = 'root';
$pass = '';
$charset = 'utf8mb4';

$dsn = "mysql:host=$host;dbname=$db;charset=$charset";
$options = [
    PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES   => false,
];

try {
     $pdo = new PDO($dsn, $user, $pass, $options);
} catch (\PDOException $e) {
     die(json_encode(['error' => 'Database connection failed: ' . $e->getMessage()]));
}

// Ensure tables exist
$pdo->exec("CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    image LONGTEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)");

$pdo->exec("CREATE TABLE IF NOT EXISTS site_settings (
    `key` VARCHAR(255) PRIMARY KEY,
    `value` LONGTEXT NOT NULL
)");

$pdo->exec("CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    pincode VARCHAR(20) NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    items TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)");

$method = $_SERVER['REQUEST_METHOD'];
$path = $_SERVER['REQUEST_URI'];

// --- ROUTING ---

// POST /api/order (Standard Checkout)
if ($method === 'POST' && strpos($path, '/api/order') !== false) {
    $data = json_decode(file_get_contents('php://input'), true);
    
    if (!$data) {
        http_response_code(400);
        echo json_encode(['error' => 'Invalid data']);
        exit;
    }

    $stmt = $pdo->prepare("INSERT INTO orders (customer_name, email, address, city, pincode, total_price, items) VALUES (?, ?, ?, ?, ?, ?, ?)");
    $stmt->execute([
        $data['name'],
        $data['email'],
        $data['address'],
        $data['city'],
        $data['pincode'],
        $data['total'],
        json_encode($data['items'])
    ]);

    echo json_encode(['success' => true, 'order_id' => $pdo->lastInsertId()]);
    exit;
}

// GET /api/product (Single Item)
if ($method === 'GET' && strpos($path, '/api/product') !== false) {
    $id = $_GET['id'] ?? null;
    if ($id) {
        $stmt = $pdo->prepare("SELECT * FROM products WHERE id = ?");
        $stmt->execute([$id]);
        echo json_encode($stmt->fetch());
    } else {
        http_response_code(400);
        echo json_encode(['error' => 'Missing ID']);
    }
    exit;
}

// GET /api/products (with Filtering)
if ($method === 'GET' && strpos($path, '/api/products') !== false) {
    $category = $_GET['category'] ?? 'all';
    $max_price = $_GET['max_price'] ?? 99999;
    
    $query = "SELECT * FROM products WHERE price <= ?";
    $params = [$max_price];
    
    if ($category !== 'all') {
        $query .= " AND category = ?";
        $params[] = $category;
    }
    
    $query .= " ORDER BY id DESC";
    
    $stmt = $pdo->prepare($query);
    $stmt->execute($params);
    echo json_encode($stmt->fetchAll());
    exit;
}

// GET /api/settings/all
if ($method === 'GET' && strpos($path, '/api/settings/all') !== false) {
    $stmt = $pdo->query("SELECT * FROM site_settings");
    echo json_encode($stmt->fetchAll());
    exit;
}

// POST /api/admin/products
if ($method === 'POST' && strpos($path, '/api/admin/products') !== false) {
    $data = json_decode(file_get_contents('php://input'), true);
    if (isset($data['name'], $data['category'], $data['price'], $data['image'])) {
        $stmt = $pdo->prepare("INSERT INTO products (name, category, price, image) VALUES (?, ?, ?, ?)");
        $stmt->execute([$data['name'], $data['category'], $data['price'], $data['image']]);
        echo json_encode(['message' => 'Product saved successfully!']);
    }
    exit;
}

// POST /api/admin/settings
if ($method === 'POST' && strpos($path, '/api/admin/settings') !== false) {
    $data = json_decode(file_get_contents('php://input'), true);
    if (isset($data['key'], $data['value'])) {
        $stmt = $pdo->prepare("INSERT INTO site_settings (`key`, `value`) VALUES (?, ?) ON DUPLICATE KEY UPDATE `value` = ?");
        $stmt->execute([$data['key'], $data['value'], $data['value']]);
        echo json_encode(['message' => 'Setting updated!']);
    }
    exit;
}

// Custom Order Submission (with File Upload)
if ($method === 'POST' && strpos($path, '/api/custom-order') !== false) {
    if (!isset($_FILES['image'])) {
        http_response_code(400);
        echo json_encode(['error' => 'No image uploaded']);
        exit;
    }

    $upload_dir = 'uploads/custom/';
    if (!is_dir($upload_dir)) mkdir($upload_dir, 0777, true);

    $file_name = time() . '_' . basename($_FILES['image']['name']);
    $target_file = $upload_dir . $file_name;

    if (move_uploaded_file($_FILES['image']['tmp_name'], $target_file)) {
        $name = $_POST['name'] ?? 'Guest';
        $email = $_POST['email'] ?? '';
        $size = $_POST['size'] ?? 'A3';
        $price = $_POST['price'] ?? 0;

        $stmt = $pdo->prepare("INSERT INTO custom_orders (customer_name, email, size, image_path, price) VALUES (?, ?, ?, ?, ?)");
        $stmt->execute([$name, $email, $size, $target_file, $price]);

        echo json_encode(['success' => true, 'message' => 'Order received!', 'order_id' => $pdo->lastInsertId()]);
    } else {
        http_response_code(500);
        echo json_encode(['error' => 'Failed to save image']);
    }
    exit;
}

// Fetch Custom Orders for Admin
if ($method === 'GET' && strpos($path, '/api/admin/custom-orders') !== false) {
    $stmt = $pdo->query("SELECT * FROM custom_orders ORDER BY created_at DESC");
    echo json_encode($stmt->fetchAll(PDO::FETCH_ASSOC));
    exit;
}

echo json_encode(['message' => 'Klaiz API is running!']);
