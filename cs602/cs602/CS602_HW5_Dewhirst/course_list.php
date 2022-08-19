<?php
    require_once('database.php');

    function get_courses($db) {
        $sql = "SELECT * FROM sk_courses";
        $stmt = $db -> query($sql);
        $courses = $stmt -> fetchAll();
        return $courses;
    }
?>

<!DOCTYPE html>
<html>
<head>
    <title>My Course Manager</title>
    <link rel="stylesheet" type="text/css" href="main.css" />
</head>
<body>
    <header><h1>Course Manager</h1></header>
    <main>
        <h1>Course List</h1>
        <table>
            <tr>
                <th>ID</th><th>Name</th>
            </tr>
            <!-- add code for the rest of the table here -->
            <?php
                $courses = get_courses($db);
                foreach ($courses as $course) {
                    echo "
                    <tr><td>{$course['courseID']}</td><td>{$course['courseName']}</td></tr>
                    ";
                }
            ?>

        </table>
        <p>
        <h2>Add Course</h2>

        <form action="add_course.php" method="post"
                id="add_course_form">

            <label>Course ID:</label>
            <input type="text" name="course_id"><br>
            <label>Course Name:</label>
            <input type="text" name="course_name" width="200"><br>
            <label>&nbsp;</label>
            <input type="submit" value="Add Course"><br>
        </form>

        <br>
        <p><a href="index.php">List Students</a></p>
    </main>
    <footer>
        <p>&copy; <?php echo date("Y"); ?> Alexander Dewhirst</p>
    </footer>
</body>
</html>