<?php
require('flag.php');
$cookie_ok = 0;
if ((isset($_COOKIE['admin'])) && ($_COOKIE['admin'] != 0)) {    
    $cookie_ok = 1;
} else {
    setcookie("admin", 0);
}
?>
<html>
<head>
 <title>Admin site ... or so</title>
 <link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
<?php
if ($cookie_ok == 1) {
    if ((isset($_POST['expiration_time'])) && 
        ($_POST['expiration_time'] != NULL) && 
        ($_POST['expiration_time'] > time()) ){
?>
<h1>Admin site</h1>
<p>
<p>
  <?php echo $flag; ?>
</p>
<?php
    } else {
        /*Expiration date not okay*/
    ?>
<h1>Your login form has expired</h1>
<div id="message">
  <img src="b.jpg" alt="expiration time is passed" title="come on, check the previous form ;)" />
</div>
    <?php
    }
} else {
?>
<h1>You're not admin, sorry</h1>
<div id="message">
  <img src="a.jpg" alt="monster" title="come on, you have to get this one!" />
</div>
<?php
}
?>

</p>
</body>
</html>
