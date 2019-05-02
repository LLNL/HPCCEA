<?php

$conn = new PDO('mysql:host=localhost;dbname=devdb', 'testu', 'Testup433');
if (!$conn) {
  die('Could not connect');
}

$sql="INSERT INTO pclamps (fk_paperid, figurenum, species, sex, graphpath) VALUES ('$_POST[paperid]', '$_POST[fignum]', '$_POST[species]', '$_POST[gender]', '$_POST[imagepath]')";
$result = $conn->prepare($sql);
$result->execute();
?>
