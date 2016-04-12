var express = require('express');
var router = express.Router();
var mongoose = require('mongoose');
var Mobile = mongoose.model('Mobile');

/*get vendor list*/
router.get('/all', function(req, res, next) {
	Mobile.aggregate([
        {
            $group: {
                _id: '$vendor',  //$region is the column name in collection
                count: {$sum: 1}
            }
        }
    ], function (err, results) {
        if (err) {
            next(err);
        } else {
        	var bundle = []	
        	for(r of results){
        		(function(result){
        			bundle.push([result._id, result.count]);	
        		})(r);        		
        	}
            res.render("vendor_all",{bundle:bundle});
        }
    });
});

router.get('/all/:search', function(req, res, next) {
    var search  = req.params.search
    Mobile.find({vendor: search}, function(err,data){
        res.render("vendor_mobiles", {mobiles : data, vendor: search});
    })

});

/*get vendors vs no. of phones*/
router.get('/', function(req, res, next) {
	res.render("vendors");
});

/*get stats*/
router.get('/stats', function(req, res, next) {
	Mobile.aggregate([
        {
            $group: {
                _id: '$vendor',  //$region is the column name in collection
                count: {$sum: 1}
            }
        }
    ], function (err, results) {
        if (err) {
            next(err);
        } else {
        	var bundle = [["Person","Number of products"]]	
        	for(r of results){
        		(function(result){
                    bundle.push([result._id, result.count]);    
        			//bundle.push({'x' : result._id, 'y' : result.count});	
        		})(r);        		
        	}
            res.json(bundle);
        }
    });	
});

module.exports = router;