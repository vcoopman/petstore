const style = {
	backgroundColor: 'yellow',
	border: '1px solid black',
	height: '10vh',
	width: '80vw',
	'margin-left': '10vw',
	display: 'inline-block'
}

function ItemCard(props) {
	return(
		<div style={style}>
			
			<img 
				src={'https://upload.wikimedia.org/wikipedia/commons/0/04/Labrador_Retriever_%281210559%29.jpg'}
				alt='labrador'
				style={{height: '10vh'}}
			/>
			<div style={{}}>
				<h1> {props.pet.pet_species} </h1>
				<h3> family: {props.pet.pet_breed} </h3>
				<h3> amount: {props.pet.pet_amount} </h3>
			</div>

		</div>
	);
}

export default ItemCard;
