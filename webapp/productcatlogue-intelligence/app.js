var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var session = require("express-session"),
MongoStore = require("connect-mongo")(session);




var app = express();


//connect to db
var mongoose = require("mongoose")
mongoose.connect("mongodb://localhost/iredb", function(err){
  if(err)
    throw err;  
    console.log("Connected to mongodb")
});

//wire-in the models

//user model
var mobileModel = require('./models/mobiles');

// We use mongodb to store session info
// expiration of the session is set to 7 days (ttl option)
app.use(session({
    store: new MongoStore({mongooseConnection: mongoose.connection,
                          ttl: 7*24*60*60}),
    saveUninitialized: true,
    resave: true,
    secret: "MyBigBigSecret"
}));

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));


//Routes
var routes = require('./routes/index');
var mobiles = require('./routes/mobiles');
var vendors = require('./routes/vendors');

app.use('/', routes);
app.use('/mobiles', mobiles);
app.use('/vendors', vendors);

//app.use('/users', users);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
  app.use(function(err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
      message: err.message,
      error: err
    });
  });
}

// production error handler
// no stacktraces leaked to user
app.use(function(err, req, res, next) {
  res.status(err.status || 500);
  res.render('error', {
    message: err.message,
    error: {}
  });
});


module.exports = app;
