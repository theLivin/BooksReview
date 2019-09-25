document.getElementById("username").addEventListener("blur", validateUname);
document.getElementById("email").addEventListener("blur", validateEmail);
document.getElementById("password").addEventListener("keyup", validatePword);
document.getElementById("cpassword").addEventListener("mouse-in", confirmPword);

function validateUname() {
  const name = document.querySelector("#username");
  const re = /^(([_.a-zA-Z0-9])*\w\d?)$/;

  if (!re.test(name.value) || name.value.length < 2) {
    name.classList.add("is-invalid");
  } else {
    name.classList.remove("is-invalid");
  }
}

function validateEmail() {
  const email = document.getElementById("email");
  const re = /^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$/;

  if (!re.test(email.value)) {
    email.classList.add("is-invalid");
  } else {
    email.classList.remove("is-invalid");
  }
}

function validatePword() {
  const pword = document.getElementById("password");
  const re = /[\d_\\/?><!"£$%^&*()-_=+}\]\{[\]\}\.@'#~*]/;

  if (pword.value.length < 8 || !re.test(pword.value)) {
    pword.classList.add("is-invalid");
  } else {
    pword.classList.remove("is-invalid");
  }
}

function confirmPword() {
  const pword = document.getElementById("password");
  const cpword = document.getElementById("cpassword");

  if (pword.value !== cpword.value) {
    cpword.classList.add("is-invalid");
  } else {
    cpword.classList.remove("is-invalid");
  }
}

// Bootstrap example starter JavaScript for disabling form submissions if there are invalid fields
(function() {
  "use strict";
  window.addEventListener(
    "load",
    function() {
      // Fetch all the forms we want to apply custom Bootstrap validation styles to
      var forms = document.getElementsByClassName("needs-validation");
      // Loop over them and prevent submission
      var validation = Array.prototype.filter.call(forms, function(form) {
        form.addEventListener(
          "submit",
          function(event) {
            if (form.checkValidity() === false) {
              event.preventDefault();
              event.stopPropagation();
            }
            form.classList.add("was-validated");
          },
          false
        );
      });
    },
    false
  );
})();
