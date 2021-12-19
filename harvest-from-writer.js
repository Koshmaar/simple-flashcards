
// Script to be used on html documents converted from LibreOffice odt files
function foo() {
let firstId = "start"
let lastId = "0a99"
let category = "kodekloud"
let count = 259;

let node = document.getElementById(firstId)
let questions= {}

while (node != null) {
  
    question_txt = node.innerText.trim();

    while ((next = node.nextElementSibling) != null) {
        if (next.nodeName == "H3") {
            question_txt += "\n" + next.innerText.trim();
        }
        if (next.nodeName == "DL") {
            break;
        }
        node = next;
    }

    //console.log(question_txt);

    node = next;
    if (node == null) {
        break;
    }
 
    answer_txt = node.innerText.trim();

    while ((next = node.nextElementSibling) != null) {
        if (next.nodeName == "H3") {
            break;
        }
        if (next.nodeName == "DL") {
            answer_txt += "\n" + next.innerText.trim();
        }
        node = next;
    }
     //console.log(answer_txt);
     

    questions[count] = {
        "question": question_txt,
        "answer": answer_txt,
        "category": category,
        "id": count
    }
    count++;

     node = node.nextElementSibling;
   }
   return questions;
}
foo()