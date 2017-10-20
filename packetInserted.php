<?php
//var_dump($packet);
$packet = ($_GET['packet']);
$image = '"http://localhost/QRcodeP' . $packet .'.png"';
//var_dump($image);
//var_dump ($packet);
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SmartTrackMe</title>
</head>
<style>
body {
    background-image: url(http://www.mpsaspen.com/wp-content/themes/mps/img/boxes.png);
    background-repeat: repeat-x;
    }
#ok_form {
    position: relative;
    top: 200px;
  }
</style>
<body style="background-color:powderblue;">



<form id ="ok_form">
    <center>
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Yes_Check_Circle.svg/768px-Yes_Check_Circle.svg.png"  style="width:20%; height:20%">
        <h1>Package added to the database</h1>
        <h2>Package code is <?php echo($packet)?> </h2>
        <img src = <?php echo($image)?> style="width:20%; height:20%">
    </center>
</form>
</body>
</html>