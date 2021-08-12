import TopBar from "../Home/TopBar.js";
import ItemList from "./ItemList.js";

import { useState } from "react";

const axios = require("axios").default;
const hash = require("object-hash");

const checkout_button_style = {
	margin: "5vw",
	"margin-bottom": "1vh",
	"margin-left": "10vw",
	height: "5vh",
	backgroundColor: "orange",
};

const waiting_button_style = {
	margin: "5vw",
	"margin-left": "10vw",
	"margin-bottom": "1vh",
	height: "5vh",
	backgroundColor: "#add8e6",
};

const text_style = {
	"margin-left": "10vw",
};

// dev data
const customer_id = "123123123";
const checkout_service_url = "http://52.86.66.73:5001/checkout";

function ShoppingCart() {
	const [done, setDone] = useState("");

	async function checkout() {
		// Send checkout request

		setDone("waiting");

		const transaction_id = hash(customer_id + Date.now());
		const payload = {
			transaction_id: transaction_id,
			customer_id: customer_id,
		};

		try {
			const response = await axios.post(checkout_service_url, payload);

			if ("error" in response.data) {
				setDone("fail");
				console.log(done);
			} else {
				setDone("success");
				console.log(done);
			}
		} catch {
			console.log("Error making checkout");
			setDone("fail");
			console.log(done);
		}
	}

	return (
		<div>
			<TopBar />
			<div style={{ height: "5vh" }} />
			{done !== "success" ? (
				<div>
					<ItemList />
					<h3 style={{ "margin-left": "10vw" }}>
						{" "}
						Total Price: $150.000{" "}
					</h3>
				</div>
			) : (
				<div />
			)}
			{done === "waiting" ? (
				<button style={waiting_button_style}> Loading... </button>
			) : (
				<button style={checkout_button_style} onClick={checkout}>
					{" "}
					Checkout!{" "}
				</button>
			)}
			{done === "success" ? (
				<p style={text_style}> Checkout Done! </p>
			) : (
				<div />
			)}
			{done === "fail" ? (
				<p style={text_style}> Checkout Failed! Please try again </p>
			) : (
				<div />
			)}
		</div>
	);
}

export default ShoppingCart;
