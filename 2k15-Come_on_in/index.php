<?php
if (isset($_COOKIE['admin'])) {
    setcookie("admin", 0);
}
?>
<html>
<head>
 <title>This website access is restricted</title>
 <link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
  <div id="container">
    <h1>Log in to continue ...</h1>
    <p>
      <form method="POST" action="admin.php">
        <label>User: <input type="text" name="user" /></label><br />
        <label>Pass: <input type="password" name="pass" /></label><br />
        <?php
            $exp = time();
        ?>
        <input type="hidden" name="expiration_time" value=<?php 
            echo '"' . $exp . '"'; ?> />
        <input type="submit" />
      </form>
    </p>
  </div>
</body>
</html>
