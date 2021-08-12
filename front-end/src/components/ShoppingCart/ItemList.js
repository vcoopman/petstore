import React, { useState, useEffect } from 'react';

import ItemCard from './ItemCard.js';

const axios = require('axios').default;
const read_sc_url = 'http://petstorecart.appspot.com/list/pets/in/123123123'

// dev data
const pets = [{
		pet_amount: 3,
		pet_breed: 'dog',
		pet_species: 'labrador'
	}]

function ItemList(){
	// const [pets, setPets] = useState([]);

	// NO PUEDE SER IMPLEMENTADO DEBIDO A FALTA DE CORS EN SERVICIO!
	// useEffect( () => {
	// 	axios.get(read_sc_url).then( res => {
	// 		setPets(res.data)
	// 	})
	// })

	return(
		<div>
		{pets.map( (pet) => <ItemCard pet={pet} /> )}
		</div>
	);
}

export default ItemList;
