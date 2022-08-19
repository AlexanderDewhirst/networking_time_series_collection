<?php
    require('database.php');
?>

<!DOCTYPE html>
<html>
<head>
    <title>My Course Manager</title>
    <link rel="stylesheet" type="text/css" href="main.css">
</head>
<body>
    <header><h1>Course Manager</h1></header>

    <main>
        <h1>Add Student</h1>
        <form action="add_student.php" method="post"
              id="add_student_form">

            <?php
                if (isset($_GET['courseID'])) {
                    $courseID = $_GET['courseID'];
                    echo "
                    <label>Course: {$courseID}</label>
                    <input type='hidden' name='courseID' value={$courseID}>
                    <br>
                    ";
                }
            ?>

            <label>First Name:</label>
            <input type="text" name="first_name"><br>

            <label>Last Name:</label>
            <input type="text" name="last_name"><br>

            <label>Email:</label>
            <input type="email" name="email"><br>

            <label>&nbsp;</label>
            <input type="submit" value="Add Student"><br>
        </form>

        <p><a href="index.php">View Student List</a></p>
    </main>

    <footer>
        <p>&copy; <?php echo date("Y"); ?> Alexander Dewhirst</p>
    </footer>
</body>
</html>
