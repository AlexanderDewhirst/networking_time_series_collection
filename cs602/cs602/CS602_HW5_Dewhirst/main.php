<?php
  function main() {
    if ($_SERVER['PHP_SELF'] == "/" || $_SERVER['PHP_SELF'] == '/index.php') {
      require_once 'index.php';
    } else if ($_SERVER['PHP_SELF'] == '/add_student_form.php') {
      require_once 'add_student_form.php';
    } else if ($_SERVER['PHP_SELF'] == '/course_list.php') {
      require_once 'course_list.php';
    } else if ($_SERVER['PHP_SELF'] == '/add_student.php') {
      require_once 'add_student.php';
    } else if ($_SERVER['PHP_SELF'] == '/add_course.php') {
      require_once 'add_course.php';
    } else if ($_SERVER['PHP_SELF'] == '/delete_student.php') {
      require_once 'delete_student.php';
    } else if ($_SERVER['PHP_SELF'] == '/rest.php') {
      require_once 'rest.php';
    } else {
      require_once 'error.php';
    }
  }

  main();
?>
