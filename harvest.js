// Script to be used on https://medium.com/bb-tutorials-and-thoughts/250-practice-questions-for-the-dca-exam-84f3b9e8f5ce
let firstId = "c37e"
let ptr = document.getElementById(firstId)
let lastId = "7ae0"

let questions = {}
let count = 0

while (true) {
    count++;

    questions[count] = {
        "question": ptr.innerText,
        "answer": ptr.nextElementSibling.innerText,
    }

    ptr = ptr.nextElementSibling.nextElementSibling;
    if (ptr.id == lastId) {
        break;
    }
}
