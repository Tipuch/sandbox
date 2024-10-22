<script>
  import { onMount } from "svelte";
  export let current_user;
  let successMessage = "";
  let errorMessage = "";

  // reference: https://developer.mozilla.org/en-US/docs/Glossary/Base64#converting_arbitrary_binary_data
  function bytesToBase64Url(bytes) {
    const base64 = btoa(String.fromCharCode.apply(null, bytes));
    return base64.replace(/\+/g, "-").replace(/\//g, "_").replace(/=/g, "");
  }

  function base64UrlToBytes(base64url) {
    const base64 = base64url
      .replace(/-/g, "+")
      .replace(/_/g, "/")
      .padEnd(base64url.length + ((4 - (base64url.length % 4)) % 4), "=");
    return Uint8Array.from(atob(base64), (c) => c.charCodeAt(0));
  }
  //TODO add a list of accesskeys credentials with add / delete actions

  async function addAccessKey() {
    try {
      let registrationOptions = await fetch("/auth/webauthn/register", {
        method: "get",
        headers: {
          "Content-Type": "application/json",
        },
      });
      let public_key_registration_options = await registrationOptions.json();
      console.log(public_key_registration_options);
      public_key_registration_options.challenge = base64UrlToBytes(
        public_key_registration_options.challenge,
      );
      public_key_registration_options.user.id = base64UrlToBytes(
        public_key_registration_options.user.id,
      );
      const excludeCredentialsLength =
        public_key_registration_options.excludeCredentials.length;

      for (let i = 0; i < excludeCredentialsLength; i++) {
        public_key_registration_options.excludeCredentials[i].id =
          base64UrlToBytes(
            public_key_registration_options.excludeCredentials[i].id,
          );
      }
      console.log(public_key_registration_options);
      console.log(typeof public_key_registration_options);

      const credential = await navigator.credentials.create({
        publicKey: public_key_registration_options,
      });

      const response = await fetch("/auth/webauthn/register", {
        method: "post",
        body: JSON.stringify(credential),
        headers: {
          "Content-Type": "application/json",
        },
      });
      if (response.status === 201) {
        successMessage = "Your passkey was saved successfully!";
        setTimeout(() => (successMessage = ""), 5000);
      } else {
        errorMessage = "There was an error saving your passkey.";
        setTimeout(() => (errorMessage = ""), 5000);
      }
    } catch (error) {
      errorMessage = "There was an error saving your passkey.";
      setTimeout(() => (errorMessage = ""), 5000);
      console.error(error);
      return;
    }
  }
</script>

<section class="section is-large">
  {#if successMessage !== ""}
    <div class="notification is-success is-light">
      <button
        class="delete"
        aria-label="Close success message"
        on:click={() => (successMessage = "")}
      ></button>
      {successMessage}
    </div>
  {/if}
  {#if errorMessage !== ""}
    <div class="notification is-danger is-light">
      <button
        class="delete"
        aria-label="Close error message"
        on:click={() => (errorMessage = "")}
      ></button>
      {errorMessage}
    </div>
  {/if}
  <div class="box">
    <h2 class="title">Your Access Keys:</h2>
    <button class="button is-primary" on:click={addAccessKey}>
      <span class="icon is-small">
        <i class="fas fa-bold fa-plus fa-solid"></i>
      </span>
      <span>Add Access Key</span>
    </button>
  </div>
</section>
