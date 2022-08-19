var register = function(Handlebars) {
  var helpers = {
    isOwner: function(value, options) {
      return value == 'owner';
    },
    isAdmin: function(value, options) {
      return value == 'administrator';
    }
  };

  if (Handlebars && typeof Handlebars.registerHelper === "function") {
    for (var prop in helpers) {
      Handlebars.registerHelper(prop, helpers[prop]);
    }
  } else {
    return helpers;
  }
};

module.exports.register = register;
module.exports.helpers = register(null);