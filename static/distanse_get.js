
function get_distance(){
        

        fetch("/distance/get")
        .then(response=> response.text())
        .then(data=> {
            console.log(data)
            if(data < '10'  ){
                postMessage('car is exist');
                get_distance()
            }
            else{
                console.log(data)
                postMessage('car is notexist');
                get_distance()
            }

        });
}

get_distance()