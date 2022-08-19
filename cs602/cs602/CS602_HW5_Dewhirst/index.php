<?php
    require_once('database.php');

    function get_courses($db) {
        $sql = "SELECT * FROM sk_courses";
        $stmt = $db -> query($sql);
        $courses = $stmt -> fetchAll();
        return $courses;
    }

    function get_students($db, $courseID) {
        $sql = "SELECT * FROM sk_students WHERE courseID=:courseID";
        $stmt = $db -> prepare($sql);
        $stmt -> execute(['courseID' => $courseID]);
        $students = $stmt -> fetchAll();
        return $students;
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
    <div style="text-align: center;"><h1>Student List</h1></div>
    <aside>
        <h2>Courses</h2>
        <nav>
            <ul>
                <?php
                    $courses = get_courses($db);
                    foreach ($courses as $course) {
                        echo "
                        <li><a href='index.php?courseID={$course['courseID']}'>{$course['courseID']}</a></li>
                        ";
                    }
                ?>
            </ul>
        </nav>
    </aside>

    <?php
        if (isset($_GET['courseID'])) {
            echo "<h2>Course {$_GET['courseID']} Students</h2>";
        } else {
            echo "<h2>Course Students</h2>";
        }
    ?>

    <section>
        <table>
            <thead>
                <tr>
                    <th>First Name</th>
                    <th>Last Name</th>
                    <th>Email</th>
                </tr>
            </thead>
            <tbody>
                <?php
                    if (isset($_GET['courseID'])) {
                        $courseID = $_GET['courseID'];
                        $students = get_students($db, $courseID);
                        foreach ($students as $student) {
                            echo "
                            <tr>
                                <td>{$student['firstName']}</td>
                                <td>{$student['lastName']}</td>
                                <td>{$student['email']}</td>
                                <td><a href='delete_student.php?id={$student['studentID']}'>Delete</a></td>
                            </tr>
                            ";
                        }
                    }
                ?>
        </table>

        <p>
            <?php
                if (isset($_GET['courseID'])) {
                    echo "<a href='add_student_form.php?courseID=$courseID'>Add Student</a>";
                }
            ?>
        </p>

        <p><a href="course_list.php">List Courses</a></p>

    </section>
</main>

<footer>
    <p>&copy; <?php echo date("Y"); ?> Alexander Dewhirst</p>
</footer>
</body>
</html>
