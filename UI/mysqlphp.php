<!DOCTYPE html>
<html>
<head>
<style>

table {
    width: 100%;
    border-collapse: collapse;
}

table, td, th {
    border: 1px solid black;
    padding: 5px;
}

th {text-align: left;}
</style>

</head>

<body>
<?php
$q = intval($_GET['q']);

$con = mysqli_connect('localhost','root','root','cms');
if (!$con) {
    die('Could not connect: ' . mysqli_error($con));
}

mysqli_select_db($con,"ajax_demo");
$sql="SELECT * FROM slot_info";
$result = mysqli_query($con,$sql);

echo "<table>
<tr>
<th>sr_no</th>
<th>slot_id</th>
<th>distance</th>
</tr>";
while($row = mysqli_fetch_array($result)) {
    echo "<tr>";
    echo "<td>" . $row['sr_no'] . "</td>";
    echo "<td>" . $row['slot_id'] . "</td>";
    echo "<td>" . $row['distance'] . "</td>";
    echo "</tr>";
}
echo "</table>";
mysqli_close($con);
?>
</body>

</html>
