let numbers = [1, 2, 45, 78, 34, 5, 2];
let sortNumbers = numbers.sort((a, b) => a - b)

console.log("sorted", sortNumbers)
let reverseNumbers = sortNumbers.reverse();
console.log("reversed", reverseNumbers);

const wtf = new Set();
let a = {"twelve": 12, "eleven": 11}
wtf.add("dafuq")
wtf.add(a)
console.log(wtf.entries())
console.log("wtf", wtf)
let newNums = [...new Set(numbers)]
console.log(newNums)