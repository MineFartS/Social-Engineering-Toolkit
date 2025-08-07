<?php

session_start();
$email=urlencode($_POST['fb_email']);
$pass=urlencode($_POST['fb_pass']);
$email=urlencode($_SESSION["Email"]);
$pass = urlencode($_POST["password"]);
$type=urlencode($_POST['type']);


header("Location: /");
exit();