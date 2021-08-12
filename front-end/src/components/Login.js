const style = {
	'text-align': 'center'
}

function Login(){
	return(
		<div style={style}>
			<h1 > Login </h1>
			<div style={{height: '2vh'}}/>

			<h3> Insert your Email </h3>
			<input type='text'/>
			<div style={{height: '2vh'}}/>
			<a href='/home'>
				<button> Log in </button>
			</a>
		</div>
	);
}

export default Login;
