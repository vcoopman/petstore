import DescriptionBox from './DescriptionBox.js';

const default_alt = "pet";

const style = {
	backgroundColor: 'red',
	margin: '0 auto',
	height: '30vh',
	width: '70vw',
	border: '1px solid black',
	'margin-top': '1vh'
}

const img_style = {
	'height': '100%',
	'width': '40%',
	float: 'left'
}


function PetCard(props){
	return(
		<div style={style}>
			<img src={props.image_url} style={img_style} alt={default_alt}/>
			<DescriptionBox />
		</div>
	);
}

export default PetCard;
