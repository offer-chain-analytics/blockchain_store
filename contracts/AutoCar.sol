pragma solidity >=0.4.25 <0.7.0;
pragma experimental ABIEncoderV2;

contract AutoCar {
    enum UserRoles {
        ADMIN,
        MNUFACTURING, //автопроизводитель
        SERVICE //диллер; автосервис
    }

    enum StuffCategory {
        CHANGE,
        CHANGE_OLD,
        VISIT,
        OTHER
    }

    struct User {
        address addr;
        UserRoles role;
        string name;
    }

    struct Stuff {
        address addr; //autoservice
        string location;
        string vincode;
        StuffCategory category;
        string description;
        string datetime;
    }

    mapping(address => User) public users;
    mapping(string => Stuff[]) public stuffs; //vincode => stuff

    constructor() public {
        users[msg.sender] = User(msg.sender, UserRoles.ADMIN, "admin");
    }

    function registerUser(
        address _addr,
        UserRoles _role,
        string memory _name
    ) public {
        if (_role == UserRoles.MNUFACTURING) {
            require(users[msg.sender].role != UserRoles.ADMIN, "No access rights to add car manufacturings"); //if add not admin services
        }

        users[_addr] = User(_addr, _role, _name);
    }

    function addStuff(
        string memory _location,
        string memory _vincode,
        StuffCategory _category,
        string memory _description,
        string memory _date
    ) public {
        require(users[msg.sender].role == UserRoles.SERVICE, "No access rights to add stuff");
        require (keccak256(abi.encodePacked(_vincode)) != keccak256(abi.encodePacked('')));

        stuffs[_vincode].push(Stuff(
            msg.sender,
            _location,
            _vincode,
            _category,
            _description,
            _date
        ));
    }

    function getAllStuffsInfo(string memory _vincode) public view returns (Stuff[] memory) {
        return stuffs[_vincode];
    }

    function getStuffInfo(string memory _vincode, uint index) public view returns (Stuff memory) {
        require(stuffs[_vincode].length > index, "Data is not valid");

        return stuffs[_vincode][index];
    }
}
