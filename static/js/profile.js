window.onload = getData();
window.data = '';

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getData() {

    $.ajax({
        url: "",
        type: "POST",
        headers: { "X-CSRFToken": getCookie('csrftoken') },
        data: {
            'action': 'profile_data',

        },

        // If success
        success: function (response) {
            //console.log(response['one_month_data']);
            makechart(response['holdings']);
        },
    });
}

function makechart(holdings) {
    const dataDoughnut = {
        labels: holdings.names,
        datasets: [
            {
                label: "My First Dataset",
                data: holdings.quantity,
                backgroundColor: [
                    "rgb(133, 105, 241)",
                    "rgb(164, 101, 241)",
                    "rgb(101, 143, 241)",
                ],
                hoverOffset: 4,
            },
        ],
    };

    const configDoughnut = {
        type: "doughnut",
        data: dataDoughnut,
        options: {},
    };

    var chartBar = new Chart(
        document.getElementById("chartDoughnut"),
        configDoughnut
    );

}