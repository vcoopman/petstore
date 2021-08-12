const style = {
	backgroundColor: 'yellow',
	width: '60%',
	height: '100%',
	float: 'left',
	'text-align': 'center'

}

function DescriptionBox(){
	return(
		<div style={style}>
			<p>
			    Lorem ipsum odor amet, consectetuer adipiscing elit. Ac purus in massa egestas mollis varius;
			    dignissim elementum. Mollis tincidunt mattis hendrerit dolor eros enim, nisi ligula ornare.
			    Hendrerit parturient habitant pharetra rutrum gravida porttitor eros feugiat. Mollis elit
			    sodales taciti duis praesent id. Consequat urna vitae morbi nunc congue.
		  	</p>
		  	<button> Add to cart </button>
		</div>
	);
}

export default DescriptionBox;
