<?php
if ($_POST['key'] == "get_json"){
    $json = file_get_contents('alumnos.json');
    echo $json;
}
