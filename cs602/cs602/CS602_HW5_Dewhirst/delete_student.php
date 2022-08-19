<?php
  require_once('database.php');
  // Delete the student from the database
  $id = $_GET['id'];
  $sql = "DELETE FROM sk_students WHERE studentID=?";
  $stmt = $db -> prepare($sql);
  $stmt -> execute([$id]);

  // Display the Home page
  include('index.php');
?>