<?php
$lat = floatval($_GET['lat']);
$long = floatval($_GET['long']);
$channel = floatval($_GET['channel']);
?>

<h1 align = "center">Package Present and History</h1>

<body background=http://wallpapercave.com/wp/IsfyoJx.jpg>

<div id="container" align="center">
    <h2>Package actual position</h2>
    <div id="map" align="center" style="width:400px ;height: 400px; margin-bottom: 50px">



        <script>
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
    <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCx5ZMkXsQzq9E8etxOEIh-6fBYE9yAlCs&callback=myMap"></script>
    <!--
    To use this code on your website, get a free API key from Google.
    Read more at: https://www.w3schools.com/graphics/google_maps_basic.asp
    -->
    </div>
    <div id="stat" align="center" style="width:auto;height:auto; position: relative">
        <h2>Temperature and Humidity History</h2>
        <iframe width="450" height="260" style="margin-right: 10px; border: 1px solid #cccccc; top: " src="https://thingspeak.com/channels/<?php echo $channel;?>/charts/1?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=5&type=line"></iframe>
        <iframe width="450" height="260" style="margin-left: 10px; border: 1px solid #cccccc;" src="https://thingspeak.com/channels/<?php echo $channel;?>/charts/2?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=5&type=line"></iframe>
    </div>
</div>
</body>
</html>
