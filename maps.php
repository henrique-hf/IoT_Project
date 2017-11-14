<?php

$lat = floatval($_GET['lat']);
$long = floatval($_GET['long']);
$channel = floatval($_GET['channel']);


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
#find_pack {
    position: relative;
    top: 200px;
  }
</style>
<body style="background-color:orange;">
<body background=http://wallpapercave.com/wp/IsfyoJx.jpg>


<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<h1 align = "center">Find Packet</h1>

<div>
<div id="map" align="center" style="width:400px;height:400px;background:yellow">

<script align = "center">
    function myMap() {
        var lat = <?php echo $lat;?>;
        var long = <?php echo $long;?>;
        var myCenter = new google.maps.LatLng(lat,long);
        console.log(lat);
        var mapOptions = {
            center: new google.maps.LatLng(lat, long),
            zoom: 16,
            mapTypeId: google.maps.MapTypeId.HYBRID
        };
        var marker = new google.maps.Marker({
            position: myCenter,
            animation: google.maps.Animation.BOUNCE
        });
        var map = new google.maps.Map(document.getElementById("map"), mapOptions);
        marker.setMap(map);

    }
</script>

</div>

<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCx5ZMkXsQzq9E8etxOEIh-6fBYE9yAlCs&callback=myMap"></script>
<!--
To use this code on your website, get a free API key from Google.
Read more at: https://www.w3schools.com/graphics/google_maps_basic.asp
-->

<iframe width="450" height="260" style="border: 1px solid #cccccc;" src="https://thingspeak.com/channels/<?php echo $channel;?>/charts/1?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=5&type=line"></iframe>
<iframe width="450" height="260" style="border: 1px solid #cccccc;" src="https://thingspeak.com/channels/<?php echo $channel;?>/charts/2?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=5&type=line"></iframe>

</div>

</html>


