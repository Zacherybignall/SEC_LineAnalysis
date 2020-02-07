const express = require('express');
const router = express.Router();
const members = require('../../Members');

// Gets All members
router.get('/', (req, res) => res.json(members));

// Get a single member
router.get('/:id', (req, res) => {

    const found = members.some(member => member.id === parseInt(req.params.id));

    if (found){
        res.json(members.filter(member => member.id === parseInt(req.params.id)));
    }
    else{
        res.status(400).json({ msg: `No member with the id of ${req.params.id}` });
    }
});

//create member

router.post('/', (req, res) => {
    const newMember = {
        id: 7,
        name: req.body.name,
        email: req.body.email,
        status: 'active'
    }
    
    if (!newMember.name || !newMember.email){
        return res.status(400).json({msg: 'Please send valid name and email'});
    }
    members.push(newMember);
    res.json(members);
});


    
module.exports = router;