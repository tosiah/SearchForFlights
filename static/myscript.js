document.addEventListener('DOMContentLoaded', function(){
    initSubmitHandler();
});

function initSubmitHandler(){
    document.querySelector('#form').onsubmit = function(){
        const request = new XMLHttpRequest();
        const flight = document.querySelector('#flight_id').value;
        request.open('GET', `/api/flights/${flight}`);
        request.onload = () =>{
            const data = JSON.parse(request.responseText);
            document.querySelector('#flightDetails').innerHTML='';
            if(data.success){
                const contents = `Details of flight number ${flight}:`;
                document.querySelector('#result').innerHTML = contents;
                for(let key in data){
                    if(key==='success'){
                        continue;
                    }
                    if(Array.isArray(data[key])){
                        console.log(data[key].length);
                        if(data[key].length==0){
                            const listElement = document.createElement('li')
                            listElement.innerHTML = 'No passengers';
                            document.querySelector('#flightDetails').append(listElement);
                        }
                        else{
                        const listElement = document.createElement('li')
                        const flightDetail = document.createElement('ul');
                        listElement.innerHTML = key;
                        listElement.append(flightDetail);
                        document.querySelector('#flightDetails').append(listElement);
                        
                        for (let index in data[key]){
                            const propertyDetail = document.createElement('li');
                            propertyDetail.innerHTML = data[key][index];
                            flightDetail.append(propertyDetail);
                            continue;
                        }
                        }
                    }
                    else{
                        const flightDetail = document.createElement('li');
                        flightDetail.innerHTML = data[key];
                        document.querySelector('#flightDetails').append(flightDetail);
                    }
                }
            }
            
            else {
                document.querySelector('#result').innerHTML = 'There was an error.';
            }
        }
        
        const data = new FormData();
        data.append('flight_id', flight);
        
        request.send(data);
        return false;
    };
}