<?php

$conn = new PDO('mysql:host=localhost;dbname=devdb', 'testu', 'Testup433');
if (!$conn) {
  die('Could not connect');
}

$sql="INSERT INTO papers (pubmedid, authors, papertext) VALUES ('$_POST[pubmedid]', '$_POST[authors]', '$_POST[paper]')";
$result = $conn->prepare($sql);
$result->execute();
?>
