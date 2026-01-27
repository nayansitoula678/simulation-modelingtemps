let cars = 0;

for (let minute = 1; minute <= 10; minute++) {
  let arriving = Math.floor(Math.random() * 5);
  cars += arriving;

  let leaving = Math.min(cars, 3);
  cars -= leaving;

  console.log(`Minute ${minute}: Cars waiting = ${cars}`);
}
