
window.onload = refresh_function();

		function refresh_function() {
			fetchdata()
		}

		function fetchdata() {
			$.ajax({
				url : "{% url 'dashboard' %}",
				type : "POST",
				data : {
					'action' : 'dashboard_data',
					csrfmiddlewaretoken: '{{ csrf_token }}' ,

				},

				success : function(response){
					update_index(response['niftyPrice'], response['niftyBankPrice'],
					             response['niftyChange'], response['niftyPChange'],
								 response['niftyBankChange'], response['niftyBankPChange'] )
					//alert(response['niftyPrice']+' '+response['niftyBankPrice']);
					update_gainers(response['topGainers'], response['logos'])
					update_losers(response['topLosers'], response['logos'])
				    
				},
			});
		}

		function update_losers(topLosers, logos) {
			loser = document.getElementById('loser');
			loser.innerHTML = ''

			for(let i=0;i<topLosers.length;i++) {
				console.log(topLosers[i]);

				var div  = document.createElement('div');
				var symbol = topLosers[i]['symbol'];
				div.id = topLosers[i]['symbol'];
				div.className = 'loser_div';
				var p = document.createElement('p');
				p.innerText = topLosers[i]['symbol'];

				var imgdiv = document.createElement('div');
				imgdiv.className = 'img_div';

				var logo = document.createElement('img');
				logo.className = 'equity_logo';
				logo.src = 'https://assets-netstorage.groww.in/stock-assets/logos/'+logos[topLosers[i]['symbol']]+'.png';

				var price = document.createElement('p');
				price.innerHTML = '₹'+topLosers[i]['ltp'];

				var change = document.createElement('p');
				change.innerHTML = '<font color="#d55438">'+parseFloat(topLosers[i]['ltp']-topLosers[i]['previousPrice']).toFixed(2)+' ('+topLosers[i]['netPrice']+'%)'+'</font>';

				div.appendChild(p);
				//div.appendChild(logo);
				imgdiv.appendChild(logo);
				div.appendChild(imgdiv);
				div.appendChild(price);
				div.appendChild(change);
				loser.appendChild(div);
			}
		}

		function update_gainers(topGainers, logos) {
			gainer = document.getElementById('gainer');
			gainer.innerHTML=''

			for(let i=0;i<topGainers.length;i++) {
				console.log(topGainers[i]);

				var div  = document.createElement('div');
				div.id = topGainers[i]['symbol'];
				div.className = 'gainer_div';
				var name = document.createElement('p');
				name.innerText = topGainers[i]['symbol'];

				var imgdiv = document.createElement('div');
				imgdiv.className = 'img_div';

				var logo = document.createElement('img');
				logo.className = 'equity_logo';
				logo.src = 'https://assets-netstorage.groww.in/stock-assets/logos/'+logos[topGainers[i]['symbol']]+'.png';

                var price = document.createElement('p');
				price.innerHTML = '₹'+topGainers[i]['ltp'];
				
				var change = document.createElement('p');
				change.innerHTML = '<font color="#0abb92">'+parseFloat(topGainers[i]['ltp']-topGainers[i]['previousPrice']).toFixed(2)+' (+'+topGainers[i]['netPrice']+'%)'+'</font>';

				div.appendChild(name);
				//div.appendChild(logo);
				imgdiv.appendChild(logo);
				div.appendChild(imgdiv);
				div.appendChild(price);
				div.appendChild(change);
				gainer.appendChild(div);
			}
		}

		function update_index(niftyPrice, niftyBankPrice, niftyChange, niftyPChange, niftyBankChange, niftyBankPChange){
			nifty_price = document.getElementById('nifty_price');
			niftyBank_price = document.getElementById('niftyBank_price');
            
			if(niftyChange >=0){
				nifty_price.innerHTML = '<font color="">'+niftyPrice+'</font>'+'<font color="#0abb92">'+'  +'+niftyChange+'  +'+niftyPChange+'%'+'</font>';
			}
			else{
				nifty_price.innerHTML = niftyPrice+'</font>'+'<font color="#d55438">'+'  -'+niftyChange+'  -'+niftyPChange+'%'+'</font>';
			}

			if(niftyBankChange >=0){
				niftyBank_price.innerHTML = niftyBankPrice+'<font color="#0abb92">'+'  +'+niftyBankChange+'  +'+niftyBankPChange+'%'+'</font>';
			}
			else{
				niftyBank_price.innerHTML = niftyBankPrice+'<font color="#d55438">'+'  -'+niftyBankChange+'  -'+niftyBankPChange+'%'+'</font>';
			}
			
		}

		$(document).ready(function(){
			setInterval(fetchdata,60000);
		})