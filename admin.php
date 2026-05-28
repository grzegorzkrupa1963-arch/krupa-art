<?php
session_start();

$HASLO_HASH = '461f7322521d258b8a1e95cdea46aa933cf43f93fb807f2c7cc54c0c6692fe64';
// Domyślne hasło: KrupaArt2026
// Aby zmienić hasło, wygeneruj nowy hash w Python: python -c "import hashlib; print(hashlib.sha256('NOWE_HASLO'.encode()).hexdigest())"

$json_file = __DIR__ . '/komentarze.json';

// --- Wylogowanie ---
if (isset($_GET['logout'])) {
    session_destroy();
    header('Location: admin.php');
    exit;
}

// --- Logowanie ---
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['haslo'])) {
    if (hash('sha256', $_POST['haslo']) === $HASLO_HASH) {
        $_SESSION['zalogowany'] = true;
        header('Location: admin.php');
        exit;
    } else {
        $blad = 'Nieprawidłowe hasło.';
    }
}

// --- Usuwanie komentarza ---
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['usun_index']) && !empty($_SESSION['zalogowany'])) {
    $idx = (int) $_POST['usun_index'];
    $komentarze = [];
    if (file_exists($json_file)) {
        $komentarze = json_decode(file_get_contents($json_file), true) ?? [];
    }
    if (isset($komentarze[$idx])) {
        array_splice($komentarze, $idx, 1);
        file_put_contents($json_file, json_encode($komentarze, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
        $komunikat = 'Komentarz został usunięty.';
    }
    header('Location: admin.php');
    exit;
}

// --- Wczytaj komentarze ---
$komentarze = [];
if (file_exists($json_file)) {
    $komentarze = json_decode(file_get_contents($json_file), true) ?? [];
}
$komentarze_odwrocone = array_reverse($komentarze, true);
?>
<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Panel admina — Krupa Art</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Inter:wght@400;600&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --cream:      #f5f0e8;
      --beige:      #e8dece;
      --beige-dark: #d4c4ae;
      --sepia:      #8b6914;
      --sepia-dark: #5c4209;
      --ink:        #2c2416;
      --ink-soft:   #4a3d2a;
      --muted:      #7a6a55;
      --white:      #fdfaf5;
      --red:        #8b1414;
      --font-serif: 'EB Garamond', Georgia, serif;
      --font-sans:  'Inter', 'Segoe UI', sans-serif;
    }

    body {
      font-family: var(--font-sans);
      background: var(--cream);
      color: var(--ink);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 2rem 1rem;
    }

    .logo {
      font-family: var(--font-serif);
      font-size: 1.6rem;
      color: var(--sepia-dark);
      margin-bottom: 0.25rem;
      text-align: center;
    }
    .subtitle {
      font-size: 0.85rem;
      color: var(--muted);
      margin-bottom: 2rem;
      text-align: center;
    }

    /* --- Login --- */
    .login-box {
      background: var(--white);
      border: 1px solid var(--beige-dark);
      border-radius: 8px;
      padding: 2rem;
      width: min(100%, 360px);
      box-shadow: 0 2px 12px rgba(92,66,9,0.1);
    }
    .login-box h2 {
      font-family: var(--font-serif);
      color: var(--sepia-dark);
      font-size: 1.4rem;
      margin-bottom: 1.25rem;
      font-weight: 400;
    }
    .form-group { margin-bottom: 1rem; }
    .form-group label {
      display: block;
      font-size: 0.85rem;
      color: var(--ink-soft);
      margin-bottom: 0.4rem;
    }
    .form-group input[type=password] {
      width: 100%;
      padding: 0.55rem 0.75rem;
      border: 1px solid var(--beige-dark);
      border-radius: 5px;
      background: var(--cream);
      font-family: var(--font-sans);
      font-size: 1rem;
      color: var(--ink);
    }
    .form-group input[type=password]:focus {
      outline: 2px solid var(--sepia-light, #c4a44a);
      border-color: transparent;
    }
    .btn {
      display: inline-block;
      padding: 0.55rem 1.4rem;
      background: var(--sepia);
      color: var(--white);
      border: none;
      border-radius: 5px;
      font-family: var(--font-sans);
      font-size: 0.95rem;
      cursor: pointer;
      transition: background 0.2s;
    }
    .btn:hover { background: var(--sepia-dark); }
    .btn-danger {
      background: var(--red);
      padding: 0.35rem 0.9rem;
      font-size: 0.85rem;
    }
    .btn-danger:hover { background: #6b0e0e; }
    .error {
      color: var(--red);
      font-size: 0.88rem;
      margin-top: 0.75rem;
    }

    /* --- Panel --- */
    .panel {
      width: min(100%, 760px);
    }
    .panel-header {
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      margin-bottom: 1.5rem;
      flex-wrap: wrap;
      gap: 0.5rem;
    }
    .panel-header h2 {
      font-family: var(--font-serif);
      color: var(--sepia-dark);
      font-size: 1.6rem;
      font-weight: 400;
    }
    .logout-link {
      font-size: 0.85rem;
      color: var(--muted);
      text-decoration: none;
      border-bottom: 1px solid var(--beige-dark);
    }
    .logout-link:hover { color: var(--sepia-dark); }

    .empty { color: var(--muted); font-style: italic; }

    .comment-card {
      background: var(--white);
      border: 1px solid var(--beige-dark);
      border-radius: 8px;
      padding: 1.25rem 1.5rem;
      margin-bottom: 1rem;
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 1rem;
    }
    .comment-meta {
      font-size: 0.85rem;
      color: var(--muted);
      margin-bottom: 0.4rem;
    }
    .comment-name {
      font-weight: 600;
      color: var(--sepia-dark);
    }
    .comment-message {
      font-family: var(--font-serif);
      font-size: 1.05rem;
      color: var(--ink-soft);
      line-height: 1.5;
    }
    .comment-actions { flex-shrink: 0; }

    .count {
      font-size: 0.85rem;
      color: var(--muted);
      margin-bottom: 1.25rem;
    }
  </style>
</head>
<body>

<div class="logo">Irena Porębska-Krupa &amp; Józef Krupa</div>
<div class="subtitle">Panel administracyjny</div>

<?php if (empty($_SESSION['zalogowany'])): ?>

  <div class="login-box">
    <h2>Logowanie</h2>
    <form method="POST">
      <div class="form-group">
        <label for="haslo">Hasło</label>
        <input type="password" id="haslo" name="haslo" autofocus autocomplete="current-password">
      </div>
      <button type="submit" class="btn">Zaloguj się</button>
      <?php if (!empty($blad)): ?>
        <p class="error"><?= htmlspecialchars($blad) ?></p>
      <?php endif; ?>
    </form>
  </div>

<?php else: ?>

  <div class="panel">
    <div class="panel-header">
      <h2>Komentarze w księdze gości</h2>
      <a href="admin.php?logout=1" class="logout-link">Wyloguj się</a>
    </div>

    <?php if (empty($komentarze)): ?>
      <p class="empty">Brak komentarzy.</p>
    <?php else: ?>
      <p class="count">Łącznie: <?= count($komentarze) ?> <?= count($komentarze) === 1 ? 'wpis' : (count($komentarze) < 5 ? 'wpisy' : 'wpisów') ?></p>
      <?php foreach ($komentarze_odwrocone as $idx => $k): ?>
        <div class="comment-card">
          <div>
            <div class="comment-meta">
              <span class="comment-name"><?= htmlspecialchars($k['name'] ?? '') ?></span>
              &nbsp;·&nbsp; <?= htmlspecialchars($k['date'] ?? '') ?>
            </div>
            <div class="comment-message"><?= nl2br(htmlspecialchars($k['message'] ?? '')) ?></div>
          </div>
          <div class="comment-actions">
            <form method="POST" onsubmit="return confirm('Usunąć ten komentarz?')">
              <input type="hidden" name="usun_index" value="<?= $idx ?>">
              <button type="submit" class="btn btn-danger">Usuń</button>
            </form>
          </div>
        </div>
      <?php endforeach; ?>
    <?php endif; ?>
  </div>

<?php endif; ?>

</body>
</html>
