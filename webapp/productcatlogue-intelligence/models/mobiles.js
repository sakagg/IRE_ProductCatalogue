var mongoose = require("mongoose");

// Declare schema

var mobileSchema = new mongoose.Schema({
    name: {type: String, required: true},
    url: {type: String, required: true},
    vendor: {type: String},
    price: {type: Array},
    image: {type: String},
    description:{type:String},
    specs : {type:String},
    updated_on: {type: Array},
    created_on: {type: Date, default: Date.now}
});

// Export schema

module.exports = mongoose.model("Mobile", mobileSchema);
