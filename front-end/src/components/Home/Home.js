import { useState } from 'react';
import TopBar from './TopBar.js';
import FilterBar from './FilterBar.js';

import PetCard from './PetCard.js';

const style = {
	backgroundColor: 'green',
	height: '100%',
}

const url_images = [
	'https://www.iucn.org/sites/dev/files/content/images/2020/ranita_de_darwin_del_sur_rhinoderma_darwinii_credito_claudio_azat.jpg',
	'https://upload.wikimedia.org/wikipedia/commons/0/04/Labrador_Retriever_%281210559%29.jpg',
	'https://vetstreet.brightspotcdn.com/dims4/default/7cc218c/2147483647/thumbnail/645x380/quality/90/?url=https%3A%2F%2Fvetstreet-brightspot.s3.amazonaws.com%2Fa5%2F69%2Fe639b7ab40c2a290e3296de726d8%2FPersian-AP-PIFN6J-645sm3614.jpg',
	'https://3dwarehouse.sketchup.com/warehouse/v1.0/publiccontent/2ff17d50-a5da-484c-8f81-41a7f7941544'						
]

function Home() {
	// const [input, setInput] = useState('');

	return(
		<div style={style}>
			<TopBar />
			{/*<FilterBar />*/}
			<PetCard image_url={url_images[0]}/>
			<PetCard image_url={url_images[1]}/>
			<PetCard image_url={url_images[2]}/>
			<PetCard image_url={url_images[3]}/>
		</div>	
	);	
}

export default Home;
