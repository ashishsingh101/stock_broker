//var csrftoken = document.cookie.get('csrftoken')
window.onload = default_function();
window.stock_data = '';

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

function default_function() {
	document.getElementById('container').style.visibility = 'hidden';
	getData();
}

async function getData(){

	$.ajax({
		url : "",
		type : "POST",
		headers: { "X-CSRFToken": getCookie('csrftoken') },
		data : {
			'action' : 'chart_data',

		},
	
		// If sucess, download file
		success: function(response) {
			  //console.log(response['one_month_data']);
			  makechart(response['one_month_data'], response['stock']);
			  window.stock_data = response['stock'];
			  buy_shares();
			  update_data();
		},
		complete: function (data) {
			// Hide image container
			document.getElementById('loading').style.visibility = 'hidden';
			document.getElementById('container').style.visibility = 'visible';
		},
	});
}

function makechart(data, stock) {
	//console.log(data);
	var options = {
		series: [{

		//anoter data format [
		//	[1538856000000, 6593.34, 6600, 6582.63, 6600], 
		//	[1538856900000, 6595.16, 6604.76, 6590.73, 6593.86]
		//  ] date, open, high, low, close

		data: data
		}],
		chart: {
		type: 'candlestick',
		height: 400
	  	},
	  title: {
		text: stock['companyName'],
		align: 'left',
		style : {
			fontSize : '25px',
			color : '#ffffff',
		},
	  },
	  subtitle: {
		text: '₹'+stock['lastPrice'],
		align: 'left',
		style : {
			fontSize : '30px',
			color : '#ffffff',
			fontWeight : 'bold',
		},
	  },
	  xaxis: {
		type: 'datetime',
		labels:{
			show : false,
		}
	  },
	  yaxis: {
		tooltip: {
		  enabled: true
		},
		labels:{
			show : false,
		},
	  },
	  grid: {
		show: false
	  },
	  };

	  var chart = new ApexCharts(document.querySelector("#chart"), options);
	  chart.render();
	
	
}

function buy_shares(){
	var buy_button = document.getElementById('buy');
	var sell_button = document.getElementById('sell');
	buy_button.style.backgroundColor = '#0abb92';
	sell_button.style.backgroundColor = 'rgb(23, 24, 26)';
	console.log(window.stock_data);

	var submit_button = document.getElementsByClassName('submit_button')[0];
	var price_input = document.getElementsByClassName('share_input')[1];
	submit_button.innerHTML = 'Buy';
	price_input.value = window.stock_data['lastPrice'];

	/*
	var buy_sell_form = document.getElementById('buy_sell_form');
	// Create a form dynamically
	buy_sell_form.innerHTML = '';
    var form = document.createElement("form");
    form.setAttribute("method", "post");
    form.setAttribute("action", "submit");
 
    // Create an input element number of share
    var shares = document.createElement("input");
    shares.setAttribute("type", 'number');
    shares.setAttribute("name", "shares");
    shares.setAttribute("placeholder", "shares");

	var s = document.createElement("input");
    s.setAttribute("type", "submit");
    s.setAttribute("value", "Buy");

	form.appendChild(shares);
	form.appendChild(s);
	buy_sell_form.appendChild(form);
	*/
}

function sell_shares(){
	var sell_button = document.getElementById('sell');
	var buy_button = document.getElementById('buy');
	sell_button.style.backgroundColor = '#0abb92';
	buy_button.style.backgroundColor = 'rgb(23, 24, 26)';

	var submit_button = document.getElementsByClassName('submit_button')[0]
	var price_input = document.getElementsByClassName('share_input')[1];
	submit_button.innerHTML = 'Sell'
	price_input.value = window.stock_data['lastPrice'];
	
	/*
	var buy_sell_form = document.getElementById('buy_sell_form');
	// Create a form dynamically
	buy_sell_form.innerHTML = '';
    var form = document.createElement("form");
    form.setAttribute("method", "post");
    form.setAttribute("action", "submit");
 
    // Create an input element number of share
    var shares = document.createElement("input");
    shares.setAttribute("type", 'number');
    shares.setAttribute("name", "shares");
    shares.setAttribute("placeholder", "shares");

	var s = document.createElement("input");
    s.setAttribute("type", "submit");
    s.setAttribute("value", "Sell");

	form.appendChild(shares);
	form.appendChild(s);
	buy_sell_form.appendChild(form);
	*/
}

function buy_sell() {
	var submit = document.getElementsByClassName('submit_button')[0];
	var price_input = document.getElementsByClassName('share_input')[1];
	var shares = document.getElementsByClassName('share_input')[0];
	var stock = window.stock_data;
	var action = submit.innerHTML;
	var price = price_input.value;
	var quantity = shares.value;
	var data = {
		'action' : action,
		'stock' : stock['symbol'],
		'price' : price,
		'quantity' : quantity,
	}
	$.ajax({
		url : "",
		type : "POST",
		headers: { "X-CSRFToken": getCookie('csrftoken') },
		data : data,
	
		// If sucess, download file
		success: function(response) {
			  console.log(response);
			  if(response['status'] == 'success'){
			  	alert('Transaction successful');
			  }
			  else if(response['status'] == 'noshare'){
				alert('Enter valid shares to buy');
			  }
			  else if(response['status'] == 'not_inuf_share'){
				alert('You do not have enough shares to sell');
			  }
			  else if(response['status'] == 'notenough_money'){
				alert('You do not have enough money to buy');
			  }
			  else{
			  	alert('Transaction failed');
			  }
		},
	});
}

function update_data() {
	var stock = window.stock_data;

	var year_low = document.getElementById('year_low');
	year_low.innerHTML = '₹'+stock['low52'];
	var year_high = document.getElementById('year_high');
	year_high.innerHTML = '₹'+stock['high52'];
	var year_high_low = document.getElementById('year_high_low');
	year_high_low.min = stock['low52'];
	year_high_low.max = stock['high52'];
	year_high_low.value = stock['lastPrice'];

	var day_low = document.getElementById('day_low');
	day_low.innerHTML = '₹'+stock['dayLow'];
	var day_high = document.getElementById('day_high');
	day_high.innerHTML = '₹'+stock['dayHigh'];
	var day_high_low = document.getElementById('day_high_low');
	day_high_low.min = stock['dayLow'];
	day_high_low.max = stock['dayHigh'];
	day_high_low.value = stock['lastPrice'];
	
}