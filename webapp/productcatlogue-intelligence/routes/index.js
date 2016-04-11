var express = require('express');
var router = express.Router();
var mongoose = require('mongoose');
var sha1 = require('sha1');
var User = mongoose.model('User');
var Mobile = mongoose.model('Mobile');

/* GET login page. */
router.get('/', function(req, res, next) {
	res.redirect("/home");	
});

/* Registration form */
router.get('/register', function(req, res, next) {
	var user = req.session.user;
	if(user)
		res.redirect("/home");
	var errorMessage = req.session.error;
	res.render('setup', { errorMessage : errorMessage});
});


/*POST:Register form*/
router.post('/register',function(req,res, next){
	var name = req.body.username;
	var password = sha1(req.body.password);

	User.create({
		name: name,
		password: password
	},function(err,user){
		if(err)
			throw err;
		res.redirect("/");
	});

});
/*GET:Home page*/

router.get('/home',function(req,res,next){	
	Mobile.find({},function(err, mobiles){
		res.render("home",{ mobiles : mobiles});					
	});				
});

/*  */
router.get('/login', function(req, res, next) {
	res.redirect("/home");
});

/* POST: login */

router.post('/login',function(req,res, next){
	var name = req.body.username;
	var password = sha1(req.body.password);
	console.log(name);
	console.log(password);
	User.findOne({name:name, password:password},function(err,user){
		if (err)
			throw err;
		if (user){
			req.session.user = user;
			res.redirect("/home");
		} else {
			req.session.error = "Invalid Username";
			res.redirect("/");
		}
	});

});

/*GET: logout */

router.get("/logout",function(req,res,next){
	var user = req.session.user;
	if(user)
		delete req.session.user;
	if(req.session.error)
		delete req.session.error;
	res.redirect("/");
});

module.exports = router;
