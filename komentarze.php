<?php
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST');
header('Access-Control-Allow-Headers: Content-Type');

$file        = __DIR__ . '/komentarze.json';
$admin_email = 'grzegorz.krupa.1963@gmail.com';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $data    = json_decode(file_get_contents('php://input'), true);
    $name    = trim($data['name']    ?? '');
    $message = trim($data['message'] ?? '');

    if (!$name || !$message) {
        http_response_code(400);
        echo json_encode(['error' => 'Brak danych']);
        exit;
    }

    $name    = mb_substr(htmlspecialchars($name,    ENT_QUOTES, 'UTF-8'), 0, 100);
    $message = mb_substr(htmlspecialchars($message, ENT_QUOTES, 'UTF-8'), 0, 2000);

    $comment = [
        'name'    => $name,
        'message' => $message,
        'date'    => date('d.m.Y H:i'),
    ];

    $comments = [];
    if (file_exists($file)) {
        $comments = json_decode(file_get_contents($file), true) ?? [];
    }
    $comments[] = $comment;
    file_put_contents($file, json_encode($comments, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));

    $subject = '=?UTF-8?B?' . base64_encode('Nowy wpis w księdze gości — ' . $name) . '?=';
    $body    = "Nowy wpis w księdze gości na krupa-art.pl\n\n"
             . "Imię: $name\n\n"
             . "Wiadomość:\n$message\n\n"
             . "Data: {$comment['date']}";
    $headers = "From: ksiega@krupa-art.pl\r\n"
             . "Reply-To: ksiega@krupa-art.pl\r\n"
             . "Content-Type: text/plain; charset=UTF-8\r\n"
             . "Content-Transfer-Encoding: base64";
    mail($admin_email, $subject, base64_encode($body), $headers);

    echo json_encode(['ok' => true, 'comment' => $comment]);

} else {
    $comments = [];
    if (file_exists($file)) {
        $comments = json_decode(file_get_contents($file), true) ?? [];
    }
    echo json_encode(array_reverse($comments));
}
