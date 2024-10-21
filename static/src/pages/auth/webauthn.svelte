<script>
  export let current_user;
  export let public_key_credential_options;
  let successMessage = "";

  //TODO add a list of accesskeys credentials with add / delete actions
  function addAccessKey() {}
</script>

<section class="section is-large">
  {#if successMessage !== ""}
    <div class="notification is-success is-light">
      <button class="delete" on:click={() => (successMessage = "")}></button>
      {successMessage}
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
