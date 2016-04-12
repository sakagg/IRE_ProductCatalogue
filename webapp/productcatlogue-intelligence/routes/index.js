var express = require('express');
var router = express.Router();
var mongoose = require('mongoose');
var Mobile = mongoose.model('Mobile');

/* GET login page. */
router.get('/', function(req, res, next) {
	res.redirect("/home");	
});

/*GET:Home page*/

router.get('/home',function(req,res,next){	
	Mobile.find({},function(err, mobiles){
		res.render("home",{ mobiles : mobiles});					
	});				
});


module.exports = router;
