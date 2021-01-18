<?php
$conn = new mysqli("localhost", "pi", "qwerty", "DrinkAI");

//Return data from last 24 hours
if($_GET['data'] == "raw") {
    $json = array();
    $dayago = time() - 86400;
    $result = $conn->query("SELECT * FROM Drink WHERE timestamp >= " . $dayago . " ORDER BY timestamp DESC");
    if ($result->num_rows > 0) {
        while($row = $result->fetch_assoc()) {
           $json += [$row["timestamp"]=>$row["score"]];
        }
    }
    echo json_encode($json);
}

//Average daily "drink amount" from the last week
if($_GET['data'] == "avg_lastweek") {
    $weekago = time() - 604800;
    $result = $conn->query("SELECT COUNT(score)/7 as r FROM Drink WHERE score > 0 AND timestamp >= " . $weekago);
    if ($result->num_rows > 0) {
        while($row = $result->fetch_assoc()) {
           echo $row["r"];
        }
    }
}

$conn->close();
?>
