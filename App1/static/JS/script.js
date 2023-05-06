const myInput = document.getElementById("password");
const letter = document.getElementById("letter");
const capital = document.getElementById("capital");
const number = document.getElementById("number");
const length = document.getElementById("length");

myInput.addEventListener("focus", () => {
  document.getElementById("message").style.display = "block";
});

myInput.addEventListener("blur", () => {
  document.getElementById("message").style.display = "none";
});

myInput.addEventListener("input", () => {
  const password = myInput.value;
  const hasLowerCaseLetters = /[a-z]/.test(password);
  const hasUpperCaseLetters = /[A-Z]/.test(password);
  const hasNumbers = /\d/.test(password);
  const isLongEnough = password.length >= 6;

  letter.classList.toggle("valid", hasLowerCaseLetters);
  letter.classList.toggle("invalid", !hasLowerCaseLetters);

  capital.classList.toggle("valid", hasUpperCaseLetters);
  capital.classList.toggle("invalid", !hasUpperCaseLetters);

  number.classList.toggle("valid", hasNumbers);
  number.classList.toggle("invalid", !hasNumbers);

  length.classList.toggle("valid", isLongEnough);
  length.classList.toggle("invalid", !isLongEnough);
});
