// Document is ready
$(document).ready(function () {

// Validate Useremail
    $('#usercheck').hide();
    let useremailError = true;
    $('#useremail').keyup(function () {
        validateUseremail();
    });

    function validateUseremail() {
      let useremailValue = $('#useremail').val();
      if (useremailValue.length == '') {
      $('#usercheck').show();
          useremailError = false;
          return false;
      }
      else if((useremailValue.length < 3)||
              (useremailValue.length > 10)) {
          $('#usercheck').show();
          $('#usercheck').html
("**length of useremail must be between 3 and 10");
          useremailError = false;
          return false;
      }
      else {
          $('#usercheck').hide();
      }
    }

   // Validate Email
    const email =
        document.getElementById('email');
    email.addEventListener('blur', ()=>{
       let regex =
/^([_\-\.0-9a-zA-Z]+)@([_\-\.0-9a-zA-Z]+)\.([a-zA-Z]){2,7}$/;
       let s = email.value;
       if(regex.test(s)){
          email.classList.remove(
                'is-invalid');
          emailError = true;
        }
        else{
            email.classList.add(
                  'is-invalid');
            emailError = false;
        }
    })

   // Validate Password
    $('#passcheck').hide();
    let passwordError = true;
    $('#password').keyup(function () {
        validatePassword();
    });
    function validatePassword() {
        let passwrdValue =
            $('#password').val();
        if (passwrdValue.length == '') {
            $('#passcheck').show();
            passwordError = false;
            return false;
        }
        if ((passwrdValue.length < 3)||
            (passwrdValue.length > 10)) {
            $('#passcheck').show();
            $('#passcheck').html
("**length of your password must be between 3 and 10");
            $('#passcheck').css("color", "red");
            passwordError = false;
            return false;
        } else {
            $('#passcheck').hide();
        }
    }

// Validate Confirm Password
    $('#conpasscheck').hide();
    let confirmPasswordError = true;
    $('#conpassword').keyup(function () {
        validateConfirmPasswrd();
    });


// Submitt button
    $('#submitbtn').click(function () {
        validateUseremail();
        validatePassword();
        validateEmail();
        if ((useremailError == true) &&
            (passwordError == true) &&
            (confirmPasswordError == true) &&
            (emailError == true)) {
            return true;
        } else {
            return false;
        }
    });
});
