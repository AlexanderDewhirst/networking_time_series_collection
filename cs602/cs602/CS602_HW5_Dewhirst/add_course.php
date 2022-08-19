<?php
    require_once('database.php');
    // Get the course form data
    $identifier = $_POST['course_id'];
    $name = $_POST['course_name'];

    // Add the course to the database
    $sql = "INSERT INTO sk_courses (courseID, courseName) VALUES (?, ?)";
    $stmt = $db -> prepare($sql);
    $stmt -> execute([$identifier, $name]);

    // Display the Course List page
    include('course_list.php');
?>
