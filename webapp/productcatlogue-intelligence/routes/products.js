var express = require('express');
var router = express.Router();
var mongoose = require('mongoose');
var sha1 = require('sha1');
var User = mongoose.model('User');
var Mobile = mongoose.model('Mobile');



module.exports = router;