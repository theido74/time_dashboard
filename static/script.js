$(document).ready(function() {
    function fetchData() {
        $.ajax({
            url: '/temps_total', // L'URL de votre route Flask
            method: 'GET',
            success: function(data) {
                // Mettez à jour la div avec le résultat
                let resultHtml = '';
                data.forEach(temps => {
                    resultHtml += `<li>${temps}</li>`; // Affichez uniquement le temps
                });
                $('#temps_total_list').html(resultHtml); // Mettez à jour la div
            },
            error: function(error) {
                console.error('Erreur lors de la récupération des données:', error);
                $('#temps_total_list').html('<li>Erreur lors de la récupération des données.</li>');
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
                $('#top5').html(resultHtml); // Mettez à jour la liste dans la
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
                    resultHtml += `<li>${item}</li>`; // Ajoute chaque résultat à la liste
                });
                $('#temps_p_p_list').html(resultHtml); // Mettez à jour la liste dans la carte
            },
            error: function(error) {
                console.error('Erreur lors de la récupération des données:', error);
                $('#temps_p_p_list').html('<li>Erreur lors de la récupération des données.</li>');
            }
        });
    }

    // Appeler fetchTemps_p_p toutes les 5 secondes
    setInterval(fetchTemps_p_p, 5000);
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

    // Appeler top_app toutes les 5 secondes
    setInterval(top_app, 5000);
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

    // Appeler top_folder toutes les 5 secondes
    setInterval(top_folder, 5000);
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

    // script.js

function fetchResults(mois) {
    if (mois) {
        fetch(`/mois/${mois}`)
            .then(response => response.json())
            .then(data => {
                const container = document.getElementById('resultatsContainer');
                container.innerHTML = ''; // Clear previous results

                if (data.length > 0) {
                    let html = `<h2>Résultats pour le mois de ${mois.charAt(0).toUpperCase() + mois.slice(1)}</h2>`;
                    html += `<table class="table table-bordered mt-4">
                                <thead>
                                    <tr>
                                        <th>Projet et Utilisateur</th>
                                        <th>Temps (en secondes)</th>
                                    </tr>
                                </thead>
                                <tbody>`;
                    data.forEach(resultat => {
                        html += `<tr>
                                    <td>${resultat['Projet et Utilisateur']}</td>
                                    <td>${resultat['Temps']}</td>
                                </tr>`;
                    });
                    html += `</tbody></table>`;
                    container.innerHTML = html;
                } else {
                    container.innerHTML = '<p>Aucun résultat trouvé pour le mois sélectionné.</p>';
                }
            })
            .catch(error => {
                console.error('Erreur:', error);
            });
    } else {
        document.getElementById('resultatsContainer').innerHTML = ''; // Clear results if no month is selected
    }
}
    // Écoutez les changements de sélection
    document.getElementById('moisSelect').addEventListener('change', function() {
        const selectedMonth = this.value;
        fetchResults(selectedMonth);
    });
});
