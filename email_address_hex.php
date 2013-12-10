function hexentities($str) {
    $return = "";
    for ($i = 0; $i < strlen($str); $i++) {
        $return .= "&#x" . bin2hex(substr($str, $i, 1)) . ";";
    }
    return $return;
}

echo hexentities("xxxx").PHP_EOL; //PHP_EOL 不同平台下的换行符
