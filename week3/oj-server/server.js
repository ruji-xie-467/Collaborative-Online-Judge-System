const express = require('express');
const app = express();
var restRouter = require('./routes/rest');
var indexRouter = require('./routes/index');
var mongoose = require("mongoose");
var path = require("path");
var http = require('http');

var socket_io = require('socket.io');
var io = socket_io();
var socketService = require('./services/SocketService.js')(io);
mongoose.connect("mongodb+srv://user:user@coj-1ellf.mongodb.net/test?retryWrites=true");

app.use(express.static(path.join(__dirname, '../public')));

app.use('/api/v1', restRouter);
app.use('/', indexRouter);
app.use(function(req, res) {
  res.sendFile("index.html", { root: path.join(__dirname, '../public') });
});

// app.listen(port, () => console.log(`Example app listening on port ${port}!`));

var server = http.createServer(app);
io.attach(server);
server.listen(3000);
server.on('error', onError);
server.on('listening', onListening);

function onError(error) {
  throw error;
}

function onListening() {
  var addr = server.address();
  var bind = typeof addr == 'string'
    ? 'pipe ' + addr 
    : 'port' + addr.port;
  console.log("Listening on " + bind);
}
