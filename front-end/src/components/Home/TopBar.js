import SearchBar from './SearchBar.js';

const style = {
	backgroundColor: 'grey',
	height: '50px',
	display: 'flex'
}

const title_style = {
	margin: '1vh',
	'font-size': 'medium'

}

function TopBar(){
	return(
		<div>
			<div style={style}>
				<a href='./home'style={title_style}> PET STORE </a>
				<SearchBar />
				<a href='./shopping-cart' style={{'margin-left': '10px', 'margin-top': '1vh' }}> Shopping Cart </a>
				<a href='./login' style={{'margin-left': '10px', 'margin-top': '1vh' }}> Log In </a>
			</div>
		</div>
	);	
}

export default TopBar;
