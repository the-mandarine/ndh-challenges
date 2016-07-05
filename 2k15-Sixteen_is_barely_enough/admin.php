<?php
// compromised passwords 
$banned_passes = array(
"2hi6dXY4AnFDvnRP",
"nqoXsMw4sf6Ghg6EpYNoHeJzIU4MDwR08WfNw",
"XjSn4fulrtswIXM39Gt"
);
$admin_pass = $banned_passes[array_rand($banned_passes)];

require('flag.php');
?>
<html>
<head>
 <title>Admin site ... or so</title>
 <link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
<?php
$form_pass = $_POST['pass'];
// Only checking the 16 first chars because it's faster
// sha384 is so secure we don't need more. LOL
$hash_password = substr(hash("sha384", $admin_pass), 0, 16);
$hash_form = substr(hash("sha384", $form_pass), 0, 16);

// I'm soooo l3333t you no byp4ss dat
if (($admin_pass != $form_pass) and 
    ($hash_password == $hash_form) and
    (!(in_array($form_pass, $banned_passes)))) {
?>
<h1>Admin site</h1>
<p>
There you go : <?php echo $flag; ?>
</p>
<?php
} else {
?>
<h1>Access denied<h1>
<p>
Sorry mate. 
</p>
<?php
}
?>
</p>
</body>
</html>
