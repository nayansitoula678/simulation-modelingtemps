
let rolls = 1000;
let count = Array(6).fill(0);

for (let i = 0; i < rolls; i++) {
  let dice = Math.floor(Math.random() * 6);
  count[dice]++;
}

for (let i = 0; i < 6; i++) {
  console.log(`Side ${i+1}: ${count[i]} times`);
}

