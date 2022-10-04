let timeoutID;
let timeout = 15000;

function setup() {
    getMessages()
	document.getElementById("theButton").addEventListener("click", makePost);
}



function makePost() {
	console.log("Sending POST request");
	const messages = document.getElementById("user_input").value
	const user = document.getElementById("so").value
	
fetch("/new_message/", {
			method: "post",
			headers: { "Content-type": "application/x-www-form-urlencoded; charset=UTF-8" },
			// body: `one=${one}&two=${two}&three=${three}`
            body: `username=${user}&message=${messages}`
		})
		.then((response) => {
			return response.json();
		})
		.then((result) => {
            let chat_window = document.getElementById("cw")
            let message = "";
            for(let i in result)
            {
                message+= result[i]+'\n'

            }
            chat_window.value = message
        })
		.catch(() => {
			console.log("Error posting new items!");
		});
        document.getElementById("user_input").value=""
}

function getMessages()
{
    fetch("/messages/") 
        .then((response) => 
        {
            return response.json(); 
        })
        .then((results) => 
        {
            let chat_window = document.getElementById("cw");
            let messages = "";
            for (let i in results) 
            {
                messages+=results[i]+'\n'
            }
            chat_window.value = messages; })
        .catch(() => 
        {
        document.getElementById("cw").value = "error retrieving messages from server";
        });

        timeoutID = window.setTimeout(getMessages, timeout);

}


window.addEventListener("load", setup);
