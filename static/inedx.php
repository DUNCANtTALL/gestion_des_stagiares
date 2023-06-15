<?php
        session_start();
	$db = mysqli_connect('localhost', 'root', '', 'data');

    if (isset($_GET['edit'])) {
		$id = $_GET['edit'];
		$update = true;
		$record = mysqli_query($db, "SELECT * FROM info WHERE id=$id");

		if (count($record) == 1 ) {
			$n = mysqli_fetch_array($record);
			$nom = $n['nom'];
			$prenom = $n['prenom'];
		}
	}
		


        ?>