<script>
  import zxcvbn from "zxcvbn";
  export let messages;
  export let errors;
  export let message;

  let password = "";
  let passwordFieldSuggestions = [];
  let passwordFieldWarning = "";
  let passwordFieldValid = null;

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
    } else {
      passwordFieldValid = true;
      passwordFieldSuggestions = [];
      passwordFieldWarning = "";
    }
  }
</script>

<section class="section is-large">
  <h1 class="title">Sign Up</h1>
  <h2 class="subtitle">Welcome to the sandbox.</h2>

  <form action="">
    <div class="field">
      <label class="label" for="name">Name</label>
      <div class="control">
        <input id="name" class="input" type="text" placeholder="Text input" />
      </div>
    </div>

    <div class="field">
      <label class="label" for="email">Email</label>
      <div class="control has-icons-left has-icons-right">
        <input
          id="email"
          class="input is-danger"
          type="email"
          placeholder="Email input"
          value="hello@"
        />
        <span class="icon is-small is-left">
          <i class="fas fa-envelope"></i>
        </span>
        <span class="icon is-small is-right">
          <i class="fas fa-exclamation-triangle"></i>
        </span>
      </div>
      <p class="help is-danger">This email is invalid</p>
    </div>

    <div class="field">
      <label class="label" for="password">Password</label>
      <div class="control has-icons-left has-icons-right">
        <input
          id="password"
          class="input"
          class:is-danger={!passwordFieldValid}
          class:is-success={passwordFieldValid}
          type="password"
          placeholder="very-secure-password"
          bind:value={password}
          on:input={checkPassword}
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
