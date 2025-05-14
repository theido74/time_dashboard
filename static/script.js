$(document).ready(function() {
    function fetchData() {
        $.ajax({
            url: '/temps_total', // L'URL de votre route Flask
            method: 'GET',
            success: function(data) {
                // Mettez à jour la div avec le résultat
                let resultHtml = '';
                data.forEach(temps => {
                    resultHtml += `<p>${temps}</p>`; // Affichez uniquement le temps
                });
                $('#result').html(resultHtml); // Mettez à jour la div
            },
            error: function(error) {
                console.error('Erreur lors de la récupération des données:', error);
                $('#result').html('Erreur lors de la récupération des données.');
            }
        });
    }

    // Appeler fetchData toutes les 5 secondes
    setInterval(fetchData, 5000);
    fetchData(); // Appel initial


    function fetchTop5() {
        $.ajax({
            url: '/top_5', // L'URL de votre route Flask
            method: 'GET',
            success: function(data) {
                // Mettez à jour la liste avec les résultats
                let resultHtml = '';
                data.forEach(item => {
                    resultHtml += `<li>${item}</li>`; // Ajoute chaque résultat à la liste
                });
                $('#top5').html(resultHtml); // Mettez à jour la liste dans la carte
            },
            error: function(error) {
                console.error('Erreur lors de la récupération des données:', error);
                $('#top5').html('<li>Erreur lors de la récupération des données.</li>');
            }
        });
    }

    // Appeler fetchTop5 toutes les 5 secondes
    setInterval(fetchTop5, 5000);
    fetchTop5(); // Appel initial

    function fetchTemps_p_p() {
        $.ajax({
            url: '/temps_par_projet', // L'URL de votre route Flask
            method: 'GET',
            success: function(data) {
                // Mettez à jour la liste avec les résultats
                let resultHtml = '';
                data.forEach(item => {
                    resultHtml += `<p>${item}</p>`; // Ajoute chaque résultat à la liste
                });
                $('#temps_p_p').html(resultHtml); // Mettez à jour la liste dans la carte
            },
            error: function(error) {
                console.error('Erreur lors de la récupération des données:', error);
                $('#temps_p_p').html('<li>Erreur lors de la récupération des données.</li>');
            }
        });
    }

    // Appeler fetchTop5 toutes les 5 secondes
    setInterval(fetchTop5, 5000);
    fetchTemps_p_p(); // Appel initial


    function top_app() {
        $.ajax({
            url: '/TOP_app', // L'URL de votre route Flask
            method: 'GET',
            success: function(data) {
                // Mettez à jour la liste avec les résultats
                let resultHtml = '';
                data.forEach(item => {
                    resultHtml += `<p>${item}</p>`; // Ajoute chaque résultat à la liste
                });
                $('#top_app').html(resultHtml); // Mettez à jour la liste dans la carte
            },
            error: function(error) {
                console.error('Erreur lors de la récupération des données:', error);
                $('#top_app').html('<li>Erreur lors de la récupération des données.</li>');
            }
        });
    }

    // Appeler fetchTop5 toutes les 5 secondes
    setInterval(fetchTop5, 5000);
    top_app(); // Appel initial

    function top_folder() {
        $.ajax({
            url: '/TOP_folder', // L'URL de votre route Flask
            method: 'GET',
            success: function(data) {
                // Mettez à jour la liste avec les résultats
                let resultHtml = '';
                data.forEach(item => {
                    resultHtml += `<p>${item}</p>`; // Ajoute chaque résultat à la liste
                });
                $('#top_folder').html(resultHtml); // Mettez à jour la liste dans la carte
            },
            error: function(error) {
                console.error('Erreur lors de la récupération des données:', error);
                $('#top_folder').html('<li>Erreur lors de la récupération des données.</li>');
            }
        });
    }

    // Appeler fetchTop5 toutes les 5 secondes
    setInterval(fetchTop5, 5000);
    top_folder(); // Appel initial

    function last_24h() {
        $.ajax({
            url: '/last_24h', // L'URL de votre route Flask
            method: 'GET',
            success: function(data) {
                // Mettez à jour la liste avec les résultats
                let resultHtml = '';
                data.forEach(item => {
                    resultHtml += `<li>${item}</li>`; // Ajoute chaque résultat à la liste
                });
                $('#last_24h_list').html(resultHtml); // Mettez à jour la liste dans la carte
            },
            error: function(error) {
                console.error('Erreur lors de la récupération des données:', error);
                $('#last_24h_list').html('<li>Erreur lors de la récupération des données.</li>');
            }
        });
    }
    
    // Appeler last_24h toutes les 5 secondes
    setInterval(last_24h, 5000);
    last_24h(); // Appel initial

});