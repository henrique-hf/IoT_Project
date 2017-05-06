<?php
$name = $_GET['name'];
$address =$_GET['address'];
$nr = $_GET['nr'];
$city = $_GET['city'];
$zip = $_GET['zip'];
$telephone = $_GET['telephone'];



function insertPacket(packet,$name,$address,$nr,$zip,$city,$telephone,lat,lon):

$script = "INSERT INTO `tracking`.`packet` (`packetid`, `name`, `address`,`n_address`, `zip`, `city`, `telephone`,`lat`,`long`) VALUES ("
$script .= "'" . $packet . "',";
$script .= "'" . $name . "',";
$script .= "'" . $address . "',";
$script .= "'" . $nr . "',";
$script .= "'" . $zip . "',";
$script .= "'" . $city . "',";
$script .= "'" . $telephone . "',";
$script .= "'" . $lat . "',";
$script .= "'" . $lon . "')";


?>

