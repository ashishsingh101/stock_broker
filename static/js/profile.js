window.onload = mainFunction;
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

function mainFunction() {
    getData();

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
            updateDetails(response['details']);
        },
    });
}

function updateDetails(details) {
    console.log(details);
    document.getElementById('name').innerHTML = details['name'];
    document.getElementById('email').innerHTML = details['email'];
    document.getElementById('phone').innerHTML = details['phone'];
    document.getElementById('gender').innerHTML = details['gender'];
    document.getElementById('dob').innerHTML = details['dob'];
    document.getElementById('uuid').innerHTML = details['uuid'];
    document.getElementById('wallet_money').innerHTML = details['wallet'];
}

function makechart(holdings) {
    const dataDoughnut = {
        labels: holdings.names,
        datasets: [
            {
                label: "My First Dataset",
                data: holdings.quantity,
                backgroundColor: [
                    '#003f5c',
                    '#2f4b7c',
                    '#665191',
                    '#a05195',
                    '#d45087',
                    '#f95d6a',
                    '#ff7c43',
                    '#ffa600',
                    '#004c6d',
                    '#006083',
                    '#007599',
                    '#008bad',
                    '#00a1c1',
                    '#00b8d3',
                    '#00cfe3',
                    '#00e7f2',
                    '#00ffff',
                    '#488f31',
                    '#6a9e3c',
                    '#8aac49',
                    '#a8bb59',
                    '#c6c96a',
                    '#e3d87d',
                    '#ffe792',
                    '#fccd7a',
                    '#f8b267',
                    '#f2975a',
                    '#eb7a52',
                    '#e15d50',
                    '#de425b',
                ],
                hoverOffset: 4,
                borderWidth: 0,
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