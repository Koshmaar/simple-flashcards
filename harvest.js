// Script to be used on https://medium.com/bb-tutorials-and-thoughts/250-practice-questions-for-the-dca-exam-84f3b9e8f5ce
let firstId = "1c43"
let lastId = "0a99"
let category = "storage"
let count = 228;

let node = document.getElementById(firstId)
let questions= {}

while (true) {
    questions[count] = {
        "question": node.innerText,
        "answer": node.nextElementSibling.innerText,
        "category": category
    }
    if (node.id == lastId) {
         break;
    }
    node = node.nextElementSibling.nextElementSibling;
    count++;

}

questions