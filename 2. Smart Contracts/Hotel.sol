// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.8.2 <0.9.0;

contract HotelRoom {
    /*
        * Ether payments
        * Modifiers
        * Visibility
        * Events
        * Enums
    */
    address payable public owner;
    enum status { vacant, occupied }
    status public cur;
    /*Event declaration, can be used to generate logs each time it is trigerred and give notification to the user*/
    event Occupy(address occupant, uint val);
    constructor () {
        /* 
            * msg is a global variable which allows access to the blockchain
            * msg.sender represents the address of the function caller(current user), 
              in our case it represents the adress of the contract owner            
        */    
        owner = payable(msg.sender);
        cur = status.vacant;
    }
    // Check status
    /* 
        Modifier to check if current status is vacant(2nd argument is displayed if required condition is
        not statisfied)
    */
    modifier onlyWhenVacant {
        require(cur == status.vacant, "Occupied");
        _; /* symbolizes where to insert in the function in which it is called(since '_' represents the function, 
        onlyWhenVacant is called at the start of function execution*/
    }
    // Check price
    modifier enoughAmount(uint _amount) {
        require(msg.value >= _amount, "Not enough Ether provided");
        _;
    }
    /* To allow a user to book a vacant room(by paying the necessary amount) */
    function book() public payable onlyWhenVacant enoughAmount(2 ether) {
        /* We want to transfer the ETH value provided by the user for this transaction to the owner */
        // transfer has  a limitation wherein the gas cost is fixed upto 2300, this can lead to breaks and hence should be avoided
        //owner.transfer(msg.value);
        
        /* We can use call instead of transfer */
        // syntax details: https://stackoverflow.com/questions/76293163/can-someone-explain-the-syntax-of-this-line-of-solidity-code 
        // Call returns the status of the transaction and calldata(which is not being used in our case hence can ommit)
        // Empty string is passed since we do not want to call this for some other smart contract
        (bool sent,) = owner.call{value: msg.value}("");
        require(sent);
        cur = status.occupied;
        // event trigerred(logs for who booked the room and the value provided by the user)
        emit Occupy(msg.sender, msg.value);
    }

}   
