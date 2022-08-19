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

  if (isset($_GET['format']) && isset($_GET['action'])) {
    $format = $_GET['format'];
    $action = $_GET['action'];

    if ($action == 'courses') {
      $data = get_courses($db);

      if ($format == 'xml') {
        $content = '&lt;?xml version="1.0"?&gt;&lt;courses&gt;';
        foreach ($data as $course) {
          $content .= "&lt;course&gt;&lt;courseID&gt;".$course['courseID']."&lt;/courseID&gt;&lt;courseName&gt;".$course['courseName']."&lt;/courseName&gt;&lt;/course&gt;";
        }
        $content .= "&lt;/courses&gt;";
        echo $content;
      } else if ($format == 'json') {
        $content = array();
        foreach ($data as $course) {
          array_push($content, array("CourseID" => $course['courseID'], "CourseName" => $course['courseName']));
        }
        echo json_encode($content);
      } else {
        require_once 'error.php';
      }
    } else if ($action == 'students' && isset($_GET['course'])) {
      $course = $_GET['course'];

      $data = get_students($db, $course);

      if ($format == 'xml') {
        $content = '&lt;?xml version="1.0"?&gt;&lt;students&gt;';
        foreach ($data as $student) {
          $content .= "&lt;student&gt;";
          $content .= "&lt;studentID&gt;".$student['studentID']."&lt;/studentID&gt;";
          $content .= "&lt;courseID&gt;".$course."&lt;/courseID&gt;";
          $content .= "&lt;firstName&gt;".$student['firstName']."&lt;/firstName&gt;";
          $content .= "&lt;lastName&gt;".$student['lastName']."&lt;/lastName&gt;";
          $content .= "&lt;/student&gt;";
        }
        $content .= "&lt;/students&gt;";

        echo $content;
      } else if ($format == 'json') {
        $content = array();
        foreach ($data as $student) {
          array_push($content, array(
            "StudentID" => $student['studentID'], 'CourseID' => $course, 'firstName' => $student['firstName'], 'lastName' => $student['lastName']
          ));
        }
        echo json_encode($content);
      } else {
        require_once 'error.php';
      }
    } else {
      require_once 'error.php';
    }
  }
?>
