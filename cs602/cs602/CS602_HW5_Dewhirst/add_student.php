<?php
    require_once('database.php');
    // Get the student form data

    if(isset($_POST['courseID']) && isset($_POST['first_name']) && isset($_POST['last_name']) && isset($_POST['email'])) {
        $firstname = $_POST['first_name'];
        $lastname = $_POST['last_name'];
        $email = $_POST['email'];
        $course = $_POST['courseID'];

        // Add the student to the database
        $sql = "INSERT INTO sk_students (courseID, firstName, lastName, email) VALUES (?, ?, ?, ?)";
        $stmt = $db -> prepare($sql);
        $stmt -> execute([$course, $firstname, $lastname, $email]);
    }

    // Display the Student List page
    include('index.php');
?>
