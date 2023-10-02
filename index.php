<html>
    <head>
        <title>Super générateur de Rand</title>
    </head>
    <body>
        <p>Super random récupéré depuis une API :</p><br>
        <?php
            $random = json_decode(file_get_contents("http://194.182.163.204:80/random/100"))->random;
            print $random;
        ?>
    </body>
</html>