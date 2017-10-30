var express = require('express');
var app = express();
var request = require('request-promise');
var BodyParser = require('body-parser');

var Gpio = require('onoff').Gpio;
var Button = new Gpio(17, 'in', 'both');

// POST the state of the button(pressed or not)
var mydata = {
    time: new Date(),
    ispressed: ispressed
}

var options = {
    uri:"http://13.59.174.162:7579/ispressed",
    method: "POST",
    form: mydata
}

mydata.ispressed = 0; // 0 - not pressed, 1 - pressed

function ispressed(err, state) {

    if(state == 1 && mydata.time != (new Date())) { // when pressed

        mydata.ispressed = 1;

        var options = {
            uri:"http://13.59.174.162:7579/ispressed",
            method: "POST",
            form: mydata
        }

        mydata.time = new Date();
        
        request(options, function(err, res, body) {
            if(err) {
                console.log("error : " + err);
            }

            // console.log(body);
        });

        console.log('pressed at ' + (new Date()));

        mydata.ispressed = 0;
    } else {
        console.log('running... ispressed : ' + mydata.ispressed);
    }
}

setInterval(function() {
    Button.watch(ispressed);
}, 6000);


// setInterval(function(){
//   ispressed
// }, 3000);
