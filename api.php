<?php
$conn = new mysqli("localhost", "pi", "qwerty", "DrinkAI");

if($_GET['data'] == "raw") {
    $json = array();
    $result = $conn->query("SELECT * FROM Drink ORDER BY timestamp DESC LIMIT 86400");
    if ($result->num_rows > 0) {
        while($row = $result->fetch_assoc()) {
           $json += [$row["timestamp"]=>$row["score"]];
        }
    }
    echo json_encode($json);
}
if($_GET['data'] == "avg_lastweek") {
    $weekago = time() - 604800;
    $result = $conn->query("SELECT COUNT(score)/168 as r FROM Drink WHERE score > 0 AND timestamp >= " . $weekago);
    if ($result->num_rows > 0) {
        while($row = $result->fetch_assoc()) {
           echo $row["r"];
        }
    }
}

$conn->close();
?>
