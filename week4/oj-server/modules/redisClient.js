var redis = require('redis');

// only one client created
var client = redis.createClient();

function set(key, value, callback) {
    client.set(key, value, function(err, res) {
        if(err) {
            console.log(err);
            return ;
        }
        callback(res);
    });
}

function get(key, callback) {
    client.get(key, function(err, res){
        if(err) {
            console.log(err);
            return ;
        }
        callback(res);
    });
}

// since redis is used as cache, data only valid for a period
function expire(key, timeInSeconds){
    client.expire(key, timeInSeconds);
}

function quit() {
    client.quit();
}

module.exports = {
    get: get,
    set: set,
    expire: expire,
    quit: quit,
    redisPrint: redis.print
};
