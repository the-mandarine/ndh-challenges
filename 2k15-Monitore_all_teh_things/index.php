<?php
include("flag.php");
$banned_chars = array(
'.',
'/');
$max_msgs = 5;
$temp_dir = "/tmp";
$temp_prefix = "monitore_";
$temp_suffix = ".txt";
?>
<!DOCTYPE html>
<html>
<head>
<title>Monitoring server</title>
<link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
<div id="container">
<?php
if ((isset($_POST['url'])) and ($_POST['url'] != NULL)) {
  $host = htmlspecialchars($_POST['url']);
  $error = '';
  foreach ($banned_chars as $needle) {
    if (!(strpos($host, $needle) === FALSE)){
      $error = $needle;
      break;
    }
  }
  if ($error != '') {
    // error_msg
    $msg="You used a forbidden character: '$error' .";
    echo "<h2>$msg</h2>";
  } else {
    // win msg
    $ch = curl_init("http://$host/" . urlencode($flag));
    curl_setopt($ch, CURLOPT_HEADER, false);
    curl_setopt($ch, CURLOPT_TIMEOUT, 5);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_FAILONERROR, true);
    $msg = substr(preg_replace("/[^a-zA-Z0-9 ]/", "", (strip_tags(curl_exec($ch)))), 0, 140);
    $error = curl_error($ch);
    curl_close($ch);
    if ($error != '') {
      echo "<h2>Error: $error</h2>";
    } else {
      //store the msg in the right files
      $id_file = $temp_dir . '/' . $temp_prefix . 'id';
      $cur_id = 0;
      if (file_exists($id_file)) {
        $fid = fopen($id_file, 'r');
        $cur_id = fread($fid, filesize($id_file));
        fclose($fid);
      }
      // bump the id
      $cur_id = ($cur_id + 1 ) % $max_msgs;
      $msg_file = fopen($temp_dir . '/' . $temp_prefix . $cur_id, 'w');
      fwrite($msg_file, $msg);
      fclose($msg_file);

      // bump the id file
      $fid = fopen($id_file, 'w');
      fwrite($fid, $cur_id);
      fclose($fid);
    }
  }
}
?>

<h1>Which webserver would you like to check?</h1>
<p>
  <form method="POST" action="">
    <label>http://
    <select name="url">
      <option value="mercury">mercury</option>
      <option value="venus">venus</option>
      <option value="earth">earth</option>
      <option value="mars">mars</option>
      <option value="saturn">saturn</option>
      <option value="uranus">uranus</option>
      <option value="neptune">neptune</option>
    </select>/{flag}</label><br />
    <input type="submit" />
  </form>
</p>
<h3>Last messages</h3>
<ul>
<?php
for ($i = 0 ; $i < $max_msgs; $i++) {
  $mon_file = $temp_dir . '/' . $temp_prefix . $i;
  if (file_exists($mon_file)) {
    $mon = fopen($mon_file, 'r');
    $msg = fread($mon, filesize($mon_file));
    fclose($mon);
    echo "<li><pre>$msg</pre></li>";
  }
}

?>
</ul>
</div>
</body>
</html>
<?php

?>