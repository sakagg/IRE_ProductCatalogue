var express = require('express');
var router = express.Router();
var mongoose = require('mongoose');
var sha1 = require('sha1');
var User = mongoose.model('User');
var Mobile = mongoose.model('Mobile');
var fs = require('fs');
var filepath = "/Users/adityagaykar/Dropbox/Development/MtechCSE/Sem2/IRE/MajorProject/src/infibeam_dump_copy";
var sys = require('sys');
var exec = require('child_process').exec;


/*Load mobiles*/
router.post('/load', function(req, res, next) {
	var filepath1 = req.body.loc;
	fs.readFile(filepath1, 'utf8', function (err,data) {
	  var error = false;
	  if (err || !data ) {
	    error = true;
	  }

	  try{
	  		var mobiles = data.split("*@*");
		  for(var m of mobiles){
		  	var name = m.split("#@#")[0];
		  	//console.log(name);
		  	if(!name)
			  		continue;
		  	(function(mobile){
		  		var data = mobile.split("#@#");
			  	var name = data[0],
			  	price = data[1],
			  	vendor = data[2],
			  	image = data[3],
			  	description = data[4],
			  	specs = data[5];
			  	//console.log(name+ " : "+ price +" : "+vendor);

			  	Mobile.findOne({
			  		name: name,
			  		vendor: vendor
			  	},function(err,mobile){
			  		if(!mobile){

			  			//console.log("inserting : "+name);
		  				Mobile.create({
					  		name: name,
					  		price: [price],
					  		vendor: vendor,
					  		image: image,
					  		description: description,
					  		specs: specs,
					  		updated_on: [Date.now()]
					  	},function(err,mobile){
					  		if(err)
					  			console.log(err);
					  		else
					  			console.log("Mobile entered : "+mobile.name);
					  	});
		  			} else {
		  				mobile.price.push(price);
		  				mobile.updated_on.push(Date.now());
			  			Mobile.update({_id: mobile._id},{
			  				name: name,
					  		price: mobile.price,
					  		vendor: mobile.vendor,
					  		image: image,
					  		description: description,
					  		specs: specs,
					  		updated_on: mobile.updated_on
				  		},function(err,mobile){
				  			if(err)
					  			console.log(err);
					  		else
					  			console.log("Mobile updated : "+mobile.name);
				  		});
		  			}
			  	});
		  	})(m);



		  }
	  } catch(e){
	  	 error = true;

	  }
	  if(error)
	  	res.send("error");
	  else
		res.send("success");
	  });

});

/*GET mobile view*/
router.get('/:id', function(req, res, next) {
	var id = req.params.id;
	var user = req.session.user;
	Mobile.findOne({_id : id}, function(err,data){
		if(data){
			Mobile.find({name: data.name},function(err,mobiles){
				var other_vendors = [];
				for (m of mobiles){
					other_vendors.push(["/mobiles/"+m._id,m.price.pop(), m.vendor]);
				}
				var specs = data.specs.split("#~#");
				var spec_arr = [];
				//console.log(specs);
				for(spec of specs){
					var spec2 = spec.split("*%*");
					(function(s){
						spec_arr.push(s);
					})(spec2);
				}
				//console.log(spec_arr);
				res.render("show_mobile",{id: id, mobile: data, user: user, specs_data: spec_arr, other_vendors : other_vendors});
			});
		}
	});
});

router.get('/refresh/:id', function(req, res, next) {
	var id = req.params.id;
	function puts(error, stdout, stderr) {res.send(stderr);}
	exec("unset http_proxy; python ../../scraping/infibeam_scraper.py update " + id, puts);
});

/*GET stats*/
router.get('/stats/:id', function(req, res, next) {
	var id = req.params.id;
	Mobile.findOne({_id : id},function(err,data){
		var price = data.price;
		var updated_on = data.updated_on;
		var len = price.length;
		var bundle = []
		for(var i = 0; i < len; i++){
			price[i] = price[i].replace(',',"");
			var date = new Date(updated_on[i]);

			bundle.push({'x' : date.getDate()+"/"+(date.getMonth()+1)+"/"+(date.getYear()+1900)+" "+date.getHours()+":"+date.getMinutes()+":"+date.getSeconds(),'y': price[i]});
		}
		res.send(JSON.stringify(bundle));
	});
});

/* GET mobiles. */
router.get('/get/:search/:opt', function(req, res, next) {
	var search = req.params.search;//.toLowerCase();
	var opt = req.params.opt.toLowerCase();
	switch(opt){
		case 'name':
			Mobile.find({name: new RegExp(search, "i")},function(err, data){
				res.render("mobiles",{mobiles: data});
			});
		break;
		case 'specs':
			Mobile.find({specs: new RegExp(search, "i")},function(err, data){
				res.render("mobiles",{mobiles: data});
			});
		break;
		case 'vendor':
			Mobile.find({vendor: new RegExp(search, "i")},function(err, data){
				res.render("mobiles",{mobiles: data});
			});
		break;
		default:
			Mobile.find({},function(err, data){
				res.render("mobiles",{mobiles: data});
			});
		break;
	}
});




module.exports = router;

// /* Registration form */
// router.get('/register', function(req, res, next) {
// 	var user = req.session.user;
// 	if(user)
// 		res.redirect("/home");
// 	var errorMessage = req.session.error;
// 	res.render('setup', { errorMessage : errorMessage});
// });


// POST:Register form
// router.post('/register',function(req,res, next){
// 	var name = req.body.username;
// 	var password = sha1(req.body.password);

// 	User.create({
// 		name: name,
// 		password: password
// 	},function(err,user){
// 		if(err)
// 			throw err;
// 		res.redirect("/");
// 	});

// });
