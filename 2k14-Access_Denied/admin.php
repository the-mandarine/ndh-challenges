<?php 
$goodref = "http://".$_SERVER['HTTP_HOST'].dirname($_SERVER['SCRIPT_NAME']).'/';
if (($_SERVER['REQUEST_METHOD'] == 'POST') and
    (($_SERVER['HTTP_REFERER'] == $goodref) or
     ($_SERVER['HTTP_REFERER'] == $goodref."index.php"))
   ) { 
   $ok = 1;   
   header("Flag: a_l1ttl3_bit_h4rd3r_th4n_th3_pr3v1ous_0ne_aintit");
}
<html>
<head>
 <title>Admin</title>
 <meta http-equiv="refresh" content="0;URL=./fail.php">
</head>
<body>
<h1>Admin site</h1>
<p>
<?php
if ($ok == 1) {
?>
The flag is not exactly here anymore !
<?php
} elseif ($_SERVER['REQUEST_METHOD'] != 'POST'){
?>
It seems you have tried to hijack our login <em>method</em>. That is not nice
of you.
<?php
} else {
?>
We do not accept login from external sources on this site. Still ... nice try.
<?php
}
?>
</p>
</body>
</html>