var mongoose = require("mongoose");

// Declare schema
var userSchema = new mongoose.Schema({
    name: {type: String, required: true, index: {unique: true}},
    password: {type: String, required: true},
    created_on: {type: Date, default: Date.now}
});

// Export schema

module.exports = mongoose.model("User", userSchema);