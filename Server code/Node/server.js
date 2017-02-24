//BELOW CODE IS TO FETCH DATA FROM MYSQL DATABASE.
var http = require('http');
var mysql = require('mysql'); // importing mysql modules
var url = require('url');
var connection = mysql.createConnection({
    host: 'technothon1.ceg3ohfqhx8p.ap-south-1.rds.amazonaws.com',
    user: 'technothon1',
    password: 'technothon123',
    database: 'technothon_park_mycar'
});

console.log('MySQL Connection details  '+connection);
http.createServer(function (request, response)
{
        var path = url.parse(request.url).pathname;
        console.log(path);
        if(path=="/hello"){ // for processing AJAX request
                connection.query('SELECT * from slot_table ', function(err, rows, fields)
                {
                        console.log('ajax part');
                        console.log("request recieved");
                        console.log('Connection result error '+err);
                        console.log('no of records is '+rows.length);
                        response.writeHead(200, {'Content-Type': 'text/html','Access-Control-Allow-Origin' : '*'});
                        var string=JSON.stringify(rows); // this line converts the data into json format
                        console.log(string);
                        response.end(string); // sending data to html
                        console.log("string sent");
                });
        }
        else {
        if(path=="/chart"){
                connection.query('SELECT * from transaction  ', function(err, rows, fields)
                {
                        console.log('ajax part2');
                        console.log("request recieved2");
                        console.log('Connection result error2 '+err);
                        console.log('no of records2 is '+rows.length);
                        response.writeHead(200, {'Content-Type': 'text/html','Access-Control-Allow-Origin' : '*'});
                        var string=JSON.stringify(rows); // this line converts the data into json format
                        console.log(string);
                        response.end(string); // sending data to html
                        console.log("string sent2");
                });

        }
        else{   // for testing only
                console.log('else part');
                connection.query('SELECT * from slot_table ', function(err, rows, fields)
                {
                        console.log('Connection result error '+err);
                        console.log('no of records is '+rows.length);
                        response.writeHead(200, { 'Content-Type': 'text/html','Access-Control-Allow-Origin' : '*'});
                        console.log(JSON.stringify(rows));
                        response.end(JSON.stringify(rows)); // this line converts the data into json format
                        //response.end(); // this line sends the json data to browser
                });
        }
} // end of global else
}).listen(8080);

