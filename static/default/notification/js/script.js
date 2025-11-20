const notifyButton = document.querySelector("#notifyButton");
const notifyBlock = document.querySelector("#notifyBlock");


notifyButton.addEventListener("click", () => {
	notifyBlock.classList.remove("active");
	localStorage.setItem("cookiesAccepted", true);
});

document.addEventListener("DOMContentLoaded", () => {
	if (localStorage.getItem("cookiesAccepted") !== "true") {
		notifyBlock.classList.add("active");
	};
});