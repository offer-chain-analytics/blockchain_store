const AutoCars = artifacts.require("AutoCar");

module.exports = function(deployer) {
  deployer.deploy(AutoCars);
};
