<script>
  import zxcvbn from "zxcvbn";
  export let messages;
  export let errors;

  let formElement = null;
  let formErrorMessage = "";

  let email = "";
  let emailField = null;
  let emailFieldValid = null;

  let name = "";
  let nameField = null;
  let nameFieldValid = null;

  let password = "";
  let passwordField = null;
  let passwordFieldSuggestions = [];
  let passwordFieldWarning = "";
  let passwordFieldValid = null;

  function checkName() {
    if (nameField.validity.valid) {
      nameFieldValid = true;
    } else {
      nameFieldValid = false;
    }
  }

  function checkEmail() {
    if (emailField.validity.valid) {
      emailFieldValid = true;
    } else {
      emailFieldValid = false;
    }
  }

  function checkPassword() {
    const results = zxcvbn(password);
    if (results.score < 3) {
      if (results.feedback.warning !== "") {
        passwordFieldWarning = results.feedback.warning;
      }
      if (results.feedback.suggestions.length > 0) {
        passwordFieldSuggestions = results.feedback.suggestions;
      }
      passwordFieldValid = false;
    } else if (passwordField.validity.valid) {
      passwordFieldValid = true;
      passwordFieldSuggestions = [];
      passwordFieldWarning = "";
    } else {
      passwordFieldValid = false;
    }
  }
  async function sendData() {
    // Associate the FormData object with the form element
    checkName();
    checkEmail();
    checkPassword();
    if (nameFieldValid && emailFieldValid && passwordFieldValid) {
      try {
        const response = await fetch("/auth/signup", {
          method: "POST",
          body: JSON.stringify({
            name: name,
            email: email,
            password: password,
          }),
          headers: {
            "Content-Type": "application/json",
          },
        });
        const response_json = await response.json();
        if (response.status !== 201) {
          formErrorMessage = response_json["detail"];
        } else {
          let loginFormData = new FormData();
          loginFormData.append("username", email);
          loginFormData.append("password", password);
          const login_response = await fetch("/auth/token", {
            method: "POST",
            body: loginFormData,
          });
          if (login_response.status !== 200) {
            formErrorMessage = "There was an error during the sign in process";
          } else {
            const jwt = await login_response.json();
            window.sessionStorage.setItem("jwt", jwt);
            location.href = "/auth/signup/success";
          }
        }
      } catch (e) {
        console.error(e);
        formErrorMessage = "There was an error while submitting your form.";
      }
    }
  }
</script>

<section class="section is-large">
  <h1 class="title">Sign Up</h1>
  <h2 class="subtitle">Welcome to the sandbox.</h2>
  {#if formErrorMessage !== ""}
    <div class="notification is-danger is-light">
      <button class="delete" on:click={() => (formErrorMessage = "")}></button>
      {formErrorMessage}
    </div>
  {/if}
  <form
    action=""
    method="post"
    bind:this={formElement}
    on:submit|preventDefault={sendData}
  >
    <div class="field">
      <label class="label" for="name">Name</label>
      <div class="control">
        <input
          id="name"
          class="input"
          type="text"
          minlength="2"
          maxlength="500"
          placeholder="Bob Ross"
          required
          class:is-danger={!nameFieldValid}
          class:is-success={nameFieldValid}
          bind:value={name}
          bind:this={nameField}
          on:input={checkName}
        />
      </div>
    </div>

    <div class="field">
      <label class="label" for="email">Email</label>
      <div class="control has-icons-left has-icons-right">
        <input
          id="email"
          class="input is-danger"
          type="email"
          maxlength="500"
          placeholder="bob@example.com"
          class:is-danger={!emailFieldValid}
          class:is-success={emailFieldValid}
          bind:value={email}
          bind:this={emailField}
          on:input={checkEmail}
          required
        />
        <span class="icon is-small is-left">
          <i class="fas fa-envelope"></i>
        </span>
        {#if emailFieldValid}
          <span class="icon is-small is-right">
            <i class="fas fa-check"></i>
          </span>
        {:else}
          <span class="icon is-small is-right">
            <i class="fas fa-exclamation-triangle"></i>
          </span>
        {/if}
      </div>
      {#if !emailFieldValid}
        <p class="help is-danger">This email is invalid</p>
      {/if}
    </div>

    <div class="field">
      <label class="label" for="password">Password</label>
      <div class="control has-icons-left has-icons-right">
        <input
          id="password"
          class="input"
          class:is-danger={!passwordFieldValid}
          class:is-success={passwordFieldValid}
          maxlength="250"
          type="password"
          placeholder="very-secure-password"
          bind:value={password}
          bind:this={passwordField}
          on:input={checkPassword}
          required
        />
        <span class="icon is-small is-left">
          <i class="fas fa-solid fa-lock"></i>
        </span>
        {#if !passwordFieldValid}
          <span class="icon is-small is-right">
            <i class="fas fa-exclamation-triangle"></i>
          </span>
        {:else}
          <span class="icon is-small is-right">
            <i class="fas fa-check"></i>
          </span>
        {/if}
      </div>
      {#if passwordFieldWarning !== ""}
        <p class="help is-danger">{passwordFieldWarning}</p>
      {/if}
      {#each passwordFieldSuggestions as suggestion}
        <p class="help">{suggestion}</p>
      {/each}
    </div>

    <div class="field is-grouped">
      <div class="control">
        <button class="button is-link">Submit</button>
      </div>
      <div class="control">
        <button class="button is-link is-light">Cancel</button>
      </div>
    </div>
  </form>
</section>
